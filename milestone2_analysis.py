import pandas as pd

df = pd.read_csv("data/GlobalWeatherRepository_clean.csv")

# 1. Basic regional weather summary
region_stats = df.groupby("country")[[
    "temperature_celsius",
    "humidity",
    "precip_mm",
    "wind_kph",
    "uv_index",
]].agg(["mean", "min", "max"]).reset_index()
print(region_stats.head())

# 2. Identify extreme weather events
hot_days = df[df["temperature_celsius"] >= 40]
heavy_rain = df[df["precip_mm"] >= 50]
strong_wind = df[df["wind_kph"] >= 60]

print("Hot days (>=40C):", len(hot_days))
print("Heavy rain events (>=50mm):", len(heavy_rain))
print("Strong wind cases (>=60 kph):", len(strong_wind))
