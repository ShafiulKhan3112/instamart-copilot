import pandas as pd

customers = pd.read_csv("data/clean/customers.csv")
orders = pd.read_csv("data/clean/orders.csv")

assert len(customers) == 1200
assert len(orders) == 12309

assert (
    orders["order_id"].nunique()
    == 12309
)

assert (
    orders["status"]
    .eq("completed")
    .sum()
    == 11110
)

assert (
    orders["status"]
    .eq("cancelled")
    .sum()
    == 1199
)

assert orders["order_amount"].isna().sum() == 0

assert (
    orders.loc[
        orders["status"]=="completed",
        "delivery_minutes"
    ].isna().sum()
    == 0
)

assert (
    orders.loc[
        orders["status"]=="cancelled",
        "delivery_minutes"
    ].isna().sum()
    == 1199
)

revenue = round(
    orders.loc[
        orders["status"]=="completed",
        "order_amount"
    ].sum(),
    2
)

assert revenue == 2998668.80

print("ALL CHECKPOINTS PASSED")