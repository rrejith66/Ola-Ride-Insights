import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# -----------------------------
# Step 1: DB Connection
# -----------------------------
user = 'root'
password = '1994'
host = '127.0.0.1'
database = 'ola_ride_analysis'

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

# -----------------------------
# Step 2: Define queries
# -----------------------------
queries = {
    "1. Successful Bookings": "SELECT COUNT(*) AS Successful_Bookings FROM ola_rides WHERE Booking_Status = 'Success';",
    "2. Average Ride Distance per Vehicle Type": "SELECT Vehicle_Type, ROUND(AVG(Ride_Distance),2) AS Avg_Ride_Distance FROM ola_rides GROUP BY Vehicle_Type;",
    "3. Total Customer Cancellations": "SELECT SUM(Customer_Cancelled) AS Total_Customer_Cancellations FROM ola_rides;",
    "4. Top 5 Customers by Rides": "SELECT Customer_ID, COUNT(*) AS Total_Rides FROM ola_rides GROUP BY Customer_ID ORDER BY Total_Rides DESC LIMIT 5;",
    "5. Driver Cancellations due to Personal/Car Issues": "SELECT COUNT(*) AS Cancelled_rides FROM ola_rides WHERE Driver_Cancelled = 1 AND Cancellation_Reason = 'Personal & Car related issue';",
    "6. Min & Max Driver Ratings for Prime Sedan": "SELECT MIN(Driver_Ratings) AS min_rating, MAX(Driver_Ratings) AS max_rating FROM ola_rides WHERE Vehicle_Type = 'Prime Sedan' AND Driver_Ratings != 0;",
    "7. Rides Paid by UPI": "SELECT * FROM ola_rides WHERE Payment_Method = 'UPI';",
    "8. Average Customer Rating per Vehicle Type": "SELECT Vehicle_Type, ROUND(AVG(Customer_Rating),2) AS Avg_Customer_Rating FROM ola_rides GROUP BY Vehicle_Type ORDER BY Avg_Customer_Rating DESC;",
    "9. Total Booking Value of Completed Rides": "SELECT SUM(Booking_Value) AS Total_Booking_Value FROM ola_rides WHERE Ride_Status = 'Completed';",
    "10. Incomplete Rides with Reason": "SELECT Booking_ID, Customer_ID, Booking_Status, Ride_Status, Incomplete_Rides_Reason FROM ola_rides WHERE Incomplete_Rides_Flag = 1;"
}

# -----------------------------
# Step 3: Streamlit UI
# -----------------------------
# st.title("📊 Ola Rides Analytics Dashboard")

# query_selection = st.selectbox("Select a query to run:", list(queries.keys()))

# if st.button("Run Query"):
#     sql_query = queries[query_selection]
#     with engine.connect() as conn:
#         df = pd.read_sql(text(sql_query), conn)
#     st.write(f"### Results for: {query_selection}")
#     st.dataframe(df)


# -----------------------------
# Step 3: Streamlit UI
# -----------------------------
st.title("📊 Ola Rides Analytics Dashboard")

query_selection = st.selectbox("Select a query to run:", list(queries.keys()), key="query_selector")

# Optional interactive filters
st.sidebar.header("🔍 Filters")
vehicle_filter = st.sidebar.multiselect("Select Vehicle Type(s):", ["Mini", "Prime Sedan", "Prime SUV", "Bike", "Auto"])
payment_filter = st.sidebar.multiselect("Select Payment Method(s):", ["Cash", "Card", "UPI", "Wallet"])

if st.button("Run Query", key="run_button"):
    sql_query = queries[query_selection]

    # Add filters dynamically only if user selects them
    filter_clauses = []
    if vehicle_filter:
        vehicles = "', '".join(vehicle_filter)
        filter_clauses.append(f"Vehicle_Type IN ('{vehicles}')")

    if payment_filter:
        payments = "', '".join(payment_filter)
        filter_clauses.append(f"Payment_Method IN ('{payments}')")

    if filter_clauses:
        if "WHERE" in sql_query.upper():
            sql_query = sql_query.rstrip(";") + " AND " + " AND ".join(filter_clauses) + ";"
        else:
            sql_query = sql_query.rstrip(";") + " WHERE " + " AND ".join(filter_clauses) + ";"

    # Run query
    with engine.connect() as conn:
        df = pd.read_sql(text(sql_query), conn)

    st.write(f"### Results for: {query_selection}")
    st.dataframe(df)

    # Optional CSV download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Results", csv, "results.csv", "text/csv")


# -----------------------------
# Step 4: Embed Power BI visuals
# -----------------------------
st.write("### 📈 Power BI Dashboard")
# Replace the URL below with your actual published Power BI report embed link
powerbi_url = "https://app.powerbi.com/view?"

st.components.v1.iframe(powerbi_url, width=1000, height=600, scrolling=True)
