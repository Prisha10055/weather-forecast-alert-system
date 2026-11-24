"""Parse raw weather JSON payloads into clean dictionaries and Pandas DataFrames."""

from typing import Dict, Any
import pandas as pd


def parse_current_weather(raw_current: Dict[str, Any]) -> Dict[str, Any]:
    """Extract key current weather metrics from raw JSON."""
    main = raw_current.get("main", {})
    wind = raw_current.get("wind", {})
    weather_list = raw_current.get("weather", [{}])
    weather = weather_list[0] if weather_list else {}
    rain = raw_current.get("rain", {})

    return {
        "city": raw_current.get("name", "Unknown"),
        "country": raw_current.get("sys", {}).get("country", ""),
        "temperature_c": float(main.get("temp", 0.0)),
        "feels_like_c": float(main.get("feels_like", 0.0)),
        "humidity_pct": int(main.get("humidity", 0)),
        "pressure_hpa": int(main.get("pressure", 0)),
        "wind_speed_ms": float(wind.get("speed", 0.0)),
        "condition": weather.get("main", "Unknown"),
        "description": weather.get("description", "Unknown").title(),
        "rain_1h_mm": float(rain.get("1h", 0.0)),
    }


def parse_forecast_dataframe(raw_forecast: Dict[str, Any]) -> pd.DataFrame:
    """Convert forecast list into a structured Pandas DataFrame."""
    rows = []
    for item in raw_forecast.get("list", []):
        main = item.get("main", {})
        wind = item.get("wind", {})
        weather_list = item.get("weather", [{}])
        weather = weather_list[0] if weather_list else {}
        rain = item.get("rain", {})

        rows.append(
            {
                "timestamp": item.get("dt_txt", ""),
                "temperature_c": float(main.get("temp", 0.0)),
                "humidity_pct": int(main.get("humidity", 0)),
                "wind_speed_ms": float(wind.get("speed", 0.0)),
                "condition": weather.get("main", "Unknown"),
                "description": weather.get("description", "Unknown").title(),
                "rain_3h_mm": float(rain.get("3h", 0.0)),
            }
        )

    df = pd.DataFrame(rows)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def summarize_forecast(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute summary statistics over the forecast window."""
    if df.empty:
        return {
            "min_temp_c": 0.0,
            "max_temp_c": 0.0,
            "avg_temp_c": 0.0,
            "max_humidity_pct": 0,
            "total_rain_mm": 0.0,
            "max_wind_ms": 0.0,
        }

    return {
        "min_temp_c": round(float(df["temperature_c"].min()), 2),
        "max_temp_c": round(float(df["temperature_c"].max()), 2),
        "avg_temp_c": round(float(df["temperature_c"].mean()), 2),
        "max_humidity_pct": int(df["humidity_pct"].max()),
        "total_rain_mm": round(float(df["rain_3h_mm"].sum()), 2),
        "max_wind_ms": round(float(df["wind_speed_ms"].max()), 2),
    }
