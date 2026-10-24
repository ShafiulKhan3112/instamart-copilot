import pandas as pd

customers = pd.read_csv("data/raw/customers.csv")
products = pd.read_csv("data/raw/products.csv")
orders = pd.read_csv("data/raw/orders.csv")

print("=" * 50)
print("CUSTOMERS")
print("=" * 50)

print("Shape:", customers.shape)
print(customers.dtypes)

print("\nMissing values")
print(customers.isna().sum())

print("\nBlank ages")
print((customers["age"].astype(str).str.strip() == "").sum())

print("\nBlank genders")
print((customers["gender"].fillna("").str.strip() == "").sum())

print("=" * 50)
print("PRODUCTS")
print("=" * 50)

print("Shape:", products.shape)

print("=" * 50)
print("ORDERS")
print("=" * 50)

print("Shape:", orders.shape)

print("\nExact duplicates")
print(orders.duplicated().sum())

print("\nPending rows")
print((orders["status"] == "pending").sum())

print("\nDistinct order ids")
print(orders["order_id"].nunique())