"""Parts master store + simulation orchestration for the inventory module."""
from db import fetch_all, fetch_one
from inventory.engine import Part, simulate, warehouse_pallet_load

_COLS = ["part_number", "description", "vendor", "vendor_name", "lead_time_weeks",
         "abc_group", "on_hand", "on_order", "forecast", "last_year_usage",
         "unit_price", "product_per_case", "cases_per_pallet", "eoq", "safety_stock"]


def _to_part(row: dict) -> Part:
    return Part(**{k: row[k] for k in _COLS})


def list_parts() -> list[dict]:
    return fetch_all("SELECT * FROM parts ORDER BY part_number")


def get_part(part_number: str) -> dict | None:
    return fetch_one("SELECT * FROM parts WHERE part_number = ?", (part_number,))


def parts_with_metrics(abc: str = None, vendor: str = None, status: str = None) -> list[dict]:
    out = []
    for row in list_parts():
        m = simulate(_to_part(row))
        if abc and row["abc_group"] != abc:
            continue
        if vendor and row["vendor"] != vendor:
            continue
        if status == "over" and m.weeks_overstocked == 0:
            continue
        if status == "under" and m.weeks_understocked == 0:
            continue
        out.append({**row,
                    "weekly_demand": m.weekly_demand, "weeks_on_hand": round(m.weeks_on_hand, 1),
                    "annual_spend": round(m.annual_spend, 2),
                    "overstock_point": m.overstock_point, "weeks_overstocked": m.weeks_overstocked,
                    "weeks_understocked": m.weeks_understocked,
                    "min_products": round(m.min_products, 1), "max_products": round(m.max_products, 1),
                    "avg_products": round(m.avg_products, 1),
                    "max_pallets_over": round(m.max_pallets_over, 1),
                    "max_pallets_under": round(m.max_pallets_under, 1)})
    return out


def part_detail(part_number: str) -> dict | None:
    row = get_part(part_number)
    if not row:
        return None
    m = simulate(_to_part(row))
    return {**row, "products": m.products, "pallets": m.pallets,
            "overstock_point": m.overstock_point, "restock_point": m.restock_point,
            "safety_stock": row["safety_stock"], "weekly_demand": m.weekly_demand,
            "weeks_overstocked": m.weeks_overstocked, "weeks_understocked": m.weeks_understocked}


def worst_offenders(kind: str, limit: int = 15) -> list[dict]:
    rows = parts_with_metrics()
    key = "weeks_overstocked" if kind == "over" else "weeks_understocked"
    return sorted(rows, key=lambda r: r[key], reverse=True)[:limit]


def warehouse_load() -> list[dict]:
    parts = [_to_part(r) for r in list_parts()]
    load = warehouse_pallet_load(parts)
    return [{"week": w, "pallets": v} for w, v in enumerate(load)]


def inventory_stats() -> dict:
    rows = parts_with_metrics()
    over = sum(1 for r in rows if r["weeks_overstocked"] > 0)
    under = sum(1 for r in rows if r["weeks_understocked"] > 0)
    spend = sum(r["annual_spend"] for r in rows)
    return {"total_parts": len(rows), "overstock_parts": over,
            "understock_parts": under, "total_annual_spend": round(spend, 2)}
