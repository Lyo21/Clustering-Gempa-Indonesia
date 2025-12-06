import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.cm as cm
import matplotlib.colors as mcolors


def run_clustering(df):
    required_cols = ["latitude", "longitude", "depth", "magnitude"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Kolom '{col}' tidak ditemukan di dataset!")

    # CLEANING DATA
    df = df.copy()
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=required_cols)

    # DATA UNTUK CLUSTERING
    X = df[required_cols].copy()

    # SCALING
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # MENCARI JUMLAH KLASTER TERBAIK
    k_range = range(2, 9)
    sil_scores = []
    best_score = -1
    best_k = 2
    best_labels = None

    for k in k_range:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        sil_scores.append(score)

        if score > best_score:
            best_score = score
            best_k = k
            best_labels = labels

    # HASIL
    df_clustered = df.copy()
    df_clustered["cluster"] = best_labels

    return df_clustered, best_k, best_score, sil_scores, k_range


def get_cluster_colors(df):
    """Menghasilkan warna konsisten untuk setiap cluster."""
    unique_clusters = sorted(df["cluster"].unique())
    cmap = cm.get_cmap("tab10", len(unique_clusters))

    color_map = {
        cluster: mcolors.to_hex(cmap(i))
        for i, cluster in enumerate(unique_clusters)
    }

    # Mengembalikan list warna sesuai setiap baris cluster
    return df["cluster"].map(color_map)