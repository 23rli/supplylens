"""
MySQL connection and all database query functions.
All SQL queries live here — never in the routers.
"""
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    """Returns a MySQL connection. Raises on failure."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "supplylens")
    )

def fetch_all(query: str, params: tuple = None) -> list[dict]:
    """Execute a SELECT query and return list of dicts."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def fetch_one(query: str, params: tuple = None) -> dict | None:
    """Execute a SELECT query and return one dict or None."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# ── Risk queries ──────────────────────────────────────────────────────────────

def get_risk_summary(site: str = None, risk_level: str = None, category: str = None) -> list[dict]:
    """
    Returns all SKUs from sku_risk_summary view with optional filters.
    Ordered by risk level (CRITICAL first) then buffer_days ascending.
    """
    query = """
        SELECT * FROM sku_risk_summary
        WHERE 1=1
    """
    params = []
    if site:
        query += " AND site_id = %s"
        params.append(site)
    if risk_level:
        query += " AND risk_level = %s"
        params.append(risk_level)
    if category:
        query += " AND category = %s"
        params.append(category)
    query += """
        ORDER BY
          FIELD(risk_level, 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'),
          buffer_days ASC
    """
    return fetch_all(query, tuple(params))

def get_top_risks(limit: int = 10) -> list[dict]:
    """Returns the top N highest-risk SKUs across all sites."""
    query = """
        SELECT * FROM sku_risk_summary
        ORDER BY
          FIELD(risk_level, 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'),
          buffer_days ASC
        LIMIT %s
    """
    return fetch_all(query, (limit,))

def get_risk_counts_by_site() -> list[dict]:
    """
    Returns risk level counts grouped by site.
    Used for the heatmap component.
    """
    query = """
        SELECT
          site_id,
          SUM(CASE WHEN risk_level = 'CRITICAL' THEN 1 ELSE 0 END) AS critical_count,
          SUM(CASE WHEN risk_level = 'HIGH' THEN 1 ELSE 0 END) AS high_count,
          SUM(CASE WHEN risk_level = 'MEDIUM' THEN 1 ELSE 0 END) AS medium_count,
          SUM(CASE WHEN risk_level = 'LOW' THEN 1 ELSE 0 END) AS low_count,
          COUNT(*) AS total_skus
        FROM sku_risk_summary
        GROUP BY site_id
        ORDER BY site_id
    """
    return fetch_all(query)

# ── Dashboard queries ─────────────────────────────────────────────────────────

def get_dashboard_stats() -> dict:
    """
    Returns 4 headline KPI numbers for the KPIBar component.
    """
    critical = fetch_one("SELECT COUNT(*) AS count FROM sku_risk_summary WHERE risk_level = 'CRITICAL'")
    high = fetch_one("SELECT COUNT(*) AS count FROM sku_risk_summary WHERE risk_level = 'HIGH'")
    avg_supply = fetch_one("SELECT ROUND(AVG(days_of_supply), 1) AS avg FROM sku_risk_summary")
    supplier_avg = fetch_one("SELECT ROUND(AVG(on_time_delivery_rate) * 100, 1) AS rate FROM suppliers WHERE active = TRUE")

    return {
        "critical_skus": critical["count"] if critical else 0,
        "high_risk_skus": high["count"] if high else 0,
        "avg_days_of_supply": avg_supply["avg"] if avg_supply else 0,
        "supplier_reliability_pct": supplier_avg["rate"] if supplier_avg else 0,
    }

# ── Supplier queries ──────────────────────────────────────────────────────────

def get_suppliers() -> list[dict]:
    """
    Returns all active suppliers enriched with incident count (last 12 months).
    """
    query = """
        SELECT
          s.*,
          COUNT(si.id) AS incident_count_12m,
          COALESCE(SUM(si.days_delayed), 0) AS total_days_delayed_12m
        FROM suppliers s
        LEFT JOIN supplier_incidents si
          ON s.supplier_id = si.supplier_id
          AND si.incident_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
        WHERE s.active = TRUE
        GROUP BY s.supplier_id
        ORDER BY s.on_time_delivery_rate DESC
    """
    return fetch_all(query)

def get_supplier_incidents(supplier_id: str = None) -> list[dict]:
    """Returns all incidents, optionally filtered by supplier."""
    query = "SELECT * FROM supplier_incidents WHERE 1=1"
    params = []
    if supplier_id:
        query += " AND supplier_id = %s"
        params.append(supplier_id)
    query += " ORDER BY incident_date DESC"
    return fetch_all(query, tuple(params))

# ── AI context queries ────────────────────────────────────────────────────────

def get_ai_context() -> dict:
    """
    Pulls all data needed to build the AI system prompt.
    Returns a dict with risk_summary, suppliers, and recent_incidents.
    """
    risk_data = get_risk_summary()
    supplier_data = get_suppliers()
    incidents = fetch_all("""
        SELECT si.*, s.supplier_name
        FROM supplier_incidents si
        JOIN suppliers s ON si.supplier_id = s.supplier_id
        ORDER BY si.incident_date DESC
        LIMIT 10
    """)
    stats = get_dashboard_stats()

    return {
        "risk_summary": risk_data,
        "suppliers": supplier_data,
        "recent_incidents": incidents,
        "stats": stats,
    }
