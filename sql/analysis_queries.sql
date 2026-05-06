-- ============================================================
-- Project 3: Retail Customer Segmentation (RFM Analysis)
-- SQL Analysis Queries
-- ============================================================

-- 1. RFM Scores per Customer
SELECT
    o.customer_id,
    DATEDIFF('2024-01-01', MAX(o.order_date))  AS recency_days,
    COUNT(DISTINCT o.order_id)                  AS frequency,
    ROUND(SUM(o.total_amount), 2)               AS monetary
FROM orders o
WHERE o.status = 'Delivered'
GROUP BY o.customer_id
ORDER BY monetary DESC;

-- 2. Revenue by Segment
SELECT
    s.segment,
    COUNT(DISTINCT s.customer_id)   AS customer_count,
    ROUND(SUM(s.monetary), 2)       AS total_revenue,
    ROUND(AVG(s.monetary), 2)       AS avg_revenue_per_customer,
    ROUND(AVG(s.recency_days), 1)   AS avg_days_since_last_order,
    ROUND(AVG(s.frequency), 1)      AS avg_orders
FROM rfm_segments s
GROUP BY s.segment
ORDER BY total_revenue DESC;

-- 3. Category Revenue Breakdown
SELECT
    category,
    COUNT(*)               AS orders,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
WHERE status = 'Delivered'
GROUP BY category
ORDER BY total_revenue DESC;

-- 4. Monthly Revenue Trend
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(DISTINCT customer_id)      AS unique_customers,
    COUNT(*)                         AS total_orders,
    ROUND(SUM(total_amount), 2)      AS total_revenue,
    ROUND(AVG(total_amount), 2)      AS avg_order_value
FROM orders
WHERE status = 'Delivered'
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;

-- 5. Champions vs Lost: Behaviour Comparison
SELECT
    segment,
    ROUND(AVG(recency_days), 1)   AS avg_recency,
    ROUND(AVG(frequency), 1)      AS avg_orders,
    ROUND(AVG(monetary), 2)       AS avg_spent,
    ROUND(AVG(rfm_score), 1)      AS avg_rfm_score
FROM rfm_segments
WHERE segment IN ('Champions', 'Lost', 'At Risk', 'Loyal Customers')
GROUP BY segment;

-- 6. Acquisition Channel Performance
SELECT
    c.acquisition_channel,
    COUNT(DISTINCT c.customer_id)    AS customers_acquired,
    COUNT(o.order_id)                AS total_orders,
    ROUND(SUM(o.total_amount), 2)    AS total_revenue,
    ROUND(AVG(o.total_amount), 2)    AS avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'Delivered'
GROUP BY c.acquisition_channel
ORDER BY total_revenue DESC;

-- 7. Discount Impact on Revenue
SELECT
    discount_pct,
    COUNT(*)                    AS orders,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
WHERE status = 'Delivered'
GROUP BY discount_pct
ORDER BY discount_pct;

-- 8. Return Rate by Category
SELECT
    category,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN status = 'Returned' THEN 1 ELSE 0 END) AS returns,
    ROUND(SUM(CASE WHEN status='Returned' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS return_rate_pct
FROM orders
GROUP BY category
ORDER BY return_rate_pct DESC;
