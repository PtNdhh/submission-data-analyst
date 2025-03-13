import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Konversi kolom tanggal
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

# Filter berdasarkan rentang tanggal
st.sidebar.header("Filter Data")

start_date = st.sidebar.date_input("Pilih Tanggal Awal", day_df["dteday"].min().date())
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", day_df["dteday"].max().date())

# Validasi rentang tanggal
if start_date > end_date:
    st.sidebar.error("Tanggal awal harus sebelum tanggal akhir")

# Filter dataset berdasarkan tanggal
filtered_day_df = day_df[(day_df["dteday"].dt.date >= start_date) & (day_df["dteday"].dt.date <= end_date)]

# Buat visualisasi rata-rata peminjaman sepeda berdasarkan kondisi cuaca
def plot_avg_rentals_by_weather():
    avg_rentals = filtered_day_df.groupby('weathersit')['cnt'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    avg_rentals.plot(kind='bar', color=['blue', 'gray', 'orange', 'red'], ax=ax)
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Rata-rata Peminjaman Sepeda')
    ax.set_title('Rata-rata Peminjaman Sepeda Berdasarkan Kondisi Cuaca')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    st.pyplot(fig)

# Buat visualisasi tren peminjaman sepeda berdasarkan jam
def plot_trend_rentals_by_hour():
    filtered_hour_df = hour_df[(hour_df['dteday'] >= str(start_date)) & (hour_df['dteday'] <= str(end_date))]

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='hr', y='cnt', data=filtered_hour_df, estimator='mean', ci=None, marker='o', color='b', ax=ax)
    ax.set_xlabel('Jam dalam Sehari')
    ax.set_ylabel('Rata-rata Peminjaman Sepeda')
    ax.set_title('Tren Peminjaman Sepeda Berdasarkan Jam')
    ax.set_xticks(range(0, 24))
    ax.grid(True)
    st.pyplot(fig)

# Streamlit layout
st.title("🚲 Dashboard Bike Sharing")

st.subheader("Rata-rata Peminjaman Sepeda Berdasarkan Kondisi Cuaca")
plot_avg_rentals_by_weather()

st.subheader("Tren Peminjaman Sepeda Berdasarkan Jam")
plot_trend_rentals_by_hour()

st.caption("Bike Sharing Dashboard © 2025")