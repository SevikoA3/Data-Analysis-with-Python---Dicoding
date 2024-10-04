import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Mengambil data
main_data = pd.read_csv('main_data.csv')

# Mengonversi tahun, bulan, hari, dan jam ke datetime
main_data['datetime'] = pd.to_datetime(main_data[['year', 'month', 'day', 'hour']])

# Sidebar untuk memfilter berdasarkan rentang tanggal
st.sidebar.header("Filter by Date")

# Mendapatkan tanggal minimum dan maksimum dari data
min_date = main_data['datetime'].min()
max_date = main_data['datetime'].max()

# Input tanggal tanpa menggunakan session state
start_date = pd.to_datetime(st.sidebar.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date))
end_date = pd.to_datetime(st.sidebar.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date))

# Memfilter data berdasarkan rentang tanggal
filtered_data = main_data[(main_data['datetime'] >= start_date) & (main_data['datetime'] <= end_date)]

# Membuat input bin di sidebar
numOfBins = st.sidebar.number_input("Number of Bins", min_value=1, max_value=100, value=30)

# Membuat bin untuk datetime berdasarkan input di sidebar
filtered_data['datetime_bin'] = pd.cut(filtered_data['datetime'], bins=numOfBins)

# Mengubah 'datetime_bin' untuk menggunakan tanggal awal setiap bin dan format sebagai yyyy-mm-dd
filtered_data['datetime_bin'] = filtered_data['datetime_bin'].apply(lambda x: x.left.strftime('%Y-%m-%d'))

# Memilih hanya kolom numerik untuk agregasi
numeric_cols = filtered_data.select_dtypes(include='number').columns
binned_data = filtered_data.groupby('datetime_bin')[numeric_cols].mean().reset_index()

# Dashboard utama
st.text("Nama: Seviko Attalarik P.H")
st.text("Email: attalarik.handoko@gmail.com")
st.text("id: seviko")
st.title("Air Quality and Weather Dashboard")
st.header("Overview of Pollutant Concentrations and Weather Conditions")

# Gambaran umum polutan
with st.container():
    st.subheader("Pollutants Overview")
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    cols = st.columns(2)
    for i, pollutant in enumerate(pollutants):
        binned_data[pollutant] = pd.to_numeric(binned_data[pollutant], errors='coerce')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=binned_data, x='datetime_bin', y=pollutant)
        plt.xlabel('Date')
        plt.ylabel('Concentration')
        plt.title(f'{pollutant} Levels Over Time')
        plt.xticks(rotation=90)
        cols[i % 2].pyplot(fig)

# Gambaran umum cuaca
with st.container():
    st.subheader("Weather Overview")
    weather = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    cols = st.columns(2)
    for i, w in enumerate(weather):
        binned_data[w] = pd.to_numeric(binned_data[w], errors='coerce')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=binned_data, x='datetime_bin', y=w)
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title(f'{w} Over Time')
        plt.xticks(rotation=90)
        cols[i % 2].pyplot(fig)

# Perbandingan stasiun
with st.container():
    st.header("Station Comparison")
    station = st.selectbox("Select Station", filtered_data['station'].unique())
    station_data = filtered_data[filtered_data['station'] == station]

    # Plot data spesifik stasiun
    cols = st.columns(2)
    for i, pollutant in enumerate(pollutants):
        station_data[pollutant] = pd.to_numeric(station_data[pollutant], errors='coerce')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=station_data, x='datetime_bin', y=pollutant)
        plt.xlabel('Date')
        plt.ylabel('Concentration')
        plt.title(f'{pollutant} Levels for Station: {station}')
        plt.xticks(rotation=90)
        cols[i % 2].pyplot(fig)

# Plot scatter untuk polutan vs parameter cuaca
with st.container():
    st.header("Scatter Plot: Pollutants vs Weather Parameters")

    # Memilih polutan dan parameter cuaca untuk plot scatter
    cols = st.columns(2)
    selected_pollutant = cols[0].selectbox("Select Pollutant", pollutants)
    selected_weather = cols[1].selectbox("Select Weather Parameter", weather)

    # Membuat plot scatter
    scatter_data = filtered_data[filtered_data['station'] == station]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=scatter_data, x=selected_weather, y=selected_pollutant)
    plt.xlabel(selected_weather)
    plt.ylabel(selected_pollutant)
    plt.title(f'Scatter Plot of {selected_pollutant} vs {selected_weather} for Station: {station}')
    st.pyplot(fig)

# Menampilkan statistik deskriptif
with st.container():
    st.subheader("Descriptive Statistics")
    st.write(filtered_data.describe())