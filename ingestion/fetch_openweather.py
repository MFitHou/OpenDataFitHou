import os
import requests
import json
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_current_weather(city="Hanoi,VN"):
    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY not set in environment.")
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    data = r.json()
    ts = datetime.utcfromtimestamp(data["dt"]).replace(tzinfo=timezone.utc).isoformat()
    result = {
        "timestamp": ts,
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "weather": data["weather"][0]["description"],
        "raw": data
    }
    return result


def save_weather_json(weather_data):
    ts = weather_data["timestamp"].replace(":", "-")
    outdir = Path("data/raw/openweather")
    outdir.mkdir(parents=True, exist_ok=True)
    fname = f"{ts}_weather.json"
    fpath = outdir / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(weather_data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {fpath}")


if __name__ == "__main__":
    city = os.getenv("OPENWEATHER_CITY", "Hanoi,VN")
    weather = fetch_current_weather(city)
    save_weather_json(weather)
