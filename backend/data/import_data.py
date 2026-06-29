"""
Imports generated CSV files into MySQL.
Run after seed_data.py and after creating schema.
Usage: python import_data.py
"""
import csv
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../.env")

def get_conn():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "supplylens")
    )

def import_suppliers():
    with open("suppliers.csv") as f:
        rows = list(csv.DictReader(f))
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM suppliers")
    for r in rows:
        cursor.execute("""
            INSERT INTO suppliers 
            (supplier_id, supplier_name, country, category, contract_tier, 
             avg_lead_time_days, on_time_delivery_rate, quality_score)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (r["supplier_id"], r["supplier_name"], r["country"], r["category"],
              r["contract_tier"], int(r["avg_lead_time_days"]),
              float(r["on_time_delivery_rate"]), float(r["quality_score"])))
    conn.commit()
    print(f"Imported {len(rows)} suppliers")
    cursor.close(); conn.close()

def import_inventory():
    with open("inventory.csv") as f:
        rows = list(csv.DictReader(f))
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory_snapshots")
    for r in rows:
        cursor.execute("""
            INSERT INTO inventory_snapshots
            (sku_id, sku_name, site_id, category, current_stock, reorder_point,
             avg_daily_demand, lead_time_days, primary_supplier_id, unit_cost)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (r["sku_id"], r["sku_name"], r["site_id"], r["category"],
              int(r["current_stock"]), int(r["reorder_point"]),
              float(r["avg_daily_demand"]), int(r["lead_time_days"]),
              r["primary_supplier_id"], float(r["unit_cost"])))
    conn.commit()
    print(f"Imported {len(rows)} inventory rows")
    cursor.close(); conn.close()

def import_orders():
    with open("orders.csv") as f:
        rows = list(csv.DictReader(f))
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders_history")
    for r in rows:
        cursor.execute("""
            INSERT INTO orders_history
            (sku_id, site_id, order_date, quantity_ordered, quantity_received,
             supplier_id, expected_delivery, actual_delivery, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (r["sku_id"], r["site_id"], r["order_date"],
              int(r["quantity_ordered"]), int(r["quantity_received"]),
              r["supplier_id"], r["expected_delivery"],
              r["actual_delivery"] or None, r["status"]))
    conn.commit()
    print(f"Imported {len(rows)} order rows")
    cursor.close(); conn.close()

def import_incidents():
    with open("incidents.csv") as f:
        rows = list(csv.DictReader(f))
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM supplier_incidents")
    for r in rows:
        cursor.execute("""
            INSERT INTO supplier_incidents
            (supplier_id, incident_date, incident_type, affected_skus,
             severity, resolution_notes, days_delayed)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (r["supplier_id"], r["incident_date"], r["incident_type"],
              r["affected_skus"], r["severity"], r["resolution_notes"],
              int(r["days_delayed"])))
    conn.commit()
    print(f"Imported {len(rows)} incidents")
    cursor.close(); conn.close()

if __name__ == "__main__":
    print("Importing data into MySQL...")
    import_suppliers()
    import_inventory()
    import_orders()
    import_incidents()
    print("Done! All data imported successfully.")
