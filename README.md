# 🌦️ Weather Forecast & Alert Application

A modular, industry-oriented Python application that fetches real-time or simulated weather data, analyzes short-term forecasts using **Pandas**, evaluates multi-condition risk alerts (rain, heat, humidity, wind/storms), generates **Matplotlib** visualizations, exports **CSV/TXT reports**, and optionally serves an interactive **Streamlit** dashboard.

---

## 📌 Problem Statement
Sudden weather changes—heavy rainfall, heatwaves, high humidity, and strong winds—disrupt daily commutes, logistics deliveries, agricultural irrigation, and outdoor events. Most basic weather apps only display raw numbers without automated, threshold-driven risk alerts or downloadable operational reports. This project solves that gap with a clean, automated weather monitoring and alerting pipeline.

---

## 🏭 Industry Relevance
- **Logistics & Supply Chain**: Reroute fleets and protect weather-sensitive cargo ahead of heavy rain or storms.
- **Agriculture**: Schedule irrigation and crop protection based on rainfall and heat forecasts.
- **Event Planning & Travel**: Trigger early advisories for outdoor venues and travelers.
- **Data Engineering & Analytics**: Demonstrates REST API integration, JSON parsing, Pandas time-series aggregation, rule engines, and automated reporting.

---

## ✨ Key Features
- **Dual Execution Modes**: Live **OpenWeatherMap API** mode (`--mode api`) and offline **Virtual Simulation** mode (`--mode sim`) using realistic JSON data.
- **Multi-Condition Alert Engine**: Evaluates High Temperature, Rainfall, High Humidity, and Wind/Thunderstorm thresholds with `INFO`, `WARNING`, and `CRITICAL` severity levels.
- **Automated Visualization**: Generates 2-panel Matplotlib charts (temperature trend + rainfall bars & humidity curve).
- **Report Generation**: Exports structured forecast CSV files (`reports/`) and human-readable alert summaries (`outputs/`).
- **Optional Interactive Dashboard**: Includes `dashboard.py` built with Streamlit for interactive threshold tuning.

---

## 🛠️ Tech Stack
- **Language**: Python 3.10+
- **API & Networking**: `requests`, OpenWeatherMap REST API
- **Data Processing**: `pandas`, `json`, `datetime`
- **Visualization**: `matplotlib`
- **Configuration & Security**: `python-dotenv` (`.env`)
- **Dashboard (Optional)**: `streamlit`

---

## 📁 Folder Structure
```text
Weather-Forecast-Alert-Application/
├── data/               # Sample JSON weather data for offline simulation
├── src/                # Modular Python source code
│   ├── config.py
│   ├── weather_fetcher.py
│   ├── weather_parser.py
│   ├── alert_engine.py
│   ├── visualizer.py
│   └── report_generator.py
├── outputs/            # Generated text-based alert summary reports
├── images/             # Generated Matplotlib forecast charts (PNG)
├── reports/            # Generated forecast CSV datasets
├── docs/               # Architecture documentation
├── tests/              # Unit tests for alert logic
├── dashboard.py        # Optional Streamlit web dashboard
├── main.py             # CLI entry point
├── requirements.txt    # Python dependencies
├── .env.example        # Safe environment variable template
└── .gitignore          # Protects .env and cache files from GitHub
```

---

## 🔑 API Setup Instructions
1. Create a free account at [OpenWeatherMap](https://openweathermap.org/api) and copy your API key.
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Paste your key into `.env`:
   ```env
   OPENWEATHER_API_KEY=your_actual_api_key_here
   ```
> **Security Note**: Never commit `.env` to GitHub. It is already listed in `.gitignore`.

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run in Virtual Simulation Mode (No API Key Needed)
```bash
python main.py --city Mumbai --mode sim
python main.py --city Delhi --mode sim
python main.py --city Pune --mode sim
```

### 3. Run in Live API Mode
```bash
python main.py --city Pune --mode api
```

### 4. Run Optional Streamlit Dashboard
```bash
streamlit run dashboard.py
```

### 5. Run Unit Tests
```bash
python -m unittest discover -s tests
```

---

## 📊 Sample Output
```text
================================================================
  WEATHER FORECAST & ALERT APPLICATION (SIM MODE)
================================================================

City        : Mumbai, IN
Data Source : Virtual Simulation (Offline JSON)
Condition   : Rain (Heavy Intensity Rain)
Temperature : 30.2°C (Feels like 36.8°C)
Humidity    : 88%
Wind Speed  : 9.5 m/s

--- Forecast Summary ---
Temp Range: 26.8°C – 30.5°C (Avg 28.42°C) | Total Rain: 59.9 mm | Max Humidity: 91%

--- Weather Alerts ---
[CRITICAL] Rain Alert: Expected cumulative rainfall of 59.9 mm (peak 3h slot: 24.0 mm).
[INFO] High Humidity Alert: Humidity reaches 91% (threshold: 80%). Expect muggy conditions.
[CRITICAL] Wind/Storm Alert: Peak wind speed 12.8 m/s with thunderstorm activity.
```

---

## 🎓 Learning Outcomes
- Integrating external REST APIs and handling HTTP/JSON errors gracefully.
- Transforming nested JSON payloads into clean Pandas DataFrames.
- Designing a configurable rule-based alerting engine.
- Securing credentials with `.env` and `.gitignore` for GitHub portfolios.
