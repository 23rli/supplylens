from fastapi import APIRouter, Query
from database import get_suppliers, get_supplier_incidents
from typing import Optional

router = APIRouter()

@router.get("/suppliers")
def suppliers():
    """Returns all active suppliers with on-time rates and incident counts."""
    return get_suppliers()

@router.get("/incidents")
def incidents(supplier_id: Optional[str] = Query(None)):
    """Returns supplier incidents, optionally filtered by supplier."""
    return get_supplier_incidents(supplier_id=supplier_id)
