# API_CREDENTIALS.md

## Hướng dẫn lấy và lưu API Keys an toàn

### 1. OpenWeatherMap
- Đăng ký tài khoản tại https://home.openweathermap.org/users/sign_up
- Vào "API keys" để lấy key
- Thêm vào file `.env`:
  ```
  OPENWEATHER_API_KEY=your_api_key_here
  ```

### 2. OpenAQ
- Đăng ký tại https://docs.openaq.org/#api-Authentication
- Thêm vào `.env`:
  ```
  OPENAQ_API_KEY=your_api_key_here
  ```

### 3. Overpass API
- Không cần API key, chỉ cần URL:
  ```
  OVERPASS_URL=https://overpass-api.de/api/interpreter
  ```

### 4. Wikidata SPARQL
- Không cần API key, chỉ cần endpoint:
  ```
  WIKIDATA_SPARQL_URL=https://query.wikidata.org/sparql
  ```

### 5. GTFS Datasets
- Tải trực tiếp từ nguồn cung cấp GTFS, không cần key.
- Hiện dữ liệu dự án đang được lưu trong thư mục file raw-data lấy từ nguồn [Hanoi--Vietnam---General-Transit-Feed-Specification--GTFS-](https://datacatalog.worldbank.org/search/dataset/0038236/Hanoi--Vietnam---General-Transit-Feed-Specification--GTFS-)

---

## Lưu ý bảo mật
- **KHÔNG commit file `.env` lên git** (đã có trong `.gitignore`)
- Chia sẻ keys qua kênh an toàn (không gửi qua email công khai)
- Đổi key nếu nghi ngờ bị lộ
