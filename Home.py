import streamlit as st
from backend import solve_bounded, get_combination_bounded
from db import get_connection  # import koneksi DB

# ---------------- CACHE DATA ----------------
@st.cache_data(ttl=60)
def get_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nama_produk, harga_produk, path_img FROM produk")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    # Return sebagai dict dengan info lengkap
    return {nama: {"harga": harga, "img": img} for nama, harga, img in data}

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
    price = products[item]["harga"] * qty
    total_price += price
    st.sidebar.write(f"{item} x{qty} = {price} ¥")

st.sidebar.write("---")
st.sidebar.write(f"**Total: {total_price} ¥**")

user_amount = st.sidebar.number_input("💰 Masukkan jumlah ¥:", min_value=0, step=100)

# ---------------- BELI SEKARANG ----------------
if st.sidebar.button("🚗 Beli Sekarang"):
    if total_price == 0:
        st.sidebar.warning("Keranjang kosong!")
    elif user_amount < total_price:
        st.sidebar.error("Uang tidak cukup untuk membeli semua produk.")
    else:
        change = user_amount - total_price
        st.sidebar.success("✅ Pembelian berhasil!")
        st.sidebar.info(f"💸 Kembalian: {change} ¥")

        if change > 0:
            memo = {}
            computed = {}
            last_used = {}
            # Ambil stok ¥ dari database
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT nominal_koin, jumlah_koin FROM koin WHERE jumlah_koin > 0")
            stock_data = cursor.fetchall()
            stock_dict = {nominal: jumlah for nominal, jumlah in stock_data}
            cursor.close()
            conn.close()

            stock = [stock_dict.get(nominal, 0) for nominal in coins]

            min_koin = solve_bounded(change, coins, stock, memo, last_used)
            kombinasi = get_combination_bounded(change, coins, stock, last_used)

            if min_koin == float('inf') or not kombinasi:
                st.sidebar.warning("⚠️ Uang tidak cukup untuk memberikan kembalian.")
            else:
                st.sidebar.success(f"🔢 Kembalian diberikan dengan {min_koin} lembar/koin:")
                for nominal, jumlah in zip(coins, kombinasi):
                    if jumlah > 0:
                        st.sidebar.write(f"{jumlah} x {nominal}¥  = {jumlah * nominal}¥")

                # ---------------- UPDATE JUMLAH KOIN DI DATABASE ----------------
                conn = get_connection()
                cursor = conn.cursor()
                for nominal, jumlah in zip(coins, kombinasi):
                    if jumlah > 0:
                        cursor.execute("UPDATE koin SET jumlah_koin = jumlah_koin - %s WHERE nominal_koin = %s", (jumlah, nominal))
                conn.commit()
                cursor.close()
                conn.close()

        # Reset keranjang
        st.session_state.cart = {}

# ---------------- FUNGSI TAMBAH ----------------
def tambah_ke_keranjang(nama_produk):
    if nama_produk in st.session_state.cart:
        st.session_state.cart[nama_produk] += 1
    else:
        st.session_state.cart[nama_produk] = 1

# ---------------- UI PRODUK ----------------
st.markdown("<h1 style='color: red;'>Vending Machine (自動販売機)</h1>", unsafe_allow_html=True)

cols = st.columns(5)

card_style = """
    <div style="
        border: 1px solid #ddd;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    ">
        <img src="{img}" style="width: 100%; border-radius: 8px; margin-bottom: 10px;">
        <h6 style="margin-bottom: 5px;">{name}</h6>
        <p style="margin: 0;"><strong>{price} ¥</strong></p>
    </div>
"""

for i, (product, detail) in enumerate(products.items()):
    col = cols[i % 5]
    with col:
        html = card_style.format(
            img=detail["img"],
            name=product,
            price=detail["harga"]
        )
        st.markdown(html, unsafe_allow_html=True)

        # Tombol ditampilkan terpisah tapi seolah bagian dari card
        st.button(
            "Tambah",
            key=f"add_{i}",
            on_click=tambah_ke_keranjang,
            args=(product,)
        )
