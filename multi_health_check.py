#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os
import json
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import csv

# === Email Config ===
EMAIL_SENDER = "anoushkak2002@gmail.com"
EMAIL_PASSWORD = "akgf xlyr etug zcvz"
EMAIL_RECEIVER = "anoushkakadam0217@gmail.com"
TIME_THRESHOLD_MIN = 15

def get_latest_log_time(folder):
    try:
        files = [f for f in os.listdir(folder) if f.endswith(".txt")]
        if not files:
            return None
        latest = max(files, key=lambda x: os.path.getmtime(os.path.join(folder, x)))
        return datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, latest)))
    except:
        return None

def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

def log_to_csv(logger_id, status, message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("run_report.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([now, logger_id, status, message])

def run_logger_health(logger_id):
    folder = os.path.join("logs", logger_id)
    last_log = get_latest_log_time(folder)
    if not last_log:
        msg = f"No logs found in {folder}"
        send_email(f"[ALERT] No logs for {logger_id}", msg)
        log_to_csv(logger_id, "FAIL", msg)
    elif datetime.now() - last_log > timedelta(minutes=TIME_THRESHOLD_MIN):
        msg = f"Log outdated: last seen at {last_log}"
        send_email(f"[ALERT] Stale log for {logger_id}", msg)
        log_to_csv(logger_id, "FAIL", msg)
    else:
        msg = f"Healthy log: last updated {last_log}"
        print(f"[✓] {logger_id}: {msg}")
        log_to_csv(logger_id, "PASS", msg)

def run_all():
    with open("loggers_config.json") as f:
        loggers = json.load(f)
    for logger in loggers:
        run_logger_health(logger["logger_id"])

if __name__ == "__main__":
    run_all()


# In[ ]:




