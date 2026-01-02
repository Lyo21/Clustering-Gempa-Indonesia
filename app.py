import streamlit as st
import pandas as pd

from clustering import (
    run_clustering,
    get_cluster_colors,
    run_elbow          # ⬅️ fungsi elbow
)
from visualization import (
    plot_elbow,
    plot_silhouette,
    plot_scatter,
    plot_map_static,
    plot_cluster_distribution
)
from mapping import plot_map_interactive


# Konfigurasi Halaman
st.set_page_config(
    page_title="Clustering Gempa Indonesia",
    layout="wide"
)

st.title("🔎 Analisis Clustering Gempa di Indonesia")


# Upload Dataset
uploaded_file = st.file_uploader(
    "Upload dataset gempa (TSV / CSV)",
    type=["csv", "tsv"]
)

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".tsv"):
            df = pd.read_csv(uploaded_file, sep="\t")
        else:
            df = pd.read_csv(uploaded_file)

        st.success("✅ Dataset berhasil dimuat!")

        # ELBOW METHOD
        inertias, k_elbow = run_elbow(df)

        st.subheader("📌 Penentuan Jumlah Klaster (Metode Elbow)")
        fig_elbow = plot_elbow(inertias, k_elbow)
        st.pyplot(fig_elbow)

        st.markdown(
            """
            Metode *Elbow* digunakan untuk mengamati perubahan nilai inertia (SSE)
            terhadap jumlah klaster.
            Titik siku (elbow) menunjukkan jumlah klaster yang mulai memberikan
            peningkatan performa yang tidak signifikan.
            """
        )

        # SILHOUETTE & CLUSTERING
        df_clustered, best_k, best_score, sil_scores, k_range = run_clustering(df)
        colors = get_cluster_colors(df_clustered)

    except ValueError as e:
        st.error("❌ Dataset tidak sesuai format!")
        st.warning(
            f"""
            **Detail kesalahan:**
            {e}

            **Dataset wajib memiliki kolom:**
            - latitude
            - longitude
            - depth
            - magnitude
            """
        )
        st.stop()

    # Hasil Silhouette
    st.subheader("📌 Penentuan Jumlah Klaster Optimal (Silhouette)")
    st.write(f"**K terbaik: {best_k}**")
    st.write(f"**Silhouette Score: {best_score:.4f}**")

    st.markdown(
        f"""
        Berdasarkan evaluasi menggunakan metode *Silhouette*,
        jumlah klaster optimal diperoleh pada **K = {best_k}**
        dengan nilai *Silhouette Score* sebesar **{best_score:.4f}**,
        yang menunjukkan kualitas pemisahan klaster yang cukup baik.
        """
    )

    fig_sil = plot_silhouette(sil_scores, k_range)
    st.pyplot(fig_sil)

    # Distribusi Jumlah Data per Klaster
    st.subheader("📌 Distribusi Jumlah Data per Klaster")

    cluster_counts = df_clustered["cluster"].value_counts().sort_index()
    fig_bar = plot_cluster_distribution(cluster_counts)
    st.pyplot(fig_bar)

    st.markdown(
        """
        Diagram batang menunjukkan jumlah kejadian gempa
        pada setiap klaster hasil clustering,
        sehingga distribusi data antar klaster dapat dianalisis.
        """
    )

    # Scatter Plot
    st.subheader("📌 Scatter Plot Clustering")
    fig_scatter = plot_scatter(df_clustered, colors)
    st.pyplot(fig_scatter)

    # Peta Statis
    st.subheader("📌 Visualisasi Klaster di Peta Statis")
    fig_static = plot_map_static(df_clustered, colors)
    st.pyplot(fig_static)

    # Peta Interaktif
    st.subheader("📌 Peta Interaktif (Folium)")
    plot_map_interactive(df_clustered, colors)

else:
    st.info("📤 Silakan upload file dataset untuk memulai analisis.")