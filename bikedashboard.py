import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st

sns.set(style='white')

#memuat dataset yang sudah dibersihkan
df = pd.read_csv('hour_cleaned.csv')
# fungsi untuk return df new

#fungsi untuk df baru visualisasi soal pertama
def func_cuaca_gp(df): 
     f_cuaca_gp = df.groupby(['Season', 'Weather'])['Total_rental'].sum().reset_index()
     return f_cuaca_gp

#fungsi untuk df baru visualisasi soal kedua bagian registered user
def func_work_registered(df): 
     f_work_registered = df.groupby('Workingday')['Registered_user'].sum().reset_index()
     return f_work_registered

#fungsi untuk df baru visualisasi soal kedua bagian Casual user
def func_work_casual(df): 
     f_work_casual = df.groupby('Workingday')[['Casual_user']].sum().reset_index()
     return f_work_casual

#fungsi untuk df baru visualisasi soal ketiga bagian Casual user
def func_hour_casual(df):
     f_hour_casual = df.groupby('Hour')['Casual_user'].sum().reset_index()
     return f_hour_casual

#fungsi untuk df baru visualisasi soal ketiga bagian Registered user
def func_hour_registered(df):
     f_hour_registered = df.groupby('Hour')['Registered_user'].sum().reset_index()
     return f_hour_registered

df['Date'] = pd.to_datetime(df['Date'])

# Menyiapkan dataframe
cuaca_gp = func_cuaca_gp(df)
work_casual = func_work_casual(df)
work_registered = func_work_registered(df)
hour_casual = func_hour_casual(df)
hour_registered = func_hour_registered(df)

with st.sidebar:

    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/images/image1_hH9B4gs.width-1000.format-webp.webp")
    

    

    #Input Filter cuaca (Visualisasi Pertanyaan 1)
    select_cuaca = st.multiselect("Filter Cuaca", cuaca_gp['Weather'].unique(), default= cuaca_gp['Weather'].unique())

    #Input Filter Hari kerja (Visualisasi Pertanyaan 2)
    select_work = st.multiselect("Filter Hari kerja", work_registered['Workingday'].unique(), default= work_registered['Workingday'].unique())
    #Input Filter jam (Visualisasi Pertanyaan 3)
    select_hour = st.slider("Pilih Jam:", 23, 23, (0, 23))



st.header(':man-biking: Bike Sharing Systems Analysis :woman-biking:')
st.subheader(':bike: Current Customer :bike:')

col1, col2, col3 = st.columns(3)
#Card Total Registered User
with col1:
    registered_user_sum = df['Registered_user'].sum()
    st.metric('Total Registered User ', registered_user_sum)

#Card Total Casual User
with col2:
    Casual_user_sum = df['Casual_user'].sum()
    st.metric('Total Casual User ', Casual_user_sum)
#Card Total User
with col3:
    Total_rental_sum = df['Total_rental'].sum()
    st.metric('Total User ', Total_rental_sum)

with st.container():

    st.subheader('Pengaruh Cuaca Pada Setiap Musim Terhadap Demand Penyewaan Sepeda')

# Visualisasi Pertanyaan 1: bagaimana cuaca pada setiap musim mempengaruhi  demand penyewaan sepeda ?  
# Barchart Pengaruh Cuaca Pada Setiap Musim Terhadap Demand Penyewaan Sepeda
    
#filter value untuk feature Weather
filtered_cuaca_gp = cuaca_gp[cuaca_gp['Weather'].isin(select_cuaca)]


warna = ["#F6995C", "#51829B", "#EADFB4", "#9BB0C1"]
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=filtered_cuaca_gp,
            x="Season",
            y="Total_rental",
            hue="Weather",
            palette=warna,
            ax=ax)
plt.xlabel(None)
plt.ylabel(None)
st.pyplot(fig)

with st.container():
# Visualisasi Pertanyaan 2: Apakah Terdapat pola dalam pemilihan hari rental bedasarkan weekend/weekdays ?  
# Pie Chart Preferensi Hari Peminjaman Sepeda bedasarkan hari kerja/non kerja.

    #filter value untuk feature registered_user
    filter_work_registered = work_registered[work_registered['Workingday'].isin(select_work)]
    #filter value untuk feature casual_user
    filter_work_casual = work_casual[work_casual['Workingday'].isin(select_work)]


st.subheader('Preferensi Hari Peminjaman Sepeda')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
ax[0].pie(filter_work_registered['Registered_user'], labels=filter_work_registered['Workingday'], autopct='%1.1f%%', colors=['#9BB0C1', '#F6995C'])
ax[0].set_title('Registered User', fontsize=15)
ax[1].pie(filter_work_casual['Casual_user'], labels=filter_work_casual['Workingday'], autopct='%1.1f%%', colors=['#F6995C', '#9BB0C1'])
ax[1].set_title('Casual User', fontsize=15)
st.pyplot(fig)


# Visualisasi Pertanyaan 3: bagaimana cuaca pada setiap musim mempengaruhi  demand penyewaan sepeda ?  
# Line Chart Visualisasi Trend Penyewaan Sepeda Per Jam
with st.container():
    st.subheader('Visualisasi Trend Penyewaan Sepeda Per Jam')
        #filter value untuk feature hour
    hour_registered_select = hour_registered[hour_registered['Hour'].between(select_hour[0], select_hour[1])]
    hour_casual_select = hour_casual[hour_casual['Hour'].between(select_hour[0], select_hour[1])]

    fig, ax = plt.subplots(figsize=(14, 6))
    sns.lineplot(data=hour_registered_select, x="Hour", y="Registered_user", color='#7F27FF', label='Registered User', ax=ax)
    sns.lineplot(data=hour_casual_select, x="Hour", y="Casual_user", color='#FF8911', label='Casual User', ax=ax)
    plt.title("Visualisasi Trend Penyewaan Sepeda Per Jam")
    plt.xlabel("Hour")
    plt.ylabel("Total Rental")
    plt.legend(loc='upper left') 
    plt.xticks(range(24))  
    st.pyplot(fig)





    st.caption('Copyright (c) Aditya Fathan 2023')