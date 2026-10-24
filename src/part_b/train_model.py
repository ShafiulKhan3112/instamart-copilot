import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import (
    train_test_split,
    GridSearchCV
)

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score
)

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

completed_before = before[
    before["status"] == "completed"
]

rfm = completed_before.groupby(
    "customer_id"
).agg(
    recency=(
        "order_ts",
        lambda x: (
            cutoff - x.max()
        ).days
    ),
    frequency=(
        "order_id",
        "nunique"
    ),
    monetary=(
        "order_amount",
        "sum"
    ),
    avg_discount=(
        "discount_pct",
        "mean"
    ),
    avg_delivery=(
        "delivery_minutes",
        "mean"
    )
).reset_index()