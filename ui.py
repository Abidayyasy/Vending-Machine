import streamlit as st
from backend import solve, get_coin_combination
from db import get_connection  # import koneksi DB

# ---------------- CACHE DATA ----------------
@st.cache_data(ttl=60)  # cache selama 60 detik
def get_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nama_produk, harga_produk FROM produk")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return {nama: harga for nama, harga in data}

@st.cache_data(ttl=60)
def get_coins():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nominal_koin FROM koin WHERE jumlah_koin > 0")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return sorted([row[0] for row in data], reverse=True)

# ---------------- INIT ----------------
st.set_page_config(page_title="Vending Machine", page_icon="🥤", layout="wide")

products = get_products()
coins = get_coins()

if 'cart' not in st.session_state:
    st.session_state.cart = {}


# ---------------- SIDEBAR ----------------
st.sidebar.header("🛒 Keranjang Belanja")

total_price = 0
for item, qty in st.session_state.cart.items():
    price = products[item] * qty
    total_price += price
    st.sidebar.write(f"{item} x{qty} = {price} koin")

st.sidebar.write("---")
st.sidebar.write(f"**Total: {total_price} koin**")

user_amount = st.sidebar.number_input("💰 Masukkan jumlah koin:", min_value=0, step=100)

# ---------------- BELI SEKARANG ----------------
if st.sidebar.button("🚗 Beli Sekarang"):
    if total_price == 0:
        st.sidebar.warning("Keranjang kosong!")
    elif user_amount < total_price:
        st.sidebar.error("Uang tidak cukup untuk membeli semua produk.")
    else:
        change = user_amount - total_price
        st.sidebar.success("✅ Pembelian berhasil!")
        st.sidebar.info(f"💸 Kembalian: {change} koin")

        if change > 0:
            memo = {}
            computed = {}
            last_used = {}

            min_koin = solve(change, coins, memo, computed, last_used)
            kombinasi = get_coin_combination(change, last_used)

            if min_koin == float('inf') or not kombinasi:
                st.sidebar.warning("⚠️ Koin tidak cukup untuk memberikan kembalian.")
            else:
                st.sidebar.success(f"🔢 Kembalian diberikan dengan {min_koin} koin:")
                st.sidebar.code(kombinasi)

        st.session_state.cart = {}  # Reset keranjang setelah beli

# ---------------- FUNGSI TAMBAH ----------------
def tambah_ke_keranjang(nama_produk):
    if nama_produk in st.session_state.cart:
        st.session_state.cart[nama_produk] += 1
    else:
        st.session_state.cart[nama_produk] = 1

# ---------------- UI PRODUK ----------------
st.markdown("<h1 style='color: red;'>🍼 Vending Machine Modern</h1>", unsafe_allow_html=True)

cols = st.columns(5)
for i, (product, price) in enumerate(products.items()):
    col = cols[i % 5]
    with col:
        st.subheader(product)
        st.write(f"Harga: {price} koin")
        st.button(
            f"Tambah",
            key=f"add_{i}",
            on_click=tambah_ke_keranjang,
            args=(product,)
        )
