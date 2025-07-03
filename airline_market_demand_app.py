import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Set up the web page
st.set_page_config(page_title="Airline Market Demand Trends", layout="wide")
st.title("✈️ Airline Booking Market Demand Dashboard")

# Sidebar for user filters
st.sidebar.header("Filter Options")
date_today = datetime.utcnow().date()
date_from = st.sidebar.date_input("From Date", date_today - timedelta(days=1))
date_to = st.sidebar.date_input("To Date", date_today)

# Dummy data for fallback (more realistic sample)
def get_dummy_data():
    data = {
        "flight_number": [
            "QF400", "QF401", "VA800", "VA801", "JQ500", "JQ501", "QF402", "VA802", "JQ502", "QF403",
            "QF404", "VA803", "JQ503", "QF405", "VA804", "JQ504", "QF406", "VA805", "JQ505", "QF407"
        ],
        "airline": [
            "Qantas", "Qantas", "Virgin Australia", "Virgin Australia", "Jetstar", "Jetstar",
            "Qantas", "Virgin Australia", "Jetstar", "Qantas",
            "Qantas", "Virgin Australia", "Jetstar", "Qantas", "Virgin Australia", "Jetstar",
            "Qantas", "Virgin Australia", "Jetstar", "Qantas"
        ],
        "estDepartureAirport": [
            "SYD", "MEL", "SYD", "MEL", "SYD", "MEL", "BNE", "SYD", "BNE", "MEL",
            "SYD", "BNE", "MEL", "BNE", "SYD", "MEL", "BNE", "SYD", "MEL", "BNE"
        ],
        "estArrivalAirport": [
            "MEL", "SYD", "MEL", "SYD", "MEL", "SYD", "SYD", "BNE", "SYD", "BNE",
            "BNE", "SYD", "BNE", "MEL", "BNE", "SYD", "MEL", "BNE", "SYD", "MEL"
        ],
        "firstSeen": [
            int(pd.Timestamp("2024-08-01 06:00").timestamp()),
            int(pd.Timestamp("2024-08-01 07:00").timestamp()),
            int(pd.Timestamp("2024-08-01 08:00").timestamp()),
            int(pd.Timestamp("2024-08-01 09:00").timestamp()),
            int(pd.Timestamp("2024-08-01 10:00").timestamp()),
            int(pd.Timestamp("2024-08-01 11:00").timestamp()),
            int(pd.Timestamp("2024-08-01 12:00").timestamp()),
            int(pd.Timestamp("2024-08-01 13:00").timestamp()),
            int(pd.Timestamp("2024-08-01 14:00").timestamp()),
            int(pd.Timestamp("2024-08-01 15:00").timestamp()),
            int(pd.Timestamp("2024-08-02 06:00").timestamp()),
            int(pd.Timestamp("2024-08-02 07:00").timestamp()),
            int(pd.Timestamp("2024-08-02 08:00").timestamp()),
            int(pd.Timestamp("2024-08-02 09:00").timestamp()),
            int(pd.Timestamp("2024-08-02 10:00").timestamp()),
            int(pd.Timestamp("2024-08-02 11:00").timestamp()),
            int(pd.Timestamp("2024-08-02 12:00").timestamp()),
            int(pd.Timestamp("2024-08-02 13:00").timestamp()),
            int(pd.Timestamp("2024-08-02 14:00").timestamp()),
            int(pd.Timestamp("2024-08-02 15:00").timestamp()),
        ],
        "price": [
            180, 175, 160, 155, 120, 125, 190, 170, 130, 185,
            200, 165, 135, 195, 150, 140, 210, 145, 138, 205
        ]
    }
    return pd.DataFrame(data)

# Always use dummy data (no API)
df = get_dummy_data()

# Filter data by selected date range
df["date"] = pd.to_datetime(df["firstSeen"], unit="s", errors="coerce").dt.date
df_filtered = df[(df["date"] >= date_from) & (df["date"] <= date_to)]

def show_dashboard(dataframe):
    dataframe = dataframe.dropna(subset=["estDepartureAirport", "estArrivalAirport"])
    dataframe["route"] = dataframe["estDepartureAirport"] + " ➔ " + dataframe["estArrivalAirport"]

    popular_routes = dataframe["route"].value_counts().head(10).reset_index()
    popular_routes.columns = ["Route", "Number of Flights"]

    flights_per_day = dataframe.groupby("date").size().reset_index(name="Flights")
    avg_price_per_day = dataframe.groupby("date")["price"].mean().reset_index(name="Avg Price")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Popular Routes")
        fig_routes = px.bar(popular_routes, x="Route", y="Number of Flights", color="Number of Flights")
        st.plotly_chart(fig_routes, use_container_width=True)

    with col2:
        st.subheader("Flights Per Day")
        fig_trend = px.line(flights_per_day, x="date", y="Flights", markers=True)
        st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("Average Price Per Day")
    fig_price = px.line(avg_price_per_day, x="date", y="Avg Price", markers=True)
    st.plotly_chart(fig_price, use_container_width=True)

    st.subheader("Raw Data Sample")
    st.dataframe(dataframe.head(50))

if not df_filtered.empty:
    show_dashboard(df_filtered)
else:
    st.info("No data available for the selected date range. Showing sample data below.")
    dummy_df = get_dummy_data()
    dummy_df["date"] = pd.to_datetime(dummy_df["firstSeen"], unit="s", errors="coerce").dt.date
    show_dashboard(dummy_df)

st.markdown("""
---
**Instructions:**  
- Use the sidebar to select date range.  
- View popular routes, daily flight trends, and price trends.  
- Data source: Sample data (no API required).
""")