#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import json
from datetime import datetime

# Simulated config
logger_config = {
    "logger_id": "DL001",
    "location": "Pune Plant",
    "ip_address": "192.168.1.101",
    "status": "active"
}

# Create config folder and save as JSON
config_folder = "config"
os.makedirs(config_folder, exist_ok=True)
with open(os.path.join(config_folder, f"{logger_config['logger_id']}_config.json"), "w") as f:
    json.dump(logger_config, f, indent=4)

# Simulate logger data folder
logger_data_folder = os.path.join("logs", logger_config["logger_id"])
os.makedirs(logger_data_folder, exist_ok=True)

# Create a dummy log file
log_filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
log_path = os.path.join(logger_data_folder, log_filename)

with open(log_path, "w") as f:
    f.write(f"Logger ID: {logger_config['logger_id']}\n")
    f.write(f"Timestamp: {datetime.now()}\n")
    f.write("Temperature: 75.2°C\n")
    f.write("Vibration: 0.03g\n")
    f.write("Status: OK\n")

print(f"[✓] Logger commissioned and data file created: {log_path}")


# In[ ]:




