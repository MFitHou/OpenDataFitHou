# OSM Data Fetcher - Usage Guide

## Tổng quan

Hệ thống thu thập dữ liệu POI từ OpenStreetMap cho Hà Nội, enrichment từ Wikidata và chuyển đổi sang RDF Turtle format.

## Cấu trúc Files

```
osm_data_fetcher.py      # Core functions (fetch, enrich, convert to RDF)
config_amenity_types.py  # Danh sách tất cả 33 loại amenity
batch_processor.py       # Script xử lý hàng loạt với error handling
datav2/                  # Thư mục output (TTL files + logs)
```

## Cách sử dụng

### 1. Test nhanh với 1 category (ATM)

```bash
python osm_data_fetcher.py
```

Kết quả: File `datav2/data_hanoi_atm.ttl`

### 2. Test với 3 categories đầu tiên

```bash
python batch_processor.py test
```

Xử lý: ATM, Bank, Post Office

### 3. Xử lý TẤT CẢ 33 categories

```bash
python batch_processor.py
```

Thời gian ước tính: 30-60 phút (tùy network)

### 4. Resume từ category cụ thể

Nếu bị gián đoạn, tiếp tục từ category bất kỳ:

```bash
python batch_processor.py from:hospital
```

### 5. Retry các categories bị lỗi

```bash
python batch_processor.py retry
```

## Output Files

### RDF Turtle files (datav2/)
- `data_hanoi_atm.ttl`
- `data_hanoi_school.ttl`
- `data_hanoi_hospital.ttl`
- ... (tổng 33 files)

### Log files (datav2/)
- `processing_progress.json` - Theo dõi tiến trình
- `processing_errors.log` - Log các lỗi
- `processing_summary.json` - Tổng kết kết quả

## Tính năng

✅ **Batch Processing**: Xử lý hàng loạt 33 loại amenity
✅ **Progress Tracking**: Lưu tiến trình, có thể resume
✅ **Error Handling**: Ghi log lỗi, retry tự động
✅ **Multilingual Support**: Label và description bằng tiếng Việt + tiếng Anh
✅ **Wikidata Enrichment**: Bổ sung thông tin từ Wikidata
✅ **RDF Output**: Chuẩn Turtle với language tags (@vi, @en)

## Danh sách 33 Amenity Types

### Tài chính & Dịch vụ (3)
- ATM, Bank, Post Office

### Giao thông (4)
- Bus Stop, Parking, Fuel Station, Charging Station

### Y tế & Khẩn cấp (5)
- Hospital, Clinic, Pharmacy, Police, Fire Station

### Tiện ích công cộng (3)
- Drinking Water, Public Toilet, Waste Basket

### Giáo dục (4)
- School, Kindergarten, University, Library

### Giải trí (3)
- Park, Playground, Community Centre

### Mua sắm & Ẩm thực (5)
- Marketplace, Supermarket, Convenience Store, Cafe, Restaurant

### Hạ tầng khác (1)
- Warehouse

## Cấu hình

Chỉnh sửa `config_amenity_types.py` để thay đổi:

```python
BATCH_CONFIG = {
    'delay_between_categories': 3,  # Giây chờ giữa các category
    'delay_between_api_calls': 2,   # Giây chờ giữa các API call
    'max_retries': 3,                # Số lần retry tối đa
    'timeout': 120,                  # Timeout (giây)
}
```

## Xử lý lỗi

Nếu gặp lỗi:

1. Kiểm tra `datav2/processing_errors.log`
2. Xem chi tiết trong `datav2/processing_summary.json`
3. Retry: `python batch_processor.py retry`

## Requirements

```
requests
pathlib
```

## Notes

- API Overpass: Tự động chia nhỏ bounding box để tránh timeout
- Wikidata: Batch query 50 IDs/lần
- Rate limiting: 2-3 giây delay giữa các requests
- Resume: Tự động skip các category đã hoàn thành
