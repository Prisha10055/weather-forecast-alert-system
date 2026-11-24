# System Architecture — Weather Forecast & Alert Application

## 1. High-Level Pipeline
```
[User Input: City + Mode]
          │
          ▼
[Weather Fetcher (src/weather_fetcher.py)]
   ├── API Mode ──► OpenWeatherMap REST API (requests)
   └── Sim Mode ──► Local JSON Dataset (data/sample_weather_data.json)
          │
          ▼
[Weather Parser (src/weather_parser.py)]
   ├── Current Weather Dict
   └── Forecast Pandas DataFrame + Summary Stats
          │
          ▼
[Alert Engine (src/alert_engine.py)]
   ├── High Temperature Check (>= 38.0°C)
   ├── Rain / Heavy Precipitation Check (>= 5.0 mm)
   ├── High Humidity Check (>= 80%)
   └── Wind / Thunderstorm Check (>= 12.0 m/s)
          │
          ▼
[Outputs & Visualization]
   ├── Terminal / Streamlit Dashboard (main.py / dashboard.py)
   ├── Forecast CSV Report (reports/weather_report_<city>.csv)
   ├── Alert Summary TXT (outputs/alert_summary_<city>.txt)
   └── Forecast Chart PNG (images/forecast_chart_<city>.png)
```

## 2. Data Flow
1. **Ingestion**: `fetch_weather(city, mode)` retrieves current and 3-hour forecast JSON payloads.
2. **Normalization**: `parse_current_weather()` and `parse_forecast_dataframe()` extract temperature, humidity, wind speed, rainfall, and weather condition fields.
3. **Rule Evaluation**: `evaluate_alerts()` compares peak/cumulative values against configurable thresholds from `.env`.
4. **Reporting & Visualization**: `report_generator.py` writes CSV and TXT artifacts, while `visualizer.py` renders a dual-panel Matplotlib chart.
