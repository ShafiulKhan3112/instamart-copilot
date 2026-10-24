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
# ---------------- LABELS ----------------

sept = orders[
    (orders["order_ts"] >= cutoff)
    &
    (orders["order_ts"] < "2025-10-01")
]

completed_sept = sept[
    sept["status"] == "completed"
]

rfm["lapsed"] = ~rfm["customer_id"].isin(
    completed_sept["customer_id"]
)

rfm["lapsed"] = rfm["lapsed"].astype(int)

# ---------------- ADD CUSTOMER DATA ----------------

data = rfm.merge(
    customers,
    on="customer_id",
    how="left"
)

print("Dataset Size:", len(data))
print("Lapsed:", data["lapsed"].sum())
# ---------------- FEATURES ----------------

feature_cols = [
    "recency",
    "frequency",
    "monetary",
    "avg_discount",
    "avg_delivery",
    "age"
]

X = data[feature_cols]

y = data["lapsed"]

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )
)

print(
    "Train:",
    len(X_train)
)

print(
    "Test:",
    len(X_test)
)
# ---------------- SCALE FEATURES ----------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)

# ---------------- LOGISTIC REGRESSION ----------------

grid = GridSearchCV(
    LogisticRegression(max_iter=1000),
    {
        "C":[0.01,0.1,1,10,100]
    },
    cv=5,
    scoring="f1"
)

grid.fit(
    X_train_scaled,
    y_train
)

best_lr = grid.best_estimator_

preds = best_lr.predict(
    X_test_scaled
)

print("\nBEST C")
print(grid.best_params_)

print("\nTEST F1")
print(
    round(
        f1_score(
            y_test,
            preds
        ),
        3
    )
)

print("\nCONFUSION MATRIX")

print(
    confusion_matrix(
        y_test,
        preds
    )
)
# ---------------- SAVE MODEL ----------------

joblib.dump(
    best_lr,
    "outputs/lapse_model.joblib"
)

loaded_model = joblib.load(
    "outputs/lapse_model.joblib"
)

loaded_preds = loaded_model.predict(
    X_test_scaled
)

same = (
    preds == loaded_preds
).all()

print(
    "\nModel Reload Check:",
    same
)
# ---------------- RETENTION LIST ----------------

segments = pd.read_csv(
    "outputs/customer_segments.csv"
)

premium_ids = set(
    segments[
        segments["is_premium"] == True
    ]["customer_id"]
)

test_df = data.loc[
    X_test.index,
    ["customer_id"]
].copy()

test_df["lapse_probability"] = (
    best_lr.predict_proba(
        X_test_scaled
    )[:,1]
)

test_df["actually_lapsed"] = (
    y_test.values
)

retention = test_df[
    test_df["customer_id"]
    .isin(premium_ids)
]

retention = retention.sort_values(
    "lapse_probability",
    ascending=False
)

retention = retention.head(10)

retention.to_csv(
    "outputs/retention_list.csv",
    index=False
)

print(
    "\nRetention List Created"
)

print(
    "Rows:",
    len(retention)
)

print(
    retention.head()
)