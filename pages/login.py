import streamlit as st
from db import get_connection  # import koneksi ke database

st.set_page_config(page_title="Login", page_icon="🔐")

st.title("🔐 Halaman Login")

# Form Login
nama_user = st.text_input("nama_user")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if nama_user and password:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE nama_user = %s AND password = %s"
        cursor.execute(query, (nama_user, password))
        result = cursor.fetchone()

        if result:
            st.success("Login berhasil! 👏")
            # Simpan status login di session state
            st.session_state.logged_in = True
            st.session_state.nama_user = nama_user
            st.switch_page("ui.py")  # Redirect ke halaman utama
        else:
            st.error("nama_user atau password salah.")

        cursor.close()
        conn.close()
    else:
        st.warning("Harap isi nama_user dan password.")
