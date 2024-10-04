import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
main_data = pd.read_csv('main_data.csv')

# Convert year, month, day, and hour to datetime
main_data['datetime'] = pd.to_datetime(main_data[['year', 'month', 'day', 'hour']])

# Sidebar for filtering by date range
st.sidebar.header("Filter by Date")

# Get the minimum and maximum dates from the data
min_date = main_data['datetime'].min()
max_date = main_data['datetime'].max()

# Date input with error handling
start_date = pd.to_datetime(st.sidebar.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date))
end_date = pd.to_datetime(st.sidebar.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date))

# Filter data by date range
filtered_data = main_data[(main_data['datetime'] >= start_date) & (main_data['datetime'] <= end_date)]

# Main dashboard
st.title("Air Quality and Weather Dashboard")
st.subheader("Overview of Pollutant Concentrations and Weather Conditions")

# Create bins for datetime
numOfBins = st.number_input("Number of Bins", min_value=1, max_value=100, value=30)
filtered_data['datetime_bin'] = pd.cut(filtered_data['datetime'], bins=numOfBins)

# Modify 'datetime_bin' to use the start date of each bin and format as yyyy-mm-dd
filtered_data['datetime_bin'] = filtered_data['datetime_bin'].apply(lambda x: x.left.strftime('%Y-%m-%d'))

# Select only numeric columns for aggregation
numeric_cols = filtered_data.select_dtypes(include='number').columns
binned_data = filtered_data.groupby('datetime_bin')[numeric_cols].mean().reset_index()

# Pollutant overview
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
    plt.xticks(rotation=90)  # Rotate the x-axis labels for better readability
    cols[i % 2].pyplot(fig)

# Weather overview
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
    plt.xticks(rotation=90)  # Rotate the x-axis labels for better readability
    cols[i % 2].pyplot(fig)

# Station comparison
st.subheader("Station Comparison")
station = st.selectbox("Select Station", filtered_data['station'].unique())
station_data = filtered_data[filtered_data['station'] == station]

# Plot station-specific data
cols = st.columns(2)
for i, pollutant in enumerate(pollutants):
    station_data[pollutant] = pd.to_numeric(station_data[pollutant], errors='coerce')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=station_data, x='datetime_bin', y=pollutant)
    plt.xlabel('Date')
    plt.ylabel('Concentration')
    plt.title(f'{pollutant} Levels for Station: {station}')
    plt.xticks(rotation=90)  # Rotate the x-axis labels for better readability
    cols[i % 2].pyplot(fig)

# Show descriptive statistics
st.subheader("Descriptive Statistics")
st.write(filtered_data.describe())
