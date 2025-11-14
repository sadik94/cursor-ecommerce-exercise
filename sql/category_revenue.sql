-- Revenue by product category along with the number of contributing orders.
WITH item_totals AS (
    SELECT
        oi.order_id,
        p.category,
        SUM(oi.quantity * oi.unit_price) AS line_total
    FROM order_items oi
    JOIN products p ON p.id = oi.product_id
    GROUP BY oi.order_id, p.category
)
SELECT
    category,
    COUNT(DISTINCT order_id) AS orders_touching_category,
    ROUND(SUM(line_total), 2) AS gross_revenue,
    ROUND(AVG(line_total), 2) AS avg_order_value
FROM item_totals
GROUP BY category
ORDER BY gross_revenue DESC;

