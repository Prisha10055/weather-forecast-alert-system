"""Optional Streamlit Dashboard for Weather Forecast & Alert Application."""

import streamlit as st
from src.weather_fetcher import fetch_weather, get_available_sim_cities
from src.weather_parser import parse_current_weather, parse_forecast_dataframe, summarize_forecast
from src.alert_engine import evaluate_alerts
from src.report_generator import save_forecast_csv, save_alert_report

st.set_page_config(page_title="Weather Forecast & Alert App", page_icon="🌦️", layout="wide")
st.title("🌦️ Weather Forecast & Alert Application")
st.caption("Real-time & simulated weather monitoring, risk alerting, and forecast analytics.")

with st.sidebar:
    st.header("Configuration")
    mode = st.radio("Data Mode", ["sim", "api"], index=0, help="Use 'sim' for offline demo data or 'api' for live OpenWeatherMap.")
    if mode == "sim":
        cities = get_available_sim_cities()
        city = st.selectbox("Select City", cities if cities else ["Pune"])
    else:
        city = st.text_input("Enter City Name", value="Pune")

    st.subheader("Alert Thresholds")
    temp_th = st.slider("High Temp Threshold (°C)", 25.0, 50.0, 38.0, 0.5)
    hum_th = st.slider("High Humidity Threshold (%)", 50, 100, 80, 5)
    rain_th = st.slider("Rain Threshold (mm)", 1.0, 30.0, 5.0, 1.0)
    wind_th = st.slider("High Wind Threshold (m/s)", 5.0, 25.0, 12.0, 0.5)

try:
    raw = fetch_weather(city=city, mode=mode)
    current = parse_current_weather(raw["current"])
    df = parse_forecast_dataframe(raw["forecast"])
    summary = summarize_forecast(df)
    alerts = evaluate_alerts(current, df, temp_th, hum_th, rain_th, wind_th)

    st.info(f"**Data Source:** {raw['source']}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temperature", f"{current['temperature_c']:.1f} °C", f"Feels {current['feels_like_c']:.1f} °C")
    c2.metric("Humidity", f"{current['humidity_pct']} %")
    c3.metric("Wind Speed", f"{current['wind_speed_ms']:.1f} m/s")
    c4.metric("Total Forecast Rain", f"{summary['total_rain_mm']} mm")

    st.subheader("⚠️ Active Weather Alerts")
    for alert in alerts:
        if alert["severity"] == "CRITICAL":
            st.error(f"**{alert['type']}**: {alert['message']}")
        elif alert["severity"] == "WARNING":
            st.warning(f"**{alert['type']}**: {alert['message']}")
        elif alert["severity"] == "INFO":
            st.info(f"**{alert['type']}**: {alert['message']}")
        else:
            st.success(alert["message"])

    st.subheader("📈 Temperature & Rainfall Forecast")
    chart_df = df.set_index("timestamp")[["temperature_c", "rain_3h_mm", "humidity_pct"]]
    st.line_chart(chart_df[["temperature_c", "humidity_pct"]])
    st.bar_chart(chart_df[["rain_3h_mm"]])

    if st.button("Export CSV & Text Report"):
        csv_p = save_forecast_csv(current["city"], df)
        txt_p = save_alert_report(current["city"], raw["source"], current, summary, alerts)
        st.success(f"Saved reports: `{csv_p.name}` and `{txt_p.name}`")

except Exception as exc:
    st.error(f"Error loading weather data: {exc}")
