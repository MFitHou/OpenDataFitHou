# 📂 Thư mục `data`

Thư mục này chứa **các dữ liệu GeoJSON** được thu thập từ **Overpass API (OpenStreetMap)**.  
Các dữ liệu ở đây dùng làm nguồn đầu vào để chuyển đổi sang định dạng **RDF/Linked Data** và phục vụ các ứng dụng khác.

---

## 🗂 Nội dung
Mỗi file trong thư mục này tương ứng với một loại đối tượng trong bản đồ mở OSM, ví dụ:
- `bus_stop.geojson` → dữ liệu bến xe bus.
- `atm.geojson` → dữ liệu cây ATM.
- `school.geojson` → dữ liệu trường học.
- `hospital.geojson` → dữ liệu bệnh viện.
- `playground.geojson` → dữ liệu sân chơi.
- `toilets.geojson` → dữ liệu nhà vệ sinh công cộng.
- `drinking_water.geojson` → dữ liệu điểm lấy nước uống.

---

## 📌 Nguồn dữ liệu
- Các file được tải từ **Overpass API** với cú pháp truy vấn dạng:
```
[out:json][timeout:60];
node"amenity"="bus_stop"
;
out;
```
- Dữ liệu phản ánh thông tin tại thời điểm truy vấn, có thể thay đổi theo thời gian do cộng đồng OSM cập nhật.

---

## ⚙️ Cách sử dụng
1. Mở file GeoJSON bằng **Jupyter Notebook** hoặc thư viện Python như `geopandas` / `json`.
 ```python
 import geopandas as gpd
 gdf = gpd.read_file("data/bus_stop.geojson")
 print(gdf.head())
