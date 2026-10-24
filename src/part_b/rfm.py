import pandas as pd

orders = pd.read_csv(
    "data/clean/orders.csv"
)

orders["order_ts"] = pd.to_datetime(
    orders["order_ts"]
)

completed = orders[
    orders["status"] == "completed"
].copy()

snapshot = pd.Timestamp(
    "2025-10-01 00:00:00"
)

rfm = completed.groupby(
    "customer_id"
).agg(
    recency=(
        "order_ts",
        lambda x: (
            snapshot - x.max()
        ).days
    ),
    frequency=(
        "order_id",
        "nunique"
    ),
    monetary=(
        "order_amount",
        "sum"
    )
).reset_index()

print("Customers:", len(rfm))

print(
    "\nRecency Median:",
    rfm["recency"].median()
)

print(
    "Recency Min:",
    rfm["recency"].min()
)

print(
    "Recency Max:",
    rfm["recency"].max()
)

print(
    "\nFrequency Mean:",
    round(
        rfm["frequency"].mean(),
        2
    )
)

print(
    "Frequency Max:",
    rfm["frequency"].max()
)

print(
    "\nMonetary Mean:",
    round(
        rfm["monetary"].mean(),
        2
    )
)

print(
    "Monetary Max:",
    round(
        rfm["monetary"].max(),
        2
    )
)

rfm.to_csv(
    "outputs/rfm.csv",
    index=False
)