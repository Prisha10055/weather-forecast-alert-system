"""Unit tests for the Weather Forecast & Alert Application."""

import unittest
from src.weather_fetcher import fetch_weather_from_simulation
from src.weather_parser import parse_current_weather, parse_forecast_dataframe
from src.alert_engine import evaluate_alerts


class TestWeatherAlertApp(unittest.TestCase):
    def test_mumbai_triggers_rain_and_humidity_alerts(self):
        raw = fetch_weather_from_simulation("Mumbai")
        current = parse_current_weather(raw["current"])
        df = parse_forecast_dataframe(raw["forecast"])
        alerts = evaluate_alerts(current, df)
        alert_types = {a["type"] for a in alerts}
        self.assertIn("RAIN_ALERT", alert_types)
        self.assertIn("HIGH_HUMIDITY", alert_types)

    def test_delhi_triggers_high_temperature_alert(self):
        raw = fetch_weather_from_simulation("Delhi")
        current = parse_current_weather(raw["current"])
        df = parse_forecast_dataframe(raw["forecast"])
        alerts = evaluate_alerts(current, df)
        alert_types = {a["type"] for a in alerts}
        self.assertIn("HIGH_TEMPERATURE", alert_types)

    def test_bengaluru_normal_conditions(self):
        raw = fetch_weather_from_simulation("Bengaluru")
        current = parse_current_weather(raw["current"])
        df = parse_forecast_dataframe(raw["forecast"])
        alerts = evaluate_alerts(current, df)
        alert_types = {a["type"] for a in alerts}
        self.assertIn("ALL_CLEAR", alert_types)


if __name__ == "__main__":
    unittest.main()
