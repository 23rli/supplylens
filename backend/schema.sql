CREATE DATABASE IF NOT EXISTS supplylens;
USE supplylens;

-- Table 1: Current inventory state per SKU per site
CREATE TABLE IF NOT EXISTS inventory_snapshots (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sku_id VARCHAR(20) NOT NULL,
  sku_name VARCHAR(100) NOT NULL,
  site_id VARCHAR(20) NOT NULL,          -- 'BOSTON', 'CHICAGO', 'SEATTLE'
  category VARCHAR(50) NOT NULL,          -- 'Critical', 'Standard', 'Consumable'
  current_stock INT NOT NULL,
  reorder_point INT NOT NULL,
  avg_daily_demand FLOAT NOT NULL,
  lead_time_days INT NOT NULL,            -- days from PO to delivery
  primary_supplier_id VARCHAR(20),
  unit_cost DECIMAL(10,2),
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY unique_sku_site (sku_id, site_id)
);

-- Table 2: Historical orders (12 months)
CREATE TABLE IF NOT EXISTS orders_history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sku_id VARCHAR(20) NOT NULL,
  site_id VARCHAR(20) NOT NULL,
  order_date DATE NOT NULL,
  quantity_ordered INT NOT NULL,
  quantity_received INT NOT NULL,
  supplier_id VARCHAR(20) NOT NULL,
  expected_delivery DATE NOT NULL,
  actual_delivery DATE,                   -- NULL if not yet delivered
  status VARCHAR(20) DEFAULT 'Delivered'  -- 'Delivered', 'Pending', 'Late'
);

-- Table 3: Supplier master data
CREATE TABLE IF NOT EXISTS suppliers (
  supplier_id VARCHAR(20) PRIMARY KEY,
  supplier_name VARCHAR(100) NOT NULL,
  country VARCHAR(50) NOT NULL,
  category VARCHAR(50) NOT NULL,          -- what they supply
  contract_tier VARCHAR(20) NOT NULL,     -- 'Primary', 'Backup', 'Spot'
  avg_lead_time_days INT NOT NULL,
  on_time_delivery_rate FLOAT NOT NULL,   -- 0.0 to 1.0
  quality_score FLOAT NOT NULL,           -- 0.0 to 1.0
  active BOOLEAN DEFAULT TRUE,
  contact_name VARCHAR(100),
  notes TEXT
);

-- Table 4: Supplier incident log
CREATE TABLE IF NOT EXISTS supplier_incidents (
  id INT AUTO_INCREMENT PRIMARY KEY,
  supplier_id VARCHAR(20) NOT NULL,
  incident_date DATE NOT NULL,
  incident_type VARCHAR(50) NOT NULL,     -- 'Late Delivery', 'Quality Issue', 'Shortage', 'Force Majeure', 'Communication Failure'
  affected_skus TEXT,                     -- comma-separated sku_ids
  severity VARCHAR(20) NOT NULL,          -- 'Low', 'Medium', 'High', 'Critical'
  resolution_notes TEXT,
  days_delayed INT DEFAULT 0,
  resolved BOOLEAN DEFAULT TRUE
);

-- View: Computed risk summary (used by backend and AI layer)
CREATE OR REPLACE VIEW sku_risk_summary AS
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
    WHEN (i.current_stock / NULLIF(i.avg_daily_demand, 0)) <= i.lead_time_days * 1.5 THEN 'Place standard order now — within reorder window'
    WHEN (i.current_stock / NULLIF(i.avg_daily_demand, 0)) <= i.lead_time_days * 2.0 THEN 'Monitor closely — approaching reorder point'
    ELSE 'No action required'
  END AS recommended_action
FROM inventory_snapshots i;
