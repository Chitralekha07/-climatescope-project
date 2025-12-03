# Milestone 1 – Data Preparation

- Source: Global Weather Repository dataset from Kaggle (110,108 rows, 41 columns). [file:52]
- Key variables: location (country, name, latitude, longitude, timezone), temperature, humidity, precipitation, wind speed, visibility, UV index, multiple air-quality indices, and sun/moon information. [file:52]
- Data quality: No missing values in any column; duplicate rows were checked and none removed. [file:52]
- Transformations:
  - Converted `last_updated` to a datetime type and derived a `date` column for time-based analysis. [file:52]
  - Dropped redundant unit columns (Fahrenheit, mph, inches, miles, duplicate gust/wind measures) to keep a clean metric-focused dataset. [file:52]
- Output: Cleaned dataset saved as `data/GlobalWeatherRepository_clean.csv`, ready for analysis and visualization in later milestones. [file:52]
