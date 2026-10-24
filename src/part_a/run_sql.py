import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "data/instamart.db"
)

print("\nQ1")
q1 = """
SELECT
customer_id,
SUM(order_amount) total_spend
FROM orders
WHERE status='completed'
AND order_amount>500
GROUP BY customer_id
HAVING SUM(order_amount)>8000
"""
df1 = pd.read_sql_query(q1, conn)
print("Rows:", len(df1))

print("\nQ2")
q2 = """
SELECT
c.city,
p.category,
ROUND(SUM(o.order_amount),2) revenue
FROM orders o
JOIN customers c
ON o.customer_id=c.customer_id
JOIN products p
ON o.product_id=p.product_id
WHERE o.status='completed'
GROUP BY c.city,p.category
"""
df2 = pd.read_sql_query(q2, conn)

print(
"Rows:",
len(df2)
)

print(
"Revenue:",
round(
df2["revenue"].sum(),
2
)
)

print("\nQ3")
q3 = """
SELECT *
FROM products
WHERE price_inr >
(
SELECT AVG(price_inr)
FROM products
)
"""
df3 = pd.read_sql_query(q3, conn)
print("Products:", len(df3))

conn.close()