import streamlit as st
import pandas as pd
import os

from clustering import run_clustering, get_cluster_colors
from visualization import plot_silhouette, plot_scatter, plot_map_static
from mapping import plot_map_interactive

# Konfigurasi halaman
st.set_page_config(page_title="Clustering Gempa Indonesia", layout="wide")

st.title("📊 Sistem Clustering Gempa Indonesia")

# Upload file
uploaded_file = st.file_uploader("Upload file gempa (.csv atau .tsv)", type=["csv", "tsv"])

if uploaded_file is not None:
    # Baca file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file, sep="\t")

    st.subheader("📄 Data Awal")
    st.write(df.head())

    # Jalankan clustering
    df_clustered, best_k, best_score, sil_scores, k_range = run_clustering(df)
    colors = get_cluster_colors(df_clustered)

    # Plot silhouette score
    st.subheader("📈 Silhouette Score")
    fig_sil = plot_silhouette(sil_scores, k_range)
    st.pyplot(fig_sil)

    st.success(f"Jumlah cluster terbaik: k = {best_k} (score = {best_score:.4f})")

    # Scatter plot clustering
    st.subheader("📊 Scatter Plot Clustering")
    fig_scatter = plot_scatter(df_clustered, colors)
    st.pyplot(fig_scatter)

    # Peta statis Indonesia
    st.subheader("🗺️ Peta Indonesia (Statis)")
    fig_map = plot_map_static(df_clustered, colors)
    st.pyplot(fig_map)

    # Peta interaktif Folium
    st.subheader("🌍 Peta Interaktif")
    plot_map_interactive(df_clustered, colors)

    # Pastikan folder output ada
    os.makedirs("output", exist_ok=True)

    # Simpan hasil clustering
    df_clustered.to_csv("output/hasil_cluster.csv", index=False)

    # Simpan gambar plot
    fig_sil.savefig("output/silhouette_plot.png", dpi=300, bbox_inches="tight")
    fig_scatter.savefig("output/hasil_scatter.png", dpi=300, bbox_inches="tight")
    fig_map.savefig("output/peta_statis.png", dpi=300, bbox_inches="tight")

    st.info("✅ Hasil disimpan otomatis di folder `output/` (jika dijalankan di lokal).")

    # Tombol download hasil clustering
    st.subheader("⬇️ Download Hasil")
    csv = df_clustered.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV Hasil Clustering", csv, "hasil_cluster.csv", "text/csv")

else:
    st.info("Silakan upload file gempa (.csv atau .tsv) untuk memulai analisis.")