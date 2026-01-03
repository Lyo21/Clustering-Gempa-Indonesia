import streamlit as st
import pandas as pd

from clustering import (
    run_clustering,
    get_cluster_colors,
    run_elbow
)
from visualization import (
    plot_elbow,
    plot_silhouette,
    plot_scatter,
    plot_map_static,
    plot_cluster_distribution
)
from mapping import plot_map_interactive


st.set_page_config(
    page_title="Clustering Gempa Indonesia",
    layout="wide"
)

st.title(
    "📊 Sistem Visualisasi dan Clustering Pola Gempa Bumi di Indonesia Menggunakan Metode K-Means"
)


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

        st.subheader("📄 Pratinjau Dataset")

        st.markdown(
            f"""
            Dataset yang digunakan dalam penelitian ini
            terdiri dari **{df.shape[0]} data kejadian gempa bumi**.
            Untuk memberikan gambaran awal terhadap karakteristik data,
            ditampilkan **10 baris pertama** dari dataset.
            """
        )

        st.dataframe(df.head(10), use_container_width=True)

        inertias, k_elbow = run_elbow(df)

        st.subheader("📌 Penentuan Jumlah Klaster (Metode Elbow)")
        fig_elbow = plot_elbow(inertias, k_elbow)
        st.pyplot(fig_elbow)

        st.markdown(
            """
            Metode *Elbow* digunakan untuk mengamati perubahan nilai inertia (SSE)
            terhadap jumlah klaster.
            Titik siku menunjukkan jumlah klaster yang memberikan
            peningkatan performa yang mulai melambat.
            """
        )

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

    st.subheader("📌 Penentuan Jumlah Klaster Optimal (Silhouette)")

    st.markdown(
        f"""
        Evaluasi menggunakan metode *Silhouette* menunjukkan bahwa
        jumlah klaster optimal diperoleh pada **K = {best_k}**
        dengan nilai *Silhouette Score* sebesar **{best_score:.4f}**.
        Nilai ini mengindikasikan kualitas pemisahan klaster yang baik.
        """
    )

    fig_sil = plot_silhouette(sil_scores, k_range)
    st.pyplot(fig_sil)

    st.subheader("📈 Distribusi Jumlah Data per Klaster")

    cluster_counts = df_clustered["cluster"].value_counts().sort_index()
    fig_bar = plot_cluster_distribution(cluster_counts, colors)
    st.pyplot(fig_bar)

    st.markdown(
        """
        Diagram batang memperlihatkan jumlah kejadian gempa
        pada masing-masing klaster hasil clustering,
        sehingga distribusi data antar klaster dapat dianalisis.
        """
    )

    st.subheader("🔎 Scatter Plot Hasil Clustering")

    fig_scatter = plot_scatter(df_clustered, colors)
    st.pyplot(fig_scatter)

    st.markdown(
        """
        Scatter plot menggambarkan pengelompokan kejadian gempa
        berdasarkan kedalaman dan magnitudo,
        sehingga pola sebaran data pada setiap klaster dapat diamati.
        """
    )

    st.subheader("🗺️ Visualisasi Klaster pada Peta Statis")

    fig_static = plot_map_static(df_clustered, colors)
    st.pyplot(fig_static)

    st.markdown(
        """
        Peta statis menyajikan persebaran spasial kejadian gempa
        di wilayah Indonesia berdasarkan hasil clustering.
        """
    )

    st.subheader("🗺️ Peta Interaktif Hasil Clustering")

    plot_map_interactive(df_clustered, colors)

    st.markdown(
        """
        Peta interaktif menampilkan hasil clustering kejadian gempa
        dalam bentuk visualisasi spasial.
        Setiap titik merepresentasikan satu kejadian gempa
        yang dikelompokkan berdasarkan karakteristik kedalaman
        dan magnitudo.
        """
    )

else:
    st.info("📤 Silakan upload file dataset untuk memulai analisis.")