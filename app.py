import streamlit as st
import pandas as pd

from clustering import run_clustering, get_cluster_colors
from visualization import plot_silhouette, plot_scatter, plot_map_static
from mapping import plot_map_interactive

st.set_page_config(page_title="Clustering Gempa Indonesia", layout="wide")

st.title("🔎 Analisis Clustering Gempa di Indonesia")

uploaded_file = st.file_uploader("Upload dataset gempa (TSV / CSV)", type=["csv", "tsv"])

if uploaded_file:
    # Load dataset
    if uploaded_file.name.endswith(".tsv"):
        df = pd.read_csv(uploaded_file, sep="\t")
    else:
        df = pd.read_csv(uploaded_file)

    st.success("Dataset berhasil dimuat!")

    # Jalankan clustering
    df_clustered, best_k, best_score, sil_scores, k_range = run_clustering(df)
    colors = get_cluster_colors(df_clustered)

    st.subheader("📌 Hasil Penentuan Jumlah Cluster Optimal")
    st.write(f"**K terbaik: {best_k}**")
    st.write(f"**Silhouette Score: {best_score:.4f}**")

    fig_sil = plot_silhouette(sil_scores, k_range)
    st.pyplot(fig_sil)

    st.subheader("📌 Scatter Plot Clustering")
    fig_scatter = plot_scatter(df_clustered, colors)
    st.pyplot(fig_scatter)

    st.subheader("📌 Visualisasi Klaster di Peta Statis")
    fig_static = plot_map_static(df_clustered, colors)
    st.pyplot(fig_static)

    st.subheader("📌 Peta Interaktif (Folium)")
    plot_map_interactive(df_clustered, colors)

else:
    st.info("Silakan upload file dataset untuk memulai analisis.")