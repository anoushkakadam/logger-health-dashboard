#!/usr/bin/env python
# coding: utf-8

# In[11]:


# import schedule
# import time
# from health_check import run_health_check  

# def job():
#     print("[⏰] Scheduled check running...")
#     run_health_check()

# # Schedule every 15 minutes
# schedule.every(15).minutes.do(job)

# print("[🚀] Starting automated health checks. Press Ctrl+C to stop.")

# while True:
#     schedule.run_pending()
#     time.sleep(1)

import smtplib
from email.message import EmailMessage

EMAIL_SENDER = "anoushkak2002@gmail.com"
EMAIL_PASSWORD = "ehql fsiz piuj afpt"
EMAIL_RECEIVER = "anoushkakadam0217@gmail.com"  # send to yourself for testing

msg = EmailMessage()
msg.set_content("Test email from Python")
msg["Subject"] = "SMTP Test"
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECEIVER

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("✅ Email sent successfully!")
except Exception as e:
    print("❌ Error:", e)


# In[ ]:




