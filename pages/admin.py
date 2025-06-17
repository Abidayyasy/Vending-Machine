import streamlit as st
from db import get_connection  # pastikan ini mengarah ke modul koneksi database kamu

# ---------------- PROTEKSI AKSES ----------------
st.set_page_config(page_title="Admin Vending Machine", layout="centered")
st.title("Admin Vending Machine")

if "is_admin" not in st.session_state or not st.session_state["is_admin"]:
    st.error("⛔ Anda tidak memiliki akses ke halaman ini.")
    st.stop()

# ---------------- LOAD DATA DARI DATABASE ----------------
@st.cache_data(ttl=60)
def get_coin_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nominal_koin, jumlah_koin FROM koin ORDER BY nominal_koin DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def update_coin_stock(nominal, tambahan):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE koin SET jumlah_koin = jumlah_koin + %s WHERE nominal_koin = %s", (tambahan, nominal))
    conn.commit()
    cursor.close()
    conn.close()

coin_data = get_coin_data()
coins = [row[0] for row in coin_data]
stock = [row[1] for row in coin_data]

# ---------------- FORM TAMBAH SALDO ----------------
st.markdown("### Tambah Saldo Koin")

with st.form("coin_form"):
    new_values = []
    for i, coin in enumerate(coins):
        current_stock = stock[i]
        added = st.number_input(
            f"Koin {coin} (stok saat ini: {current_stock})",
            min_value=0,
            step=1,
            key=f"add_{i}"
        )
        new_values.append((coin, added))

    submitted = st.form_submit_button("💾 Simpan Perubahan")
    if submitted:
        for nominal, tambahan in new_values:
            if tambahan > 0:
                update_coin_stock(nominal, tambahan)
        st.success("✅ Saldo koin berhasil diperbarui!")
        st.cache_data.clear()  # Clear cache agar data diperbarui
        st.rerun()

# ---------------- TOMBOL LOGOUT ----------------
if st.button("🚪 Logout"):
    st.session_state.clear()
    st.rerun()

