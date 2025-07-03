import streamlit as st
import pandas as pd
import requests
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

# Function to fetch flight data (API or fallback to sample data)

@st.cache_data(show_spinner=True)
def fetch_flights(date_from, date_to):
    api_key = "1703192fa624ca761bda7bb0dacf2346" # Use your actual API key
    all_data = []
    current_date = date_from
    while current_date <= date_to:
        date_str = current_date.strftime("%Y-%m-%d")
        url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&flight_date={date_str}&limit=100"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                flights = resp.json().get("data", [])
                for flight in flights:
                    dep = flight.get("departure", {}).get("iata")
                    arr = flight.get("arrival", {}).get("iata")
                    time_str = flight.get("departure", {}).get("scheduled")
                    if dep and arr and time_str:
                        try:
                            first_seen = int(pd.to_datetime(time_str).timestamp())
                        except Exception:
                            first_seen = None
                        all_data.append({
                            "estDepartureAirport": dep,
                            "estArrivalAirport": arr,
                            "firstSeen": first_seen
                        })
            else:
                st.warning(f"No data returned from API for {date_str}.")
        except Exception as e:
            st.error(f"API error for {date_str}: {e}")
        current_date += timedelta(days=1)
    if all_data:
        return pd.DataFrame(all_data)
    else:
        return pd.DataFrame()
df = fetch_flights(date_from, date_to)  # <-- Add this line

if not df.empty:
    df = df.dropna(subset=["estDepartureAirport", "estArrivalAirport"])
    df["route"] = df["estDepartureAirport"] + " ➔ " + df["estArrivalAirport"]

    popular_routes = df["route"].value_counts().head(10).reset_index()
    popular_routes.columns = ["Route", "Number of Flights"]

    df["date"] = pd.to_datetime(df["firstSeen"], unit="s").dt.date
    flights_per_day = df.groupby("date").size().reset_index(name="Flights")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Popular Routes")
        fig_routes = px.bar(popular_routes, x="Route", y="Number of Flights", color="Number of Flights")
        st.plotly_chart(fig_routes, use_container_width=True)

    with col2:
        st.subheader("Flights Per Day")
        fig_trend = px.line(flights_per_day, x="date", y="Flights", markers=True)
        st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("Raw Data Sample")
    st.dataframe(df.head(50))
else:
    st.info("No data available for the selected date range.")

st.markdown("""
---
**Instructions:**  
- Use the sidebar to select date range.  
- View popular routes and daily flight trends.  
- Data source: AviationStack API
""")