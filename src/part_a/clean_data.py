import pandas as pd
import numpy as np
import os

os.makedirs("data/clean", exist_ok=True)

customers = pd.read_csv("data/raw/customers.csv")

# ---------------- CITY ----------------

customers["city"] = (
    customers["city"]
    .astype(str)
    .str.strip()
    .str.title()
)

# ---------------- GENDER ----------------

gender_map = {
    "male": "male",
    "Male": "male",
    "M": "male",
    "m": "male",
    "MALE": "male",

    "female": "female",
    "Female": "female",
    "F": "female",
    "f": "female",
    "FEMALE": "female"
}

customers["gender"] = customers["gender"].map(gender_map)
customers["gender"] = customers["gender"].fillna("unknown")

# ---------------- AGE ----------------

customers["age"] = pd.to_numeric(
    customers["age"],
    errors="coerce"
)

customers.loc[
    (customers["age"] < 10) |
    (customers["age"] > 100),
    "age"
] = np.nan

customers["age"] = (
    customers
    .groupby("city")["age"]
    .transform(
        lambda x: x.fillna(x.median())
    )
)

customers["age"] = customers["age"].astype(int)

# ---------------- DATE ----------------

customers["signup_date"] = pd.to_datetime(
    customers["signup_date"]
)

print("\nCITY COUNTS")
print(customers["city"].value_counts())

print("\nGENDER COUNTS")
print(customers["gender"].value_counts())

print("\nMISSING AGE")
print(customers["age"].isna().sum())

print("\nAGE RANGE")
print(
    customers["age"].min(),
    customers["age"].max()
)

customers.to_csv(
    "data/clean/customers.csv",
    index=False
)
# ==========================
# ORDERS CLEANING
# ==========================

orders = pd.read_csv("data/raw/orders.csv")
products = pd.read_csv("data/raw/products.csv")

orders["order_ts"] = pd.to_datetime(
    orders["order_ts"]
)

# Remove exact duplicates

orders = orders.drop_duplicates()

# Keep latest record per order_id

orders = (
    orders
    .sort_values("order_ts")
    .drop_duplicates(
        subset="order_id",
        keep="last"
    )
)

# Convert order_amount

orders["order_amount"] = pd.to_numeric(
    orders["order_amount"],
    errors="coerce"
)

# Merge products

orders = orders.merge(
    products[
        ["product_id","price_inr","category"]
    ],
    on="product_id",
    how="left"
)

# Fill missing amounts

calc_amount = (
    orders["price_inr"]
    * orders["quantity"]
    * (1 - orders["discount_pct"]/100)
)

calc_amount = calc_amount.round(2)

orders["order_amount"] = orders[
    "order_amount"
].fillna(calc_amount)

# Negative delivery

orders["delivery_minutes"] = pd.to_numeric(
    orders["delivery_minutes"],
    errors="coerce"
)

orders.loc[
    orders["delivery_minutes"] < 0,
    "delivery_minutes"
] = np.nan

# Category median

completed = orders["status"] == "completed"

orders.loc[completed, "delivery_minutes"] = (
    orders.loc[completed]
    .groupby("category")["delivery_minutes"]
    .transform(
        lambda x: x.fillna(x.median())
    )
)

# Remove helper columns

orders = orders.drop(
    columns=["price_inr","category"]
)

print("\nORDER ROWS")
print(len(orders))

print("\nSTATUS COUNTS")
print(orders["status"].value_counts())

print("\nMISSING AMOUNTS")
print(orders["order_amount"].isna().sum())

print("\nSUM COMPLETED REVENUE")
print(
    round(
        orders.loc[
            orders["status"]=="completed",
            "order_amount"
        ].sum(),
        2
    )
)

print("\nMISSING DELIVERY COMPLETED")
print(
    orders.loc[
        orders["status"]=="completed",
        "delivery_minutes"
    ].isna().sum()
)

print("\nMISSING DELIVERY CANCELLED")
print(
    orders.loc[
        orders["status"]=="cancelled",
        "delivery_minutes"
    ].isna().sum()
)

orders.to_csv(
    "data/clean/orders.csv",
    index=False
)

products.to_csv(
    "data/clean/products.csv",
    index=False
)