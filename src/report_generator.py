"""Generate CSV forecast reports and text-based alert summaries."""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
from src.config import REPORTS_DIR, OUTPUTS_DIR


def save_forecast_csv(city: str, forecast_df: pd.DataFrame, output_dir: Path = REPORTS_DIR) -> Path:
    """Save parsed forecast DataFrame to a CSV file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_city = city.strip().lower().replace(" ", "_")
    csv_path = output_dir / f"weather_report_{safe_city}.csv"
    forecast_df.to_csv(csv_path, index=False)
    return csv_path


def save_alert_report(
    city: str,
    source: str,
    current: Dict[str, Any],
    summary: Dict[str, Any],
    alerts: List[Dict[str, str]],
    output_dir: Path = OUTPUTS_DIR,
) -> Path:
    """Save a human-readable weather & alert summary report."""
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_city = city.strip().lower().replace(" ", "_")
    txt_path = output_dir / f"alert_summary_{safe_city}.txt"

    lines = [
        "=" * 60,
        f"WEATHER FORECAST & ALERT REPORT — {city.upper()}",
        f"Generated At : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Data Source  : {source}",
        "=" * 60,
        "",
        "[CURRENT WEATHER]",
        f"  Condition   : {current['condition']} ({current['description']})",
        f"  Temperature : {current['temperature_c']:.1f}°C (Feels like {current['feels_like_c']:.1f}°C)",
        f"  Humidity    : {current['humidity_pct']}%",
        f"  Wind Speed  : {current['wind_speed_ms']:.1f} m/s",
        f"  Pressure    : {current['pressure_hpa']} hPa",
        "",
        "[FORECAST SUMMARY]",
        f"  Min / Max Temp : {summary['min_temp_c']}°C / {summary['max_temp_c']}°C (Avg: {summary['avg_temp_c']}°C)",
        f"  Max Humidity   : {summary['max_humidity_pct']}%",
        f"  Total Rainfall : {summary['total_rain_mm']} mm",
        f"  Max Wind Speed : {summary['max_wind_ms']} m/s",
        "",
        "[ALERTS TRIGGERED]",
    ]

    for idx, alert in enumerate(alerts, start=1):
        lines.append(f"  {idx}. [{alert['severity']}] {alert['type']}: {alert['message']}")

    lines.append("=" * 60)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return txt_path
