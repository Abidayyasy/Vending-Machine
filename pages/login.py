import streamlit as st

st.set_page_config(page_title="Login Admin", layout="centered")

st.title("🔐 Login Admin")

# Dummy kredensial (untuk demo, sebaiknya diganti dengan validasi DB)
USERNAME = "admin"
PASSWORD = "123456"

# Input login
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Tombol login
if st.button("Login"):
    if username == USERNAME and password == PASSWORD:
        st.session_state["is_admin"] = True
        st.success("✅ Login berhasil!")

        # Redirect ke halaman admin
        st.markdown("Klik halaman **Admin** di sidebar untuk mengakses panel.")
        # st.experimental_rerun()  # atau rerun jika ingin langsung reload
    else:
        st.error("❌ Username atau password salah.")
