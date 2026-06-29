-- SupplyLens schema for Azure SQL Database (T-SQL)
-- Create the database via the portal/CLI, then run this against it.

-- Table 1: Current inventory state per SKU per site
IF OBJECT_ID('dbo.inventory_snapshots', 'U') IS NULL
CREATE TABLE dbo.inventory_snapshots (
  id INT IDENTITY(1,1) PRIMARY KEY,
  sku_id VARCHAR(20) NOT NULL,
  sku_name VARCHAR(100) NOT NULL,
  site_id VARCHAR(20) NOT NULL,            -- 'BOSTON', 'CHICAGO', 'SEATTLE'
  category VARCHAR(50) NOT NULL,           -- 'Critical', 'Standard', 'Consumable'
  current_stock INT NOT NULL,
  reorder_point INT NOT NULL,
  avg_daily_demand FLOAT NOT NULL,
  lead_time_days INT NOT NULL,             -- days from PO to delivery
  primary_supplier_id VARCHAR(20),
  unit_cost DECIMAL(10,2),
  last_updated DATETIME2 DEFAULT SYSUTCDATETIME(),
  CONSTRAINT unique_sku_site UNIQUE (sku_id, site_id)
);

-- Table 2: Historical orders (12 months)
IF OBJECT_ID('dbo.orders_history', 'U') IS NULL
CREATE TABLE dbo.orders_history (
  id INT IDENTITY(1,1) PRIMARY KEY,
  sku_id VARCHAR(20) NOT NULL,
  site_id VARCHAR(20) NOT NULL,
  order_date DATE NOT NULL,
  quantity_ordered INT NOT NULL,
  quantity_received INT NOT NULL,
  supplier_id VARCHAR(20) NOT NULL,
  expected_delivery DATE NOT NULL,
  actual_delivery DATE,                    -- NULL if not yet delivered
  status VARCHAR(20) DEFAULT 'Delivered'   -- 'Delivered', 'Pending', 'Late'
);

-- Table 3: Supplier master data
IF OBJECT_ID('dbo.suppliers', 'U') IS NULL
CREATE TABLE dbo.suppliers (
  supplier_id VARCHAR(20) PRIMARY KEY,
  supplier_name VARCHAR(100) NOT NULL,
  country VARCHAR(50) NOT NULL,
  category VARCHAR(50) NOT NULL,           -- what they supply
  contract_tier VARCHAR(20) NOT NULL,      -- 'Primary', 'Backup', 'Spot'
  avg_lead_time_days INT NOT NULL,
  on_time_delivery_rate FLOAT NOT NULL,    -- 0.0 to 1.0
  quality_score FLOAT NOT NULL,            -- 0.0 to 1.0
  active BIT DEFAULT 1,
  contact_name VARCHAR(100),
  notes VARCHAR(MAX)
);

-- Table 4: Supplier incident log
IF OBJECT_ID('dbo.supplier_incidents', 'U') IS NULL
CREATE TABLE dbo.supplier_incidents (
  id INT IDENTITY(1,1) PRIMARY KEY,
  supplier_id VARCHAR(20) NOT NULL,
  incident_date DATE NOT NULL,
  incident_type VARCHAR(50) NOT NULL,      -- 'Late Delivery', 'Quality Issue', 'Shortage', 'Force Majeure', 'Communication Failure'
  affected_skus VARCHAR(MAX),              -- comma-separated sku_ids
  severity VARCHAR(20) NOT NULL,           -- 'Low', 'Medium', 'High', 'Critical'
  resolution_notes VARCHAR(MAX),
  days_delayed INT DEFAULT 0,
  resolved BIT DEFAULT 1
);
GO

-- View: Computed risk summary (used by backend and AI layer)
CREATE OR ALTER VIEW dbo.sku_risk_summary AS
SELECT
  i.sku_id,
  i.sku_name,
  i.site_id,
  i.category,
  i.current_stock,
  i.avg_daily_demand,
  i.lead_time_days,
  i.reorder_point,
  i.primary_supplier_id,
  i.unit_cost,
  ROUND(i.current_stock / NULLIF(i.avg_daily_demand, 0), 1) AS days_of_supply,
  ROUND((i.current_stock / NULLIF(i.avg_daily_demand, 0)) - i.lead_time_days, 1) AS buffer_days,
  CASE
    WHEN (i.current_stock / NULLIF(i.avg_daily_demand, 0)) <= i.lead_time_days THEN 'CRITICAL'
    WHEN (i.current_stock / NULLIF(i.avg_daily_demand, 0)) <= i.lead_time_days * 1.5 THEN 'HIGH'
    WHEN (i.current_stock / NULLIF(i.avg_daily_demand, 0)) <= i.lead_time_days * 2.0 THEN 'MEDIUM'
    ELSE 'LOW'
  END AS risk_level,
  CASE
    WHEN (i.current_stock / NULLIF(i.avg_daily_demand, 0)) <= i.lead_time_days THEN
      CASE i.category
        WHEN 'Critical' THEN 'EXPEDITE immediately from backup supplier'
        ELSE 'Place emergency order or rebalance from sister site'
      END
    WHEN (i.current_stock / NULLIF(i.avg_daily_demand, 0)) <= i.lead_time_days * 1.5 THEN 'Place standard order now - within reorder window'
    WHEN (i.current_stock / NULLIF(i.avg_daily_demand, 0)) <= i.lead_time_days * 2.0 THEN 'Monitor closely - approaching reorder point'
    ELSE 'No action required'
  END AS recommended_action
FROM dbo.inventory_snapshots i;
GO
