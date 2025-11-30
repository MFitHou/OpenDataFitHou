# Quick Start Guide

Hướng dẫn nhanh để bắt đầu với OpenDataFitHou.

## Cài đặt nhanh

### 1. Clone repository
```bash
git clone https://github.com/MFitHou/OpenDataFitHou.git
cd OpenDataFitHou
```

### 2. Tạo môi trường ảo
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

## Sử dụng cơ bản

### Thu thập dữ liệu từ OpenStreetMap

```python
from src.fetchers.osm_data_fetcher import OSMDataFetcher

# Khởi tạo fetcher
fetcher = OSMDataFetcher()

# Thu thập dữ liệu ATM ở Hà Nội
atm_data = fetcher.fetch_amenity("atm", "Hanoi")

# Lưu vào file
fetcher.save_to_geojson(atm_data, "data/atm.geojson")
```

### Xử lý dữ liệu batch

```python
from src.processors.batch_processor import BatchProcessor

# Khởi tạo processor
processor = BatchProcessor()

# Xử lý tất cả file GeoJSON
processor.process_all("data/", "data/opendata_hanoi/")
```

### Chạy Jupyter Notebooks

```bash
# Khởi động Jupyter
jupyter notebook

# Mở notebooks/OverpassApi.ipynb để xem ví dụ
```

## Chạy với Docker

```bash
# Build image
docker-compose build

# Khởi động services
docker-compose up -d
```

## Cấu trúc dữ liệu

### Input: GeoJSON
Dữ liệu đầu vào từ OpenStreetMap ở định dạng GeoJSON:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [105.8342, 21.0278]
      },
      "properties": {
        "name": "ATM Vietcombank",
        "amenity": "atm"
      }
    }
  ]
}
```

### Output: RDF/Turtle
Dữ liệu đầu ra ở định dạng RDF Turtle:
```turtle
@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .
@prefix odh: <http://opendatahanoi.org/ontology#> .

odh:atm_001 a odh:ATM ;
    odh:name "ATM Vietcombank" ;
    geo:lat "21.0278" ;
    geo:long "105.8342" .
```

## Các lệnh hữu ích

### Chạy tests
```bash
# Tất cả tests
pytest tests/

# Test cụ thể
pytest tests/test_geocoding.py
```

### Format code
```bash
black src/ tests/
```

### Check linting
```bash
flake8 src/ tests/
```

## Tài liệu chi tiết

- [Project Structure](PROJECT_STRUCTURE.md) - Cấu trúc chi tiết của project
- [API Documentation](API_CREDENTIALS.md) - Hướng dẫn API
- [Contributing Guide](CONTRIBUTING_GUIDE.md) - Hướng dẫn đóng góp
- [System Design](System_Design.md) - Thiết kế hệ thống

## Troubleshooting

### Lỗi import module
```bash
# Đảm bảo đã kích hoạt virtual environment
# Cài lại dependencies
pip install -r requirements.txt
```

### Lỗi kết nối API
```bash
# Kiểm tra file .env
cp .env.example .env
# Điền thông tin API credentials
```

## Liên hệ và hỗ trợ

- GitHub Issues: [Report bugs](https://github.com/MFitHou/OpenDataFitHou/issues)
- Documentation: Xem thư mục `docs/`
