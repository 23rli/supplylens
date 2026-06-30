# Using Your Own Data

SupplyLens ships with realistic sample data so you can explore it immediately. When
you're ready to use **your** suppliers, inventory, and parts, there are three ways
to load data, from easiest to most production-ready.

| Method | Best for | Where |
|---|---|---|
| **A. Import parts file (CSV/XLSX)** | Quickly loading your parts master into the Inventory Engine | In-app, no code |
| **B. Edit the seed scripts** | Replacing the local demo dataset (risk, suppliers, SKUs) | `backend/data/`, `backend/inventory/` |
| **C. Load CSVs into Azure SQL** | Production with the cloud database | `backend/data/` |

> **Tip:** The fastest way to see your own numbers is Method A for parts, and
> Method B if you also want your own suppliers and risk SKUs.

---

## Method A — Import a parts file (no code)

The Inventory Engine accepts a **CSV or XLSX** upload directly in the app.

1. Log in and go to **Inventory → Parts**.
2. Click **Import** and choose your `.csv` or `.xlsx` file.
3. The parts load instantly and the 52-week simulation recalculates.

### Required columns

The first row must be a header with these exact column names. `part_number` is the
only strictly required value per row; the rest default to `0` if blank.

| Column | Type | Meaning |
|---|---|---|
| `part_number` | text | Unique part ID (**required**) |
| `description` | text | Human-readable name |
| `vendor` | text | Vendor code |
| `vendor_name` | text | Vendor display name |
| `lead_time_weeks` | integer | Weeks from order to delivery |
| `abc_group` | text | `A`, `B`, or `C` value classification |
| `on_hand` | integer | Units currently in stock |
| `on_order` | integer | Units already on order |
| `forecast` | number | Annual demand (units/year) |
| `last_year_usage` | number | Units consumed last year |
| `unit_price` | number | Cost per unit |
| `product_per_case` | integer | Units per case |
| `cases_per_pallet` | integer | Cases per pallet |
| `eoq` | integer | Economic order quantity (units per order) |
| `safety_stock` | integer | Minimum buffer to keep on hand |

### Example CSV

```csv
part_number,description,vendor,vendor_name,lead_time_weeks,abc_group,on_hand,on_order,forecast,last_year_usage,unit_price,product_per_case,cases_per_pallet,eoq,safety_stock
PN-1001,Steel Bracket A36,V1,Midwest Steel,3,A,400,0,12000,11800,8.50,12,40,200,80
PN-1002,Aluminum Extrusion 6061,V1,Midwest Steel,3,A,150,200,9000,8700,12.75,6,40,200,60
PN-1003,PCB Controller Board,V2,Pacific Components,14,B,40,0,2400,2300,45.00,1,40,100,30
```

> Re-importing a `part_number` that already exists **overwrites** it
> (`INSERT OR REPLACE`), so you can re-upload a corrected file safely.

You can also import via the API directly — see
[`POST /api/inventory/import`](api-reference.md#inventory-engine).

---

## Method B — Edit the seed scripts (replace the local dataset)

The local SQLite database (`backend/supplylens.db`) is built by small, readable
Python scripts. Edit the data lists at the top of each script, then re-run it.

### B1. Suppliers + risk SKUs — `backend/data/seed_risk.py`

Edit the `SUPPLIERS` and `SKUS` lists near the top of the file:

```python
SUPPLIERS = [
    # (id, name, country, category, contract_tier, lead_time_days, on_time_rate, quality_score)
    ("SUP001", "Midwest Steel Co", "United States", "Raw Materials", "Primary", 5, 0.94, 0.97),
    # ... add your suppliers here ...
]

SKUS = [
    # (sku_id, name, category, avg_daily_demand, lead_time_days, supplier_id, unit_cost)
    ("SKU001", "Steel Bracket A36", "Critical", 62, 7, "SUP001", 8.50),
    # ... add your SKUs here ...
]
```

The script automatically computes days-of-supply, buffer days, and the risk level
for each SKU across the three sites. Then re-run it:

```bash
cd backend
python data/seed_risk.py
```

> `category` should be `Critical`, `Standard`, or `Consumable`. `contract_tier` is
> typically `Primary`, `Backup`, or `Spot`.

### B2. Parts master — `backend/inventory/seed_parts.py`

This generates the ~120 demo parts. To use your own, the cleanest path is **Method
A** (import a file). If you'd rather script it, replace the row-building loop with
your own list of tuples matching the `parts` table column order (see the schema
below), then run `python inventory/seed_parts.py`.

### B3. Demo users — `backend/data/seed_users.py`

Edit the `USERS` list to change the login(s):

```python
USERS = [
    # (email, name, password, role, tenant_id)
    ("admin@supplylens.io", "Demo Admin", "demo1234", "admin", "demo"),
]
```

Passwords are hashed with PBKDF2 before storage. Re-run `python data/seed_users.py`.

> **Sites** (Boston / Chicago / Seattle) are defined by the `SITES` list in
> `seed_risk.py` — change them there if your operation uses different locations.

---

## Method C — Load CSVs into Azure SQL (production)

For production, SupplyLens reads from Azure SQL instead of SQLite. The data is
loaded from four CSV files in `backend/data/`.

1. **Generate or replace the CSVs.** You can regenerate fresh synthetic ones with
   `python data/seed_data.py`, or drop in your own files using the formats below.
2. **Create the schema** by running `backend/schema.sql` against your Azure SQL
   database.
3. **Import** with:
   ```bash
   cd backend/data
   python import_data.py
   ```
   (Requires `pyodbc` + ODBC Driver 18, and Azure SQL credentials in `backend/.env`.)

### CSV formats

**`suppliers.csv`**
```csv
supplier_id,supplier_name,country,category,contract_tier,avg_lead_time_days,on_time_delivery_rate,quality_score,active
SUP001,Midwest Steel Co,United States,Raw Materials,Primary,5,0.94,0.97,1
```

**`inventory.csv`**
```csv
sku_id,sku_name,site_id,category,current_stock,reorder_point,avg_daily_demand,lead_time_days,primary_supplier_id,unit_cost
SKU001,Steel Bracket A36,BOSTON,Critical,655,315,45,7,SUP001,8.5
```

**`orders.csv`** (historical orders, used for supplier on-time analysis)
```csv
sku_id,site_id,order_date,quantity_ordered,quantity_received,supplier_id,expected_delivery,actual_delivery,status
SKU001,BOSTON,2025-06-30,364,364,SUP001,2025-07-07,2025-07-07,Delivered
```

**`incidents.csv`** (supplier disruptions)
```csv
supplier_id,incident_date,incident_type,affected_skus,severity,resolution_notes,days_delayed
SUP002,2026-05-31,Late Delivery,"SKU020,SKU021",High,Resolved via air freight,6
```

> Dates are `YYYY-MM-DD`. `affected_skus` is a comma-separated list **in quotes**.
> Set `DB_BACKEND=azure` in `.env` so the running app reads from Azure SQL.

---

## Reference: the `parts` table schema

This is what the Inventory Engine reads. It maps 1:1 to the import columns in
Method A.

| Column | Type | Required |
|---|---|---|
| `part_number` | TEXT (primary key) | yes |
| `description` | TEXT | no |
| `vendor` / `vendor_name` | TEXT | no |
| `lead_time_weeks` | INTEGER | yes |
| `abc_group` | TEXT | no |
| `on_hand` / `on_order` | INTEGER | yes |
| `forecast` | REAL | yes |
| `last_year_usage` | REAL | no |
| `unit_price` | REAL | no |
| `product_per_case` | INTEGER | yes |
| `cases_per_pallet` | INTEGER | yes |
| `eoq` | INTEGER | yes |
| `safety_stock` | INTEGER | yes |

---

## Starting over

To wipe the local database and reseed from scratch, delete the SQLite file and
re-run the seed scripts:

```bash
cd backend
rm supplylens.db                # Windows: del supplylens.db
python data/seed_risk.py
python inventory/seed_parts.py
python data/seed_users.py
```
</content>
