"""
c25k_utils/weather.py
Handles weather integration and suggestions.
Stub: To be implemented with weather API logic.
"""

import requests


def get_weather_suggestion(location: str, workout_date: str) -> str:
    """
    Fetch a simple weather forecast for the given location and date using Open-Meteo (free, no API key required).
    Returns a brief suggestion string in Fahrenheit.
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
            return "Weather: location not found."
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        # Get date in YYYY-MM-DD
        date_str = workout_date[:10]
        # Weather forecast: get daily summary for that date, enforce Fahrenheit
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}"
            f"&longitude={lon}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
            f"weathercode"
            f"&timezone=auto&start_date={date_str}&end_date={date_str}"
            f"&temperature_unit=fahrenheit"
        )
        weather_resp = requests.get(weather_url, timeout=5)
        weather = weather_resp.json().get("daily", {})
        if not weather or not weather.get("temperature_2m_max"):
            return "Weather: forecast unavailable."
        tmin = weather["temperature_2m_min"][0]
        tmax = weather["temperature_2m_max"][0]
        precip = weather["precipitation_sum"][0]
        code = weather["weathercode"][0]
        # Simple interpretation
        desc = f"{tmin:.0f}-{tmax:.0f}°F, "
        if precip > 2:
            desc += "rain likely, "
        elif precip > 0:
            desc += "chance of showers, "
        # Weather code: 0=clear, 1-3=partly/cloudy, 45/48=fog,
        # 51+=rain, 71+=snow
        if code == 0:
            desc += "clear skies."
        elif code in [1, 2, 3]:
            desc += "partly/cloudy."
        elif code in [45, 48]:
            desc += "foggy."
        elif 51 <= code <= 67:
            desc += "rainy."
        elif 71 <= code <= 77:
            desc += "snowy."
        else:
            desc += "variable."
        return f"Forecast: {desc}"
    except Exception as e:
        return f"Weather: error or unavailable. ({e})"
