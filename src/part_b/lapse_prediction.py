import pandas as pd

orders = pd.read_csv(
    "data/clean/orders.csv"
)

customers = pd.read_csv(
    "data/clean/customers.csv"
)

orders["order_ts"] = pd.to_datetime(
    orders["order_ts"]
)

cutoff = pd.Timestamp(
    "2025-09-01"
)

before = orders[
    orders["order_ts"] < cutoff
]

sept = orders[
    (orders["order_ts"] >= cutoff)
    &
    (
        orders["order_ts"]
        <
        "2025-10-01"
    )
]

completed_before = before[
    before["status"]=="completed"
]

completed_sept = sept[
    sept["status"]=="completed"
]

cohort = set(
    completed_before["customer_id"]
)

labels = []

for cid in cohort:

    active = (
        completed_sept[
            completed_sept[
                "customer_id"
            ] == cid
        ].shape[0]
    )

    labels.append(
        [
            cid,
            0 if active > 0 else 1
        ]
    )

label_df = pd.DataFrame(
    labels,
    columns=[
        "customer_id",
        "lapsed"
    ]
)

print(
    "Customers:",
    len(label_df)
)

print(
    "Lapsed:",
    label_df["lapsed"].sum()
)

print(
    "Percent:",
    round(
        label_df["lapsed"].mean()
        *100,
        2
    )
)