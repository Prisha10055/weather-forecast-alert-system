"""Rule-based weather alert evaluation engine."""

from typing import Dict, Any, List
import pandas as pd
from src.config import (
    TEMP_HIGH_THRESHOLD_C,
    HUMIDITY_HIGH_THRESHOLD_PCT,
    RAIN_THRESHOLD_MM,
    WIND_HIGH_THRESHOLD_MS,
)


def evaluate_alerts(
    current: Dict[str, Any],
    forecast_df: pd.DataFrame,
    temp_threshold: float = TEMP_HIGH_THRESHOLD_C,
    humidity_threshold: float = HUMIDITY_HIGH_THRESHOLD_PCT,
    rain_threshold: float = RAIN_THRESHOLD_MM,
    wind_threshold: float = WIND_HIGH_THRESHOLD_MS,
) -> List[Dict[str, str]]:
    """Evaluate current and forecast weather against alert thresholds."""
    alerts: List[Dict[str, str]] = []

    max_forecast_temp = float(forecast_df["temperature_c"].max()) if not forecast_df.empty else current["temperature_c"]
    max_forecast_humidity = int(forecast_df["humidity_pct"].max()) if not forecast_df.empty else current["humidity_pct"]
    total_forecast_rain = float(forecast_df["rain_3h_mm"].sum()) if not forecast_df.empty else 0.0
    max_forecast_rain_slot = float(forecast_df["rain_3h_mm"].max()) if not forecast_df.empty else 0.0
    max_forecast_wind = float(forecast_df["wind_speed_ms"].max()) if not forecast_df.empty else current["wind_speed_ms"]

    # 1. High Temperature / Heat Alert
    peak_temp = max(current["temperature_c"], max_forecast_temp)
    if peak_temp >= temp_threshold:
        severity = "CRITICAL" if peak_temp >= temp_threshold + 3.0 else "WARNING"
        alerts.append({
            "type": "HIGH_TEMPERATURE",
            "severity": severity,
            "message": f"High Temperature Alert: Peak temperature reaches {peak_temp:.1f}°C (threshold: {temp_threshold:.1f}°C). Stay hydrated and avoid peak afternoon sun.",
        })

    # 2. Rain Alert
    if current.get("rain_1h_mm", 0.0) >= rain_threshold or max_forecast_rain_slot >= rain_threshold or total_forecast_rain >= rain_threshold * 2:
        severity = "CRITICAL" if max_forecast_rain_slot >= rain_threshold * 3 else "WARNING"
        alerts.append({
            "type": "RAIN_ALERT",
            "severity": severity,
            "message": f"Rain Alert: Expected cumulative rainfall of {total_forecast_rain:.1f} mm (peak 3h slot: {max_forecast_rain_slot:.1f} mm). Carry rain gear and plan travel accordingly.",
        })

    # 3. High Humidity Alert
    peak_humidity = max(current["humidity_pct"], max_forecast_humidity)
    if peak_humidity >= humidity_threshold:
        alerts.append({
            "type": "HIGH_HUMIDITY",
            "severity": "INFO",
            "message": f"High Humidity Alert: Humidity reaches {peak_humidity}% (threshold: {humidity_threshold:.0f}%). Expect muggy conditions.",
        })

    # 4. High Wind / Storm Alert
    peak_wind = max(current["wind_speed_ms"], max_forecast_wind)
    has_thunderstorm = (
        "thunderstorm" in current.get("description", "").lower()
        or (not forecast_df.empty and forecast_df["condition"].str.lower().str.contains("thunderstorm").any())
    )
    if peak_wind >= wind_threshold or has_thunderstorm:
        alerts.append({
            "type": "STORM_WIND_ALERT",
            "severity": "CRITICAL" if has_thunderstorm else "WARNING",
            "message": f"Wind/Storm Alert: Peak wind speed {peak_wind:.1f} m/s{' with thunderstorm activity' if has_thunderstorm else ''}. Secure loose outdoor items.",
        })

    if not alerts:
        alerts.append({
            "type": "ALL_CLEAR",
            "severity": "NORMAL",
            "message": "No severe weather alerts triggered. Conditions are within normal thresholds.",
        })

    return alerts
