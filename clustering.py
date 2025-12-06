import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.cm as cm
import matplotlib.colors as mcolors


def run_clustering(df):
    """
    Jalankan clustering otomatis untuk data gempa.
    Output:
      - df_clustered: DataFrame dengan kolom 'cluster'
      - best_k: jumlah cluster terbaik
      - best_score: nilai silhouette terbaik
      - sil_scores: list skor silhouette untuk tiap k
      - k_range: list k yang diuji
    """

    # Pastikan kolom yang dibutuhkan ada
    required_cols = ["latitude", "longitude", "depth", "magnitude"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Kolom '{col}' tidak ditemukan di dataset!")

    # Ambil hanya kolom numerik untuk clustering
    X = df[required_cols].copy()

    # Normalisasi (biar tiap fitur seimbang)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Uji berbagai jumlah cluster
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

    # Simpan hasil terbaik
    df_clustered = df.copy()
    df_clustered["cluster"] = best_labels

    return df_clustered, best_k, best_score, sil_scores, k_range


def get_cluster_colors(df):
    """
    Menghasilkan dictionary warna HEX untuk tiap cluster berdasarkan jumlah cluster.
    Warna ini akan digunakan seragam di semua visualisasi.
    """
    cluster_ids = sorted(df["cluster"].unique())
    num_clusters = len(cluster_ids)

    cmap = cm.get_cmap("tab10", num_clusters)
    colors = {
        cluster_id: mcolors.to_hex(cmap(i))
        for i, cluster_id in enumerate(cluster_ids)
    }

    return colors