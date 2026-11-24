"""Configuration loader for Weather Forecast & Alert Application."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env if present
load_dotenv(BASE_DIR / ".env")

# API Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
OPENWEATHER_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Default settings
DEFAULT_MODE = os.getenv("DEFAULT_MODE", "sim")
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Pune")

# Alert Thresholds
TEMP_HIGH_THRESHOLD_C = float(os.getenv("TEMP_HIGH_THRESHOLD_C", "38.0"))
HUMIDITY_HIGH_THRESHOLD_PCT = float(os.getenv("HUMIDITY_HIGH_THRESHOLD_PCT", "80.0"))
RAIN_THRESHOLD_MM = float(os.getenv("RAIN_THRESHOLD_MM", "5.0"))
WIND_HIGH_THRESHOLD_MS = float(os.getenv("WIND_HIGH_THRESHOLD_MS", "12.0"))

# Directory paths
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"
IMAGES_DIR = BASE_DIR / "images"
REPORTS_DIR = BASE_DIR / "reports"

SAMPLE_DATA_FILE = DATA_DIR / "sample_weather_data.json"
