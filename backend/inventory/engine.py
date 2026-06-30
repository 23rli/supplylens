"""
52-Week Inventory Overstock/Understock Simulation Engine.

Pure, deterministic functions - no DB, no IO. One part in, weekly series out.
Projects each part's stock week by week using forecast demand, lead time,
safety stock, and EOQ.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field

WEEKS = 52


@dataclass
class Part:
    part_number: str
    description: str = ""
    vendor: str = ""
    vendor_name: str = ""
    lead_time_weeks: int = 1
    abc_group: str = "C"
    on_hand: int = 0
    on_order: int = 0
    forecast: float = 0.0          # annual demand (products)
    last_year_usage: float = 0.0
    unit_price: float = 0.0
    product_per_case: int = 1
    cases_per_pallet: int = 1
    eoq: int = 1
    safety_stock: int = 0


@dataclass
class PartMetrics:
    weekly_demand: int
    restock_point: float
    overstock_point: float
    overstock_pallet_point: float
    weeks_on_hand: float
    annual_spend: float
    weeks_overstocked: int
    weeks_understocked: int
    min_products: float
    max_products: float
    avg_products: float
    min_pallets: float
    max_pallets: float
    avg_pallets: float
    max_pallets_over: float
    max_pallets_under: float
    products: list[float] = field(default_factory=list)
    pallets: list[float] = field(default_factory=list)


def _pallet_capacity(part: Part) -> float:
    return max(1, part.cases_per_pallet * part.product_per_case)


def simulate(part: Part, weeks: int = WEEKS) -> PartMetrics:
    """Roll a week-by-week inventory projection and return metrics + series."""
    weekly = math.ceil(part.forecast / 52) if part.forecast else 0
    weekly = max(weekly, 0)
    overstock_point = weekly * part.lead_time_weeks + part.safety_stock + part.eoq
    restock_point = weekly * part.lead_time_weeks + part.safety_stock
    cap = _pallet_capacity(part)

    # Existing pipeline arrivals (backlog) spread by arrival interval.
    sip = math.ceil(part.on_order / part.eoq) if part.eoq and part.on_order > 0 else 0
    interval = (part.lead_time_weeks / sip) if sip else 0
    backlog_arrivals = [0] * weeks
    if sip:
        for i in range(1, sip + 1):
            w = round(i * interval)
            if 0 <= w < weeks:
                backlog_arrivals[w] += 1

    new_arrivals = [0] * weeks      # replenishment orders this engine decides to place
    projection = [0.0] * weeks      # projected on-hand stock at the end of each week
    projection[0] = part.on_hand
    over_ct = under_ct = 0

    for w in range(weeks):
        # Roll stock forward: last week's level + arrivals (each = one EOQ) - demand.
        if w > 0:
            gain = (backlog_arrivals[w] + new_arrivals[w]) * part.eoq
            projection[w] = projection[w - 1] + gain - weekly
        # Below safety stock -> place an order that lands after the lead time.
        if projection[w] < part.safety_stock:
            arr = w + part.lead_time_weeks
            if arr < weeks:
                new_arrivals[arr] += 1
        # Tally weeks spent over the overstock ceiling / under the safety floor.
        if projection[w] > overstock_point:
            over_ct += 1
        if projection[w] < part.safety_stock:
            under_ct += 1

    pallets = [p / cap for p in projection]
    over_excess = [max(0.0, (p - overstock_point) / cap) for p in projection]
    under_short = [max(0.0, (part.safety_stock - p) / cap) for p in projection]

    return PartMetrics(
        weekly_demand=weekly,
        restock_point=restock_point,
        overstock_point=overstock_point,
        overstock_pallet_point=overstock_point / cap,
        weeks_on_hand=(part.on_hand / weekly) if weekly else float("inf"),
        annual_spend=part.unit_price * part.forecast,
        weeks_overstocked=over_ct,
        weeks_understocked=under_ct,
        min_products=min(projection),
        max_products=max(projection),
        avg_products=sum(projection) / weeks,
        min_pallets=min(pallets),
        max_pallets=max(pallets),
        avg_pallets=sum(pallets) / weeks,
        max_pallets_over=max(over_excess),
        max_pallets_under=max(under_short),
        products=[round(p, 1) for p in projection],
        pallets=[round(p, 2) for p in pallets],
    )


def warehouse_pallet_load(parts: list[Part], weeks: int = WEEKS) -> list[float]:
    """Total projected pallets across all parts, per week."""
    total = [0.0] * weeks
    for p in parts:
        m = simulate(p, weeks)
        for w in range(weeks):
            total[w] += m.pallets[w]
    return [round(t, 1) for t in total]
