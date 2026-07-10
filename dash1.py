import os
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime

# =====================================
# KONFIGURASI HALAMAN
# =====================================

st.set_page_config(
    page_title="Dashboard Aktivitas Harian",
    page_icon="📊",
    layout="wide"
)

FILE_NAME = "data.xlsx"

# =====================================
# MEMBUAT FILE EXCEL JIKA BELUM ADA
# =====================================

if not os.path.exists(FILE_NAME):

    aktivitas = pd.DataFrame(columns=[
        "Tanggal",
        "Kegiatan",
        "Kategori",
        "Durasi_Jam",
        "Catatan",
        "Mood"
    ])

    todo = pd.DataFrame(columns=[
        "Tanggal",
        "Tugas",
        "Prioritas",
        "Status"
    ])

    with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as writer:
        aktivitas.to_excel(
            writer,
            sheet_name="Aktivitas",
            index=False
        )

        todo.to_excel(
            writer,
            sheet_name="ToDo",
            index=False
        )

# =====================================
# LOAD DATA
# =====================================

try:
    df = pd.read_excel(
        FILE_NAME,
        sheet_name="Aktivitas"
    )
except:
    df = pd.DataFrame(columns=[
        "Tanggal",
        "Kegiatan",
        "Kategori",
        "Durasi_Jam",
        "Catatan",
        "Mood"
    ])

try:
    todo = pd.read_excel(
        FILE_NAME,
        sheet_name="ToDo"
    )
except:
    todo = pd.DataFrame(columns=[
        "Tanggal",
        "Tugas",
        "Prioritas",
        "Status"
    ])

# =====================================
# FUNGSI SIMPAN
# =====================================

def simpan_excel():

    with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as writer:

        df.to_excel(
            writer,
            sheet_name="Aktivitas",
            index=False
        )

        todo.to_excel(
            writer,
            sheet_name="ToDo",
            index=False
        )

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("📊 Dashboard")

menu = st.sidebar.radio(
    "Pilih Menu",
    [
        "Dashboard Aktivitas",
        "To Do List"
    ]
)

st.title("📊 Dashboard Aktivitas Harian")
