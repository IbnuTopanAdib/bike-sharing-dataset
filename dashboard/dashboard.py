import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

plt.style.use('tableau-colorblind10')

day_data = pd.read_csv(r"day.csv")
hour_data = pd.read_csv(r"hour.csv")


def create_users_per_month(day_data):
    users_per_month = day_data.groupby("mnth").agg({
        'casual': 'sum',
        'registered': 'sum'
    })
    return users_per_month


def create_mean_users_holiday(day_data):
    mean_user_holiday = day_data.groupby(by='holiday').agg({
        'instant': 'nunique',
        'registered': 'mean',
        'casual': 'mean',
        'cnt': 'mean'
    })
    return mean_user_holiday


def create_users_per_season(day_data):
    users_per_season = day_data.groupby(by="season").agg({
        'casual': 'sum',
        'registered': 'sum'
    })
    return users_per_season


def create_users_per_time(hour_data):
    users_per_time = hour_data.groupby(by="time_category").agg({
        'casual': 'mean',
        'registered': 'mean'
    })
    return users_per_time


def create_weathersit_user(hour_data):
    weathersit_user = hour_data.groupby(by='weathersit').agg({
        'casual': 'mean',
        'registered': 'mean'
    })
    return weathersit_user


def create_users_feeling_temperature(day_data):
    users_feeling_temperature = day_data.groupby(by='atemp_category').agg({
        'casual': 'mean',
        'registered': 'mean'
    })
    return users_feeling_temperature


hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
min_date = hour_data['dteday'].min()
max_date = hour_data['dteday'].max()


with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


main_hour_df = hour_data[(hour_data["dteday"] >= str(start_date)) &
                         (hour_data["dteday"] <= str(end_date))]

main_day_df = day_data[(day_data["dteday"] >= str(start_date)) &
                       (day_data["dteday"] <= str(end_date))]

users_per_month = create_users_per_month(main_day_df)
mean_users_holiday = create_mean_users_holiday(main_day_df)
mean_users_per_time = create_users_per_time(main_hour_df)
users_feeling_temperature = create_users_feeling_temperature(main_day_df)
weathersit_user = create_weathersit_user(main_hour_df)

st.header('Bike Sharing')

st.subheader('Perbandingan Peminjam Sepeda Per bulan')

col1, col2 = st.columns(2)
total_registered_user = main_day_df['registered'].sum()
total_casual_user = main_day_df['casual'].sum()

with col1:
    st.metric("Total Registered Users", value=total_registered_user)

with col2:
    st.metric("Total Casual Users", value=total_casual_user)

month = users_per_month.index
casual = users_per_month['casual']
registered = users_per_month['registered']

bar_width = 0.35
bar_pos = [i for i in range(len(month))]
fig, ax = plt.subplots(figsize=(16, 8))


ax.bar(bar_pos, casual, width=bar_width, label='Casual Users')
ax.bar([pos + bar_width for pos in bar_pos], registered,
       width=bar_width, label='Registered Users')


ax.set_xticks([pos + bar_width / 2 for pos in bar_pos])
ax.set_xticklabels(month)

ax.set_xlabel('Month')
ax.set_ylabel('Number of Users')
ax.legend()
ax.set_title('Casual and Registered Users per Month')
st.pyplot(fig)


st.subheader('Perbandingan User Pada Hari Libur dan Non Libur')

col1, col2 = st.columns(2)

with col1:
    hari_libur = mean_users_holiday.index
    jumlah_hari_libur = mean_users_holiday['instant']

    fig, ax = plt.subplots()
    ax.bar(hari_libur, jumlah_hari_libur)
    for i, v in enumerate(jumlah_hari_libur):
        ax.text(i, v, str(v), ha='center', va='bottom')

    ax.set_xticks(hari_libur)
    ax.set_xticklabels(['Non-Holiday', 'Holiday'])

    ax.set_xlabel('Kategori Hari Libur')
    ax.set_ylabel('Jumlah Hari Libur')
    ax.set_title('Jumlah Hari Libur vs Bukan Hari Libur')
    st.pyplot(fig)

with col2:
    casual = mean_users_holiday['casual']
    registered = mean_users_holiday['registered']
    hari_libur = mean_users_holiday.index

    fig, ax = plt.subplots()

    ax.bar(hari_libur, casual, label='Casual Users')
    ax.bar(hari_libur, registered, bottom=casual, label='Registered Users')

    # Set x-axis tick positions and labels
    ax.set_xticks(hari_libur)
    ax.set_xticklabels(['Non-Holiday', 'Holiday'])

    ax.set_xlabel('hari_libur')
    ax.set_ylabel('Number of Users')
    ax.legend()
    ax.set_title('Casual and Registered Holiday vs not Holiday')

    st.pyplot(fig)

st.subheader('Rata-rata peminjam sepeda pada waktu tertentu')

casual = mean_users_per_time['casual']
registered = mean_users_per_time['registered']
time_category = mean_users_per_time.index
fig, ax = plt.subplots()


ax.bar(time_category, casual, label='Casual Users')
ax.bar(time_category, registered, bottom=casual, label='Registered Users')

ax.set_xlabel('time_category')
ax.set_ylabel('Number of Users')
ax.legend()
ax.set_title('Casual and Registered Users per Time Category')
st.pyplot(fig)


st.subheader('Pengaruh Cuaca Terhadap Peminjam Sepeda')
col1, col2, col3 = st.columns(3)
temp_avg = main_hour_df['temp'].mean()
hum_avg = main_hour_df['hum'].mean()
windspeed_avg = main_hour_df['windspeed'].mean()

with col1:
    st.metric("Rata-rata Suhu Udara", value=(f"{temp_avg:0.2f}"))
with col2:
    st.metric("Rata-rata Kelembaban", value=(f"{hum_avg:0.2f}"))
with col3:
    st.metric("Rata-rata Kecepatan Angin", value=(f"{windspeed_avg:0.2f}"))

casual = users_feeling_temperature['casual']
registered = users_feeling_temperature['registered']
feeling_temperature = users_feeling_temperature.index

fig, ax = plt.subplots()


ax.bar(feeling_temperature, casual, label='Casual Users')
ax.bar(feeling_temperature, registered,
       bottom=casual, label='Registered Users')

ax.set_xlabel('feeling_temperature')
ax.set_ylabel('Number of Users')
ax.legend()
ax.set_title('Casual and Registered Users per Feeling Temperature')

st.pyplot(fig)
keterangan1 = {
    'Kategori': ['cold', 'cool', 'warm', 'hot', 'very hot'],
    'Rentang Suhu': ['-10°C - 15°C', '15°C - 25°C', '25°C - 30°C', '30°C - 38°C', '>38°C']
}

st.write('Keterangan')
st.table(keterangan1)

casual = users_feeling_temperature['casual']
registered = users_feeling_temperature['registered']
feeling_temperature = users_feeling_temperature.index

fig, ax = plt.subplots()


casual = weathersit_user['casual']
registered = weathersit_user['registered']
weather_situation = weathersit_user.index

ax.bar(weather_situation, casual, label='Casual Users')
ax.bar(weather_situation, registered, bottom=casual, label='Registered Users')
ax.set_xlabel('weather_situation')
ax.set_ylabel('Number of Users')
ax.set_xticks(weather_situation)
ax.set_xticklabels([1, 2, 3, 4])
ax.legend()
ax.set_title('Casual and Registered Holiday vs Weather Situations')

st.pyplot(fig)

keterangan2 = {
    "Kondisi Cuaca": [1, 2, 3, 4],
    "Deskripsi": [
        "Clear, Few clouds, Partly cloudy, Partly cloudy",
        "Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds",
        "Light Snow, Light Rain, Thunderstorm, Scattered clouds, Light Rain + Scattered clouds",
        "Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog",
    ],
}

st.write('Keterangan')
st.table(keterangan2)

