import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Konfigurasi tampilan
st.set_page_config(
    page_title="Advanced Marketplace Dashboard",
    page_icon="📈",
    layout="wide"
)
import streamlit as st
from PIL import Image

# Header
st.markdown(
    """
    <style>
    .main-title {
        background-color: #4CAF50;
        color: white;
        padding: 20px;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        border-radius: 10px;
    }
    .subtitle {
        font-size: 20px;
        text-align: center;
        color: #6D6D6D;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">Advanced Marketplace Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">By Jessica Pasaribu - 11322017</div>', unsafe_allow_html=True)

# Add a horizontal line for style
st.markdown("---")

# Example visual content to follow
st.write("**Selamat datang di dashboard ini! Silakan eksplorasi data dan analisis yang tersedia.**")

# Rest of the content
st.write("### Analisis dan visualisasi mendalam untuk memantau performa marketplace Anda!")


# Load dataset
customers = pd.read_csv('dashboard/customers_dataset.csv')
sellers = pd.read_csv('dashboard/sellers_dataset.csv')
products = pd.read_csv('dashboard/products_dataset.csv')
orders = pd.read_csv('dashboard/orders_dataset.csv')
order_reviews = pd.read_csv('dashboard/order_reviews_dataset.csv')
order_items = pd.read_csv('dashboard/order_items_dataset.csv')

# Bagian pertama: Ringkasan Data
st.markdown("## 📋 Ringkasan Data")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Jumlah Pelanggan", f"{customers['customer_unique_id'].nunique()}")

with col2:
    st.metric("Jumlah Penjual", f"{sellers['seller_id'].nunique()}")

with col3:
    st.metric("Jumlah Produk", f"{products['product_id'].nunique()}")

with col4:
    st.metric("Jumlah Pesanan", f"{orders['order_id'].nunique()}")

st.markdown("---")

# Pilihan visualisasi interaktif
st.markdown("## 📊 Analisis Visualisasi Data")
chart_selection = st.selectbox(
    "Pilih Visualisasi yang Ingin Anda Lihat:",
    [
        "📍 Peta Distribusi Pelanggan",
        "⭐ Distribusi Skor Ulasan",
        "🚚 Analisis Ongkos Kirim",
        "📦 Performa Kategori Produk",
        "🕒 Tren Pesanan Berdasarkan Waktu",
        "💬 Analisis Sentimen Ulasan"
    ]
)

# Peta Distribusi Pelanggan
if chart_selection == "📍 Peta Distribusi Pelanggan":
    st.subheader("📍 Peta Distribusi Pelanggan Berdasarkan Kota")
    customer_city_count = customers['customer_city'].value_counts().reset_index()
    customer_city_count.columns = ['city', 'count']

    fig = px.scatter_geo(
        customer_city_count,
        locations="city",
        locationmode="country names",
        size="count",
        title="Distribusi Pelanggan Berdasarkan Kota",
        template="plotly",
        projection="natural earth"
    )
    st.plotly_chart(fig)

# Distribusi Skor Ulasan
elif chart_selection == "⭐ Distribusi Skor Ulasan":
    st.subheader("⭐ Distribusi Skor Ulasan Pesanan")
    review_scores = order_reviews['review_score'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=review_scores.index, y=review_scores.values, palette="coolwarm", ax=ax)
    ax.set_title("Distribusi Skor Ulasan Pesanan", fontsize=16)
    ax.set_xlabel("Skor Ulasan", fontsize=12)
    ax.set_ylabel("Jumlah", fontsize=12)
    st.pyplot(fig)

# Analisis Ongkos Kirim
elif chart_selection == "🚚 Analisis Ongkos Kirim":
    st.subheader("🚚 Analisis Ongkos Kirim per Produk")
    shipping_avg = order_items.groupby('product_id')['freight_value'].mean().reset_index()
    shipping_avg = shipping_avg.sort_values(by='freight_value', ascending=False).head(10)

    fig = px.bar(
        shipping_avg,
        x='product_id',
        y='freight_value',
        title="10 Produk dengan Ongkos Kirim Tertinggi",
        color='freight_value',
        template="plotly",
    )
    st.plotly_chart(fig)

# Performa Kategori Produk
elif chart_selection == "📦 Performa Kategori Produk":
    st.subheader("📦 Performa Kategori Produk")
    product_counts = products['product_category_name'].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=product_counts.index, y=product_counts.values, palette="viridis", ax=ax)
    ax.set_title("10 Kategori Produk Terbanyak", fontsize=16)
    ax.set_xlabel("Kategori Produk", fontsize=12)
    ax.set_ylabel("Jumlah", fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Tren Pesanan Berdasarkan Waktu
elif chart_selection == "🕒 Tren Pesanan Berdasarkan Waktu":
    st.subheader("🕒 Tren Pesanan Berdasarkan Waktu")
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    order_trend = orders.groupby(orders['order_purchase_timestamp'].dt.date).size()

    fig = px.line(
        order_trend,
        title="Tren Jumlah Pesanan Berdasarkan Waktu",
        labels={'value': 'Jumlah Pesanan', 'index': 'Tanggal'},
        template="plotly"
    )
    st.plotly_chart(fig)

# Analisis Sentimen Ulasan
elif chart_selection == "💬 Analisis Sentimen Ulasan":
    st.subheader("💬 Analisis Sentimen Ulasan")
    order_reviews['review_length'] = order_reviews['review_comment_message'].fillna('').str.len()
    avg_review_length = order_reviews.groupby('review_score')['review_length'].mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=avg_review_length.index, y=avg_review_length.values, palette="mako", ax=ax)
    ax.set_title("Rata-rata Panjang Ulasan Berdasarkan Skor", fontsize=16)
    ax.set_xlabel("Skor Ulasan", fontsize=12)
    ax.set_ylabel("Panjang Ulasan", fontsize=12)
    st.pyplot(fig)

# Footer
st.markdown("""
    <style>
    .footer {
        text-align: center;
        padding: 10px;
        margin-top: 50px;
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
    }
    </style>
    <div class="footer">
        🚀 Powered by Advanced Marketplace Data Analysis
    </div>
""", unsafe_allow_html=True)
