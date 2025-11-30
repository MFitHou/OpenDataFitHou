# -*- coding: utf-8 -*-
"""
@File    : iot_collector.py
@Project : OpenDataFitHou
@Date    : 2025-11-30 18:00:00
@Author  : MFitHou Team

Part of OpenDataFitHou - Ứng dụng dữ liệu mở liên kết phục vụ chuyển đổi số

Mô-đun thu thập dữ liệu Smart City từ các nguồn khác nhau (thời tiết, chất lượng
không khí, giao thông, ngập lụt) và lưu trữ vào InfluxDB.

Copyright (C) 2025 FITHOU

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

# Standard library imports
import json
import math
import os
import random
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

# Third-party imports
import requests
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

# Local imports
# (Sẽ được thêm khi cần thiết)

# ============================================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================================

# Load .env file trước khi đọc environment variables
load_dotenv()

# Debug: Kiểm tra xem các API keys đã được load chưa
print("🔑 Checking API Keys...")
if os.getenv("OPENWEATHER_API_KEY"):
    print("   ✅ OPENWEATHER_API_KEY: Key Found")
else:
    print("   ❌ OPENWEATHER_API_KEY: Key Missing")

if os.getenv("OPENAQ_API_KEY"):
    print("   ✅ OPENAQ_API_KEY: Key Found")
else:
    print("   ⚠️  OPENAQ_API_KEY: Key Missing (optional)")


# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

# InfluxDB Configuration (từ docker-compose.yml hoặc environment variables)
INFLUX_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUXDB_TOKEN", "opendata_fithou_token_secret")
INFLUX_ORG = os.getenv("INFLUXDB_ORG", "opendata_fithou")
INFLUX_BUCKET = os.getenv("INFLUXDB_BUCKET", "smartcity")  # Chứa: weather, air_quality, traffic, noise, flood, parking

# OpenWeatherMap API Configuration
OWM_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# OpenAQ API v3 Configuration (cần API key)
OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY", "")
OPENAQ_API_URL = "https://api.openaq.org/v3/locations"
OPENAQ_PARAMETERS = ["pm25", "pm10", "o3", "no2", "so2", "co"]  # Các thông số chất lượng không khí

# Weather Stations - Các trạm quan trắc thời tiết tại Hà Nội với đặc tính riêng
STATIONS = [
    # CENTER & HIGH TRAFFIC
    {"id": "urn:ngsi-ld:Device:Hanoi:station:Lang", "name": "Trạm Láng", "lat": 21.017, "lon": 105.800, "traffic_factor": 1.2, "drainage_rate": 2.0},  # Floods easily
    {"id": "urn:ngsi-ld:Device:Hanoi:station:CauGiay", "name": "Trạm Cầu Giấy", "lat": 21.033, "lon": 105.800, "traffic_factor": 1.4, "drainage_rate": 3.0},  # Very congested
    {"id": "urn:ngsi-ld:Device:Hanoi:station:RoyalCity", "name": "Trạm Ngã Tư Sở", "lat": 21.003, "lon": 105.813, "traffic_factor": 1.5, "drainage_rate": 1.5},  # Extreme traffic & flood
    {"id": "urn:ngsi-ld:Device:Hanoi:station:HoGuom", "name": "Trạm Hồ Gươm", "lat": 21.028, "lon": 105.852, "traffic_factor": 1.1, "drainage_rate": 6.0},  # Center
    {"id": "urn:ngsi-ld:Device:Hanoi:station:TimeCity", "name": "Trạm Minh Khai", "lat": 20.995, "lon": 105.868, "traffic_factor": 1.3, "drainage_rate": 4.0},
    # SUBURBAN & OPEN SPACE
    {"id": "urn:ngsi-ld:Device:Hanoi:station:HaDong", "name": "Trạm Hà Đông", "lat": 20.971, "lon": 105.776, "traffic_factor": 1.0, "drainage_rate": 5.0},
    {"id": "urn:ngsi-ld:Device:Hanoi:station:LongBien", "name": "Trạm Long Biên", "lat": 21.036, "lon": 105.894, "traffic_factor": 0.8, "drainage_rate": 9.0},  # Good drainage
    {"id": "urn:ngsi-ld:Device:Hanoi:station:MyDinh", "name": "Trạm Mỹ Đình", "lat": 21.020, "lon": 105.763, "traffic_factor": 0.9, "drainage_rate": 6.0},
    {"id": "urn:ngsi-ld:Device:Hanoi:station:TayHo", "name": "Trạm Tây Hồ", "lat": 21.070, "lon": 105.823, "traffic_factor": 0.7, "drainage_rate": 8.0},  # Good air
    {"id": "urn:ngsi-ld:Device:Hanoi:station:HoangMai", "name": "Trạm Hoàng Mai", "lat": 20.963, "lon": 105.843, "traffic_factor": 1.2, "drainage_rate": 3.0},
]

# Persistent Flood State - Theo dõi mực nước ngập tại mỗi trạm
STATION_FLOOD_STATES = {station["id"]: 0.0 for station in STATIONS}

# Parking Lots - Bãi đỗ xe thông minh
PARKING_LOTS = [
    {
        "id": "urn:ngsi-ld:ParkingLot:hanoi-parking-01",
        "capacity": 150
    },
    {
        "id": "urn:ngsi-ld:ParkingLot:hanoi-parking-02",
        "capacity": 200
    },
    {
        "id": "urn:ngsi-ld:ParkingLot:hanoi-parking-03",
        "capacity": 100
    },
    {
        "id": "urn:ngsi-ld:ParkingLot:hanoi-parking-04",
        "capacity": 250
    }
]

# API Endpoints
OWM_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
OWM_AIR_POLLUTION_URL = "https://api.openweathermap.org/data/2.5/air_pollution"

# Timeouts & Retries
API_TIMEOUT = 30
MAX_RETRIES = 3


# ============================================================================
# PLACEHOLDER FUNCTIONS
# ============================================================================

def get_weather(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """
    Lấy dữ liệu thời tiết từ OpenWeatherMap API.
    
    Args:
        lat: Vĩ độ
        lon: Kinh độ
        
    Returns:
        Dictionary chứa dữ liệu thời tiết hoặc None nếu thất bại
        Format: {
            'temperature': float,  # Nhiệt độ (°C)
            'humidity': int,       # Độ ẩm (%)
            'wind_speed': float,   # Tốc độ gió (m/s)
            'rain_1h': float       # Lượng mưa 1h (mm)
        }
    """
    if not OWM_API_KEY or OWM_API_KEY == "your-openweathermap-api-key-here":
        print("❌ Thiếu OPENWEATHER_API_KEY trong file .env")
        return None
    
    try:
        # Gọi OpenWeatherMap API
        params = {
            'lat': lat,
            'lon': lon,
            'appid': OWM_API_KEY,
            'units': 'metric'  # Celsius, m/s
        }
        
        response = requests.get(
            OWM_WEATHER_URL,
            params=params,
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Extract dữ liệu thời tiết
        main_data = data.get('main', {})
        wind_data = data.get('wind', {})
        rain_data = data.get('rain', {})  # rain key có thể không tồn tại
        
        result = {
            'temperature': main_data.get('temp', 0.0),
            'humidity': main_data.get('humidity', 0),
            'wind_speed': wind_data.get('speed', 0.0),
            'rain_1h': rain_data.get('1h', 0.0)  # Handle missing rain key -> default 0.0
        }
        
        print(f"✅ Lấy dữ liệu thời tiết: {result['temperature']}°C, {result['humidity']}%, gió {result['wind_speed']}m/s")
        return result
        
    except requests.Timeout:
        print(f"⏱️  Timeout khi gọi OpenWeatherMap API cho ({lat}, {lon})")
        return None
    except requests.RequestException as e:
        print(f"❌ Lỗi khi lấy dữ liệu thời tiết: {e}")
        return None
    except Exception as e:
        print(f"❌ Lỗi không xác định khi lấy thời tiết: {e}")
        return None


def get_air_quality(lat: float, lon: float, radius: int = 25000) -> Dict[str, Any]:
    """
    Lấy dữ liệu chất lượng không khí từ OpenAQ API V3.
    
    OpenAQ là nền tảng dữ liệu mở về chất lượng không khí toàn cầu,
    cung cấp dữ liệu thời gian thực từ các trạm quan trắc chính phủ và tổ chức.
    
    FALLBACK: Nếu OpenAQ không có dữ liệu (coverage thưa), sẽ mô phỏng dữ liệu.
    
    Args:
        lat: Vĩ độ
        lon: Kinh độ
        radius: Bán kính tìm kiếm (mét), mặc định 25km (max allowed)
        
    Returns:
        Dictionary chứa dữ liệu chất lượng không khí (luôn trả về, không bao giờ None)
        Format: {
            'pm25': float,  # PM2.5 (µg/m³)
            'pm10': float,  # PM10 (µg/m³)
            'aqi': int      # Air Quality Index
        }
    """
    # Case A: Thử lấy dữ liệu thật từ OpenAQ API V3
    if OPENAQ_API_KEY:
        try:
            # Gọi OpenAQ API V3 /locations endpoint
            openaq_v3_url = "https://api.openaq.org/v3/locations"
            
            params = {
                'coordinates': f'{lat},{lon}',
                'radius': min(radius, 25000),  # Max 25km theo API limit
                'limit': 1
            }
            
            headers = {
                'X-API-Key': OPENAQ_API_KEY
            }
            
            response = requests.get(
                openaq_v3_url,
                params=params,
                headers=headers,
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            
            # API V3 trả về format: {"meta": {...}, "results": [...]}
            if data.get('results') and len(data['results']) > 0:
                location = data['results'][0]
                
                # V3: parameters array chứa latest measurements
                parameters = location.get('parameters', [])
                
                # Parse parameters để tìm pm25 và pm10
                pm25_value = None
                pm10_value = None
                
                for param in parameters:
                    param_id = param.get('id')
                    param_name = param.get('name', '').lower()
                    latest = param.get('latest', {})
                    value = latest.get('value')
                    
                    # Match PM2.5
                    if value is not None and (param_id == 2 or 'pm25' in param_name or 'pm2.5' in param_name):
                        pm25_value = value
                    # Match PM10
                    elif value is not None and (param_id == 1 or 'pm10' in param_name):
                        pm10_value = value
                
                # Nếu có ít nhất PM2.5, tính AQI và trả về
                if pm25_value is not None:
                    pm25 = pm25_value
                    pm10 = pm10_value if pm10_value is not None else 0
                    aqi = calculate_vn_aqi(pm25)
                    
                    result = {
                        'pm25': pm25,
                        'pm10': pm10,
                        'aqi': aqi
                    }
                    
                    location_name = location.get('name', 'Unknown')
                    distance_km = location.get('distance', 0) / 1000 if location.get('distance') else 0
                    print(f"✅ Dữ liệu OpenAQ V3 từ {location_name} ({distance_km:.1f}km): PM2.5={pm25:.1f}, PM10={pm10:.1f}, AQI={aqi}")
                    return result
                    
        except requests.Timeout:
            print(f"⏱️  Timeout khi gọi OpenAQ API V3 cho ({lat}, {lon})")
        except requests.RequestException as e:
            print(f"⚠️  Lỗi OpenAQ API V3: {e}")
        except Exception as e:
            print(f"⚠️  Lỗi không xác định khi gọi OpenAQ V3: {e}")
    
    # Case B: FALLBACK - Mô phỏng dữ liệu (OpenAQ coverage thưa)
    print(f"⚠️  OpenAQ missing data for ({lat}, {lon}), using simulated data.")
    
    # Generate dữ liệu mô phỏng ở mức Moderate (20-60 µg/m³)
    pm25_simulated = random.uniform(20, 60)
    pm10_simulated = random.uniform(40, 80)
    aqi_simulated = calculate_vn_aqi(pm25_simulated)
    
    result = {
        'pm25': round(pm25_simulated, 1),
        'pm10': round(pm10_simulated, 1),
        'aqi': aqi_simulated
    }
    
    print(f"🔄 Dữ liệu mô phỏng: PM2.5={result['pm25']}, PM10={result['pm10']}, AQI={result['aqi']}")
    return result


def calculate_vn_aqi(pm25_conc: float) -> int:
    """
    Tính Air Quality Index (AQI) từ nồng độ PM2.5 theo chuẩn Vietnam/US EPA.
    
    AQI Categories:
    - 0-50: Good (Tốt)
    - 51-100: Moderate (Trung bình)
    - 101-150: Unhealthy for Sensitive Groups (Không tốt cho nhóm nhạy cảm)
    - 151-200: Unhealthy (Không tốt cho sức khỏe)
    - 200+: Very Unhealthy (Rất xấu)
    
    Args:
        pm25_conc: Nồng độ PM2.5 (µg/m³)
        
    Returns:
        Air Quality Index (0-200+)
    """
    if pm25_conc is None or pm25_conc < 0:
        return 0
    
    # Breakpoints theo Vietnam/US EPA simplified standard
    breakpoints = [
        (0.0, 12.0, 0, 50),        # Good
        (12.0, 35.4, 51, 100),     # Moderate
        (35.5, 55.4, 101, 150),    # Unhealthy for Sensitive
        (55.5, 150.4, 151, 200),   # Unhealthy
    ]
    
    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= pm25_conc <= c_high:
            # AQI formula: I = ((I_high - I_low) / (C_high - C_low)) * (C - C_low) + I_low
            aqi = ((i_high - i_low) / (c_high - c_low)) * (pm25_conc - c_low) + i_low
            return int(round(aqi))
    
    # Nếu vượt quá 150.5, trả về 200+ (Very Unhealthy)
    if pm25_conc > 150.5:
        return 200 + int((pm25_conc - 150.5) / 2)  # Scale progressively
    
    return 200


def simulate_traffic_flow(current_hour: int, traffic_factor: float = 1.0) -> tuple[int, int]:
    """
    Mô phỏng lưu lượng giao thông dựa trên giờ trong ngày và đặc điểm địa điểm.
    
    Args:
        current_hour: Giờ hiện tại (0-23)
        traffic_factor: Hệ số giao thông theo địa điểm (0.7-1.5)
                       - >1.2: Khu vực trung tâm đông đúc
                       - ~1.0: Khu vực bình thường
                       - <0.9: Khu vực ngoại ô thông thoáng
        
    Returns:
        Tuple (intensity, avg_speed):
        - intensity: Cường độ giao thông (0-100)
        - avg_speed: Tốc độ trung bình (km/h)
    """
    # Tính base intensity theo thời gian trong ngày
    base_intensity = 0
    
    # Rush Hour - Giờ cao điểm (7-8h, 17-18h)
    if current_hour in [7, 8, 17, 18]:
        base_intensity = random.randint(70, 80)
    
    # Busy Day - Giờ làm việc (9-16h)
    elif 9 <= current_hour <= 16:
        base_intensity = random.randint(40, 50)
    
    # Evening - Buổi tối (19-22h)
    elif 19 <= current_hour <= 22:
        base_intensity = random.randint(30, 40)
    
    # Night - Ban đêm (23-5h)
    else:
        base_intensity = random.randint(5, 10)
    
    # Áp dụng location adjustment với traffic_factor
    final_intensity = int(base_intensity * traffic_factor)
    
    # Đảm bảo intensity không vượt quá 100
    final_intensity = min(100, final_intensity)
    
    # Tính speed nghịch đảo với intensity (càng đông càng chậm)
    # Formula: speed = max(5, 60 - (intensity * 0.6))
    avg_speed = max(5, int(60 - (final_intensity * 0.6)))
    
    return (final_intensity, avg_speed)


def simulate_noise_level(traffic_intensity: int) -> float:
    """
    Mô phỏng mức độ tiếng ồn dựa trên cường độ giao thông.
    
    Args:
        traffic_intensity: Cường độ giao thông (0-100)
        
    Returns:
        Mức độ tiếng ồn (dB), làm tròn 1 chữ số thập phân
    """
    # Base noise level: 45 dB (môi trường yên tĩnh)
    base_noise = 45.0
    
    # Traffic contribution: 0.4 dB per traffic intensity unit
    traffic_contribution = traffic_intensity * 0.4
    
    # Random fluctuation: -2 đến +2 dB
    random_fluctuation = random.uniform(-2.0, 2.0)
    
    # Tính toán tổng mức độ tiếng ồn
    noise_level = base_noise + traffic_contribution + random_fluctuation
    
    # Làm tròn đến 1 chữ số thập phân
    return round(noise_level, 1)


def simulate_flood_depth(rain_1h: float, current_level: float, drainage_rate: float = 5.0) -> float:
    """
    Mô phỏng độ sâu ngập lụt dựa trên lượng mưa, mực nước hiện tại và khả năng thoát nước.
    
    Args:
        rain_1h: Lượng mưa trong 1 giờ (mm)
        current_level: Mực nước hiện tại (cm)
        drainage_rate: Tốc độ thoát nước (cm/cycle)
                      - 1.5-3.0: Khu vực thoát nước kém (trung tâm đô thị)
                      - 5.0-6.0: Thoát nước trung bình
                      - 8.0-9.0: Thoát nước tốt (ngoại ô, gần sông)
        
    Returns:
        Mực nước mới (cm)
    """
    # Inflow - Nước tích tụ từ mưa
    water_in = 0.0
    if rain_1h > 0:
        water_in = rain_1h * 0.5  # 1mm mưa → 0.5cm nước tích tụ
    
    # Outflow - Hệ thống thoát nước luôn hoạt động
    water_out = drainage_rate
    
    # Net Change - Thay đổi mực nước
    new_level = current_level + water_in - water_out
    
    # Đảm bảo boundary: 0 <= new_level <= 100
    new_level = max(0.0, min(100.0, new_level))
    
    return new_level


def simulate_traffic(station_id: str, traffic_factor: float = 1.0) -> Dict[str, Any]:
    """
    Mô phỏng dữ liệu giao thông cho trạm quan trắc.
    
    Args:
        station_id: ID của trạm quan trắc
        traffic_factor: Hệ số giao thông theo địa điểm
        
    Returns:
        Dictionary chứa dữ liệu giao thông mô phỏng
    """
    current_hour = datetime.now().hour
    
    # Sử dụng hàm mô phỏng chi tiết
    intensity, avg_speed = simulate_traffic_flow(current_hour, traffic_factor)
    noise_level = simulate_noise_level(intensity)
    
    return {
        "station_id": station_id,
        "intensity": intensity,
        "avg_speed": avg_speed,
        "noise_level": noise_level,
        "timestamp": datetime.now().isoformat()
    }


def simulate_flood(station_id: str, lat: float, lon: float, drainage_rate: float = 5.0) -> Dict[str, Any]:
    """
    Mô phỏng dữ liệu ngập lụt dựa trên vị trí và thời tiết.
    
    Args:
        station_id: ID của trạm quan trắc
        lat: Vĩ độ
        lon: Kinh độ
        drainage_rate: Tốc độ thoát nước (cm/cycle)
        
    Returns:
        Dictionary chứa dữ liệu ngập lụt mô phỏng
    """
    # Lấy dữ liệu thời tiết thực tế
    weather = get_weather(lat, lon)
    
    if weather:
        rain_1h = weather.get('rain_1h', 0.0)
    else:
        # Fallback nếu không lấy được dữ liệu thời tiết
        rain_1h = random.uniform(0, 2)
    
    # Lấy mực nước hiện tại từ persistent state
    current_level = STATION_FLOOD_STATES.get(station_id, 0.0)
    
    # Tính mực nước mới
    new_level = simulate_flood_depth(rain_1h, current_level, drainage_rate)
    
    # Cập nhật state
    STATION_FLOOD_STATES[station_id] = new_level
    
    # Xác định cảnh báo
    risk_level = "Low"
    if new_level > 50:
        risk_level = "Critical"
    elif new_level > 30:
        risk_level = "High"
    elif new_level > 10:
        risk_level = "Moderate"
    
    return {
        "station_id": station_id,
        "water_level": round(new_level, 2),
        "rain_1h": rain_1h,
        "risk_level": risk_level,
        "timestamp": datetime.now().isoformat()
    }


def write_to_influx(
    measurement: str, 
    tags: Dict[str, str], 
    fields: Dict[str, Any]
) -> bool:
    """
    Ghi dữ liệu vào InfluxDB.
    
    Args:
        measurement: Tên measurement trong InfluxDB (weather, air_quality, traffic, flood, etc.)
        tags: Dictionary chứa các tags (station_id, location, etc.)
        fields: Dictionary chứa các fields (giá trị đo)
        
    Returns:
        True nếu ghi thành công, False nếu thất bại
    """
    try:
        # Tạo InfluxDB client
        client = InfluxDBClient(
            url=INFLUX_URL,
            token=INFLUX_TOKEN,
            org=INFLUX_ORG
        )
        
        # Tạo write API với SYNCHRONOUS mode
        write_api = client.write_api(write_options=SYNCHRONOUS)
        
        # Tạo Point với measurement, tags và fields
        point = Point(measurement)
        
        # Thêm tags
        for tag_key, tag_value in tags.items():
            point = point.tag(tag_key, tag_value)
        
        # Thêm fields
        for field_key, field_value in fields.items():
            point = point.field(field_key, field_value)
        
        # Ghi vào InfluxDB
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        
        # Đóng client
        client.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi ghi vào InfluxDB: {e}")
        return False


def collect_and_store_data():
    """
    Thu thập dữ liệu từ tất cả các trạm và lưu vào InfluxDB.
    
    Workflow:
    1. Lặp qua tất cả các trạm quan trắc
    2. Thu thập dữ liệu thời tiết, chất lượng không khí
    3. Mô phỏng dữ liệu giao thông, tiếng ồn, ngập lụt
    4. Ghi tất cả vào InfluxDB
    """
    print(f"\n{'='*80}")
    print(f"🔄 DATA COLLECTION CYCLE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")
    
    success_count = 0
    error_count = 0
    
    for idx, station in enumerate(STATIONS, 1):
        station_id = station['id']
        station_name = station['name']
        lat = station['lat']
        lon = station['lon']
        traffic_factor = station['traffic_factor']
        drainage_rate = station['drainage_rate']
        
        print(f"\n📍 [{idx}/{len(STATIONS)}] {station_name}")
        
        try:
            # 1. Thu thập dữ liệu thời tiết
            weather = get_weather(lat, lon)
            if weather:
                weather_success = write_to_influx(
                    measurement="weather",
                    tags={
                        "station_id": station_id,
                        "station_name": station_name,
                        "location": f"{lat},{lon}"
                    },
                    fields={
                        "temperature": float(weather['temperature']),
                        "humidity": float(weather['humidity']),
                        "wind_speed": float(weather['wind_speed']),
                        "rain_1h": float(weather['rain_1h'])
                    }
                )
                if weather_success:
                    print(f"   ✅ Weather: {weather['temperature']}°C, {weather['humidity']}%, Rain: {weather['rain_1h']}mm")
                    success_count += 1
                else:
                    print(f"   ❌ Weather: Failed to write to InfluxDB")
                    error_count += 1
            
            # 2. Thu thập dữ liệu chất lượng không khí
            air_quality = get_air_quality(lat, lon)
            if air_quality:
                aq_success = write_to_influx(
                    measurement="air_quality",
                    tags={
                        "station_id": station_id,
                        "station_name": station_name,
                        "location": f"{lat},{lon}"
                    },
                    fields={
                        "pm25": float(air_quality['pm25']),
                        "pm10": float(air_quality['pm10']),
                        "aqi": int(air_quality['aqi'])
                    }
                )
                if aq_success:
                    print(f"   ✅ Air Quality: PM2.5={air_quality['pm25']:.1f}, AQI={air_quality['aqi']}")
                    success_count += 1
                else:
                    print(f"   ❌ Air Quality: Failed to write to InfluxDB")
                    error_count += 1
            
            # 3. Mô phỏng dữ liệu giao thông
            traffic = simulate_traffic(station_id, traffic_factor)
            traffic_success = write_to_influx(
                measurement="traffic",
                tags={
                    "station_id": station_id,
                    "station_name": station_name,
                    "location": f"{lat},{lon}"
                },
                fields={
                    "intensity": int(traffic['intensity']),
                    "avg_speed": int(traffic['avg_speed']),
                    "noise_level": float(traffic['noise_level'])
                }
            )
            if traffic_success:
                print(f"   ✅ Traffic: Intensity={traffic['intensity']}, Speed={traffic['avg_speed']}km/h, Noise={traffic['noise_level']}dB")
                success_count += 1
            else:
                print(f"   ❌ Traffic: Failed to write to InfluxDB")
                error_count += 1
            
            # 4. Mô phỏng dữ liệu ngập lụt
            flood = simulate_flood(station_id, lat, lon, drainage_rate)
            flood_success = write_to_influx(
                measurement="flood",
                tags={
                    "station_id": station_id,
                    "station_name": station_name,
                    "location": f"{lat},{lon}",
                    "risk_level": flood['risk_level']
                },
                fields={
                    "water_level": float(flood['water_level']),
                    "rain_1h": float(flood['rain_1h'])
                }
            )
            if flood_success:
                print(f"   ✅ Flood: Level={flood['water_level']}cm, Risk={flood['risk_level']}")
                success_count += 1
            else:
                print(f"   ❌ Flood: Failed to write to InfluxDB")
                error_count += 1
                
        except Exception as e:
            print(f"   ❌ Error processing station: {e}")
            error_count += 1
    
    print(f"\n{'='*80}")
    print(f"✅ Collection Complete: {success_count} successful, {error_count} errors")
    print(f"{'='*80}\n")
    
    return success_count, error_count


def test_functions():
    """Test các hàm đã implement."""
    print("\n" + "=" * 60)
    print("🧪 TESTING DATA COLLECTION FUNCTIONS")
    print("=" * 60)
    
    # Test với trạm đầu tiên
    station = STATIONS[0]
    print(f"\n📍 Testing với {station['name']} ({station['lat']}, {station['lon']})")
    
    # Test 1: calculate_vn_aqi
    print("\n1️⃣  Test calculate_vn_aqi():")
    test_pm25_values = [5, 20, 40, 60, 100, 160]
    for pm25 in test_pm25_values:
        aqi = calculate_vn_aqi(pm25)
        print(f"   PM2.5={pm25:>6.1f} µg/m³ → AQI={aqi:>3d}")
    
    # Test 2: get_weather
    print(f"\n2️⃣  Test get_weather():")
    weather = get_weather(station['lat'], station['lon'])
    if weather:
        print(f"   ✅ Nhiệt độ: {weather['temperature']}°C")
        print(f"   ✅ Độ ẩm: {weather['humidity']}%")
        print(f"   ✅ Tốc độ gió: {weather['wind_speed']} m/s")
        print(f"   ✅ Lượng mưa 1h: {weather['rain_1h']} mm")
    else:
        print("   ❌ Không lấy được dữ liệu thời tiết")
    
    # Test 3: get_air_quality
    print(f"\n3️⃣  Test get_air_quality():")
    air_quality = get_air_quality(station['lat'], station['lon'])
    print(f"   ✅ PM2.5: {air_quality['pm25']} µg/m³")
    print(f"   ✅ PM10: {air_quality['pm10']} µg/m³")
    print(f"   ✅ AQI: {air_quality['aqi']}")
    
    # Test tất cả các trạm
    print(f"\n4️⃣  Test với tất cả {len(STATIONS)} trạm:")
    for idx, st in enumerate(STATIONS, 1):
        print(f"\n   Trạm {idx}: {st['name']}")
        aq = get_air_quality(st['lat'], st['lon'])
        print(f"      → PM2.5={aq['pm25']:.1f}, AQI={aq['aqi']}")
    
    print("\n" + "=" * 60)
    print("✅ TESTING COMPLETED")
    print("=" * 60 + "\n")


def main():
    """
    Entry point của script.
    
    Chế độ hoạt động:
    - Continuous mode với interval từ environment variable
    - Nếu không có COLLECTION_INTERVAL, mặc định 300s (5 phút)
    """
    print("\n" + "=" * 80)
    print("🚀 IoT Data Collector - OpenDataFitHou")
    print("=" * 80)
    print(f"Số lượng trạm quan trắc: {len(STATIONS)}")
    print(f"Số lượng bãi đỗ xe: {len(PARKING_LOTS)}")
    print("\nCấu hình InfluxDB:")
    print(f"  URL: {INFLUX_URL}")
    print(f"  Org: {INFLUX_ORG}")
    print(f"  Bucket: {INFLUX_BUCKET}")
    print("=" * 80)
    
    # Lấy interval từ environment variable
    interval = int(os.getenv("COLLECTION_INTERVAL", "300"))
    if interval < 10:
        print("⚠️  Interval tối thiểu là 10 giây. Sử dụng 10s.")
        interval = 10
    
    print(f"\n♾️  Running CONTINUOUS MODE (every {interval}s)...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            collect_and_store_data()
            print(f"⏳ Waiting {interval} seconds until next collection...\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopped by user. Exiting...\n")


if __name__ == "__main__":
    main()
