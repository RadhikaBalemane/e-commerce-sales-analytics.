
-- E-COMMERCE SALES & CUSTOMER ANALYTICS
USE analytics;

-- 1. Check total records
SELECT COUNT(*) AS total_records
FROM cleaned_online_retail;

-- 2. Calculate total revenue
SELECT ROUND(SUM(TotalAmount), 2) AS total_revenue
FROM cleaned_online_retail;

-- 3. Count unique orders
SELECT COUNT(DISTINCT InvoiceNo) AS total_orders
FROM cleaned_online_retail;

-- 4. Count unique customers
SELECT COUNT(DISTINCT CustomerID) AS total_customers
FROM cleaned_online_retail;

-- 5. Top 10 products by revenue
SELECT
    Description,
    ROUND(SUM(TotalAmount), 2) AS revenue
FROM cleaned_online_retail
GROUP BY Description
ORDER BY revenue DESC
LIMIT 10;

-- 6. Top 10 customers by spending
SELECT
    CustomerID,
    ROUND(SUM(TotalAmount), 2) AS total_spending
FROM cleaned_online_retail
GROUP BY CustomerID
ORDER BY total_spending DESC
LIMIT 10;

-- 7. Revenue by country
SELECT
    Country,
    ROUND(SUM(TotalAmount), 2) AS revenue
FROM cleaned_online_retail
GROUP BY Country
ORDER BY revenue DESC
LIMIT 10;

-- 8. Monthly revenue trend
SELECT
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS month,
    ROUND(SUM(TotalAmount), 2) AS monthly_revenue
FROM cleaned_online_retail
GROUP BY DATE_FORMAT(InvoiceDate, '%Y-%m')
ORDER BY month;

-- 9. Average order value
SELECT
    ROUND(
        SUM(TotalAmount) / COUNT(DISTINCT InvoiceNo),
        2
    ) AS average_order_value
FROM cleaned_online_retail;

-- 10. Revenue by country and number of orders
SELECT
    Country,
    COUNT(DISTINCT InvoiceNo) AS total_orders,
    ROUND(SUM(TotalAmount), 2) AS total_revenue
FROM cleaned_online_retail
GROUP BY Country
ORDER BY total_revenue DESC;
