#!/usr/bin/env python3
"""Generates synthetic CSV seed data for SupplyLens medical device distribution platform."""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

OUTPUT_DIR = Path(__file__).parent
TODAY = date(2026, 4, 22)
PERIOD_START = date(2025, 4, 22)

# ─── Reference Data ───────────────────────────────────────────────────────────

SITES = ["BOS", "CHI", "SEA"]

SUPPLIERS = [
    {
        "supplier_id": "SUP001", "supplier_name": "MedTech Dynamics",
        "country": "USA",     "category": "Surgical Instruments",
        "contract_tier": "Tier 1", "avg_lead_time_days": 7,  "on_time_delivery_rate": 0.96,
    },
    {
        "supplier_id": "SUP002", "supplier_name": "GlobalMed Supply",
        "country": "Germany", "category": "Diagnostic Equipment",
        "contract_tier": "Tier 1", "avg_lead_time_days": 14, "on_time_delivery_rate": 0.92,
    },
    {
        "supplier_id": "SUP003", "supplier_name": "PrecisionCare Corp",
        "country": "Japan",   "category": "Implants",
        "contract_tier": "Tier 1", "avg_lead_time_days": 21, "on_time_delivery_rate": 0.94,
    },
    {
        "supplier_id": "SUP004", "supplier_name": "SafeGuard Medical",
        "country": "USA",     "category": "PPE",
        "contract_tier": "Tier 2", "avg_lead_time_days": 5,  "on_time_delivery_rate": 0.88,
    },
    {
        "supplier_id": "SUP005", "supplier_name": "LabCore Solutions",
        "country": "Ireland", "category": "Lab Equipment",
        "contract_tier": "Tier 2", "avg_lead_time_days": 10, "on_time_delivery_rate": 0.85,
    },
    {
        "supplier_id": "SUP006", "supplier_name": "MedConsume Ltd",
        "country": "China",   "category": "Consumables",
        "contract_tier": "Tier 2", "avg_lead_time_days": 30, "on_time_delivery_rate": 0.79,
    },
    {
        "supplier_id": "SUP007", "supplier_name": "Apex Instruments",
        "country": "USA",     "category": "Surgical Instruments",
        "contract_tier": "Tier 3", "avg_lead_time_days": 12, "on_time_delivery_rate": 0.82,
    },
    {
        "supplier_id": "SUP008", "supplier_name": "BioSource International",
        "country": "India",   "category": "Consumables",
        "contract_tier": "Tier 3", "avg_lead_time_days": 45, "on_time_delivery_rate": 0.75,
    },
]

SUPPLIER_MAP = {s["supplier_id"]: s for s in SUPPLIERS}

# 30 SKUs across 6 categories (5 per category)
SKUS = [
    # Surgical Instruments
    {"sku_id": "SKU-SRG-001", "sku_name": "Laparoscopic Trocar Set",         "category": "Surgical Instruments", "supplier_id": "SUP001", "base_demand": 3.5,  "lead_time_days": 7},
    {"sku_id": "SKU-SRG-002", "sku_name": "Electrosurgical Pencil",          "category": "Surgical Instruments", "supplier_id": "SUP001", "base_demand": 8.0,  "lead_time_days": 7},
    {"sku_id": "SKU-SRG-003", "sku_name": "Titanium Clip Applier",           "category": "Surgical Instruments", "supplier_id": "SUP007", "base_demand": 5.2,  "lead_time_days": 12},
    {"sku_id": "SKU-SRG-004", "sku_name": "Bipolar Forceps Kit",             "category": "Surgical Instruments", "supplier_id": "SUP007", "base_demand": 2.8,  "lead_time_days": 12},
    {"sku_id": "SKU-SRG-005", "sku_name": "Irrigation/Suction Cannula",      "category": "Surgical Instruments", "supplier_id": "SUP001", "base_demand": 6.5,  "lead_time_days": 7},
    # Diagnostic Equipment
    {"sku_id": "SKU-DGN-001", "sku_name": "Portable Ultrasound Probe",       "category": "Diagnostic Equipment", "supplier_id": "SUP002", "base_demand": 0.5,  "lead_time_days": 14},
    {"sku_id": "SKU-DGN-002", "sku_name": "ECG Lead Set 10-Wire",            "category": "Diagnostic Equipment", "supplier_id": "SUP002", "base_demand": 4.0,  "lead_time_days": 14},
    {"sku_id": "SKU-DGN-003", "sku_name": "Pulse Oximeter Clip Sensor",      "category": "Diagnostic Equipment", "supplier_id": "SUP002", "base_demand": 12.0, "lead_time_days": 10},
    {"sku_id": "SKU-DGN-004", "sku_name": "Blood Pressure Cuff Adult",       "category": "Diagnostic Equipment", "supplier_id": "SUP002", "base_demand": 7.5,  "lead_time_days": 14},
    {"sku_id": "SKU-DGN-005", "sku_name": "Digital Thermometer Probe Cover", "category": "Diagnostic Equipment", "supplier_id": "SUP002", "base_demand": 25.0, "lead_time_days": 10},
    # Implants
    {"sku_id": "SKU-IMP-001", "sku_name": "Titanium Hip Stem Size M",        "category": "Implants", "supplier_id": "SUP003", "base_demand": 1.2,  "lead_time_days": 21},
    {"sku_id": "SKU-IMP-002", "sku_name": "Knee Replacement Tibial Tray",    "category": "Implants", "supplier_id": "SUP003", "base_demand": 1.5,  "lead_time_days": 21},
    {"sku_id": "SKU-IMP-003", "sku_name": "Spinal Fusion Cage L4-L5",        "category": "Implants", "supplier_id": "SUP003", "base_demand": 0.8,  "lead_time_days": 21},
    {"sku_id": "SKU-IMP-004", "sku_name": "Cortical Bone Screw 4.5mm",       "category": "Implants", "supplier_id": "SUP003", "base_demand": 15.0, "lead_time_days": 14},
    {"sku_id": "SKU-IMP-005", "sku_name": "Resorbable Suture Anchor",        "category": "Implants", "supplier_id": "SUP003", "base_demand": 8.5,  "lead_time_days": 21},
    # PPE
    {"sku_id": "SKU-PPE-001", "sku_name": "N95 Respirator Mask",             "category": "PPE", "supplier_id": "SUP004", "base_demand": 150.0, "lead_time_days": 5},
    {"sku_id": "SKU-PPE-002", "sku_name": "Sterile Latex-Free Gloves M",     "category": "PPE", "supplier_id": "SUP004", "base_demand": 200.0, "lead_time_days": 5},
    {"sku_id": "SKU-PPE-003", "sku_name": "Disposable Isolation Gown",       "category": "PPE", "supplier_id": "SUP004", "base_demand": 85.0,  "lead_time_days": 5},
    {"sku_id": "SKU-PPE-004", "sku_name": "Face Shield Full Coverage",       "category": "PPE", "supplier_id": "SUP004", "base_demand": 30.0,  "lead_time_days": 7},
    {"sku_id": "SKU-PPE-005", "sku_name": "Surgical Cap Bouffant",           "category": "PPE", "supplier_id": "SUP004", "base_demand": 120.0, "lead_time_days": 5},
    # Consumables
    {"sku_id": "SKU-CON-001", "sku_name": "IV Catheter 18G",                 "category": "Consumables", "supplier_id": "SUP006", "base_demand": 45.0,  "lead_time_days": 30},
    {"sku_id": "SKU-CON-002", "sku_name": "Sterile Gauze 4x4 in",            "category": "Consumables", "supplier_id": "SUP008", "base_demand": 300.0, "lead_time_days": 45},
    {"sku_id": "SKU-CON-003", "sku_name": "Disposable Syringe 10mL",         "category": "Consumables", "supplier_id": "SUP006", "base_demand": 90.0,  "lead_time_days": 30},
    {"sku_id": "SKU-CON-004", "sku_name": "Foley Catheter 16Fr",             "category": "Consumables", "supplier_id": "SUP008", "base_demand": 22.0,  "lead_time_days": 45},
    {"sku_id": "SKU-CON-005", "sku_name": "Wound Closure Strip 1/4in",       "category": "Consumables", "supplier_id": "SUP006", "base_demand": 60.0,  "lead_time_days": 30},
    # Lab Equipment
    {"sku_id": "SKU-LAB-001", "sku_name": "Centrifuge Tube 15mL",            "category": "Lab Equipment", "supplier_id": "SUP005", "base_demand": 80.0,  "lead_time_days": 10},
    {"sku_id": "SKU-LAB-002", "sku_name": "Pipette Tip 200uL Sterile",       "category": "Lab Equipment", "supplier_id": "SUP005", "base_demand": 250.0, "lead_time_days": 10},
    {"sku_id": "SKU-LAB-003", "sku_name": "Microtainer Blood Collection",    "category": "Lab Equipment", "supplier_id": "SUP005", "base_demand": 65.0,  "lead_time_days": 10},
    {"sku_id": "SKU-LAB-004", "sku_name": "PCR Reaction Plate 96-Well",      "category": "Lab Equipment", "supplier_id": "SUP005", "base_demand": 12.0,  "lead_time_days": 14},
    {"sku_id": "SKU-LAB-005", "sku_name": "Specimen Transport Container",    "category": "Lab Equipment", "supplier_id": "SUP005", "base_demand": 35.0,  "lead_time_days": 10},
]

# Hardcoded incident narratives — realistic supply chain events across the 12-month window
_INCIDENT_DATA = [
    {
        "supplier_id": "SUP008", "incident_date": "2025-06-12",
        "incident_type": "Manufacturing Disruption", "affected_sku_category": "Consumables",
        "severity": "CRITICAL",
        "resolution_notes": "Factory floor shutdown due to equipment failure; production resumed after 18 days with third-party auditor sign-off.",
        "days_delayed": 22,
    },
    {
        "supplier_id": "SUP006", "incident_date": "2025-07-03",
        "incident_type": "Customs Hold", "affected_sku_category": "Consumables",
        "severity": "HIGH",
        "resolution_notes": "Shipment detained at Port of Los Angeles for labeling non-compliance; relabeling completed and goods released.",
        "days_delayed": 11,
    },
    {
        "supplier_id": "SUP004", "incident_date": "2025-08-19",
        "incident_type": "Quality Hold", "affected_sku_category": "PPE",
        "severity": "HIGH",
        "resolution_notes": "Lot recall issued for N95 mask filtration defect; replacement lot shipped from backup inventory.",
        "days_delayed": 8,
    },
    {
        "supplier_id": "SUP003", "incident_date": "2025-09-05",
        "incident_type": "Shipping Delay", "affected_sku_category": "Implants",
        "severity": "MEDIUM",
        "resolution_notes": "Trans-Pacific shipping congestion at Tokyo port; cargo re-routed via Osaka with 9-day delay.",
        "days_delayed": 9,
    },
    {
        "supplier_id": "SUP007", "incident_date": "2025-09-22",
        "incident_type": "Capacity Shortage", "affected_sku_category": "Surgical Instruments",
        "severity": "MEDIUM",
        "resolution_notes": "Increased demand from competing hospital networks depleted available stock; partial fulfillment issued with backorder.",
        "days_delayed": 6,
    },
    {
        "supplier_id": "SUP005", "incident_date": "2025-10-11",
        "incident_type": "Raw Material Shortage", "affected_sku_category": "Lab Equipment",
        "severity": "HIGH",
        "resolution_notes": "Polypropylene resin shortage globally; supplier sourced alternative resin with FDA equivalency documentation.",
        "days_delayed": 14,
    },
    {
        "supplier_id": "SUP001", "incident_date": "2025-10-28",
        "incident_type": "Regulatory Action", "affected_sku_category": "Surgical Instruments",
        "severity": "CRITICAL",
        "resolution_notes": "FDA Warning Letter issued for GMP violations at manufacturing site; facility remediation required before resuming shipments.",
        "days_delayed": 35,
    },
    {
        "supplier_id": "SUP008", "incident_date": "2025-11-14",
        "incident_type": "Natural Disaster", "affected_sku_category": "Consumables",
        "severity": "CRITICAL",
        "resolution_notes": "Cyclone Zara damaged warehouse facilities in Chennai; inventory destroyed, emergency procurement activated.",
        "days_delayed": 28,
    },
    {
        "supplier_id": "SUP002", "incident_date": "2025-12-02",
        "incident_type": "Shipping Delay", "affected_sku_category": "Diagnostic Equipment",
        "severity": "LOW",
        "resolution_notes": "Holiday freight backlog caused minor delay; goods arrived 4 days past scheduled delivery window.",
        "days_delayed": 4,
    },
    {
        "supplier_id": "SUP006", "incident_date": "2026-01-08",
        "incident_type": "Quality Hold", "affected_sku_category": "Consumables",
        "severity": "HIGH",
        "resolution_notes": "Sterility breach detected in IV catheter lot; quarantine enforced and replacement lot shipped within 2 weeks.",
        "days_delayed": 13,
    },
    {
        "supplier_id": "SUP004", "incident_date": "2026-01-25",
        "incident_type": "Capacity Shortage", "affected_sku_category": "PPE",
        "severity": "MEDIUM",
        "resolution_notes": "Seasonal demand spike during influenza outbreak reduced available stock; priority allocation negotiated with distributor.",
        "days_delayed": 5,
    },
    {
        "supplier_id": "SUP003", "incident_date": "2026-02-10",
        "incident_type": "Customs Hold", "affected_sku_category": "Implants",
        "severity": "MEDIUM",
        "resolution_notes": "Import permits expired for titanium components; documentation renewed and customs clearance obtained in 7 days.",
        "days_delayed": 7,
    },
    {
        "supplier_id": "SUP005", "incident_date": "2026-02-28",
        "incident_type": "Shipping Delay", "affected_sku_category": "Lab Equipment",
        "severity": "LOW",
        "resolution_notes": "Vessel diversion due to North Atlantic weather advisory; cargo re-routed via Rotterdam with minor delay.",
        "days_delayed": 3,
    },
    {
        "supplier_id": "SUP007", "incident_date": "2026-03-15",
        "incident_type": "Manufacturing Disruption", "affected_sku_category": "Surgical Instruments",
        "severity": "HIGH",
        "resolution_notes": "CNC machine failure halted precision machining line; backup equipment brought online after 10 days.",
        "days_delayed": 10,
    },
    {
        "supplier_id": "SUP001", "incident_date": "2026-04-05",
        "incident_type": "Raw Material Shortage", "affected_sku_category": "Surgical Instruments",
        "severity": "MEDIUM",
        "resolution_notes": "Stainless steel alloy 316L shortage due to export restrictions; alternative qualified vendor sourced.",
        "days_delayed": 6,
    },
]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def _write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote {len(rows):>5,} rows  →  {path.name}")

# ─── Generators ───────────────────────────────────────────────────────────────

def generate_suppliers() -> list[dict]:
    return list(SUPPLIERS)


def generate_inventory_snapshots() -> list[dict]:
    # Specific stock multipliers (relative to lead_time * demand) for interesting risk variety
    forced_stock_multipliers = {
        ("SKU-CON-002", "BOS"): 0.55,   # CRITICAL — Sterile Gauze nearly out in Boston
        ("SKU-CON-004", "CHI"): 0.72,   # CRITICAL — Foley Catheter critically low Chicago
        ("SKU-CON-001", "SEA"): 0.68,   # CRITICAL — IV Catheter low in Seattle
        ("SKU-IMP-001", "SEA"): 1.10,   # HIGH     — Hip Stem thin buffer Seattle
        ("SKU-IMP-003", "BOS"): 1.20,   # HIGH     — Spinal Cage low Boston
        ("SKU-SRG-004", "CHI"): 1.30,   # HIGH     — Bipolar Forceps Chicago
        ("SKU-PPE-001", "BOS"): 1.40,   # HIGH     — N95 borderline Boston
        ("SKU-LAB-004", "SEA"): 1.65,   # MEDIUM   — PCR Plates Seattle
    }

    rows = []
    for sku in SKUS:
        for site in SITES:
            demand = round(sku["base_demand"] * random.uniform(0.85, 1.15), 2)
            lead_time = sku["lead_time_days"]
            reorder_point = int(round(lead_time * demand * 1.20))

            key = (sku["sku_id"], site)
            if key in forced_stock_multipliers:
                current_stock = int(round(lead_time * demand * forced_stock_multipliers[key]))
            else:
                current_stock = int(round(lead_time * demand * random.uniform(1.6, 4.2)))

            rows.append({
                "sku_id":          sku["sku_id"],
                "sku_name":        sku["sku_name"],
                "site_id":         site,
                "category":        sku["category"],
                "current_stock":   max(0, current_stock),
                "reorder_point":   reorder_point,
                "avg_daily_demand": demand,
                "lead_time_days":  lead_time,
            })
    return rows


def generate_orders_history() -> list[dict]:
    rows = []
    order_seq = 1

    for sku in SKUS:
        supplier = SUPPLIER_MAP[sku["supplier_id"]]
        on_time_rate = supplier["on_time_delivery_rate"]
        avg_lead_time = supplier["avg_lead_time_days"]

        # Order interval drives order frequency; high-velocity items replenish weekly
        base_demand = sku["base_demand"]
        if base_demand >= 100:
            order_interval = 7
        elif base_demand >= 20:
            order_interval = 14
        elif base_demand >= 5:
            order_interval = 21
        else:
            order_interval = 30

        for site in SITES:
            site_demand = base_demand * random.uniform(0.85, 1.15)
            current_date = PERIOD_START

            while current_date < TODAY:
                jitter = random.randint(-2, 3)
                order_date = current_date + timedelta(days=max(0, jitter))
                if order_date >= TODAY:
                    break

                qty_ordered = max(1, int(order_interval * site_demand * random.uniform(0.90, 1.20)))
                expected_delivery = order_date + timedelta(days=avg_lead_time)

                on_time = random.random() < on_time_rate
                delay_days = random.randint(0, 1) if on_time else random.randint(3, 15)
                actual_delivery = expected_delivery + timedelta(days=delay_days)

                # Occasional partial fills (≈5% of orders)
                if random.random() < 0.05:
                    qty_received = int(qty_ordered * random.uniform(0.55, 0.90))
                else:
                    qty_received = qty_ordered

                # Future deliveries have no received quantity yet
                if actual_delivery > TODAY:
                    actual_delivery_str = ""
                    qty_received = 0
                else:
                    actual_delivery_str = actual_delivery.isoformat()

                rows.append({
                    "order_id":          f"ORD-{order_seq:05d}",
                    "sku_id":            sku["sku_id"],
                    "site_id":           site,
                    "order_date":        order_date.isoformat(),
                    "quantity_ordered":  qty_ordered,
                    "quantity_received": qty_received,
                    "supplier_id":       sku["supplier_id"],
                    "expected_delivery": expected_delivery.isoformat(),
                    "actual_delivery":   actual_delivery_str,
                })
                order_seq += 1
                current_date += timedelta(days=order_interval)

    return rows


def generate_supplier_incidents() -> list[dict]:
    # Build category → sku_id lookup for realistic affected_skus values
    category_skus: dict[str, list[str]] = {}
    for sku in SKUS:
        category_skus.setdefault(sku["category"], []).append(sku["sku_id"])

    rows = []
    for i, inc in enumerate(_INCIDENT_DATA, start=1):
        pool = category_skus.get(inc["affected_sku_category"], [])
        count = random.randint(1, min(3, len(pool)))
        affected_skus = ",".join(random.sample(pool, count))

        rows.append({
            "incident_id":      f"INC-{i:03d}",
            "supplier_id":      inc["supplier_id"],
            "incident_date":    inc["incident_date"],
            "incident_type":    inc["incident_type"],
            "affected_skus":    affected_skus,
            "severity":         inc["severity"],
            "resolution_notes": inc["resolution_notes"],
            "days_delayed":     inc["days_delayed"],
        })
    return rows

# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print("Generating SupplyLens seed data...\n")

    _write_csv(
        OUTPUT_DIR / "suppliers.csv",
        generate_suppliers(),
        ["supplier_id", "supplier_name", "country", "category",
         "contract_tier", "avg_lead_time_days", "on_time_delivery_rate"],
    )
    _write_csv(
        OUTPUT_DIR / "inventory_snapshots.csv",
        generate_inventory_snapshots(),
        ["sku_id", "sku_name", "site_id", "category",
         "current_stock", "reorder_point", "avg_daily_demand", "lead_time_days"],
    )
    orders = generate_orders_history()
    _write_csv(
        OUTPUT_DIR / "orders_history.csv",
        orders,
        ["order_id", "sku_id", "site_id", "order_date", "quantity_ordered",
         "quantity_received", "supplier_id", "expected_delivery", "actual_delivery"],
    )
    incidents = generate_supplier_incidents()
    _write_csv(
        OUTPUT_DIR / "supplier_incidents.csv",
        incidents,
        ["incident_id", "supplier_id", "incident_date", "incident_type",
         "affected_skus", "severity", "resolution_notes", "days_delayed"],
    )

    print(f"\nDone.")
    print(f"  {len(SUPPLIERS)} suppliers  |  {len(SKUS) * len(SITES)} inventory snapshots  "
          f"|  {len(orders)} orders  |  {len(incidents)} incidents")


if __name__ == "__main__":
    main()
