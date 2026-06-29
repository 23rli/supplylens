CREATE TABLE IF NOT EXISTS parts (
  part_number TEXT PRIMARY KEY,
  description TEXT,
  vendor TEXT,
  vendor_name TEXT,
  lead_time_weeks INTEGER NOT NULL,
  abc_group TEXT,
  on_hand INTEGER NOT NULL,
  on_order INTEGER NOT NULL,
  forecast REAL NOT NULL,
  last_year_usage REAL,
  unit_price REAL,
  product_per_case INTEGER NOT NULL,
  cases_per_pallet INTEGER NOT NULL,
  eoq INTEGER NOT NULL,
  safety_stock INTEGER NOT NULL
);
