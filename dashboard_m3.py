import streamlit as st
import pandas as pd

df = pd.read_csv("data/GlobalWeatherRepository_clean.csv")
df["last_updated"] = pd.to_datetime(df["last_updated"])
df["date"] = df["last_updated"].dt.date

st.title("ClimateScope – Milestone 2 Dashboard")

import plotly.express as px

st.header("Global overview")

st.subheader("Top 10 hottest countries (avg temp)")

country_stats = (
    df.groupby("country")["temperature_celsius"]
    .mean()
    .reset_index()
    .sort_values("temperature_celsius", ascending=False)
    .head(10)
)

fig_top10 = px.bar(
    country_stats,
    x="country",
    y="temperature_celsius",
    labels={"country": "Country", "temperature_celsius": "Avg temperature (°C)"},
    title="Top 10 countries by average temperature",
    color="temperature_celsius",
    color_continuous_scale="OrRd",
)
fig_top10.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_top10, use_container_width=True)


st.subheader("Temperature vs Humidity")
st.scatter_chart(df[["temperature_celsius", "humidity"]])

st.subheader("Extreme Weather Counts")
hot_days = (df["temperature_celsius"] >= 40).sum()
heavy_rain = (df["precip_mm"] >= 50).sum()
strong_wind = (df["wind_kph"] >= 60).sum()
st.write(f"Hot days (>=40°C): {hot_days}")
st.write(f"Heavy rain events (>=50 mm): {heavy_rain}")
st.write(f"Strong wind cases (>=60 kph): {strong_wind}")
import plotly.express as px

st.subheader("Temperature over time for a country")

countries = sorted(df["country"].unique())
selected_country = st.selectbox("Select country", countries)

country_df = df[df["country"] == selected_country].sort_values("last_updated")

fig_line = px.line(
    country_df,
    x="last_updated",
    y="temperature_celsius",
    title=f"Temperature over time – {selected_country}",
    labels={"last_updated": "Date", "temperature_celsius": "Temperature (°C)"},
)
st.plotly_chart(fig_line, use_container_width=True)
st.subheader("Monthly average temperature heatmap")

# Create a month column
df["month"] = df["last_updated"].dt.month

# Let user choose a few countries to compare
all_countries = sorted(df["country"].unique())
selected_countries = st.multiselect(
    "Select countries for heatmap",
    all_countries,
    default=all_countries[:5],  # first 5 as default
)

heat_df = (
    df[df["country"].isin(selected_countries)]
    .groupby(["country", "month"])["temperature_celsius"]
    .mean()
    .reset_index()
)

import plotly.express as px

fig_heat = px.density_heatmap(
    heat_df,
    x="month",
    y="country",
    z="temperature_celsius",
    color_continuous_scale="RdYlBu_r",
    labels={"month": "Month", "temperature_celsius": "Avg temp (°C)"},
)
st.plotly_chart(fig_heat, use_container_width=True)
