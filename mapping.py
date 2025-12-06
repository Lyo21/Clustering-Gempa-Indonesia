import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import os


def plot_map_interactive(df, colors=None):
    """
    Membuat peta interaktif Folium berdasarkan hasil clustering gempa.
    Ditampilkan di Streamlit menggunakan st_folium dengan ukuran full width.
    """

    # Titik tengah Indonesia
    m = folium.Map(location=[-2, 120], zoom_start=5, tiles="CartoDB positron")

    # Menghindari marker menumpuk
    marker_cluster = MarkerCluster().add_to(m)

    # Jika warna tidak dikirim dari app.py, buat otomatis
    if colors is None:
        cluster_ids = sorted(df["cluster"].unique())
        cmap = cm.get_cmap("tab10", len(cluster_ids))
        colors = {
            cluster_id: mcolors.to_hex(cmap(i))
            for i, cluster_id in enumerate(cluster_ids)
        }

    # Tambahkan marker ke peta
    for _, row in df.iterrows():
        color = colors.get(row["cluster"], "#000000")  
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            popup=folium.Popup(
                f"""
                <b>Tanggal:</b> {row.get('datetime', '-')}<br>
                <b>Magnitudo:</b> {row['magnitude']}<br>
                <b>Kedalaman:</b> {row['depth']} km<br>
                <b>Cluster:</b> {row['cluster']}
                """,
                max_width=250
            ),
        ).add_to(marker_cluster)

    # LEGEND HTML
    legend_html = """
    <div style="
        position: fixed;
        bottom: 40px;
        left: 40px;
        background-color: white;
        padding: 10px 12px;
        border: 2px solid grey;
        z-index: 9999;
        font-size: 14px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    ">
        <b>Legenda Klaster</b><br>
    """

    for cluster_id, color in colors.items():
        legend_html += f"""
        <div style="margin-top:4px;">
            <i style="
                background:{color};
                width:14px;
                height:14px;
                display:inline-block;
                margin-right:6px;
                border:1px solid #000;">
            </i>
            Cluster {cluster_id}
        </div>
        """

    legend_html += "</div>"

    m.get_root().html.add_child(folium.Element(legend_html))

    st_folium(
        m,
        width=None,
        height=800,
        returned_objects=[]
    )

    # Simpan file jika folder output ada
    if os.path.isdir("output"):
        try:
            m.save("output/peta_interaktif.html")
        except Exception:
            pass