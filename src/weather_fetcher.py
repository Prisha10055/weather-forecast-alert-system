"""Fetch weather data from OpenWeatherMap API or local simulation dataset."""

import json
import requests
from typing import Dict, Any, List
from src.config import (
    OPENWEATHER_API_KEY,
    OPENWEATHER_CURRENT_URL,
    OPENWEATHER_FORECAST_URL,
    SAMPLE_DATA_FILE,
)


def get_available_sim_cities() -> List[str]:
    """Return the list of cities available in the local simulation dataset."""
    if not SAMPLE_DATA_FILE.exists():
        return []
    with open(SAMPLE_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return list(data.keys())


def fetch_weather_from_api(city: str) -> Dict[str, Any]:
    """Fetch live current weather and 5-day/3-hour forecast from OpenWeatherMap."""
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "your_openweathermap_api_key_here":
        raise ValueError(
            "Missing valid OPENWEATHER_API_KEY. Set it in your .env file or run in simulation mode (--mode sim)."
        )

    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}

    current_resp = requests.get(OPENWEATHER_CURRENT_URL, params=params, timeout=10)
    if current_resp.status_code == 404:
        raise ValueError(f"City '{city}' not found by OpenWeatherMap API.")
    current_resp.raise_for_status()

    forecast_resp = requests.get(OPENWEATHER_FORECAST_URL, params=params, timeout=10)
    forecast_resp.raise_for_status()

    return {
        "source": "OpenWeatherMap Live API",
        "current": current_resp.json(),
        "forecast": forecast_resp.json(),
    }


def fetch_weather_from_simulation(city: str) -> Dict[str, Any]:
    """Load weather data for the requested city from the local JSON simulation file."""
    if not SAMPLE_DATA_FILE.exists():
        raise FileNotFoundError(f"Simulation dataset not found at {SAMPLE_DATA_FILE}")

    with open(SAMPLE_DATA_FILE, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # Case-insensitive lookup
    matched_key = next((k for k in dataset.keys() if k.lower() == city.strip().lower()), None)
    if not matched_key:
        available = ", ".join(dataset.keys())
        raise ValueError(
            f"City '{city}' is not in the simulation dataset. Available cities: {available}"
        )

    city_data = dataset[matched_key]
    return {
        "source": "Virtual Simulation (Offline JSON)",
        "current": city_data["current"],
        "forecast": city_data["forecast"],
    }


def fetch_weather(city: str, mode: str = "sim") -> Dict[str, Any]:
    """Unified entry point to fetch weather data in either 'api' or 'sim' mode."""
    mode = mode.lower().strip()
    if mode == "api":
        return fetch_weather_from_api(city)
    elif mode == "sim":
        return fetch_weather_from_simulation(city)
    else:
        raise ValueError(f"Unsupported mode '{mode}'. Use 'api' or 'sim'.")
