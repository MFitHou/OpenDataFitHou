import os
import requests
import json
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAQ_API_KEY")
BASE_URL = "https://api.openaq.org/v3/locations"


def pm25_to_aqi(pm25):
    # US EPA AQI breakpoints for PM2.5
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500),
    ]
    for c_low, c_high, aqi_low, aqi_high in breakpoints:
        if c_low <= pm25 <= c_high:
            return round((aqi_high - aqi_low) / (c_high - c_low) * (pm25 - c_low) + aqi_low)
    return None

def fetch_airquality(lat=21.0285, lon=105.8542, radius=15000):
    if not API_KEY:
        raise ValueError("OPENAQ_API_KEY not set in environment.")
    
    # 1. Lấy danh sách Locations từ v3
    params = {
        "coordinates": f"{lat},{lon}",
        "radius": radius,
        "limit": 100
    }
    headers = {"x-api-key": API_KEY}
    
    print(f"DEBUG: Fetching locations from {BASE_URL}...")
    r = requests.get(BASE_URL, params=params, headers=headers)
    r.raise_for_status()
    locations = r.json().get("results", [])
    print(f"DEBUG: Found {len(locations)} locations.")

    stations = []
    
    # 2. Với mỗi location, lấy dữ liệu từ sensors tương ứng
    for loc in locations:
        loc_name = loc.get("name", "Unknown")
        coords = loc.get("coordinates")
        
        pm25 = None
        pm10 = None
        last_updated = None
        
        sensors = loc.get("sensors", [])
        # Lọc các sensor đo PM2.5 hoặc PM10
        target_sensors = [s for s in sensors if s.get("parameter", {}).get("name") in ["pm25", "pm10"]]
        
        if not target_sensors:
            continue
            
        for sensor in target_sensors:
            sensor_id = sensor["id"]
            param_name = sensor.get("parameter", {}).get("name")
            
            # Gọi API lấy measurement mới nhất cho sensor này
            url_sensor = f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements"
            try:
                r_s = requests.get(url_sensor, params={"limit": 1}, headers=headers)
                if r_s.status_code == 200:
                    measurements = r_s.json().get("results", [])
                    if measurements:
                        latest = measurements[0]
                        val = latest.get("value")
                        # Cấu trúc timestamp có thể khác nhau, kiểm tra kỹ
                        ts = latest.get("period", {}).get("datetimeTo") 
                        if not ts: ts = latest.get("datetime")

                        if param_name == "pm25":
                            pm25 = val
                            if ts: last_updated = ts
                        elif param_name == "pm10":
                            pm10 = val
                            if not last_updated and ts: last_updated = ts
            except Exception as e:
                # print(f"DEBUG: Error fetching sensor {sensor_id}: {e}")
                pass
        
        # Chỉ thêm vào danh sách nếu có dữ liệu
        if pm25 is not None or pm10 is not None:
            stations.append({
                "location": loc_name,
                "coordinates": coords,
                "pm25": pm25,
                "pm10": pm10,
                "timestamp": last_updated,
                "aqi_pm25": pm25_to_aqi(pm25) if pm25 is not None else None
            })
            
    return stations

def save_airquality_json(data):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
    outdir = Path("data/raw/openaq")
    outdir.mkdir(parents=True, exist_ok=True)
    fname = f"{ts}_airquality.json"
    fpath = outdir / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {fpath}")

if __name__ == "__main__":
    stations = fetch_airquality()
    if stations:
        save_airquality_json(stations)
    else:
        print("No air quality data found.")
