"""Seed a SQLite medical-device risk dataset + decision tables for local dev.
Run: python seed_risk.py  (creates tables, suppliers, inventory, view-equivalent rows)."""
import random, sqlite3
from pathlib import Path

random.seed(42)
DB = Path(__file__).parent.parent / "supplylens.db"
SITES = ["BOSTON", "CHICAGO", "SEATTLE"]
SUPPLIERS = [
    ("SUP001","MediCore USA","United States","Surgical","Primary",5,0.94,0.97),
    ("SUP002","Pacific Medtech","Taiwan","Diagnostic","Primary",12,0.87,0.91),
    ("SUP006","Apex BioSupply","United States","Critical Care","Primary",6,0.89,0.94),
    ("SUP007","GlobalMed Dist","Singapore","Diagnostic","Backup",18,0.82,0.88),
]
SKUS = [
    ("SKU001","Surgical Gloves (M)","Critical",62,7,"SUP001",8.50),
    ("SKU004","IV Catheters 18G","Critical",28,10,"SUP006",12.75),
    ("SKU021","Pulse Oximeters","Standard",8,14,"SUP002",45.00),
    ("SKU028","Isolation Gowns","Standard",50,7,"SUP007",5.50),
    ("SKU015","Alcohol Wipes","Consumable",200,3,"SUP001",0.15),
]

c = sqlite3.connect(DB)
c.executescript("""
CREATE TABLE IF NOT EXISTS suppliers (supplier_id TEXT PRIMARY KEY, supplier_name TEXT, country TEXT,
  category TEXT, contract_tier TEXT, avg_lead_time_days INT, on_time_delivery_rate REAL,
  quality_score REAL, active INT DEFAULT 1, incident_count_12m INT DEFAULT 0, total_days_delayed_12m INT DEFAULT 0);
CREATE TABLE IF NOT EXISTS sku_risk_summary (sku_id TEXT, sku_name TEXT, site_id TEXT, category TEXT,
  current_stock INT, avg_daily_demand REAL, lead_time_days INT, primary_supplier_id TEXT, unit_cost REAL,
  days_of_supply REAL, buffer_days REAL, risk_level TEXT, recommended_action TEXT);
CREATE TABLE IF NOT EXISTS actions (id INTEGER PRIMARY KEY AUTOINCREMENT, sku_id TEXT, site_id TEXT,
  action_type TEXT, label TEXT, cost REAL, benefit REAL, status TEXT DEFAULT 'pending', created_at TEXT);
CREATE TABLE IF NOT EXISTS decision_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, sku_id TEXT, site_id TEXT,
  detail TEXT, created_at TEXT);
DELETE FROM suppliers; DELETE FROM sku_risk_summary;
""")
c.executemany("INSERT INTO suppliers(supplier_id,supplier_name,country,category,contract_tier,avg_lead_time_days,on_time_delivery_rate,quality_score) VALUES (?,?,?,?,?,?,?,?)", SUPPLIERS)
for sid,name,cat,dem,lead,sup,cost in SKUS:
    for site in SITES:
        roll=random.random()
        stock=int(lead*dem*(0.6 if roll<0.3 else 1.3 if roll<0.6 else 3.0))
        dos=round(stock/dem,1); buf=round(dos-lead,1)
        lvl="CRITICAL" if dos<=lead else "HIGH" if dos<=lead*1.5 else "MEDIUM" if dos<=lead*2 else "LOW"
        c.execute("INSERT INTO sku_risk_summary VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (sid,name,site,cat,stock,dem,lead,sup,cost,dos,buf,lvl,"see decision panel"))
c.commit(); c.close()
print("Seeded risk + decision tables")
