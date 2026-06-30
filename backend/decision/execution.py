"""Execution stubs: simulate fixes and log to DB, scoped per tenant. Real PO export is V2."""
from datetime import datetime
from db import get_connection


def _log_action(tenant_id, sku, site, atype, label, cost, benefit) -> int:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""INSERT INTO actions (tenant_id, sku_id, site_id, action_type, label, cost, benefit, status, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                (tenant_id, sku, site, atype, label, cost, benefit, "executing", datetime.now().isoformat()))
    conn.commit()
    rid = cur.lastrowid
    cur.close(); conn.close()
    return rid


def create_po(tenant_id, sku, site, label="Expedite PO", cost=0, benefit=0) -> dict:
    aid = _log_action(tenant_id, sku, site, "EXPEDITE", label, cost, benefit)
    return {"action_id": aid, "type": "EXPEDITE", "status": "executing", "eta_days": 2}


def transfer_stock(tenant_id, sku, site, label="Transfer", cost=0, benefit=0) -> dict:
    aid = _log_action(tenant_id, sku, site, "REBALANCE", label, cost, benefit)
    return {"action_id": aid, "type": "REBALANCE", "status": "executing", "eta_days": 1}


def list_actions(tenant_id) -> list[dict]:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT * FROM actions WHERE tenant_id = ? ORDER BY id DESC", (tenant_id,))
    rows = [dict(r) for r in cur.fetchall()]
    cur.close(); conn.close()
    return rows
