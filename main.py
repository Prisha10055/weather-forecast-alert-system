"""Main CLI entry point for Weather Forecast & Alert Application."""

import argparse
import sys
from src.config import DEFAULT_CITY, DEFAULT_MODE
from src.weather_fetcher import fetch_weather, get_available_sim_cities
from src.weather_parser import parse_current_weather, parse_forecast_dataframe, summarize_forecast
from src.alert_engine import evaluate_alerts
from src.visualizer import plot_forecast_chart
from src.report_generator import save_forecast_csv, save_alert_report


def run_pipeline(city: str, mode: str) -> None:
    """Execute the end-to-end weather forecast, alert, chart, and report pipeline."""
    print("=" * 64)
    print(f"  WEATHER FORECAST & ALERT APPLICATION ({mode.upper()} MODE)")
    print("=" * 64)

    raw_data = fetch_weather(city=city, mode=mode)
    current = parse_current_weather(raw_data["current"])
    forecast_df = parse_forecast_dataframe(raw_data["forecast"])
    summary = summarize_forecast(forecast_df)
    alerts = evaluate_alerts(current, forecast_df)

    print(f"\nCity        : {current['city']}, {current['country']}")
    print(f"Data Source : {raw_data['source']}")
    print(f"Condition   : {current['condition']} ({current['description']})")
    print(f"Temperature : {current['temperature_c']:.1f}°C (Feels like {current['feels_like_c']:.1f}°C)")
    print(f"Humidity    : {current['humidity_pct']}%")
    print(f"Wind Speed  : {current['wind_speed_ms']:.1f} m/s")

    print("\n--- Forecast Summary ---")
    print(
        f"Temp Range: {summary['min_temp_c']}°C – {summary['max_temp_c']}°C (Avg {summary['avg_temp_c']}°C) | "
        f"Total Rain: {summary['total_rain_mm']} mm | Max Humidity: {summary['max_humidity_pct']}%"
    )

    print("\n--- Weather Alerts ---")
    for alert in alerts:
        print(f"[{alert['severity']}] {alert['message']}")

    csv_path = save_forecast_csv(current["city"], forecast_df)
    txt_path = save_alert_report(current["city"], raw_data["source"], current, summary, alerts)
    chart_path = plot_forecast_chart(current["city"], forecast_df)

    print("\n--- Generated Deliverables ---")
    print(f"Forecast CSV   : {csv_path}")
    print(f"Alert Summary  : {txt_path}")
    print(f"Forecast Chart : {chart_path}")
    print("=" * 64)


def main() -> None:
    parser = argparse.ArgumentParser(description="Weather Forecast & Alert Application")
    parser.add_argument("--city", type=str, help="City name (e.g., Pune, Mumbai, Delhi, Bengaluru)")
    parser.add_argument("--mode", type=str, choices=["sim", "api"], default=DEFAULT_MODE, help="Execution mode: 'sim' or 'api'")
    args = parser.parse_args()

    city = args.city
    if not city:
        sim_cities = ", ".join(get_available_sim_cities())
        prompt_hint = f" (Simulation cities: {sim_cities})" if args.mode == "sim" and sim_cities else ""
        city = input(f"Enter city name{prompt_hint} [default: {DEFAULT_CITY}]: ").strip() or DEFAULT_CITY

    try:
        run_pipeline(city=city, mode=args.mode)
    except Exception as exc:
        print(f"\n[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
