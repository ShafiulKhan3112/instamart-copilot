import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

rfm = pd.read_csv(
    "outputs/rfm.csv"
)

X = rfm[
    ["recency","frequency","monetary"]
]

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

kmeans = KMeans(
    n_clusters=4,
    n_init=10,
    random_state=42
)

rfm["segment_id"] = kmeans.fit_predict(
    X_scaled
)

summary = rfm.groupby(
    "segment_id"
).agg({
    "recency":"mean",
    "frequency":"mean",
    "monetary":"mean",
    "customer_id":"count"
})

print(summary)

premium_segment = (
    summary["monetary"]
    .idxmax()
)

name_map = {
    0:"Regular Customers",
    1:"Premium Customers",
    2:"At Risk Customers",
    3:"Frequent Buyers"
}

rfm["segment_name"] = (
    rfm["segment_id"]
    .map(name_map)
)

rfm["is_premium"] = (
    rfm["segment_id"]
    == premium_segment
)

pca = PCA(
    n_components=2
)

pca.fit(X_scaled)

print(
    "\nPCA Variance:"
)

print(
    pca.explained_variance_ratio_
)

rfm.to_csv(
    "outputs/customer_segments.csv",
    index=False
)

print(
    "\ncustomer_segments.csv saved"
)