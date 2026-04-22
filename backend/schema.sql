-- SupplyLens MySQL Schema
-- Medical device distribution platform

CREATE DATABASE IF NOT EXISTS supplylens;
USE supplylens;

-- ─── Tables ───────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id           VARCHAR(10)    NOT NULL,
    supplier_name         VARCHAR(100)   NOT NULL,
    country               VARCHAR(50)    NOT NULL,
    category              VARCHAR(50)    NOT NULL,
    contract_tier         VARCHAR(10)    NOT NULL,
    avg_lead_time_days    INT            NOT NULL,
    on_time_delivery_rate DECIMAL(4, 3)  NOT NULL,
    PRIMARY KEY (supplier_id)
);

CREATE TABLE IF NOT EXISTS inventory_snapshots (
    id               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    sku_id           VARCHAR(20)     NOT NULL,
    sku_name         VARCHAR(100)    NOT NULL,
    site_id          VARCHAR(10)     NOT NULL,
    category         VARCHAR(50)     NOT NULL,
    current_stock    INT             NOT NULL,
    reorder_point    INT             NOT NULL,
    avg_daily_demand DECIMAL(8, 2)   NOT NULL,
    lead_time_days   INT             NOT NULL,
    snapshot_date    DATE            NOT NULL DEFAULT (CURRENT_DATE),
    PRIMARY KEY (id),
    INDEX idx_sku_site (sku_id, site_id),
    INDEX idx_snapshot_date (snapshot_date)
);

CREATE TABLE IF NOT EXISTS orders_history (
    order_id          VARCHAR(15)  NOT NULL,
    sku_id            VARCHAR(20)  NOT NULL,
    site_id           VARCHAR(10)  NOT NULL,
    supplier_id       VARCHAR(10)  NOT NULL,
    order_date        DATE         NOT NULL,
    quantity_ordered  INT          NOT NULL,
    quantity_received INT          NOT NULL DEFAULT 0,
    expected_delivery DATE         NOT NULL,
    actual_delivery   DATE         NULL,
    PRIMARY KEY (order_id),
    INDEX idx_supplier (supplier_id),
    INDEX idx_sku (sku_id),
    INDEX idx_order_date (order_date),
    CONSTRAINT fk_orders_supplier
        FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id)
);

CREATE TABLE IF NOT EXISTS supplier_incidents (
    incident_id      VARCHAR(10)  NOT NULL,
    supplier_id      VARCHAR(10)  NOT NULL,
    incident_date    DATE         NOT NULL,
    incident_type    VARCHAR(50)  NOT NULL,
    affected_skus    TEXT         NOT NULL,       -- comma-separated sku_ids
    severity         ENUM('CRITICAL','HIGH','MEDIUM','LOW') NOT NULL,
    resolution_notes TEXT         NOT NULL,
    days_delayed     INT          NOT NULL DEFAULT 0,
    PRIMARY KEY (incident_id),
    INDEX idx_supplier (supplier_id),
    INDEX idx_incident_date (incident_date),
    INDEX idx_severity (severity),
    CONSTRAINT fk_incidents_supplier
        FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id)
);

-- ─── View ─────────────────────────────────────────────────────────────────────

-- sku_risk_summary: latest snapshot per SKU+site enriched with supplier context
-- and a computed risk tier based on days-of-stock relative to lead time.
CREATE OR REPLACE VIEW sku_risk_summary AS
WITH latest AS (
    -- Most recent snapshot per sku+site
    SELECT
        s.sku_id,
        s.sku_name,
        s.site_id,
        s.category,
        s.current_stock,
        s.reorder_point,
        s.avg_daily_demand,
        s.lead_time_days,
        s.snapshot_date,
        ROW_NUMBER() OVER (
            PARTITION BY s.sku_id, s.site_id
            ORDER BY s.snapshot_date DESC, s.id DESC
        ) AS rn
    FROM inventory_snapshots s
),
skus AS (
    SELECT * FROM latest WHERE rn = 1
),
supplier_map AS (
    -- Derive supplier per SKU from the most recent order placed for that SKU
    SELECT
        oh.sku_id,
        oh.supplier_id
    FROM orders_history oh
    INNER JOIN (
        SELECT sku_id, MAX(order_date) AS latest_order
        FROM orders_history
        GROUP BY sku_id
    ) lо ON oh.sku_id = lо.sku_id AND oh.order_date = lо.latest_order
),
incident_counts AS (
    -- Rolling 12-month incident count per supplier
    SELECT
        supplier_id,
        COUNT(*)                                                    AS incident_count_12m,
        SUM(CASE WHEN severity = 'CRITICAL' THEN 1 ELSE 0 END)     AS critical_incidents_12m,
        SUM(days_delayed)                                           AS total_days_delayed_12m
    FROM supplier_incidents
    WHERE incident_date >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
    GROUP BY supplier_id
)
SELECT
    sk.sku_id,
    sk.sku_name,
    sk.site_id,
    sk.category,
    sk.current_stock,
    sk.reorder_point,
    sk.avg_daily_demand,
    sk.lead_time_days,
    sk.snapshot_date,
    -- Days of stock remaining
    ROUND(
        CASE WHEN sk.avg_daily_demand > 0
             THEN sk.current_stock / sk.avg_daily_demand
             ELSE NULL
        END, 1
    ) AS days_of_stock,
    -- Whether stock is at or below the reorder trigger
    (sk.current_stock <= sk.reorder_point) AS below_reorder_point,
    -- Supplier context
    sm.supplier_id,
    sup.supplier_name,
    sup.country,
    sup.contract_tier,
    sup.on_time_delivery_rate,
    COALESCE(ic.incident_count_12m,    0) AS incident_count_12m,
    COALESCE(ic.critical_incidents_12m, 0) AS critical_incidents_12m,
    COALESCE(ic.total_days_delayed_12m, 0) AS total_days_delayed_12m,
    -- Risk tier: CRITICAL / HIGH / MEDIUM / LOW
    CASE
        WHEN sk.current_stock = 0                                                    THEN 'CRITICAL'
        WHEN sk.avg_daily_demand > 0
             AND sk.current_stock / sk.avg_daily_demand < sk.lead_time_days * 0.75  THEN 'CRITICAL'
        WHEN sk.current_stock <= sk.reorder_point                                   THEN 'HIGH'
        WHEN sk.avg_daily_demand > 0
             AND sk.current_stock / sk.avg_daily_demand < sk.lead_time_days * 1.5   THEN 'MEDIUM'
        ELSE 'LOW'
    END AS risk_tier
FROM skus sk
LEFT JOIN supplier_map sm  ON sk.sku_id = sm.sku_id
LEFT JOIN suppliers    sup ON sm.supplier_id = sup.supplier_id
LEFT JOIN incident_counts ic ON sm.supplier_id = ic.supplier_id;
