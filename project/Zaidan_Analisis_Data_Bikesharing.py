import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Proyek Analisis Data Bike Sharing Dataset")
st.subheader("by Zaidan Abhinoya Athayumna")
st.markdown("""
            Dashboard ini diciptakan dengan tujuan menampilkan hasil analisis pada Jupyter Notebook secara interaktif.\
            Saya melakukan analisis untuk menjawab dua pertanyaan :
            1. Pada musim apa orang-orang paling banyak menggunakan layanan Bike Sharing?
            2. Pada rentang jam berapa orang-orang banyak menggunakan layanan Bike Sharing?
            """)
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

season_names = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Autumn"}
split_by_season_daypeople = day_df.groupby('season')[['casual', 'registered']].mean()
split_by_season_daypeople = split_by_season_daypeople.rename(index=season_names)

split_by_season_daypeople_df = split_by_season_daypeople.reset_index()
mean_by_season_melted_day = split_by_season_daypeople_df.melt(id_vars='season', var_name='user_type', value_name='mean_value')

cnt_by_season_daypeople = day_df.groupby('season')['cnt'].mean()
cnt_by_season_daypeople = cnt_by_season_daypeople.rename(index=season_names)

split_by_season_hourpeople = hour_df.groupby('season')[['casual', 'registered']].mean()
split_by_season_hourpeople = split_by_season_hourpeople.rename(index=season_names)

split_by_season_hourpeople_df = split_by_season_hourpeople.reset_index()
mean_by_season_melted_hour = split_by_season_hourpeople_df.melt(id_vars='season', var_name='user_type', value_name='mean_value')

cnt_by_season_hourpeople = hour_df.groupby('season')['cnt'].mean()
cnt_by_season_hourpeople = cnt_by_season_hourpeople.rename(index=season_names)

st.subheader("Pertanyaan Pertama")

st.markdown("""
            Berikut adalah hasil analisa saya terhadap banyaknya orang yang menggunakan layanan
            Bike Sharing pada setiap musim.
            """)

tab1, tab2= st.tabs(["Counted Per Day", "Counted Per Hour"])

 
with tab1:
    st.header("Casual and Registered Users of Bike Sharing by Season")
    fig1, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=mean_by_season_melted_day, x='season', y='mean_value', hue='user_type')
    plt.title('')
    plt.xlabel('Season')
    plt.ylabel('Mean Value')
    plt.legend(title='User Type')

    st.pyplot(fig1)
    with st.expander("See explanation"):
        st.markdown(
            """
            Chart ini mempresentasikan nilai rata-rata dari user Bike Sharing setiap musim yang dibagi menjadi
            user casual (tidak berlangganan) dan registered (berlangganan).
            """
        )

    st.header("Bike Sharing Users Percentage by Season")
    fig2, ax = plt.subplots(figsize=(8,4))  # Create a figure and axes object
    cnt_by_season_daypeople.plot(kind='pie', autopct='%1.1f%%', startangle=180, ax=ax)  # Plot the pie chart on the axes
    plt.ylabel('')
    plt.title('')

    st.pyplot(fig2)
    with st.expander("See explanation"):
        st.markdown(
            """
            Chart ini mempresentasikan persentase dari total user Bike Sharing setiap musim.
            """
        )
 
with tab2:
    st.header("Casual and Registered Users of Bike Sharing by Season")
    fig3, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=mean_by_season_melted_hour, x='season', y='mean_value', hue='user_type')
    plt.title('')
    plt.xlabel('Season')
    plt.ylabel('Mean Value')
    plt.legend(title='User Type')

    st.pyplot(fig3)
    with st.expander("See explanation"):
        st.markdown(
            """
            Chart ini mirip dengan Clustered Bar Chart pada tab "Counted Per Day" perbedaannya adalah Chart ini dihitung per jam.
            """
        )

    st.header("Bike Sharing Users Percentage by Season")
    fig4, ax = plt.subplots(figsize=(8,4))  # Create a figure and axes object
    cnt_by_season_hourpeople.plot(kind='pie', autopct='%1.1f%%', startangle=180, ax=ax)  # Plot the pie chart on the axes
    plt.ylabel('')
    plt.title('')

    st.pyplot(fig4)

    with st.expander("See explanation"):
        st.markdown(
            """
            Chart ini mempresentasikan persentase dari total user Bike Sharing setiap musim yang dihitung per jam.
            """
        )

grup1 = list(range(0, 7))
grup2 = list(range(6, 13))
grup3 = list(range(12, 19))
grup4 = list(range(18, 24)) + [0]

def assign_group(hour):
    if hour in grup1:
        return 'Midnight to Morning'
    elif hour in grup2:
        return 'Morning to Noon'
    elif hour in grup3:
        return 'Noon to Evening'
    elif hour in grup4:
        return 'Evening to Midnight'
    
hour_df['group_hour'] = hour_df['hr'].apply(assign_group)

grouped_data = hour_df.groupby('group_hour')['cnt'].mean()
grouped_data_split = hour_df.groupby('group_hour')[['casual', 'registered']].mean()

group_order = ['Midnight to Morning', 'Morning to Noon', 'Noon to Evening', 'Evening to Midnight']
grouped_data_sorted = grouped_data.reindex(group_order)
grouped_data_sorted_split = grouped_data_split.reindex(group_order)

st.markdown("""
            -------------------
            """)

st.subheader("Pertanyaan Kedua")

st.markdown("""
            Berikut adalah hasil analisa saya terhadap banyaknya orang yang menggunakan layanan
            Bike Sharing pada rentang jam yang berbeda.

 
            Note:


            Untuk memahami Chart dibawah, perlu dipahami maksud dari setiap hour range:

            - Midnight to Morning : Jam 00:00 ~ 06:00
            - Morning to Noon : Jam 06:00 ~ 12:00
            - Noon to Evening : Jam 12:00 ~ 18:00
            - Evening to Midnight : Jam 18:00 ~ 00:00 
            
            """)


st.header("Bike Sharing Users Percentage by Hour Range")
fig5, ax = plt.subplots(figsize=(10,6))
grouped_data_sorted.plot(kind='pie', autopct='%1.1f%%', startangle=180, ax=ax)
plt.ylabel('')
plt.title('')
st.pyplot(fig5)

with st.expander("See explanation"):
    st.markdown(
        """
       Chart ini mempresentasikan persentase dari total user Bike Sharing setiap rentang jam (hour range).
        """
    )

st.header("Casual and Registered Users of Bike Sharing by Hour Range")

grouped_data_sorted_split.reset_index(inplace=True)
melted_data = grouped_data_sorted_split.melt(id_vars='group_hour', var_name='user_type', value_name='mean_value')

fig6, ax = plt.subplots(figsize=(10, 6))
sns.barplot(ax=ax, data=melted_data, x='group_hour', y='mean_value', hue='user_type')
plt.title('')
plt.xlabel('Hour Group')
plt.ylabel('Mean Value')
plt.xticks(rotation=0)
plt.legend(title='User Type')
plt.tight_layout()

st.pyplot(fig6)

with st.expander("See explanation"):
    st.markdown(
        """
        Chart ini mempresentasikan nilai rata-rata dari user Bike Sharing pada setiap rentang jam yang dibagi menjadi
        user casual (tidak berlangganan) dan registered (berlangganan).
        """
    )

st.markdown("""
            -------------------
            """)

st.subheader("Kesimpulan")

tab3, tab4= st.tabs(["Pertanyaan 1", "Pertanyaan 2"])

with tab3:
    st.markdown("""
                "Pada musim apa orang-orang paling banyak menggunakan layanan Bike Sharing?"

                Pertanyaan ini bisa dijawab dari Chart hasil analisa yang telah dibuat. Diketahui bahwa 
                musim yang memiliki persentase total count user terbesar adalah musim panas (Summer)
                dengan persentase 31%. Pernyataan ini juga didukung oleh Clustered Bar Chart yang menunjukkan
                Summer memiliki bar tertinggi pada kedua tipe user, casual dan registered.

                """)

with tab4:
    st.markdown("""
                "Pada rentang jam apa orang-orang banyak menggunakan layanan Bike Sharing?"

                Pertanyaan ini bisa dijawab dari Chart hasil analisis yang telah dibuat. Diketahui bahwa 
                rentang jam yang memiliki persentase total count user terbesar dan adalah rentang jam siang sampai sore
                (Noon to Evening) dengan persentase 41% pada Pie Chart. Pernyataan ini juga didukung oleh Clustered Bar Chart 
                yang menunjukkan Noon to Evening memiliki bar tertinggi pada kedua tipe user, casual dan registered.             
                """)
