# Airline Booking Market Demand Dashboard
This Streamlit app visualizes airline booking market demand using sample data.  
You can explore popular routes, daily flight trends, and average price trends.

## Features
- **Date Range Filter:** Select a date range to filter flight data.
- **Popular Routes:** View the top 10 most popular flight routes.
- **Flights Per Day:** See the number of flights per day.
- **Average Price Per Day:** Track average ticket prices over time.
- **Raw Data Sample:** Preview the underlying data.
- 
## How to Run
1. **Install requirements:**
    ```
    py -m pip install streamlit pandas requests plotly
    ```
2. **Run the app:**
    ```
    py -m streamlit run airline_market_demand_app.py
    ```

3. **Open in browser:**  
   The app will open automatically, or visit the URL shown in your terminal.

## Notes
- This app uses sample (dummy) data if data is not availabe from API or from selected range.
- Use the sidebar to select your desired date range.
- in date from-2024/08/01( 1August 2024) to 2024/08/02(( 1August 2024)) . 
