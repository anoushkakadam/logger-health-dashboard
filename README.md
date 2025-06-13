# 📊 Logger Health Dashboard

A Streamlit-based dashboard for monitoring the health and performance of industrial data loggers. Built as part of a predictive maintenance system.

## 🌐 Live App

View App Here [Streamlit Cloud](https://share.streamlit.io/):

## 🔧 Features

- ✅ Auto-refreshing dashboard (every 30 seconds)
- 📈 Visual trends of logger performance (PASS/FAIL)
- 🗓️ Date range filtering for log analysis
- 🧠 Logger-wise log exploration
- ⬇️ CSV export for individual logger logs
- 🗺️ Map visualization of logger locations
- 📤 Ready for Streamlit Cloud deployment

## 📁 Project Structure

```
logger-health-dashboard/
├── dashboard.py               # Main Streamlit app
├── run_report.csv             # Sample health check logs
├── loggers_config.json        # Metadata with logger locations
├── .gitignore                 # Git ignored files
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 How to Run

1. Clone this repo:
```bash
git clone https://github.com/anoushkakadam/logger-health-dashboard.git
cd logger-health-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run dashboard.py
```



1. Push to a public GitHub repository
2. Go to share.streamlit.io and connect your repo
3. Select `dashboard.py` as the entry point
4. Click **Deploy**

## 📌 Requirements

- Python 3.8+
- Streamlit
- pandas
- altair

## 📬 Contact

Made with ❤️ by Anoushka Kadam  
🔗 [LinkedIn](https://linkedin.com/in/anoushka-kadam-230748210) | [GitHub](https://github.com/anoushkakadam/logger-health-dashboard)
