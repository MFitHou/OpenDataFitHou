# 🚀 OpenDataFitHou IoT Collector - Standalone Deployment

> **Deployment gọn nhẹ:** Chỉ cần 5 files để chạy hệ thống thu thập dữ liệu IoT + InfluxDB

---

## 📦 Package này bao gồm:

```
deployment/
├── README.md                    # File này
├── iot_collector.py             # Script thu thập dữ liệu
├── requirements.txt             # Python dependencies
├── docker-compose.yml           # Docker orchestration
├── Dockerfile                   # IoT collector container
└── .env.template                # Environment variables template
```

---

## 🚀 Quick Start (3 bước)

### Bước 1: Copy files lên VPS

```bash
# Trên VPS
mkdir -p ~/iot-collector
cd ~/iot-collector
```

**Upload 5 files này lên thư mục `~/iot-collector/`:**
- `iot_collector.py`
- `requirements.txt`
- `docker-compose.yml`
- `Dockerfile`
- `.env.template`

### Bước 2: Cấu hình

```bash
# Tạo file environment
cp .env.template .env

# Chỉnh sửa API keys
nano .env
```

**Điền các giá trị:**
```env
INFLUXDB_TOKEN=your_token_here           # Generate: openssl rand -base64 32
OPENWEATHER_API_KEY=your_api_key_here    # Từ openweathermap.org
INFLUXDB_ADMIN_PASSWORD=your_password    # Mật khẩu mạnh
```

### Bước 3: Khởi động

```bash
# Cài Docker nếu chưa có
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Logout và login lại

# Start services
docker compose up -d

# Xem logs
docker compose logs -f iot-collector
```

**Expected output:**
```
[INFO] [2025-12-01 10:00:00] Thu thập dữ liệu từ 10 trạm...
[INFO] [2025-12-01 10:00:05] ✅ Đã ghi 40 measurements vào InfluxDB
```

---

## 🔧 Quản lý

```bash
# Xem trạng thái
docker compose ps

# Xem logs
docker compose logs -f iot-collector
docker compose logs -f influxdb

# Restart
docker compose restart

# Stop
docker compose stop

# Xóa toàn bộ (bao gồm data!)
docker compose down -v
```

---

## 📊 Truy cập dữ liệu

### InfluxDB UI
- URL: `http://your_vps_ip:8086`
- Username: `admin`
- Password: `<INFLUXDB_ADMIN_PASSWORD từ .env>`
- Organization: `opendata_fithou`
- Bucket: `smartcity`

### Query CLI
```bash
docker exec -it influxdb influx

# Trong shell:
> use smartcity
> SELECT * FROM weather LIMIT 5
> SELECT COUNT(*) FROM traffic
> exit
```

---

## 💾 Backup

```bash
# Backup dữ liệu
docker exec influxdb influx backup /backup/backup_$(date +%Y%m%d) -b smartcity
docker cp influxdb:/backup/backup_20251201 ~/backups/

# Restore
docker cp ~/backups/backup_20251201 influxdb:/backup/
docker exec influxdb influx restore /backup/backup_20251201 --bucket smartcity
```

---

## 🔄 Cập nhật

```bash
# Stop collector
docker compose stop iot-collector

# Update file iot_collector.py (upload file mới)

# Rebuild và restart
docker compose build iot-collector
docker compose up -d iot-collector
```

---

## ⚙️ Configuration

### Thu thập dữ liệu mỗi X phút

Edit `.env`:
```env
COLLECTION_INTERVAL=600  # 10 minutes
```

Restart:
```bash
docker compose restart iot-collector
```

### Thay đổi 10 trạm thu thập

Edit `iot_collector.py`, tìm biến `STATIONS` (line ~50):
```python
STATIONS = [
    {
        "id": "station_hoan_kiem",
        "name": "Trạm Hồ Gươm",
        "location": {"lon": 105.8520, "lat": 21.0285},
        "traffic_factor": 1.5,
        "drainage_rate": 3.0
    },
    # ... thêm/sửa stations
]
```

---

## 🐛 Troubleshooting

### Collector không kết nối được InfluxDB
```bash
# Kiểm tra InfluxDB health
docker compose ps influxdb
docker compose logs influxdb

# Kiểm tra network
docker network inspect iot-collector_iot-network
```

### Không có dữ liệu trong InfluxDB
```bash
# Xem logs collector
docker compose logs iot-collector | grep ERROR

# Kiểm tra API key
docker compose exec iot-collector env | grep OPENWEATHER
```

### Out of disk space
```bash
# Check disk usage
df -h
docker system df

# Clean up
docker system prune -a
```

---

## 📈 Data Schema

### Measurements

#### 1. **weather**
```
Tags:
  - station_id
  - station_name
  - location
Fields:
  - temperature (float, °C)
  - humidity (float, %)
  - pressure (float, hPa)
  - wind_speed (float, m/s)
```

#### 2. **air_quality**
```
Tags:
  - station_id
  - station_name
  - location
Fields:
  - pm25 (float, μg/m³)
  - pm10 (float, μg/m³)
  - aqi (int, 0-500)
```

#### 3. **traffic**
```
Tags:
  - station_id
  - station_name
  - location
Fields:
  - vehicle_count (int, vehicles/hour)
  - average_speed (float, km/h)
  - congestion_level (int, 1-5)
  - noise_level (float, dB)
```

#### 4. **flood**
```
Tags:
  - station_id
  - station_name
  - location
Fields:
  - water_depth (float, cm)
  - rain_intensity (float, mm/h)
  - drainage_status (int, 1-3)
```

---

## 🌐 10 Monitoring Stations

1. **Trạm Hồ Gươm** - (105.8520°E, 21.0285°N)
2. **Trạm Mỹ Đình** - (105.7654°E, 21.0285°N)
3. **Trạm Cầu Giấy** - (105.8012°E, 21.0333°N)
4. **Trạm Đống Đa** - (105.8260°E, 21.0140°N)
5. **Trạm Thanh Xuân** - (105.8044°E, 20.9987°N)
6. **Trạm Hai Bà Trưng** - (105.8563°E, 21.0070°N)
7. **Trạm Long Biên** - (105.8897°E, 21.0368°N)
8. **Trạm Tây Hồ** - (105.8195°E, 21.0668°N)
9. **Trạm Nam Từ Liêm** - (105.7563°E, 21.0150°N)
10. **Trạm Hoàng Mai** - (105.8563°E, 20.9808°N)

---

## 📋 Requirements

### System
- **OS:** Ubuntu 20.04/22.04 hoặc bất kỳ Linux có Docker
- **RAM:** 2 GB minimum, 4 GB khuyến nghị
- **Disk:** 20 GB minimum
- **Network:** Internet connection cho API calls

### APIs
- **OpenWeatherMap API:** Free tier (60 calls/minute)
- **OpenAQ API:** Optional (có fallback simulation)

---

## 📞 Support

- **Issues:** GitHub repository
- **License:** GNU GPL v3.0
- **Author:** OpenDataFitHou Team (MFitHou)

---

**Last Updated:** December 1, 2025  
**Version:** 1.0.0 (Standalone Deployment)
