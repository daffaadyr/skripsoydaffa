import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
from streamlit_folium import folium_static

# Load the dataset
uploaded_file = '/workspaces/gdp-dashboard/data/DataSkripsiKecelakaanUnlabeledClustered.xlsx'
data = pd.read_excel(uploaded_file)

# Convert columns to appropriate data types if needed
data['Tahun'] = data['Tahun'].astype(str)

# Inisialisasi awal untuk filtered_datas
filtered_datas = pd.DataFrame()  # Default sebagai DataFrame kosong

# Sidebar for navigation
st.sidebar.header("Menu")
menu = st.sidebar.radio("Pilih Menu:", options=["Analisis Cluster", "Visualisasi Data"])

if menu == "Analisis Cluster":
    # Pie Chart for Cluster Distribution
    if 'Cluster' in data.columns:
        pie_fig = px.pie(data, values=data['Cluster'].value_counts().values,
                         names=data['Cluster'].value_counts().index,
                         title="Distribusi Cluster")
        st.plotly_chart(pie_fig)
    else:
        st.write("Data cluster tidak tersedia.")

    # Box Plot for Cluster Characteristics
    st.header("Box Plot - Karakteristik Antar Cluster")
    if 'Cluster' in data.columns:
        numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
        if not numeric_columns.empty:
            selected_metric = st.selectbox("Pilih Kolom untuk Boxplot:", 
                                           options=["Jumlah_Kecelakaan", "Jumlah_Meninggal", "Jumlah_Kendaraan_Rusak_Berat"])
            plt.figure(figsize=(10, 6))
            sns.boxplot(x='Cluster', y=selected_metric, data=data, palette='Set2')
            plt.title(f'Perbandingan {selected_metric} antar Cluster')
            st.pyplot(plt)
        else:
            st.write("Tidak ada data numerik untuk visualisasi boxplot.")
    else:
        st.write("Kolom 'Cluster' tidak tersedia dalam dataset.")

elif menu == "Visualisasi Data":
    # Sidebar for filtering
    st.sidebar.header("Filter Data")

    # Filter Tahun
    years = data['Tahun'].unique()
    selected_years = st.sidebar.multiselect("Pilih Tahun:", options=years, default=years)

    # Filter Ruas Tol
    if 'Ruas_Tol' in data.columns:
        tol_roads = data['Ruas_Tol'].unique()
        selected_tols = st.sidebar.multiselect("Pilih Ruas Tol:", options=tol_roads, default=tol_roads)
        # Apply filters
        filtered_datas = data[(data['Tahun'].isin(selected_years)) & (data['Ruas_Tol'].isin(selected_tols))]
    else:
        st.error("Kolom 'Ruas_Tol' tidak ditemukan dalam dataset.")
        filtered_datas = data[data['Tahun'].isin(selected_years)]

    # Display filtered table
    st.header("Tabel Data Hasil Filtrasi")
    st.dataframe(filtered_datas)

    # Dropdown for selecting visualization metric
    st.header("Visualisasi Data")
    selected_metric = st.selectbox(
        "Pilih Kategori untuk Visualisasi:", 
        options=["Jumlah_Kecelakaan", "Jumlah_Meninggal", "Jumlah_Kendaraan_Rusak_Berat"],
        index=0
    )

    # Line Plot
    st.subheader("Line Plot")
    if not filtered_datas.empty:
        filtered_datas['Tahun'] = filtered_datas['Tahun'].astype(str)
        line_fig = px.line(
            filtered_datas, 
            x='Tahun', 
            y=selected_metric, 
            color='Ruas_Tol', 
            markers=True,
            title=f"{selected_metric} per Tahun berdasarkan Ruas Tol", 
            hover_name='Ruas_Tol',
            labels={'y': selected_metric},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(line_fig)
    else:
        st.write("Data tidak tersedia untuk visualisasi plot garis.")

    # Bar Chart
    st.subheader("Bar Chart")
    if not filtered_datas.empty:
        bar_fig = px.bar(
            filtered_datas, 
            x='Ruas_Tol', 
            y=selected_metric, 
            color='Tahun',
            title=f"{selected_metric} berdasarkan Ruas Tol", 
            hover_name='Ruas_Tol',
            labels={'y': selected_metric},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(bar_fig)
    else:
        st.write("Data tidak tersedia untuk visualisasi bar chart.")
