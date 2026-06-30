#!/usr/bin/env python3
"""
Generates synthetic CSV seed data for SupplyLens commodity & manufacturing operations.
Produces: suppliers.csv, inventory.csv, orders.csv, incidents.csv
Run with: python seed_data.py
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

OUTPUT_DIR = Path(__file__).parent
TODAY = date.today()
PERIOD_START = TODAY - timedelta(days=365)

SITES = ["BOSTON", "CHICAGO", "SEATTLE"]

SUPPLIERS = [
    {"supplier_id": "SUP001", "supplier_name": "Midwest Steel Co",      "country": "United States", "category": "Raw Materials",         "contract_tier": "Primary", "avg_lead_time_days": 5,  "on_time_delivery_rate": 0.94, "quality_score": 0.97},
    {"supplier_id": "SUP002", "supplier_name": "Pacific Components",    "country": "Taiwan",        "category": "Electronics",           "contract_tier": "Primary", "avg_lead_time_days": 12, "on_time_delivery_rate": 0.87, "quality_score": 0.91},
    {"supplier_id": "SUP003", "supplier_name": "EuroForge GmbH",       "country": "Germany",       "category": "Castings",              "contract_tier": "Backup",  "avg_lead_time_days": 14, "on_time_delivery_rate": 0.91, "quality_score": 0.95},
    {"supplier_id": "SUP004", "supplier_name": "RapidParts Express",   "country": "United States", "category": "Hardware",              "contract_tier": "Spot",    "avg_lead_time_days": 3,  "on_time_delivery_rate": 0.78, "quality_score": 0.83},
    {"supplier_id": "SUP005", "supplier_name": "CanFab Solutions",     "country": "Canada",        "category": "Consumables",           "contract_tier": "Primary", "avg_lead_time_days": 7,  "on_time_delivery_rate": 0.93, "quality_score": 0.96},
    {"supplier_id": "SUP006", "supplier_name": "Apex Hydraulics",      "country": "United States", "category": "Critical Components",    "contract_tier": "Primary", "avg_lead_time_days": 6,  "on_time_delivery_rate": 0.89, "quality_score": 0.94},
    {"supplier_id": "SUP007", "supplier_name": "GlobalMotor Dist",     "country": "Singapore",     "category": "Electronics",           "contract_tier": "Backup",  "avg_lead_time_days": 18, "on_time_delivery_rate": 0.82, "quality_score": 0.88},
    {"supplier_id": "SUP008", "supplier_name": "Regional Fasteners Co","country": "United States", "category": "Consumables",           "contract_tier": "Backup",  "avg_lead_time_days": 4,  "on_time_delivery_rate": 0.85, "quality_score": 0.90},
]

SUPPLIER_MAP = {s["supplier_id"]: s for s in SUPPLIERS}

# sku_id, sku_name, category, avg_daily_demand, lead_time_days, reorder_point, primary_supplier_id, unit_cost
SKUS = [
    ("SKU001", "Steel Bracket A36",         "Critical",   45,  7,  315, "SUP001", 8.50),
    ("SKU002", "Aluminum Extrusion 6061",   "Critical",   62,  7,  434, "SUP001", 8.50),
    ("SKU003", "Stainless Sheet 304",       "Critical",   38,  7,  266, "SUP001", 8.50),
    ("SKU004", "Hydraulic Cylinder 18mm",   "Critical",   28, 10,  280, "SUP006", 12.75),
    ("SKU005", "Hydraulic Cylinder 20mm",   "Critical",   35, 10,  350, "SUP006", 12.75),
    ("SKU006", "Industrial Gasket Set",     "Critical",   20, 12,  240, "SUP003", 22.00),
    ("SKU007", "Welding Electrodes",        "Critical",   55,  8,  440, "SUP001", 3.25),
    ("SKU008", "Cutting Discs",             "Standard",  120,  5,  600, "SUP005", 0.85),
    ("SKU009", "Hex Bolts M6 (box)",        "Consumable", 90,  5,  450, "SUP001", 4.20),
    ("SKU010", "Hex Bolts M8 (box)",        "Consumable",110,  5,  550, "SUP001", 4.20),
    ("SKU011", "Hex Bolts M10 (box)",       "Consumable", 75,  5,  375, "SUP001", 4.20),
    ("SKU012", "Copper Wire 4mm",           "Consumable", 85,  4,  340, "SUP005", 1.50),
    ("SKU013", "Copper Wire 2mm",           "Consumable", 65,  4,  260, "SUP005", 1.20),
    ("SKU014", "Insulation Tape",           "Consumable", 40,  4,  160, "SUP008", 2.10),
    ("SKU015", "Threadlocker",              "Consumable",200,  3,  600, "SUP005", 0.15),
    ("SKU016", "Coolant 500mL",             "Critical",   30, 10,  300, "SUP006", 4.80),
    ("SKU017", "Coolant 1L",                "Critical",   22, 10,  220, "SUP006", 7.20),
    ("SKU018", "Ball Bearings 30mm",        "Standard",   95,  6,  570, "SUP008", 0.45),
    ("SKU019", "Ball Bearings 50mm",        "Standard",   60,  6,  360, "SUP008", 0.65),
    ("SKU020", "PCB Controller Board",      "Standard",   45,  8,  360, "SUP002", 1.90),
    ("SKU021", "PLC Module",                "Standard",    8, 14,  112, "SUP002", 45.00),
    ("SKU022", "Rubber Seals 20mm",         "Consumable", 70,  4,  280, "SUP008", 0.95),
    ("SKU023", "Rubber Seals 40mm",         "Consumable", 45,  4,  180, "SUP008", 1.40),
    ("SKU024", "Adhesive Sealant",          "Standard",   25,  7,  175, "SUP003", 3.60),
    ("SKU025", "Cutting Tool Inserts",      "Critical",   15, 12,  180, "SUP003", 18.50),
    ("SKU026", "Precision Drill Bits",      "Critical",   10, 14,  140, "SUP003", 32.00),
    ("SKU027", "Tooling Jig Set",           "Critical",   12, 10,  120, "SUP006", 28.00),
    ("SKU028", "Conveyor Belt",             "Standard",   50,  7,  350, "SUP007", 5.50),
    ("SKU029", "Drive Motor",               "Standard",   30,  7,  210, "SUP007", 7.80),
    ("SKU030", "Polymer Resin Pellets",     "Consumable", 18,  5,   90, "SUP005", 9.20),
]

INCIDENTS = [
    ("SUP002", "Late Delivery",          "High",     6,  "SKU020,SKU021"),
    ("SUP007", "Shortage",               "Critical", 12, "SKU028,SKU029"),
    ("SUP004", "Quality Issue",          "Medium",   0,  "SKU001,SKU002"),
    ("SUP002", "Late Delivery",          "Medium",   4,  "SKU021"),
    ("SUP003", "Force Majeure",          "High",     9,  "SKU006,SKU025,SKU026"),
    ("SUP007", "Late Delivery",          "High",     8,  "SKU028"),
    ("SUP004", "Communication Failure",  "Low",      2,  "SKU003"),
    ("SUP008", "Late Delivery",          "Low",      3,  "SKU018,SKU019"),
    ("SUP002", "Quality Issue",          "High",     0,  "SKU020"),
    ("SUP007", "Shortage",               "High",     15, "SKU029"),
    ("SUP004", "Late Delivery",          "Medium",   5,  "SKU001,SKU002,SKU003"),
    ("SUP003", "Late Delivery",          "Medium",   4,  "SKU024"),
    ("SUP006", "Communication Failure",  "Low",      1,  "SKU016"),
    ("SUP002", "Late Delivery",          "Critical", 11, "SKU020,SKU021"),
    ("SUP007", "Quality Issue",          "Medium",   0,  "SKU028,SKU029"),
]


def _write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote {len(rows):>5} rows  ->  {path.name}")


def generate_suppliers():
    return [dict(s, active=1) for s in SUPPLIERS]


def generate_inventory():
    rows = []
    critical_count = 0
    for sku_id, sku_name, category, demand, lead, reorder, supplier, cost in SKUS:
        for site in SITES:
            roll = random.random()
            if roll < 0.20:
                stock = random.randint(0, int(lead * demand * 0.9))
            elif roll < 0.50:
                stock = random.randint(int(lead * demand), int(lead * demand * 1.8))
            else:
                stock = random.randint(int(lead * demand * 2), int(lead * demand * 4))
            if stock / demand <= lead:
                critical_count += 1
            rows.append({
                "sku_id": sku_id, "sku_name": sku_name, "site_id": site,
                "category": category, "current_stock": stock, "reorder_point": reorder,
                "avg_daily_demand": demand, "lead_time_days": lead,
                "primary_supplier_id": supplier, "unit_cost": cost,
            })
    # Ensure at least 3 CRITICAL exist
    while critical_count < 3:
        r = random.choice(rows)
        lead = r["lead_time_days"]; demand = r["avg_daily_demand"]
        r["current_stock"] = random.randint(0, int(lead * demand * 0.5))
        critical_count += 1
    return rows


def generate_orders(inventory):
    rows = []
    for sku_id, sku_name, category, demand, lead, reorder, supplier, cost in SKUS:
        sup = SUPPLIER_MAP[supplier]
        for site in SITES:
            d = PERIOD_START
            while d < TODAY:
                qty = random.randint(int(reorder * 0.8), int(reorder * 1.5))
                if random.random() < 0.95:
                    received = qty
                else:
                    received = int(qty * random.uniform(0.80, 0.99))
                expected = d + timedelta(days=lead)
                if random.random() < 0.88:
                    actual = expected
                else:
                    actual = expected + timedelta(days=random.randint(1, 8))
                if (TODAY - d).days <= 14:
                    status = "Pending"
                    actual_val = ""
                else:
                    status = "Late" if actual > expected else "Delivered"
                    actual_val = actual.isoformat()
                rows.append({
                    "sku_id": sku_id, "site_id": site, "order_date": d.isoformat(),
                    "quantity_ordered": qty, "quantity_received": received,
                    "supplier_id": supplier, "expected_delivery": expected.isoformat(),
                    "actual_delivery": actual_val, "status": status,
                })
                d += timedelta(days=30)
    return rows


def generate_incidents():
    rows = []
    for sid, itype, sev, delay, skus in INCIDENTS:
        offset = random.randint(0, 364)
        idate = PERIOD_START + timedelta(days=offset)
        rows.append({
            "supplier_id": sid, "incident_date": idate.isoformat(),
            "incident_type": itype, "affected_skus": skus, "severity": sev,
            "resolution_notes": "Resolved via air freight from backup supplier",
            "days_delayed": delay,
        })
    return rows


if __name__ == "__main__":
    print("Generating seed data...")
    _write_csv(OUTPUT_DIR / "suppliers.csv", generate_suppliers(),
               ["supplier_id", "supplier_name", "country", "category", "contract_tier",
                "avg_lead_time_days", "on_time_delivery_rate", "quality_score", "active"])
    inv = generate_inventory()
    _write_csv(OUTPUT_DIR / "inventory.csv", inv,
               ["sku_id", "sku_name", "site_id", "category", "current_stock", "reorder_point",
                "avg_daily_demand", "lead_time_days", "primary_supplier_id", "unit_cost"])
    _write_csv(OUTPUT_DIR / "orders.csv", generate_orders(inv),
               ["sku_id", "site_id", "order_date", "quantity_ordered", "quantity_received",
                "supplier_id", "expected_delivery", "actual_delivery", "status"])
    _write_csv(OUTPUT_DIR / "incidents.csv", generate_incidents(),
               ["supplier_id", "incident_date", "incident_type", "affected_skus",
                "severity", "resolution_notes", "days_delayed"])
    print("Done.")
