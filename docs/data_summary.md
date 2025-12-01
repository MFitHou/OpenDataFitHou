# Tổng hợp dữ liệu và thuộc tính

## 📂 Dữ liệu trong thư mục `cleaned`
Dữ liệu trong thư mục `cleaned` thuộc thư mục `datav2` đã được xử lý và chuẩn hóa. Dưới đây là danh sách các loại dữ liệu và các thuộc tính chính:

### **1. Dữ liệu RDF/Turtle**
#### **Các loại dữ liệu:**
- `data_hanoi_atm.ttl`: Vị trí các cây ATM.
- `data_hanoi_bus_stop.ttl`: Vị trí các trạm xe buýt.
- `data_hanoi_drinking_water.ttl`: Điểm nước uống công cộng.
- `data_hanoi_hospital.ttl`: Vị trí các bệnh viện.
- `data_hanoi_school.ttl`: Vị trí các trường học.
- `data_hanoi_toilets.ttl`: Nhà vệ sinh công cộng.
- `data_hanoi_park.ttl`: Công viên.
- `data_hanoi_marketplace.ttl`: Chợ.
- `data_hanoi_library.ttl`: Thư viện.
- `data_hanoi_restaurant.ttl`: Nhà hàng.
- `data_hanoi_cafe.ttl`: Quán cà phê.
- `data_hanoi_supermarket.ttl`: Siêu thị.
- `data_hanoi_pharmacy.ttl`: Hiệu thuốc.
- `data_hanoi_clinic.ttl`: Phòng khám.
- `data_hanoi_fire_station.ttl`: Trạm cứu hỏa.
- `data_hanoi_police.ttl`: Đồn cảnh sát.
- `data_hanoi_post_office.ttl`: Bưu điện.
- `data_hanoi_university.ttl`: Trường đại học.
- `data_hanoi_kindergarten.ttl`: Trường mẫu giáo.
- `data_hanoi_community_centre.ttl`: Trung tâm cộng đồng.
- `data_hanoi_charging_station.ttl`: Trạm sạc xe điện.
- `data_hanoi_fuel_station.ttl`: Trạm xăng dầu.
- `data_hanoi_playground.ttl`: Khu vui chơi trẻ em.
- `data_hanoi_parking.ttl`: Bãi đỗ xe.
- `data_hanoi_warehouse.ttl`: Kho bãi.
- `data_hanoi_waste_basket.ttl`: Thùng rác công cộng.
- `data_hanoi_topology.ttl`: Dữ liệu topology (cấu trúc không gian).

#### **Thuộc tính chung:**
- `@id`: Định danh duy nhất của đối tượng.
- `name`: Tên địa điểm.
- `latitude`: Vĩ độ.
- `longitude`: Kinh độ.
- `address`: Địa chỉ chi tiết.
- `amenity`: Loại tiện ích (ATM, trường học, bệnh viện, v.v.).
- `capacity` (nếu có): Sức chứa (áp dụng cho bãi đỗ xe, nhà vệ sinh, v.v.).

#### **Thuộc tính cụ thể theo loại dữ liệu:**

- **ATM (`data_hanoi_atm_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `brand`: Thương hiệu của ngân hàng.
  - `legalName`: Tên pháp lý của ngân hàng.
  - `name`: Tên của trạm ATM.
  - `operator`: Đơn vị vận hành.
  - `sameAs`: Liên kết đến Wikidata.
  - `url`: Trang web của ngân hàng.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Trạm xe buýt (`data_hanoi_bus_stop_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của trạm xe buýt.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Điểm nước uống (`data_hanoi_drinking_water_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của điểm nước uống.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Bệnh viện (`data_hanoi_hospital_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của bệnh viện.
  - `operator`: Đơn vị vận hành.
  - `telephone`: Số điện thoại liên hệ.
  - `url`: Trang web của bệnh viện.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_street`: Đường phố.
  - `addr_housenumber`: Số nhà.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Trường học (`data_hanoi_school_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của trường học.
  - `operator`: Đơn vị vận hành.
  - `telephone`: Số điện thoại liên hệ.
  - `url`: Trang web của trường.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_street`: Đường phố.
  - `addr_housenumber`: Số nhà.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Quán cà phê (`data_hanoi_cafe_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `brand`: Thương hiệu của quán cà phê.
  - `legalName`: Tên pháp lý của quán cà phê.
  - `name`: Tên của quán cà phê.
  - `sameAs`: Liên kết đến Wikidata.
  - `url`: Trang web của quán cà phê.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Trạm sạc xe điện (`data_hanoi_charging_station_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `brand`: Thương hiệu của trạm sạc.
  - `legalName`: Tên pháp lý của trạm sạc.
  - `name`: Tên của trạm sạc.
  - `operator`: Đơn vị vận hành.
  - `sameAs`: Liên kết đến Wikidata.
  - `url`: Trang web của trạm sạc.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Phòng khám (`data_hanoi_clinic_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của phòng khám.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Trung tâm cộng đồng (`data_hanoi_community_centre_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của trung tâm cộng đồng.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_housenumber`: Số nhà.
  - `addr_street`: Đường phố.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Cửa hàng tiện lợi (`data_hanoi_convenience_store_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `brand`: Thương hiệu của cửa hàng.
  - `legalName`: Tên pháp lý của cửa hàng.
  - `name`: Tên của cửa hàng.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_housenumber`: Số nhà.
  - `addr_street`: Đường phố.
  - `sameAs`: Liên kết đến Wikidata.
  - `url`: Trang web của cửa hàng.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Trạm cứu hỏa (`data_hanoi_fire_station_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của trạm cứu hỏa.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_street`: Đường phố.
  - `addr_housenumber`: Số nhà.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Trạm xăng dầu (`data_hanoi_fuel_station_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của trạm xăng dầu.
  - `brand`: Thương hiệu của trạm xăng dầu.
  - `legalName`: Tên pháp lý của trạm xăng dầu.
  - `operator`: Đơn vị vận hành.
  - `sameAs`: Liên kết đến Wikidata.
  - `url`: Trang web của trạm xăng dầu.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Thư viện (`data_hanoi_library_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của thư viện.
  - `operator`: Đơn vị vận hành.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_street`: Đường phố.
  - `addr_housenumber`: Số nhà.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Chợ (`data_hanoi_marketplace_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của chợ.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_street`: Đường phố.
  - `addr_housenumber`: Số nhà.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Công viên (`data_hanoi_park_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của công viên.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Hiệu thuốc (`data_hanoi_pharmacy_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của hiệu thuốc.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_street`: Đường phố.
  - `addr_housenumber`: Số nhà.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Khu vui chơi trẻ em (`data_hanoi_playground_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của khu vui chơi.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Đồn cảnh sát (`data_hanoi_police_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của đồn cảnh sát.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_street`: Đường phố.
  - `addr_housenumber`: Số nhà.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Bưu điện (`data_hanoi_post_office_cleaned.ttl`):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của bưu điện.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_street`: Đường phố.
  - `addr_housenumber`: Số nhà.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Nhà vệ sinh công cộng (Public Toilets):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của nhà vệ sinh công cộng.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_street`: Đường phố.
  - `addr_housenumber`: Số nhà.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Nhà hàng (Restaurants):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của nhà hàng.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_street`: Đường phố.
  - `addr_housenumber`: Số nhà.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Trường học (Schools):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của trường học.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_street`: Đường phố.
  - `addr_housenumber`: Số nhà.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Siêu thị (Supermarkets):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của siêu thị.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_street`: Đường phố.
  - `addr_housenumber`: Số nhà.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Trường đại học (Universities):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của trường đại học.
  - `addr_city`: Thành phố.
  - `addr_district`: Quận/huyện.
  - `addr_street`: Đường phố.
  - `addr_housenumber`: Số nhà.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Bãi đỗ xe (Parking Lots):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của bãi đỗ xe.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Trường mẫu giáo (Kindergartens):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của trường mẫu giáo.
  - `addr_street`: Đường phố (nếu có).
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Thùng rác (Waste Baskets):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của thùng rác.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

- **Nhà kho (Warehouses):**
  - `osm_id`: ID của đối tượng trong OpenStreetMap.
  - `osm_type`: Loại đối tượng (node, way, relation).
  - `name`: Tên của nhà kho.
  - `geo:asWKT`: Tọa độ địa lý (WKT).

---

## 📂 Dữ liệu IoT
Dữ liệu IoT được mô phỏng hoặc thu thập từ các API và được lưu trữ trong InfluxDB. Dưới đây là các loại dữ liệu IoT và các thuộc tính chính:

### **1. Dữ liệu thời tiết**
#### **Nguồn:** OpenWeatherMap API hoặc mô phỏng.
#### **Thuộc tính:**
- `temperature`: Nhiệt độ (°C).
- `humidity`: Độ ẩm (%).
- `wind_speed`: Tốc độ gió (m/s).
- `rain_1h`: Lượng mưa trong 1 giờ (mm).
- `timestamp`: Thời gian ghi nhận.

### **2. Dữ liệu chất lượng không khí**
#### **Nguồn:** OpenAQ API hoặc mô phỏng.
#### **Thuộc tính:**
- `pm25`: Nồng độ PM2.5 (µg/m³).
- `pm10`: Nồng độ PM10 (µg/m³).
- `aqi`: Chỉ số chất lượng không khí (AQI).
- `timestamp`: Thời gian ghi nhận.

### **3. Dữ liệu giao thông**
#### **Nguồn:** Mô phỏng.
#### **Thuộc tính:**
- `station_id`: ID của trạm quan trắc.
- `intensity`: Cường độ giao thông (0-100).
- `avg_speed`: Tốc độ trung bình (km/h).
- `noise_level`: Mức độ tiếng ồn (dB).
- `timestamp`: Thời gian ghi nhận.

### **4. Dữ liệu ngập lụt**
#### **Nguồn:** Mô phỏng dựa trên lượng mưa và khả năng thoát nước.
#### **Thuộc tính:**
- `station_id`: ID của trạm quan trắc.
- `flood_depth`: Độ sâu ngập lụt (cm).
- `timestamp`: Thời gian ghi nhận.

---

## 📊 Kết luận
Dữ liệu trong dự án bao gồm cả dữ liệu tĩnh (RDF/Turtle) và dữ liệu động (IoT). Các thuộc tính được chuẩn hóa để dễ dàng tích hợp và phân tích. Dữ liệu IoT hỗ trợ các bài toán thời gian thực, trong khi dữ liệu tĩnh cung cấp thông tin nền tảng cho các ứng dụng Smart City.