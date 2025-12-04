# Milestone 2 – Analysis & Dashboard

- Used cleaned dataset `GlobalWeatherRepository_clean.csv` for analysis. [file:52]
- For each country, calculated mean, min, and max of temperature, humidity, rainfall, wind speed, and UV index to understand regional weather patterns. 
- Defined extreme events as:
  - Hot days: temperature_celsius ≥ 40°C
  - Heavy rain: precip_mm ≥ 50 mm
  - Strong wind: wind_kph ≥ 60 kph
- Built a basic Streamlit dashboard (`dashboard_m2.py`) with:
  - Bar chart of average temperature by country
  - Scatter plot of temperature vs humidity
  - Text counts of extreme events
- This milestone provides first insights into which regions are hotter, more humid, or windier, and how frequent extreme events are, ready to be shown in the milestone presentation.
