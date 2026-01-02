import streamlit as st
import pandas as pd

from clustering import run_clustering, get_cluster_colors
from visualization import plot_silhouette, plot_scatter, plot_map_static
from mapping import plot_map_interactive


st.set_page_config(
    page_title="Clustering Gempa Indonesia",
    layout="wide"
)

st.title("🔎 Analisis Clustering Gempa di Indonesia")


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

        # Jalankan Clustering
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
        st.info("📤 Silakan upload ulang file dataset yang benar.")
        st.stop()

    # Hasil
    st.subheader("📌 Hasil Penentuan Jumlah Klaster Optimal")
    st.write(f"**K terbaik: {best_k}**")
    st.write(f"**Silhouette Score: {best_score:.4f}**")

    st.markdown(
        f"""
        Penentuan jumlah klaster dilakukan menggunakan metode *Silhouette*.
        Jumlah klaster optimal diperoleh pada **K = {best_k}**
        dengan nilai *Silhouette Score* sebesar **{best_score:.4f}**,
        yang menunjukkan kualitas pemisahan klaster yang cukup baik.
        """
    )


    fig_sil = plot_silhouette(sil_scores, k_range)
    st.pyplot(fig_sil)

    st.markdown(
        """
        Grafik ini menunjukkan perbandingan nilai *Silhouette Score*
        untuk setiap variasi jumlah klaster (K),
        di mana nilai tertinggi dipilih sebagai jumlah klaster optimal.
        """
    )


    st.subheader("📌 Scatter Plot Clustering")
    fig_scatter = plot_scatter(df_clustered, colors)
    st.pyplot(fig_scatter)

    st.markdown(
        """
        Scatter plot menampilkan pengelompokan kejadian gempa
        berdasarkan kedalaman dan magnitudo,
        sehingga pola distribusi data pada setiap klaster dapat diamati.
        """
    )


    st.subheader("📌 Visualisasi Klaster di Peta Statis")
    fig_static = plot_map_static(df_clustered, colors)
    st.pyplot(fig_static)

    st.markdown(
        """
        Peta statis menunjukkan persebaran spasial kejadian gempa
        di wilayah Indonesia berdasarkan hasil clustering.
        """
    )


    st.subheader("📌 Peta Interaktif (Folium)")
    plot_map_interactive(df_clustered, colors)

    st.markdown(
        """
        Peta interaktif menyajikan hasil clustering kejadian gempa
        dalam bentuk visualisasi spasial.
        Setiap titik mewakili satu kejadian gempa yang dikelompokkan
        berdasarkan karakteristik kedalaman dan magnitudo,
        sehingga membantu analisis pola seismik antar wilayah.
        """
    )

else:
    st.info("Silakan upload file dataset untuk memulai analisis.")