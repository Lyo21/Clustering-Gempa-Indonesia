import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


# ELBOW METHOD
def run_elbow(df):
    required_cols = ["latitude", "longitude", "depth", "magnitude"]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Kolom '{col}' tidak ditemukan di dataset!")

    df = df.copy()
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=required_cols)

    X = df[required_cols].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    k_range = range(2, 9)
    inertias = []

    for k in k_range:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(X_scaled)
        inertias.append(model.inertia_)

    return inertias, k_range


# SILHOUETTE & CLUSTERING
def run_clustering(df):
    required_cols = ["latitude", "longitude", "depth", "magnitude"]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Kolom '{col}' tidak ditemukan di dataset!")

    df = df.copy()
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=required_cols)

    X = df[required_cols].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    k_range = range(2, 9)
    silhouette_scores = []

    best_score = -1
    best_k = 2
    best_labels = None

    for k in k_range:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        silhouette_scores.append(score)

        if score > best_score:
            best_score = score
            best_k = k
            best_labels = labels

    df_clustered = df.copy()
    df_clustered["cluster"] = best_labels

    return df_clustered, best_k, best_score, silhouette_scores, k_range


# JUMLAH DATA PER KLASTER
def get_cluster_counts(df_clustered):
    return df_clustered["cluster"].value_counts().sort_index()


# WARNA KLASTER (KONTRAS TOTAL)
def get_cluster_colors(df_clustered):
    distinct_colors = [
        "#E41A1C",  # Merah
        "#377EB8",  # Biru
        "#4DAF4A",  # Hijau
        "#FF7F00",  # Oranye
        "#984EA3",  # Ungu
        "#FFFF33",  # Kuning
        "#A65628",  # Coklat
        "#F781BF"   # Pink
    ]

    unique_clusters = sorted(df_clustered["cluster"].unique())

    return {
        cluster: distinct_colors[i % len(distinct_colors)]
        for i, cluster in enumerate(unique_clusters)
    }