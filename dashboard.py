import streamlit as st
import pandas as pd
import altair as alt
import json
from datetime import datetime

# === THIS MUST BE FIRST ===
st.set_page_config(page_title="Logger Health Dashboard", layout="wide")
# --- BRANDED HEADER ---
logo_path = "logo.png"  # Make sure this file exists in your project folder

st.markdown("""
    <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;'>
        <div style='display: flex; align-items: center;'>
            <img src='logo.png' style='height: 50px; margin-right: 15px;' />
            <h1 style='margin: 0; color: #333;'>Anoushka Kadam</h1>
        </div>
        <p style='margin: 0; font-size: 16px; color: #666;'>Logger Health Monitoring Dashboard</p>
    </div>
""", unsafe_allow_html=True)

# === AUTO REFRESH ===
st.query_params.update(run=str(datetime.now()))
st.markdown(
    "<meta http-equiv='refresh' content='30'>",
    unsafe_allow_html=True
)

# === TITLE ===
st.title("📊 Data Logger Health Dashboard")

# === PROJECT DESCRIPTION ===
st.markdown("""
This dashboard is part of a predictive maintenance project designed to monitor and evaluate the health of industrial data loggers.

- 🔍 Automatically tracks logger activity (PASS/FAIL)  
- 🕒 Displays trends over time and recent checks  
- 📈 Helps detect anomalies based on log age and status  
- 📍 Visualizes logger locations on a map  
- 📤 Supports CSV export for individual logger reports  

The system runs periodic health checks and feeds results into this visual interface to assist operations and maintenance teams.
""")

try:
    # === LOAD LOGGER LOCATION DATA ===
    with open("loggers_config.json") as f:
        logger_meta = pd.DataFrame(json.load(f))

    # === LOAD HEALTH CHECK LOG DATA ===
    df = pd.read_csv("run_report.csv", names=["Timestamp", "Logger ID", "Status", "Message"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df = df.sort_values(by="Timestamp", ascending=False)

    # === DATE FILTER ===
    st.markdown("### 🗓️ Filter Logs by Date Range")
    min_date = df["Timestamp"].min().date()
    max_date = df["Timestamp"].max().date()
    start_date, end_date = st.date_input("Select date range", [min_date, max_date])
    df = df[(df["Timestamp"].dt.date >= start_date) & (df["Timestamp"].dt.date <= end_date)]

    # === METRICS ===
    st.markdown("### 🔍 Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("🖥️ Loggers Checked", df["Logger ID"].nunique())
    col2.metric("📄 Total Checks", len(df))
    col3.metric("❌ Fails", (df["Status"] == "FAIL").sum())

    # === STATUS SUMMARY CHART ===
    st.markdown("### ✅ Status Summary")
    status_count = df["Status"].value_counts().reset_index()
    status_count.columns = ["Status", "Count"]
    st.altair_chart(
        alt.Chart(status_count).mark_bar().encode(
            x=alt.X("Status", sort=None),
            y="Count",
            color="Status"
        ).properties(width=500),
        use_container_width=True
    )

    # === TREND LINE CHART ===
    st.markdown("### 📈 Health Checks Over Time")
    trend = df.groupby([df["Timestamp"].dt.date, "Status"]).size().reset_index(name="Count")
    st.altair_chart(
        alt.Chart(trend).mark_line(point=True).encode(
            x="Timestamp:T",
            y="Count:Q",
            color="Status:N"
        ).properties(height=300),
        use_container_width=True
    )

    # === LATEST LOGS TABLE ===
    st.markdown("### 📋 Latest Log Entries")
    df_display = df.head(20).copy()
    df_display["Status"] = df_display["Status"].apply(
        lambda x: f"🟢 {x}" if x == "PASS" else f"🔴 {x}"
    )
    st.dataframe(df_display, use_container_width=True)

    # === LOGGER-WISE FILTER AND DOWNLOAD ===
    st.markdown("### 🧠 Analyze by Logger")
    logger_ids = df["Logger ID"].unique()
    selected = st.selectbox("Select a Logger", logger_ids)

    filtered_df = df[df["Logger ID"] == selected]
    st.write(filtered_df)

    st.download_button(
        label="⬇️ Download Selected Logger Logs as CSV",
        data=filtered_df.to_csv(index=False),
        file_name=f"{selected}_logs.csv",
        mime="text/csv"
    )

    # === LOGGER MAP VIEW ===
    st.markdown("### 🗺️ Logger Locations")
    st.map(logger_meta.rename(columns={"lat": "latitude", "lon": "longitude"}))

except FileNotFoundError:
    st.warning("⚠️ Missing file: Make sure both `run_report.csv` and `loggers_config.json` are in the project folder.")
