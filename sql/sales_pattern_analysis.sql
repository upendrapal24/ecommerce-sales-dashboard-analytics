-- =============================================================================
-- E-COMMERCE SALES PATTERN ANALYSIS SQL QUERY SUITE
-- Author: Upendra Pal (github.com/upendrapal24)
-- Target Engine: SQLite / PostgreSQL / MySQL / Power BI SQL Connector
-- Database Table: sales
-- Description: Queries analyzing top sellers, discount impact, category dynamics,
--              underperforming inventory, and regional payment distributions.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. OVERALL EXECUTIVE SALES SUMMARY
-- Calculates core metrics: Total Revenue, Gross Revenue, Units Sold, Avg Order Value
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(product_id) AS total_products_listed,
    SUM(units_sold) AS total_units_sold,
    ROUND(SUM(total_revenue), 2) AS total_revenue_usd,
    ROUND(SUM(gross_revenue), 2) AS total_gross_revenue_usd,
    ROUND(SUM(total_discount_loss), 2) AS total_discount_given_usd,
    ROUND(AVG(price), 2) AS avg_list_price,
    ROUND(AVG(final_price), 2) AS avg_final_price,
    ROUND(AVG(discount_percent), 2) AS avg_discount_percent,
    ROUND(AVG(rating), 2) AS avg_product_rating
FROM sales;

-- -----------------------------------------------------------------------------
-- 2. TOP SELLER PERFORMANCE LEADERBOARD
-- Ranks sellers by total revenue generated, volume, and customer rating
-- -----------------------------------------------------------------------------
SELECT 
    seller,
    seller_city,
    COUNT(product_id) AS products_offered,
    SUM(units_sold) AS total_units_sold,
    ROUND(SUM(total_revenue), 2) AS total_revenue_usd,
    ROUND(AVG(seller_rating), 2) AS avg_seller_rating,
    ROUND(AVG(discount_percent), 2) AS avg_discount_offered,
    ROUND(SUM(total_revenue) * 100.0 / (SELECT SUM(total_revenue) FROM sales), 2) AS revenue_share_percent
FROM sales
GROUP BY seller, seller_city
ORDER BY total_revenue_usd DESC;

-- -----------------------------------------------------------------------------
-- 3. DISCOUNT IMPACT ANALYSIS (PRICE ELASTICITY & REVENUE MARGINS)
-- Analyzes sales velocity and revenue generation across discount brackets
-- -----------------------------------------------------------------------------
SELECT 
    discount_tier,
    COUNT(product_id) AS total_products,
    SUM(units_sold) AS total_units_sold,
    ROUND(AVG(units_sold), 1) AS avg_units_per_product,
    ROUND(SUM(total_revenue), 2) AS total_revenue_usd,
    ROUND(SUM(total_discount_loss), 2) AS gross_discount_cost_usd,
    ROUND(AVG(rating), 2) AS avg_customer_rating
FROM sales
GROUP BY discount_tier
ORDER BY total_revenue_usd DESC;

-- -----------------------------------------------------------------------------
-- 4. CATEGORY PERFORMANCE MATRIX
-- Evaluates category revenue contribution, average order size, and return policy
-- -----------------------------------------------------------------------------
SELECT 
    category,
    COUNT(product_id) AS product_count,
    SUM(units_sold) AS total_units_sold,
    ROUND(SUM(total_revenue), 2) AS total_revenue_usd,
    ROUND(AVG(final_price), 2) AS avg_selling_price,
    ROUND(AVG(discount_percent), 2) AS avg_discount_percent,
    ROUND(AVG(rating), 2) AS avg_category_rating,
    ROUND(AVG(stock_available), 1) AS avg_stock_level,
    SUM(CASE WHEN is_returnable = 1 THEN 1 ELSE 0 END) AS returnable_products_count
FROM sales
GROUP BY category
ORDER BY total_revenue_usd DESC;

-- -----------------------------------------------------------------------------
-- 5. BEST-SELLING PRODUCTS (TOP 10 BY UNITS & REVENUE)
-- Identifies top 10 star products driving overall catalog performance
-- -----------------------------------------------------------------------------
SELECT 
    product_id,
    product_name,
    category,
    brand,
    seller,
    price,
    discount_percent,
    final_price,
    units_sold,
    ROUND(total_revenue, 2) AS total_revenue_usd,
    rating
FROM sales
ORDER BY total_revenue DESC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- 6. UNDERPERFORMING PRODUCT INVENTORY AUDIT
-- Identifies low-velocity inventory (Bottom percentile by volume & high stock)
-- -----------------------------------------------------------------------------
SELECT 
    product_id,
    product_name,
    category,
    seller,
    price,
    final_price,
    stock_available,
    units_sold,
    ROUND(total_revenue, 2) AS total_revenue_usd,
    rating,
    performance_segment
FROM sales
WHERE performance_segment = 'Underperformer'
ORDER BY units_sold ASC, stock_available DESC
LIMIT 15;

-- -----------------------------------------------------------------------------
-- 7. PRICE TIER VS VOLUME BREAKDOWN
-- Analyzes sales distribution across Budget, Mid-Range, Premium, and Luxury price tiers
-- -----------------------------------------------------------------------------
SELECT 
    price_tier,
    COUNT(product_id) AS product_count,
    SUM(units_sold) AS total_units_sold,
    ROUND(SUM(total_revenue), 2) AS total_revenue_usd,
    ROUND(AVG(discount_percent), 2) AS avg_discount_percent,
    ROUND(AVG(rating), 2) AS avg_rating
FROM sales
GROUP BY price_tier
ORDER BY total_revenue_usd DESC;

-- -----------------------------------------------------------------------------
-- 8. PAYMENT MODE & LOGISTICS EFFICIENCY ANALYSIS
-- Analyzes sales volume and delivery days across payment configurations
-- -----------------------------------------------------------------------------
SELECT 
    payment_modes,
    COUNT(product_id) AS product_listings,
    SUM(units_sold) AS total_units_sold,
    ROUND(SUM(total_revenue), 2) AS total_revenue_usd,
    ROUND(AVG(delivery_days), 1) AS avg_delivery_days,
    ROUND(AVG(return_policy_days), 1) AS avg_return_policy_days
FROM sales
GROUP BY payment_modes
ORDER BY total_revenue_usd DESC;
