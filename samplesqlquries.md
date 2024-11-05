1. Total Sales by Region
This query calculates the total sales value (price * quantity) grouped by each region

SELECT region, SUM(price * quantity) AS total_sales
FROM df
GROUP BY region
ORDER BY total_sales DESC;

2. Average Price per Category
This query finds the average price for products in each category.

SELECT category, AVG(price) AS average_price
FROM df
GROUP BY category
ORDER BY average_price DESC;

3. Total Quantity Sold by Product
This query calculates the total quantity sold for each product.

SELECT product, SUM(quantity) AS total_quantity
FROM df
GROUP BY product
ORDER BY total_quantity DESC;

4. Top 3 Most Expensive Products
This query retrieves the top 3 most expensive products based on price.

SELECT product, price
FROM df
ORDER BY price DESC
LIMIT 3;

5. Sales by Month
This query calculates total sales by month, extracting the month from the sale_date.

SELECT strftime('%Y-%m', sale_date) AS month, SUM(price * quantity) AS total_sales
FROM df
GROUP BY month
ORDER BY month;

6. Products Sold in Each Category in North Region
This query lists products sold in each category specifically in the North region.

SELECT category, product, SUM(quantity) AS quantity_sold
FROM df
WHERE region = 'North'
GROUP BY category, product
ORDER BY quantity_sold DESC;

7. Total Revenue for Electronics
This query calculates the total revenue generated from products in the "Electronics" category.

SELECT SUM(price * quantity) AS electronics_revenue
FROM df
WHERE category = 'Electronics';







