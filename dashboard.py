import streamlit as st
import pandas as pd
import altair as alt
import json
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Logger Health Dashboard", layout="wide")

# --- THEME / STYLE ---
st.markdown("""
    <style>
        body { font-family: 'Segoe UI', sans-serif; }
        .main { background-color: #f9f9f9; }
        h1, h2, h3 { color: #4b4b4b; }
        .st-emotion-cache-1r4qj8v { color: #333 !important; }
        .metric-label { font-weight: bold; }
        .badge-pass { background-color: #28a745; padding: 4px 8px; color: white; border-radius: 6px; }
        .badge-fail { background-color: #dc3545; padding: 4px 8px; color: white; border-radius: 6px; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🛠️ Logger Health Monitoring Dashboard")
st.markdown("Monitor real-time data logger health, identify failures, and support predictive maintenance decisions.")

# --- REFRESH ---
st.query_params.update(run=str(datetime.now()))
st.markdown("<meta http-equiv='refresh' content='30'>", unsafe_allow_html=True)

try:
    # --- LOAD DATA ---
    with open("loggers_config.json") as f:
        logger_meta = pd.DataFrame(json.load(f))

    df = pd.read_csv("run_report.csv", names=["Timestamp", "Logger ID", "Status", "Message"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df = df.sort_values(by="Timestamp", ascending=False)

    # --- FILTER: Date Range ---
    st.markdown("### 📆 Filter by Date")
    min_date = df["Timestamp"].min().date()
    max_date = df["Timestamp"].max().date()
    start_date, end_date = st.date_input("Select date range", [min_date, max_date])
    df = df[(df["Timestamp"].dt.date >= start_date) & (df["Timestamp"].dt.date <= end_date)]

    # --- METRICS ---
    st.markdown("### 📊 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("🖥️ Total Loggers", df["Logger ID"].nunique())
    col2.metric("📄 Total Checks", len(df))
    col3.metric("❌ Failures", (df["Status"] == "FAIL").sum())

    # --- STATUS CHART ---
    st.markdown("### ✅ Health Status Overview")
    status_count = df["Status"].value_counts().reset_index()
    status_count.columns = ["Status", "Count"]
    st.altair_chart(
        alt.Chart(status_count).mark_bar().encode(
            x="Status",
            y="Count",
            color="Status"
        ).properties(width=500),
        use_container_width=True
    )

    # --- TREND CHART ---
    st.markdown("### 📈 Log Check Trend Over Time")
    trend = df.groupby([df["Timestamp"].dt.date, "Status"]).size().reset_index(name="Count")
    st.altair_chart(
        alt.Chart(trend).mark_line(point=True).encode(
            x="Timestamp:T",
            y="Count:Q",
            color="Status:N"
        ).properties(height=300),
        use_container_width=True
    )

    # --- RECENT LOG TABLE ---
    st.markdown("### 📋 Recent Log Entries")
    def badge(status):
        return f"<span class='badge-pass'>{status}</span>" if status == "PASS" else f"<span class='badge-fail'>{status}</span>"

    df_display = df.head(20).copy()
    df_display["Status"] = df_display["Status"].apply(lambda x: badge(x))
    st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)

    # --- LOGGER FILTER ---
    st.markdown("### 🔍 View Specific Logger")
    selected = st.selectbox("Choose a Logger", df["Logger ID"].unique())
    filtered_df = df[df["Logger ID"] == selected]
    st.dataframe(filtered_df, use_container_width=True)

    # --- DOWNLOAD ---
    st.download_button(
        label="⬇️ Download Logs as CSV",
        data=filtered_df.to_csv(index=False),
        file_name=f"{selected}_logs.csv",
        mime="text/csv"
    )

    # --- MAP ---
    st.markdown("### 🌍 Logger Locations")
    st.map(logger_meta.rename(columns={"lat": "latitude", "lon": "longitude"}))

except FileNotFoundError:
    st.warning("⚠️ Missing file: Make sure `run_report.csv` and `loggers_config.json` are present.")
