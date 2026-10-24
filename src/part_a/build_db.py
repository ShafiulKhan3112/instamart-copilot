import sqlite3
import pandas as pd

customers = pd.read_csv("data/clean/customers.csv")
products = pd.read_csv("data/clean/products.csv")
orders = pd.read_csv("data/clean/orders.csv")

conn = sqlite3.connect("data/instamart.db")

customers.to_sql(
    "customers",
    conn,
    if_exists="replace",
    index=False
)

products.to_sql(
    "products",
    conn,
    if_exists="replace",
    index=False
)

orders.to_sql(
    "orders",
    conn,
    if_exists="replace",
    index=False
)

conn.commit()

for table in [
    "customers",
    "products",
    "orders"
]:
    count = pd.read_sql_query(
        f"SELECT COUNT(*) as cnt FROM {table}",
        conn
    )
    print(table)
    print(count)

conn.close()

print("\nDATABASE CREATED")