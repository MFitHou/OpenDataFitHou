# Giả lập trong iot_collector.py

## 📌 Giới thiệu
Module `iot_collector.py` được thiết kế để thu thập và mô phỏng dữ liệu từ các nguồn khác nhau, bao gồm thời tiết, chất lượng không khí, giao thông, tiếng ồn, và ngập lụt. Các giả lập được sử dụng để:
- Cung cấp dữ liệu thay thế khi không có dữ liệu thực tế.
- Mô phỏng các điều kiện môi trường dựa trên các yếu tố đầu vào.

---

## 📂 Cấu trúc các giả lập

### **1. Giả lập thời tiết**
#### **Hàm: `get_weather(lat: float, lon: float)`**
- **Mục đích:** Lấy dữ liệu thời tiết từ OpenWeatherMap API hoặc xử lý lỗi khi không có dữ liệu.
- **Dữ liệu trả về:**
  - Nhiệt độ (`temperature`): °C
  - Độ ẩm (`humidity`): %
  - Tốc độ gió (`wind_speed`): m/s
  - Lượng mưa 1 giờ (`rain_1h`): mm
- **Xử lý lỗi:**
  - In ra thông báo khi thiếu API key hoặc lỗi kết nối.

---

### **2. Giả lập chất lượng không khí**
#### **Hàm: `get_air_quality(lat: float, lon: float, radius: int = 25000)`**
- **Mục đích:** Lấy dữ liệu chất lượng không khí từ OpenAQ API hoặc mô phỏng dữ liệu khi không có dữ liệu thực tế.
- **Dữ liệu trả về:**
  - PM2.5 (`pm25`): µg/m³
  - PM10 (`pm10`): µg/m³
  - Chỉ số chất lượng không khí (`aqi`): AQI
- **Mô phỏng dữ liệu:**
  - PM2.5: Giá trị ngẫu nhiên từ 20-60 µg/m³.
  - PM10: Giá trị ngẫu nhiên từ 40-80 µg/m³.
  - AQI: Tính toán từ PM2.5 theo chuẩn Vietnam/US EPA.

---

### **3. Giả lập lưu lượng giao thông**
#### **Hàm: `simulate_traffic_flow(current_hour: int, traffic_factor: float = 1.0)`**
- **Mục đích:** Mô phỏng cường độ giao thông và tốc độ trung bình dựa trên giờ trong ngày và đặc điểm địa điểm.
- **Dữ liệu trả về:**
  - Cường độ giao thông (`intensity`): 0-100
  - Tốc độ trung bình (`avg_speed`): km/h
- **Logic:**
  - **Giờ cao điểm:** 7-8h, 17-18h (cường độ cao).
  - **Giờ làm việc:** 9-16h (cường độ trung bình).
  - **Buổi tối:** 19-22h (cường độ thấp).
  - **Ban đêm:** 23-5h (cường độ rất thấp).
  - Áp dụng hệ số `traffic_factor` để điều chỉnh cường độ.

---

### **4. Giả lập mức độ tiếng ồn**
#### **Hàm: `simulate_noise_level(traffic_intensity: int)`**
- **Mục đích:** Mô phỏng mức độ tiếng ồn dựa trên cường độ giao thông.
- **Dữ liệu trả về:**
  - Mức độ tiếng ồn (`noise_level`): dB
- **Logic:**
  - Tiếng ồn cơ bản: 45 dB.
  - Đóng góp từ giao thông: 0.4 dB cho mỗi đơn vị cường độ giao thông.
  - Dao động ngẫu nhiên: ±2 dB.

---

### **5. Giả lập ngập lụt**
#### **Hàm: `simulate_flood_depth(rain_1h: float, current_level: float, drainage_rate: float = 5.0)`**
- **Mục đích:** Mô phỏng độ sâu ngập lụt dựa trên lượng mưa, mực nước hiện tại và khả năng thoát nước.
- **Dữ liệu trả về:**
  - Mực nước mới (`new_level`): cm
- **Logic:**
  - **Nước vào:** 1 mm mưa → 0.5 cm nước tích tụ.
  - **Nước thoát:** Tốc độ thoát nước phụ thuộc vào `drainage_rate`.
  - **Giới hạn:** Mực nước luôn nằm trong khoảng 0-100 cm.

---

### **6. Giả lập tổng hợp giao thông**
#### **Hàm: `simulate_traffic(station_id: str, traffic_factor: float = 1.0)`**
- **Mục đích:** Mô phỏng dữ liệu giao thông tổng hợp cho một trạm quan trắc.
- **Dữ liệu trả về:**
  - ID trạm (`station_id`)
  - Cường độ giao thông (`intensity`)
  - Tốc độ trung bình (`avg_speed`)
  - Mức độ tiếng ồn (`noise_level`)
  - Thời gian (`timestamp`)

---

### **7. Giả lập tổng hợp ngập lụt**
#### **Hàm: `simulate_flood(station_id: str, lat: float, lon: float, drainage_rate: float = 5.0)`**
- **Mục đích:** Mô phỏng dữ liệu ngập lụt tổng hợp cho một trạm quan trắc.
- **Dữ liệu trả về:**
  - ID trạm (`station_id`)
  - Mực nước ngập (`flood_depth`)
  - Thời gian (`timestamp`)

---

## 🌐 API và cấu hình liên quan
- **OpenWeatherMap API:**
  - URL: `https://api.openweathermap.org/data/2.5/weather`
  - API Key: `OPENWEATHER_API_KEY`
- **OpenAQ API:**
  - URL: `https://api.openaq.org/v3/locations`
  - API Key: `OPENAQ_API_KEY`

---

## 📜 Thuật toán chi tiết cho các giả lập không sử dụng API

### **1. Giả lập chất lượng không khí (Fallback)**
#### **Hàm: `get_air_quality` (Fallback)**
- **Mục đích:** Mô phỏng dữ liệu chất lượng không khí khi không có dữ liệu từ OpenAQ API.
- **Thuật toán:**
  1. Sinh giá trị ngẫu nhiên cho PM2.5 trong khoảng [20, 60] µg/m³.
  2. Sinh giá trị ngẫu nhiên cho PM10 trong khoảng [40, 80] µg/m³.
  3. Tính chỉ số AQI từ PM2.5 bằng hàm `calculate_vn_aqi`.
  4. Trả về kết quả dưới dạng dictionary:
     ```python
     {
         'pm25': round(pm25_simulated, 1),
         'pm10': round(pm10_simulated, 1),
         'aqi': aqi_simulated
     }
     ```

---

### **2. Giả lập lưu lượng giao thông**
#### **Hàm: `simulate_traffic_flow`**
- **Mục đích:** Mô phỏng cường độ giao thông và tốc độ trung bình.
- **Thuật toán:**
  1. **Xác định cường độ giao thông cơ bản (`base_intensity`)**:
     - Giờ cao điểm (7-8h, 17-18h): Sinh giá trị ngẫu nhiên trong khoảng [70, 80].
     - Giờ làm việc (9-16h): Sinh giá trị ngẫu nhiên trong khoảng [40, 50].
     - Buổi tối (19-22h): Sinh giá trị ngẫu nhiên trong khoảng [30, 40].
     - Ban đêm (23-5h): Sinh giá trị ngẫu nhiên trong khoảng [5, 10].
  2. **Điều chỉnh cường độ giao thông với `traffic_factor`**:
     ```python
     final_intensity = int(base_intensity * traffic_factor)
     final_intensity = min(100, final_intensity)  # Giới hạn tối đa là 100
     ```
  3. **Tính tốc độ trung bình (`avg_speed`)**:
     - Công thức: `speed = max(5, 60 - (intensity * 0.6))`.
  4. Trả về tuple `(final_intensity, avg_speed)`.

---

### **3. Giả lập mức độ tiếng ồn**
#### **Hàm: `simulate_noise_level`**
- **Mục đích:** Mô phỏng mức độ tiếng ồn dựa trên cường độ giao thông.
- **Thuật toán:**
  1. Xác định mức tiếng ồn cơ bản: `base_noise = 45.0` (dB).
  2. Tính đóng góp từ giao thông: `traffic_contribution = traffic_intensity * 0.4`.
  3. Thêm dao động ngẫu nhiên: `random_fluctuation = random.uniform(-2.0, 2.0)`.
  4. Tính tổng mức độ tiếng ồn:
     ```python
     noise_level = base_noise + traffic_contribution + random_fluctuation
     ```
  5. Làm tròn kết quả đến 1 chữ số thập phân và trả về.

---

### **4. Giả lập ngập lụt**
#### **Hàm: `simulate_flood_depth`**
- **Mục đích:** Mô phỏng độ sâu ngập lụt dựa trên lượng mưa và khả năng thoát nước.
- **Thuật toán:**
  1. **Tính lượng nước tích tụ từ mưa (`water_in`)**:
     - Nếu `rain_1h > 0`, tính: `water_in = rain_1h * 0.5` (1 mm mưa → 0.5 cm nước).
  2. **Tính lượng nước thoát (`water_out`)**:
     - Giá trị cố định: `water_out = drainage_rate`.
  3. **Tính mực nước mới (`new_level`)**:
     ```python
     new_level = current_level + water_in - water_out
     new_level = max(0.0, min(100.0, new_level))  # Giới hạn trong khoảng [0, 100]
     ```
  4. Trả về `new_level`.