#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import csv
import os
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

# === Configuration ===
LOGGER_ID = "DL001"
LOGGER_FOLDER = os.path.join("logs", LOGGER_ID)
TIME_THRESHOLD_MIN = 15  # alert if no fresh logs in 15 minutes

# === Email Configuration ===
EMAIL_SENDER = "anoushkak2002@gmail.com"
EMAIL_PASSWORD = "ehql fsiz piuj afpt"  # Use an app-specific password!
EMAIL_RECEIVER = "anoushkakadam0217@gmail.com"

def get_latest_log_time():
    try:
        log_files = [f for f in os.listdir(LOGGER_FOLDER) if f.endswith(".txt")]
        if not log_files:
            return None

        latest_file = max(log_files, key=lambda x: os.path.getmtime(os.path.join(LOGGER_FOLDER, x)))
        latest_path = os.path.join(LOGGER_FOLDER, latest_file)
        mod_time = datetime.fromtimestamp(os.path.getmtime(latest_path))
        return mod_time
    except Exception as e:
        print("Error during file scan:", e)
        return None

def send_email_alert(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print("[!] Email alert sent.")

def run_health_check():
    print("[~] Running health check...")
    last_log_time = get_latest_log_time()

    if not last_log_time:
        message = "No logs found."
        send_email_alert(
            subject=f"[ALERT] No logs found for {LOGGER_ID}",
            body=message
        )
        log_result("FAIL", message)
    elif datetime.now() - last_log_time > timedelta(minutes=TIME_THRESHOLD_MIN):
        message = f"Log outdated: last at {last_log_time}"
        send_email_alert(
            subject=f"[ALERT] Log is outdated for {LOGGER_ID}",
            body=message
        )
        log_result("FAIL", message)
    else:
        message = f"Log OK: last at {last_log_time}"
        print(f"[✓] {message}")
        log_result("PASS", message)

    
def log_result(status, message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [now, LOGGER_ID, status, message]
    with open("run_report.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)


# In[ ]:




