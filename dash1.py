import os
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Dashboard Aktivitas Harian",
    page_icon="📊",
    layout="wide"
)

FILE_NAME = "data.xlsx"

# Load Data
if os.path.exists(FILE_NAME):
    df = pd.read_excel(FILE_NAME)
else:
    df = pd.DataFrame(columns=[
        "Tanggal",
        "Kegiatan",
        "Kategori",
        "Durasi_Jam",
        "Catatan",
        "Mood"
    ])

st.title("📊 Dashboard Aktivitas Harian")

# =======================
# FORM INPUT
# =======================

with st.form("form_input"):

    col1, col2 = st.columns(2)

    with col1:
        tanggal = st.date_input("Tanggal", datetime.today())
        kegiatan = st.text_input("Kegiatan")
        kategori = st.selectbox(
            "Kategori",
            ["Kerja", "Rapat", "Belajar", "Admin", "Pribadi"]
        )

    with col2:
        durasi = st.number_input(
            "Durasi (Jam)",
            min_value=0.0,
            value=1.0
        )

        mood = st.selectbox(
            "Mood",
            [
                "😀 Senang",
                "😐 Biasa",
                "😫 Capek",
                "🔥 Produktif"
            ]
        )

    catatan = st.text_area("Catatan")

    simpan = st.form_submit_button("💾 Simpan")

if simpan:

    baru = pd.DataFrame([{
        "Tanggal": tanggal,
        "Kegiatan": kegiatan,
        "Kategori": kategori,
        "Durasi_Jam": durasi,
        "Catatan": catatan,
        "Mood": mood
    }])

    df = pd.concat([df, baru], ignore_index=True)
    df.to_excel(FILE_NAME, index=False)

    st.success("Data berhasil disimpan.")

# =======================
# DASHBOARD
# =======================

if len(df) > 0:

    df["Tanggal"] = pd.to_datetime(df["Tanggal"])

    total_jam = df["Durasi_Jam"].sum()
    total_kegiatan = len(df)
    rata = round(df["Durasi_Jam"].mean(), 2)

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Jam", total_jam)
    c2.metric("Total Kegiatan", total_kegiatan)
    c3.metric("Rata-rata Durasi", rata)

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.pie(
            df,
            names="Kategori",
            values="Durasi_Jam",
            title="Waktu Berdasarkan Kategori"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        harian = df.groupby("Tanggal")["Durasi_Jam"].sum().reset_index()

        fig2 = px.line(
            harian,
            x="Tanggal",
            y="Durasi_Jam",
            markers=True,
            title="Produktivitas Harian"
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("10 Aktivitas Terakhir")

    st.dataframe(
        df.sort_values("Tanggal", ascending=False).head(10),
        use_container_width=True
    )

else:
    st.info("Belum ada data.")

# =======================
# DOWNLOAD
# =======================

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "rb") as f:
        st.download_button(
            "⬇ Download Excel",
            f,
            file_name="data.xlsx"
        )
