"""
c25k_utils/weather.py
Handles weather integration and suggestions.
Stub: To be implemented with weather API logic.
"""

import requests


def get_weather_suggestion(location: str, workout_date: str) -> str:
    """
    Fetch a weather forecast for the given location and date using Open-Meteo (free, no API key required).
    Returns a brief, actionable suggestion string in Fahrenheit for beginners.
    """
    try:
        # Geocoding: get lat/lon from location (city or ZIP) using Open-Meteo geocoding
        geo_url = (
            f"https://geocoding-api.open-meteo.com/v1/search?name={location}"
            f"&count=1&language=en&format=json"
        )
        geo_resp = requests.get(geo_url, timeout=5)
        geo_data = geo_resp.json()
        if not geo_data.get("results"):
            return "Weather: location not found. Dress for comfort and check local conditions."
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        # Get date in YYYY-MM-DD
        date_str = workout_date[:10]
        # Weather forecast: get daily summary for that date, enforce Fahrenheit
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}"
            f"&longitude={lon}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode"
            f"&timezone=auto&start_date={date_str}&end_date={date_str}"
            f"&temperature_unit=fahrenheit"
        )
        weather_resp = requests.get(weather_url, timeout=5)
        weather = weather_resp.json().get("daily", {})
        if not weather or not weather.get("temperature_2m_max"):
            return "Weather: forecast unavailable. Check your local forecast before running."
        tmin = weather["temperature_2m_min"][0]
        tmax = weather["temperature_2m_max"][0]
        precip = weather["precipitation_sum"][0]
        code = weather["weathercode"][0]
        # Actionable suggestion logic
        temp_range = f"{tmin:.0f}-{tmax:.0f}°F"
        if tmax >= 90:
            temp_advice = "It's hot: hydrate well, wear light clothes, and consider running early or late."
        elif tmin <= 40:
            temp_advice = "It's chilly: dress in layers and warm up well."
        else:
            temp_advice = "Comfortable temperature for running."
        if precip > 2:
            rain_advice = "Heavy rain likely: consider rescheduling or wear a rain jacket."
        elif precip > 0:
            rain_advice = "Chance of showers: bring a light rain jacket just in case."
        else:
            rain_advice = "No rain expected."
        if code == 0:
            sky_advice = "Clear skies—great weather for your first run!"
        elif code in [1, 2, 3]:
            sky_advice = "Partly/cloudy skies."
        elif code in [45, 48]:
            sky_advice = "Foggy: be visible and watch your footing."
        elif 51 <= code <= 67:
            sky_advice = "Rainy: take care on slippery surfaces."
        elif 71 <= code <= 77:
            sky_advice = "Snowy: consider indoor exercise or use caution."
        else:
            sky_advice = "Variable conditions."
        return (
            f"Forecast: {temp_range}, {sky_advice} {rain_advice} {temp_advice}"
        )
    except Exception:
        return (
            "Weather: error or unavailable. Dress for comfort and check your local forecast."
        )
