import streamlit as st
import pandas as pd
import plotly.express as px

# --------- DATA LOADING ---------
@st.cache_data
def load_data():
    df = pd.read_csv("data/GlobalWeatherRepository_clean.csv")
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    df["date"] = df["last_updated"].dt.date
    df["month"] = df["last_updated"].dt.month

    # Season column for seasonal filter
    def month_to_season(m):
        if m in [12, 1, 2]:
            return "Winter"
        elif m in [3, 4, 5]:
            return "Spring"
        elif m in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"

    df["season"] = df["month"].apply(month_to_season)
    return df


df = load_data()

# --------- SIDEBAR FILTERS (SHARED) ---------
st.sidebar.title("ClimateScope Filters")

# Country multiselect
all_countries = sorted(df["country"].unique())
selected_countries = st.sidebar.multiselect(
    "Select countries",
    all_countries,
    default=all_countries[:5],
)

# Date range slider
min_date = df["date"].min()
max_date = df["date"].max()
selected_dates = st.sidebar.slider(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# Metric selector
metric_options = ["temperature_celsius", "humidity", "precip_mm", "wind_kph"]
selected_metric = st.sidebar.selectbox("Select metric", metric_options)

# Extreme threshold
threshold = st.sidebar.number_input(
    "Extreme threshold for selected metric",
    value=40.0,
)

# Above / below for extremes
extreme_type = st.sidebar.radio(
    "Show extremes above or below threshold?",
    ["Above", "Below"],
)

# Time aggregation
agg_level = st.sidebar.radio(
    "Time aggregation",
    ["Daily", "Monthly"],
    index=0,
)

# Seasonal filter
season = st.sidebar.selectbox(
    "Season (optional)",
    ["All seasons", "Winter", "Spring", "Summer", "Autumn"],
)

# --------- APPLY FILTERS TO BASE DATAFRAME ---------
filtered_df = df.copy()

if selected_countries:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

filtered_df = filtered_df[
    (filtered_df["date"] >= selected_dates[0])
    & (filtered_df["date"] <= selected_dates[1])
]

if season != "All seasons":
    filtered_df = filtered_df[filtered_df["season"] == season]

# Extreme subset (using all filters + above/below choice)
if extreme_type == "Above":
    extreme_filtered_df = filtered_df[filtered_df[selected_metric] > threshold]
else:
    extreme_filtered_df = filtered_df[filtered_df[selected_metric] < threshold]

# --------- PAGE SELECTION ---------
page = st.sidebar.radio(
    "Go to page",
    ["Executive dashboard", "Statistical analysis", "Climate trends", "Extreme events", "Help"],
)

# --------- PAGE FUNCTIONS ---------
def page_executive(df_page):
    st.title("Executive Dashboard")

    st.subheader(f"Key metrics ({agg_level} view)")

    avg_temp = df_page["temperature_celsius"].mean()
    avg_hum = df_page["humidity"].mean()

    if extreme_type == "Above":
        extreme_count = (df_page[selected_metric] > threshold).sum()
    else:
        extreme_count = (df_page[selected_metric] < threshold).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg temperature (°C)", f"{avg_temp:.1f}")
    col2.metric("Avg humidity (%)", f"{avg_hum:.1f}")
    col3.metric(
        f"Extreme events ({'>' if extreme_type=='Above' else '<'} {threshold})",
        f"{extreme_count}",
    )

    st.write(
        "These KPIs update with the sidebar filters (countries, dates, metric, threshold, season). "
        "Use the other pages for detailed trend and distribution views."
    )

    st.divider()
    st.subheader(f"Global map of {selected_metric}")

    map_df = (
        df_page.groupby("country")[selected_metric]
        .mean()
        .reset_index()
    )

    fig_map = px.scatter_geo(
        map_df,
        locations="country",
        locationmode="country names",
        color=selected_metric,
        size=selected_metric,
        hover_name="country",
        color_continuous_scale="Turbo",
        projection="natural earth",
        title=f"Average {selected_metric} by country (filtered selection)",
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown(
        "The map shows how the selected metric varies by country for the chosen filters. "
        "Use the sidebar to adjust countries, date range, metric, and season."
    )


def page_statistical(df_page):
    st.title("Statistical Analysis")

    st.subheader(f"Scatter plot: {selected_metric} vs humidity")

    fig_scatter = px.scatter(
        df_page,
        x="humidity",
        y=selected_metric,
        color="country",
        opacity=0.4,
        labels={"humidity": "Humidity (%)", selected_metric: selected_metric},
        title=f"{selected_metric} vs humidity",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown(
        "This scatter plot shows how the selected metric relates to humidity for the "
        "filtered countries, dates, and season."
    )

    st.subheader(f"Country comparison for {selected_metric}")

    country_stats = (
        df_page.groupby("country")[selected_metric]
        .mean()
        .reset_index()
        .sort_values(selected_metric, ascending=False)
        .head(15)
    )

    fig_bar = px.bar(
        country_stats,
        x="country",
        y=selected_metric,
        labels={"country": "Country", selected_metric: f"Mean {selected_metric}"},
        title=f"Top 15 countries by mean {selected_metric}",
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown(
        "This bar chart compares average values by country using the current filters."
    )

    st.subheader(f"Distributions of {selected_metric}")

    col1, col2 = st.columns(2)

    with col1:
        fig_hist = px.histogram(
            df_page,
            x=selected_metric,
            nbins=40,
            marginal="rug",
            labels={selected_metric: selected_metric},
            title=f"Histogram of {selected_metric}",
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        # Violin plot (new requirement)
        fig_violin = px.violin(
            df_page,
            x="country",
            y=selected_metric,
            box=True,
            points="all",
            color="country",
            labels={"country": "Country", selected_metric: selected_metric},
            title=f"Violin plot of {selected_metric} by country",
        )
        fig_violin.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_violin, use_container_width=True)

    st.markdown(
        "The histogram shows the overall distribution, while the violin plot highlights "
        "the spread and density of values by country."
    )

    st.subheader("Correlation heatmap (core metrics)")

    corr_cols = ["temperature_celsius", "humidity", "precip_mm", "wind_kph", "uv_index"]
    corr_df = df_page[corr_cols].corr()

    fig_corr = px.imshow(
        corr_df,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Correlation between key weather metrics",
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown(
        "Values close to 1 indicate strong positive correlation, "
        "values close to -1 indicate strong negative correlation."
    )


def page_trends(df_page):
    st.title("Climate Trends")

    st.subheader(f"{agg_level} time-series of {selected_metric}")

    df_ts = df_page.sort_values("last_updated")

    if agg_level == "Daily":
        fig_line = px.line(
            df_ts,
            x="last_updated",
            y=selected_metric,
            color="country",
            labels={"last_updated": "Date", selected_metric: selected_metric},
            title=f"{selected_metric} over time by country (daily)",
        )
        fig_line.update_layout(xaxis_rangeslider_visible=True)
        st.plotly_chart(fig_line, use_container_width=True)

        st.markdown("Daily line chart by country with range slider.")

        df_daily = (
            df_ts.groupby("date")[selected_metric]
            .mean()
            .reset_index()
            .sort_values("date")
        )

        fig_area = px.area(
            df_daily,
            x="date",
            y=selected_metric,
            labels={"date": "Date", selected_metric: f"Daily mean {selected_metric}"},
            title=f"Daily average {selected_metric} (all selected countries)",
        )
        fig_area.update_layout(xaxis_rangeslider_visible=True)
        st.plotly_chart(fig_area, use_container_width=True)

    else:  # Monthly
        df_page = df_page.copy()
        df_page["year_month"] = df_page["last_updated"].dt.to_period("M").astype(str)

        df_monthly_country = (
            df_page.groupby(["year_month", "country"])[selected_metric]
            .mean()
            .reset_index()
            .sort_values("year_month")
        )

        fig_line = px.line(
            df_monthly_country,
            x="year_month",
            y=selected_metric,
            color="country",
            labels={"year_month": "Year-Month", selected_metric: selected_metric},
            title=f"Monthly average {selected_metric} by country",
        )
        st.plotly_chart(fig_line, use_container_width=True)

        df_monthly_all = (
            df_page.groupby("year_month")[selected_metric]
            .mean()
            .reset_index()
            .sort_values("year_month")
        )

        fig_area = px.area(
            df_monthly_all,
            x="year_month",
            y=selected_metric,
            labels={
                "year_month": "Year-Month",
                selected_metric: f"Monthly mean {selected_metric}",
            },
            title=f"Overall monthly average {selected_metric}",
        )
        st.plotly_chart(fig_area, use_container_width=True)

        st.markdown(
            "Monthly aggregation smooths short‑term noise to show long‑term trends."
        )


def page_extremes(df_page):
    st.title("Extreme Events")

    st.subheader(f"Top 5 days with highest {selected_metric}")

    top5 = (
        df_page.sort_values(selected_metric, ascending=False)[
            ["date", "country", selected_metric]
        ]
        .head(5)
    )
    st.dataframe(top5, use_container_width=True)

    st.markdown(
        f"These are the 5 highest values of **{selected_metric}** in the filtered data."
    )

    st.subheader(
        f"Events where {selected_metric} "
        f"{'>' if extreme_type=='Above' else '<'} {threshold}"
    )

    extreme_df = extreme_filtered_df

    col1, col2 = st.columns(2)
    col1.metric("Number of extreme events", len(extreme_df))
    if not extreme_df.empty:
        col2.metric(
            "Countries affected",
            extreme_df["country"].nunique(),
        )

    if extreme_df.empty:
        st.info("No extreme events for the current filters and threshold.")
        return

    st.subheader("Extreme events by country")

    country_counts = (
        extreme_df.groupby("country")[selected_metric]
        .count()
        .reset_index(name="event_count")
        .sort_values("event_count", ascending=False)
    )

    fig_bar = px.bar(
        country_counts.head(15),
        x="country",
        y="event_count",
        labels={"country": "Country", "event_count": "Number of extreme events"},
        title=f"Top countries by extreme {selected_metric} events",
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Extreme events over time (monthly count)")

    extreme_df = extreme_df.copy()
    extreme_df["year_month"] = extreme_df["last_updated"].dt.to_period("M").astype(str)
    monthly_counts = (
        extreme_df.groupby("year_month")[selected_metric]
        .count()
        .reset_index(name="event_count")
        .sort_values("year_month")
    )

    fig_line = px.line(
        monthly_counts,
        x="year_month",
        y="event_count",
        labels={"year_month": "Year-Month", "event_count": "Extreme events"},
        title=f"Monthly count of extreme {selected_metric} events",
    )
    st.plotly_chart(fig_line, use_container_width=True)


def page_help():
    st.title("Help & User Guide")

    st.subheader("How to use the dashboard")
    st.markdown(
        """
- **Filters (left sidebar)**  
  - Select one or more countries.  
  - Use the date range slider to focus on a specific period.  
  - Choose the metric (temperature, humidity, precipitation, wind speed).  
  - Set an extreme threshold and whether to show values above or below it.  
  - Switch between *Daily* and *Monthly* aggregation for the Climate Trends page.  
  - Optionally filter by season (Winter, Spring, Summer, Autumn).  
- **Pages**  
  - *Executive dashboard*: Key KPIs and global map overview.  
  - *Statistical analysis*: Scatter plots, distributions, violin plot, and correlation heatmap.  
  - *Climate trends*: Daily/Monthly time‑series and area charts.  
  - *Extreme events*: Top extreme days, country counts, and monthly frequency trends.  
- **Interactivity**  
  - Hover over points/bars/map bubbles to see exact values.  
  - Use the Plotly toolbar on each chart to zoom, pan, and download as PNG.
        """
    )

    st.subheader("Notes")
    st.markdown(
        """
- Data source: Global Weather Repository (Kaggle) cleaned in earlier milestones.  
- All charts respect the current sidebar filters unless stated otherwise.
        """
    )


# --------- RENDER SELECTED PAGE ---------
if page == "Executive dashboard":
    page_executive(filtered_df)
elif page == "Statistical analysis":
    page_statistical(filtered_df)
elif page == "Climate trends":
    page_trends(filtered_df)
elif page == "Extreme events":
    page_extremes(filtered_df)
else:
    page_help()
