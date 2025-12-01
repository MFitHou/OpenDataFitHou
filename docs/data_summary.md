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