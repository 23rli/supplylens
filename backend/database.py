"""
Risk/supplier query layer. Uses the shared db backend (SQLite local / Azure prod).
All SQL queries live here — never in the routers.
"""
from db import fetch_all, fetch_one

# CASE expression used to order rows CRITICAL -> LOW (replaces MySQL FIELD()).
_RISK_ORDER = """
    CASE risk_level
      WHEN 'CRITICAL' THEN 0 WHEN 'HIGH' THEN 1
      WHEN 'MEDIUM' THEN 2 ELSE 3 END, buffer_days ASC
"""

def get_risk_summary(site: str = None, risk_level: str = None, category: str = None) -> list[dict]:
    """
    Returns all SKUs from sku_risk_summary view with optional filters.
    Ordered by risk level (CRITICAL first) then buffer_days ascending.
    """
    query = "SELECT * FROM sku_risk_summary WHERE 1=1"
    params = []
    if site:
        query += " AND site_id = ?"
        params.append(site)
    if risk_level:
        query += " AND risk_level = ?"
        params.append(risk_level)
    if category:
        query += " AND category = ?"
        params.append(category)
    query += f" ORDER BY {_RISK_ORDER}"
    return fetch_all(query, tuple(params))

def get_top_risks(limit: int = 10) -> list[dict]:
    """Returns the top N highest-risk SKUs across all sites."""
    query = f"SELECT TOP (?) * FROM sku_risk_summary ORDER BY {_RISK_ORDER}"
    return fetch_all(query, (limit,))

def get_risk_counts_by_site() -> list[dict]:
    """Returns risk level counts grouped by site. Used for the heatmap component."""
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
    """Returns 4 headline KPI numbers for the KPIBar component."""
    critical = fetch_one("SELECT COUNT(*) AS count FROM sku_risk_summary WHERE risk_level = 'CRITICAL'")
    high = fetch_one("SELECT COUNT(*) AS count FROM sku_risk_summary WHERE risk_level = 'HIGH'")
    avg_supply = fetch_one("SELECT ROUND(AVG(days_of_supply), 1) AS avg FROM sku_risk_summary")
    supplier_avg = fetch_one("SELECT ROUND(AVG(on_time_delivery_rate) * 100, 1) AS rate FROM suppliers WHERE active = 1")

    return {
        "critical_skus": critical["count"] if critical else 0,
        "high_risk_skus": high["count"] if high else 0,
        "avg_days_of_supply": avg_supply["avg"] if avg_supply else 0,
        "supplier_reliability_pct": supplier_avg["rate"] if supplier_avg else 0,
    }

# ── Supplier queries ──────────────────────────────────────────────────────────

def get_suppliers() -> list[dict]:
    """Returns all active suppliers enriched with incident count (last 12 months)."""
    query = """
        SELECT
          s.supplier_id, s.supplier_name, s.country, s.category, s.contract_tier,
          s.avg_lead_time_days, s.on_time_delivery_rate, s.quality_score, s.active,
          COUNT(si.id) AS incident_count_12m,
          COALESCE(SUM(si.days_delayed), 0) AS total_days_delayed_12m
        FROM suppliers s
        LEFT JOIN supplier_incidents si
          ON s.supplier_id = si.supplier_id
          AND si.incident_date >= DATEADD(MONTH, -12, CAST(GETDATE() AS DATE))
        WHERE s.active = 1
        GROUP BY s.supplier_id, s.supplier_name, s.country, s.category, s.contract_tier,
                 s.avg_lead_time_days, s.on_time_delivery_rate, s.quality_score, s.active
        ORDER BY s.on_time_delivery_rate DESC
    """
    return fetch_all(query)

def get_supplier_incidents(supplier_id: str = None) -> list[dict]:
    """Returns all incidents, optionally filtered by supplier."""
    query = "SELECT * FROM supplier_incidents WHERE 1=1"
    params = []
    if supplier_id:
        query += " AND supplier_id = ?"
        params.append(supplier_id)
    query += " ORDER BY incident_date DESC"
    return fetch_all(query, tuple(params))

# ── AI context queries ────────────────────────────────────────────────────────

def get_ai_context() -> dict:
    """
    Pulls all data needed to build the AI system prompt across every module.
    Resilient: any module that isn't seeded is skipped.
    """
    risk_data, supplier_data, incidents, stats = [], [], [], {}
    try:
        risk_data = get_risk_summary()
        supplier_data = get_suppliers()
        incidents = fetch_all("""
            SELECT TOP (10) si.*, s.supplier_name
            FROM supplier_incidents si
            JOIN suppliers s ON si.supplier_id = s.supplier_id
            ORDER BY si.incident_date DESC
        """)
        stats = get_dashboard_stats()
    except Exception:
        pass

    inventory_stats = hedging = {}
    try:
        from inventory.store import inventory_stats as inv_stats
        inventory_stats = inv_stats()
    except Exception:
        pass
    try:
        from hedging.store import run_scenario
        hedging = run_scenario()
    except Exception:
        pass

    return {
        "risk_summary": risk_data,
        "suppliers": supplier_data,
        "recent_incidents": incidents,
        "stats": stats,
        "inventory": inventory_stats,
        "hedging": hedging,
    }
