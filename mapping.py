import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import os


def plot_map_interactive(df, colors=None):
    """
    Membuat peta interaktif Folium berdasarkan hasil clustering gempa.
    Ditampilkan langsung di Streamlit menggunakan streamlit-folium.
    """

    # Titik tengah Indonesia
    m = folium.Map(location=[-2, 120], zoom_start=5, tiles="CartoDB positron")

    # Cluster marker biar gak numpuk
    marker_cluster = MarkerCluster().add_to(m)

    # Kalau warna belum dikirim dari app.py, buat otomatis
    if colors is None:
        cluster_ids = sorted(df["cluster"].unique())
        num_clusters = len(cluster_ids)
        cmap = cm.get_cmap("tab10", num_clusters)
        colors = {
            cluster_id: mcolors.to_hex(cmap(i))
            for i, cluster_id in enumerate(cluster_ids)
        }

    # Tambahkan marker untuk setiap gempa
    for _, row in df.iterrows():
        color = colors.get(row["cluster"], "#000000")  # warna fallback hitam
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=4,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=(
                f"<b>Tanggal:</b> {row.get('datetime', '-')}"
                f"<br><b>Magnitudo:</b> {row['magnitude']}"
                f"<br><b>Kedalaman:</b> {row['depth']} km"
                f"<br><b>Cluster:</b> {row['cluster']}"
            ),
        ).add_to(marker_cluster)

    # Buat legenda otomatis dari warna cluster
    legend_items = ""
    for cluster_id, color in colors.items():
        legend_items += f"""
            <i style="background:{color};
                      width:15px;height:15px;
                      display:inline-block;
                      margin-right:5px;
                      border:1px solid #000;"></i>
            Cluster {cluster_id}<br>
        """

    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 50px; left: 50px;
        width: 180px;
        background-color: white;
        border: 2px solid grey;
        z-index: 9999;
        font-size: 14px;
        padding: 10px;">
        <b>Legenda Klaster Gempa</b><br>
        {legend_items}
    </div>
    """

    # Tambahkan legenda ke peta
    m.get_root().html.add_child(folium.Element(legend_html))

    # Tampilkan di Streamlit
    st_folium(m, width=700, height=500)

    # Simpan ke file (kalau di lokal)
    if os.path.exists("output"):
        m.save("output/peta_interaktif.html")