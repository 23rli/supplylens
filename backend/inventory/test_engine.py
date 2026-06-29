"""Unit tests for the inventory simulation engine (run: python -m pytest)."""
import math
from inventory.engine import Part, simulate, warehouse_pallet_load


def _part(**kw):
    base = dict(part_number="P1", lead_time_weeks=4, on_hand=400, on_order=0,
                forecast=520, eoq=100, safety_stock=50,
                product_per_case=1, cases_per_pallet=1, unit_price=2.0)
    base.update(kw)
    return Part(**base)


def test_weekly_demand_ceil():
    assert simulate(_part(forecast=520)).weekly_demand == 10
    assert simulate(_part(forecast=521)).weekly_demand == 11


def test_overstock_point():
    m = simulate(_part(forecast=520, lead_time_weeks=4, safety_stock=50, eoq=100))
    assert m.overstock_point == 10 * 4 + 50 + 100


def test_annual_spend():
    assert simulate(_part(forecast=520, unit_price=2.0)).annual_spend == 1040.0


def test_depletes_and_reorders():
    m = simulate(_part(on_hand=400, on_order=0))
    assert m.min_products < m.max_products
    assert m.weeks_understocked >= 0
    assert len(m.products) == 52


def test_pallet_conversion():
    m = simulate(_part(on_hand=400, product_per_case=2, cases_per_pallet=5))
    assert m.products[0] == 400
    assert m.pallets[0] == 40.0  # 400 / (5*2)


def test_warehouse_load():
    load = warehouse_pallet_load([_part(), _part(part_number="P2")])
    assert len(load) == 52 and load[0] > 0
