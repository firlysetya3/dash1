import os
from datetime import datetime

import pandas as pd
import streamlit as st

# =====================================
# KONFIGURASI
# =====================================
st.set_page_config(
    page_title="Productivity Dashboard",
    page_icon="📒",
    layout="wide"
)

FILE_NAME = "data.xlsx"

# =====================================
# MEMBUAT FILE EXCEL JIKA BELUM ADA
# =====================================
def create_excel():
    if not os.path.exists(FILE_NAME):
        notes = pd.DataFrame(columns=[
            "Tanggal",
            "Judul",
            "Catatan"
        ])

        todo = pd.DataFrame(columns=[
            "Task",
            "Priority",
            "Deadline",
            "Status"
        ])

        with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as writer:
            notes.to_excel(writer, sheet_name="Daily Notes", index=False)
            todo.to_excel(writer, sheet_name="To Do List", index=False)

create_excel()

# =====================================
# LOAD DATA
# =====================================
def load_notes():
    return pd.read_excel(FILE_NAME, sheet_name="Daily Notes")

def load_todo():
    return pd.read_excel(FILE_NAME, sheet_name="To Do List")

# =====================================
# SIMPAN DATA
# =====================================
def save_data(notes_df, todo_df):
    with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as writer:
        notes_df.to_excel(
            writer,
            sheet_name="Daily Notes",
            index=False
        )

        todo_df.to_excel(
            writer,
            sheet_name="To Do List",
            index=False
        )

notes_df = load_notes()
todo_df = load_todo()

# =====================================
# SIDEBAR
# =====================================
st.sidebar.title("📒 Productivity Dashboard")

menu = st.sidebar.radio(
    "Menu",
    [
        "📝 Daily Notes",
        "✅ To Do List"
    ]
)

# =====================================
# DAILY NOTES
# =====================================
if menu == "📝 Daily Notes":

    st.title("📝 Daily Notes")

    with st.form("notes_form"):

        tanggal = st.date_input(
            "Tanggal",
            datetime.today()
        )

        judul = st.text_input(
            "Judul"
        )

        catatan = st.text_area(
            "Catatan",
            height=200
        )

        simpan = st.form_submit_button(
            "💾 Simpan Catatan"
        )

    if simpan:

        data_baru = pd.DataFrame({
            "Tanggal": [tanggal],
            "Judul": [judul],
            "Catatan": [catatan]
        })

        notes_df = pd.concat(
            [notes_df, data_baru],
            ignore_index=True
        )

        save_data(notes_df, todo_df)

        st.success("Catatan berhasil disimpan.")

        st.rerun()

    st.divider()

    st.subheader("Riwayat Daily Notes")

    if len(notes_df) == 0:
        st.info("Belum ada catatan.")
    else:

        edited_notes = st.data_editor(
            notes_df,
            use_container_width=True,
            num_rows="dynamic"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button("💾 Update Catatan"):

                save_data(
                    edited_notes,
                    todo_df
                )

                st.success("Berhasil diupdate.")
                st.rerun()

        with col2:

            if st.button("🗑 Hapus Semua Catatan"):

                notes_df = pd.DataFrame(
                    columns=[
                        "Tanggal",
                        "Judul",
                        "Catatan"
                    ]
                )

                save_data(
                    notes_df,
                    todo_df
                )

                st.success("Semua catatan dihapus.")
                st.rerun()

# =====================================
# TODO LIST
# =====================================
if menu == "✅ To Do List":

    st.title("✅ To Do List")

    with st.form("todo_form"):

        task = st.text_input("Task")

        priority = st.selectbox(
            "Priority",
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        deadline = st.date_input(
            "Deadline",
            datetime.today()
        )

        status = st.selectbox(
            "Status",
            [
                "Not Started",
                "On Progress",
                "Done"
            ]
        )

        tambah = st.form_submit_button(
            "➕ Tambah Task"
        )

    if tambah:

        data_baru = pd.DataFrame({

            "Task":[task],
            "Priority":[priority],
            "Deadline":[deadline],
            "Status":[status]

        })

        todo_df = pd.concat(
            [todo_df, data_baru],
            ignore_index=True
        )

        save_data(
            notes_df,
            todo_df
        )

        st.success("Task berhasil ditambahkan.")

        st.rerun()

    st.divider()

    st.subheader("Daftar Task")

    if len(todo_df) == 0:

        st.info("Belum ada task.")

    else:

        edited_todo = st.data_editor(
            todo_df,
            use_container_width=True,
            num_rows="dynamic"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button("💾 Update Task"):

                save_data(
                    notes_df,
                    edited_todo
                )

                st.success("Task berhasil diupdate.")
                st.rerun()

        with col2:

            if st.button("🗑 Hapus Semua Task"):

                todo_df = pd.DataFrame(
                    columns=[
                        "Task",
                        "Priority",
                        "Deadline",
                        "Status"
                    ]
                )

                save_data(
                    notes_df,
                    todo_df
                )

                st.success("Semua task dihapus.")
                st.rerun()
