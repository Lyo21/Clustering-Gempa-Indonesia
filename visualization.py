import matplotlib.pyplot as plt
import geopandas as gpd


# --------------------------------------------------
# 1️⃣ Plot Elbow Method
# --------------------------------------------------
def plot_elbow(inertias, k_range):
    """
    Membuat grafik Elbow Method (Inertia vs Jumlah Cluster).
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(list(k_range), inertias, marker="o", linewidth=2)
    ax.set_xlabel("Jumlah Cluster (k)")
    ax.set_ylabel("Inertia (SSE)")
    ax.set_title("Metode Elbow untuk Penentuan Jumlah Cluster Optimal")
    ax.grid(True, linestyle="--", alpha=0.5)
    return fig


# --------------------------------------------------
# 2️⃣ Plot Silhouette Score
# --------------------------------------------------
def plot_silhouette(sil_scores, k_range):
    """
    Membuat grafik Silhouette Score untuk menentukan jumlah cluster optimal.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(list(k_range), sil_scores, marker="o", linewidth=2)
    ax.set_xlabel("Jumlah Cluster (k)")
    ax.set_ylabel("Silhouette Score")
    ax.set_title("Evaluasi Jumlah Cluster Optimal (Silhouette)")
    ax.grid(True, linestyle="--", alpha=0.5)
    return fig


# --------------------------------------------------
# 3️⃣ Scatter Plot Clustering
# --------------------------------------------------
def plot_scatter(df, colors):
    """
    Membuat scatter plot hasil clustering berdasarkan Depth dan Magnitude.
    Warna klaster mengikuti get_cluster_colors().
    """
    fig, ax = plt.subplots(figsize=(7, 5))

    for cluster_id, color in colors.items():
        cluster_data = df[df["cluster"] == cluster_id]
        ax.scatter(
            cluster_data["depth"],
            cluster_data["magnitude"],
            label=f"Cluster {cluster_id}",
            color=color,
            alpha=0.7,
            edgecolors="black",
            linewidth=0.5
        )

    ax.set_xlabel("Kedalaman (km)")
    ax.set_ylabel("Magnitudo")
    ax.set_title("Hasil Clustering Gempa (K-Means)")
    ax.legend(title="Cluster")
    ax.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    return fig


# --------------------------------------------------
# 4️⃣ Bar Chart Jumlah Data per Klaster
# --------------------------------------------------
def plot_cluster_distribution(cluster_counts, colors):
    """
    Membuat bar chart jumlah data pada setiap klaster
    dengan warna yang konsisten dengan scatter & peta.
    """
    fig, ax = plt.subplots(figsize=(6, 4))

    # Warna bar mengikuti ID klaster
    bar_colors = [colors[cluster_id] for cluster_id in cluster_counts.index]

    cluster_counts.plot(
        kind="bar",
        ax=ax,
        color=bar_colors,
        edgecolor="black"
    )

    ax.set_xlabel("Klaster")
    ax.set_ylabel("Jumlah Data Gempa")
    ax.set_title("Distribusi Jumlah Data pada Setiap Klaster")
    ax.set_xticklabels(cluster_counts.index, rotation=0)
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    plt.tight_layout()
    return fig


# --------------------------------------------------
# 5️⃣ Peta Statis Indonesia
# --------------------------------------------------
def plot_map_static(df, colors):
    """
    Membuat peta statis Indonesia dengan titik gempa
    berwarna sesuai klaster.
    """
    world = gpd.read_file(
        "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
    )

    indonesia = (
        world[world["NAME"] == "Indonesia"]
        if "NAME" in world.columns
        else world[world["name"] == "Indonesia"]
    )

    fig, ax = plt.subplots(figsize=(8, 6))
    indonesia.plot(ax=ax, color="lightyellow", edgecolor="black")

    for cluster_id, color in colors.items():
        cluster_data = df[df["cluster"] == cluster_id]
        ax.scatter(
            cluster_data["longitude"],
            cluster_data["latitude"],
            label=f"Cluster {cluster_id}",
            color=color,
            alpha=0.7,
            edgecolors="black",
            linewidth=0.5,
            s=40
        )

    ax.set_title("Visualisasi Klaster Gempa di Peta Indonesia")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend(title="Cluster")
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    return fig