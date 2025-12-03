import pandas as pd

# 1. Load the raw data
file_path = "data/GlobalWeatherRepository.csv"   # change to .xlsx if needed
df = pd.read_csv(file_path)

# 2. Basic info
print("Shape:", df.shape)
print("\nColumns:\n", df.columns)
print("\nInfo:")
print(df.info())

# 3. Missing values per column
print("\nMissing values per column:")
print(df.isna().sum().sort_values(ascending=False))

# 4. First few rows
print("\nHead:")
print(df.head())
# 5. Convert last_updated to datetime and add a date column
df["last_updated"] = pd.to_datetime(df["last_updated"])
df["date"] = df["last_updated"].dt.date

# 6. Drop obviously redundant columns
cols_to_drop = [
    "temperature_fahrenheit",
    "wind_mph",
    "pressure_in",
    "precip_in",
    "visibility_miles",
    "feels_like_fahrenheit",
    "gust_mph",
]
df_reduced = df.drop(columns=cols_to_drop)

print("\nNew shape after dropping columns:", df_reduced.shape)

# 7. Remove any duplicate rows
before = df_reduced.shape[0]
df_reduced = df_reduced.drop_duplicates()
after = df_reduced.shape[0]
print(f"Rows before dedup: {before}, after dedup: {after}")

# 8. Save cleaned data
output_path = "data/GlobalWeatherRepository_clean.csv"
df_reduced.to_csv(output_path, index=False)
print(f"\nCleaned data saved to {output_path}")
