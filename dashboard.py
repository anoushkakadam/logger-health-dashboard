#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd

st.set_page_config(page_title="Logger Health Dashboard", layout="wide")
st.title("📊 Data Logger Health Dashboard")

try:
    df = pd.read_csv("run_report.csv", names=["Timestamp", "Logger ID", "Status", "Message"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df = df.sort_values(by="Timestamp", ascending=False)

    st.metric("Total Loggers Checked", df["Logger ID"].nunique())
    st.metric("Checks Run", len(df))
    st.metric("Fails", (df["Status"] == "FAIL").sum())

    st.subheader("Latest Log Statuses")
    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("Status Summary")
    st.bar_chart(df["Status"].value_counts())

    st.subheader("Logs by Logger ID")
    selected_logger = st.selectbox("Select Logger ID", df["Logger ID"].unique())
    st.write(df[df["Logger ID"] == selected_logger])

except FileNotFoundError:
    st.warning("No run_report.csv file found. Run a health check first.")


# In[ ]:




