import streamlit as st
import pandas as pd

df = pd.read_csv("data/GlobalWeatherRepository_clean.csv")

st.title("ClimateScope – Milestone 2 Dashboard")

st.subheader("Average Weather by Country")
country_stats = df.groupby("country")[["temperature_celsius", "humidity", "precip_mm"]].mean().reset_index()
st.bar_chart(country_stats.set_index("country")["temperature_celsius"])

st.subheader("Temperature vs Humidity")
st.scatter_chart(df[["temperature_celsius", "humidity"]])

st.subheader("Extreme Weather Counts")
hot_days = (df["temperature_celsius"] >= 40).sum()
heavy_rain = (df["precip_mm"] >= 50).sum()
strong_wind = (df["wind_kph"] >= 60).sum()
st.write(f"Hot days (>=40°C): {hot_days}")
st.write(f"Heavy rain events (>=50 mm): {heavy_rain}")
st.write(f"Strong wind cases (>=60 kph): {strong_wind}")
