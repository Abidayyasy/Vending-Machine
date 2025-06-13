import streamlit as st

st.set_page_config(page_title="Admin Vending Machine", layout="centered")

# Simulasi login
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = True  # Simulasi login tetap aktif

# Inisialisasi koin dan stok
if "coins" not in st.session_state:
    st.session_state.coins = [30, 3000, 4000]
    st.session_state.stock = [20, 10, 11]

st.title("Admin Vending Machine")

st.markdown("### Tambah Saldo Koin")

with st.form("coin_form"):
    new_values = []
    for i, coin in enumerate(st.session_state.coins):
        current_stock = st.session_state.stock[i]
        added = st.number_input(
            f"Koin {coin} (stok saat ini: {current_stock})",
            min_value=0,
            step=1,
            key=f"add_{i}"
        )
        new_values.append(added)

    submitted = st.form_submit_button("Simpan Perubahan")
    if submitted:
        for i, add_value in enumerate(new_values):
            st.session_state.stock[i] += add_value
        st.success("Saldo koin berhasil diperbarui!")

# Tombol logout (reset)
if st.button("Logout"):
    st.session_state.clear()
    st.experimental_rerun()
