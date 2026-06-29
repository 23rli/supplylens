from fastapi import APIRouter, Query, HTTPException, UploadFile, File
from typing import Optional
from inventory.store import (parts_with_metrics, part_detail, worst_offenders,
                             warehouse_load, inventory_stats)
from inventory.importer import parse_csv, parse_xlsx, import_parts

router = APIRouter()

@router.get("/inventory/stats")
def stats():
    return inventory_stats()

@router.get("/inventory/parts")
def parts(abc: Optional[str] = Query(None), vendor: Optional[str] = Query(None),
          status: Optional[str] = Query(None, description="over | under")):
    return parts_with_metrics(abc=abc, vendor=vendor, status=status)

@router.get("/inventory/part/{part_number}")
def detail(part_number: str):
    d = part_detail(part_number)
    if not d:
        raise HTTPException(404, "Part not found")
    return d

@router.get("/inventory/worst")
def worst(kind: str = Query("over", description="over | under"), limit: int = 15):
    return worst_offenders(kind, limit)

@router.get("/inventory/warehouse-load")
def warehouse():
    return warehouse_load()

@router.post("/inventory/import")
async def import_file(file: UploadFile = File(...)):
    data = await file.read()
    try:
        rows = parse_xlsx(data) if file.filename.lower().endswith((".xlsx", ".xlsm")) else parse_csv(data)
        n = import_parts(rows)
    except Exception as e:
        raise HTTPException(400, f"Import failed: {e}")
    return {"imported": n}
