-- Example joined query: total revenue per customer with order counts.
WITH order_totals AS (
    SELECT
        oi.order_id,
        SUM(oi.quantity * oi.unit_price) AS order_total
    FROM order_items oi
    GROUP BY oi.order_id
)
SELECT
    c.id AS customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.country,
    COUNT(DISTINCT o.id) AS orders_placed,
    ROUND(SUM(order_totals.order_total), 2) AS lifetime_value
FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_totals ON order_totals.order_id = o.id
GROUP BY c.id
ORDER BY lifetime_value DESC
LIMIT 10;

