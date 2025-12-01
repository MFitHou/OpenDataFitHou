# Tổng hợp dữ liệu và thuộc tính

## 📋 Danh sách Prefix (@prefix) được sử dụng trong các file RDF/Turtle

### **Prefix trong file cleaned (dữ liệu địa điểm)**
```turtle
@prefix ext: <http://opendatafithou.org/def/extension/> 
# Định nghĩa các thuộc tính mở rộng tùy chỉnh cho dự án OpenDataFitHou

@prefix fiware: <https://smartdatamodels.org/dataModel.PointOfInterest/> 
# Mô hình dữ liệu FIWARE cho điểm quan tâm (Point of Interest)

@prefix geo: <http://www.opengis.net/ont/geosparql#> 
# Ontology GeoSPARQL cho dữ liệu không gian địa lý

@prefix schema: <http://schema.org/> 
# Từ vựng Schema.org cho dữ liệu có cấu trúc

@prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
# Các kiểu dữ liệu XML Schema
```

### **Prefix trong file topology (data_hanoi_topology.ttl)**
```turtle
@prefix ext: <http://opendatafithou.org/def/extension/> 
# Định nghĩa các thuộc tính mở rộng

@prefix schema: <http://schema.org/> 
# Từ vựng Schema.org, sử dụng thuộc tính quan hệ không gian
```

### **Prefix trong file IoT Infrastructure (iot_infrastructure.ttl)**
```turtle
@prefix fiware: <https://uri.fiware.org/ns/data-models#> 
# Mô hình dữ liệu FIWARE cho IoT

@prefix geo: <http://www.opengis.net/ont/geosparql#> 
# Ontology GeoSPARQL

@prefix property: <http://opendatafithou.org/property/> 
# Định nghĩa các thuộc tính IoT tùy chỉnh (nhiệt độ, độ ẩm, chất lượng không khí, v.v.)

@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
# RDF Schema - cung cấp các thuộc tính như label, comment

@prefix schema1: <http://schema.org/> 
# Từ vựng Schema.org (sử dụng alias schema1 để tránh xung đột)

@prefix sf: <http://www.opengis.net/ont/sf#> 
# Simple Features - mô tả hình học địa lý (Point, LineString, Polygon)

@prefix sosa: <http://www.w3.org/ns/sosa/> 
# SOSA (Sensor, Observation, Sample, and Actuator) ontology

@prefix ssn: <http://www.w3.org/ns/ssn/> 
# Semantic Sensor Network ontology

@prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
# Các kiểu dữ liệu XML Schema
```

### **Prefix trong file IoT Coverage (iot_coverage.ttl)**
```turtle
@prefix sosa: <http://www.w3.org/ns/sosa/> 
# SOSA ontology - mô tả mối quan hệ giữa địa điểm và trạm cảm biến
```

---

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

#### **Chú thích ý nghĩa các thuộc tính chung:**

- **`ext:osm_id`**: ID định danh duy nhất của đối tượng trong cơ sở dữ liệu OpenStreetMap (OSM).
- **`ext:osm_type`**: Loại hình học của đối tượng OSM:
  - `node`: Điểm đơn lẻ (có tọa độ kinh độ/vĩ độ)
  - `way`: Đường nét hoặc vùng khép kín (tập hợp các node)
  - `relation`: Quan hệ phức tạp giữa nhiều đối tượng
- **`schema:name`**: Tên hiển thị của địa điểm (hỗ trợ đa ngôn ngữ với tag @en, @vi).
- **`schema:brand`**: Thương hiệu/nhãn hiệu của cơ sở kinh doanh.
- **`schema:legalName`**: Tên pháp lý chính thức của tổ chức/doanh nghiệp.
- **`schema:operator`**: Đơn vị/tổ chức vận hành/quản lý địa điểm.
- **`schema:sameAs`**: Liên kết đến cùng một thực thể trên Wikidata (để tích hợp dữ liệu).
- **`schema:url`**: Địa chỉ website chính thức.
- **`schema:telephone`**: Số điện thoại liên hệ.
- **`schema:openingHours`**: Giờ mở cửa (định dạng chuẩn OSM).
- **`ext:addr_city`**: Tên thành phố/tỉnh.
- **`ext:addr_district`**: Tên quận/huyện.
- **`ext:addr_street`**: Tên đường phố.
- **`ext:addr_housenumber`**: Số nhà.
- **`geo:asWKT`**: Tọa độ địa lý theo định dạng WKT (Well-Known Text), thường là POINT(kinh_độ vĩ_độ).
- **`a schema:Type`**: Khai báo kiểu đối tượng theo Schema.org (VD: schema:FinancialService, schema:Hospital).
- **`a fiware:PointOfInterest`**: Khai báo là điểm quan tâm theo mô hình FIWARE.

#### **Thuộc tính cụ thể theo loại dữ liệu:**

- **ATM (`data_hanoi_atm_cleaned.ttl`):**
  - `ext:osm_id`: ID của đối tượng trong OpenStreetMap.
  - `ext:osm_type`: Loại đối tượng (node, way, relation).
  - `schema:brand`: Thương hiệu của ngân hàng.
  - `schema:legalName`: Tên pháp lý của ngân hàng.
  - `schema:name`: Tên của trạm ATM.
  - `schema:operator`: Đơn vị vận hành.
  - `schema:sameAs`: Liên kết đến Wikidata.
  - `schema:url`: Trang web của ngân hàng.
  - `geo:asWKT`: Tọa độ địa lý (WKT).
  - `a schema:FinancialService, fiware:PointOfInterest`: Khai báo kiểu là dịch vụ tài chính.

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
  - `ext:osm_id`: ID của đối tượng trong OpenStreetMap.
  - `ext:osm_type`: Loại đối tượng (node, way, relation).
  - `schema:name`: Tên của nhà kho.
  - `geo:asWKT`: Tọa độ địa lý (WKT).
  - `a schema:Warehouse, fiware:PointOfInterest`: Khai báo kiểu là nhà kho.

---

## 📂 Dữ liệu Topology (data_hanoi_topology.ttl)

### **Mô tả:**
File topology chứa dữ liệu về mối quan hệ không gian giữa các địa điểm. Dữ liệu này mô tả các địa điểm nằm gần nhau hoặc chứa trong nhau.

### **Thuộc tính quan hệ không gian:**

- **`schema:isNextTo`**: Quan hệ "nằm kề bên" - chỉ ra hai địa điểm nằm gần nhau.
  - **Ví dụ:** ATM nằm kề bên ngân hàng, ATM nằm kề bên trạm xăng.
  - **Cú pháp:** `<địa_điểm_A> schema:isNextTo <địa_điểm_B>`

- **`schema:containedInPlace`**: Quan hệ "chứa trong" - chỉ ra một địa điểm nằm bên trong địa điểm khác.
  - **Ví dụ:** ATM nằm bên trong trạm xăng, ATM nằm trong chợ.
  - **Cú pháp:** `<địa_điểm_A> schema:containedInPlace <địa_điểm_B>`

### **Ứng dụng:**
- Hỗ trợ tìm kiếm theo ngữ cảnh không gian (VD: tìm ATM gần ngân hàng).
- Phân tích mối quan hệ giữa các loại dịch vụ.
- Tối ưu hóa định tuyến và gợi ý địa điểm.

---

## 📂 Dữ liệu IoT Infrastructure (iot_infrastructure.ttl)

### **Mô tả:**
File này định nghĩa cơ sở hạ tầng cảm biến IoT bao gồm các trạm quan trắc, loại cảm biến và thuộc tính quan sát.

### **Các thực thể chính:**

#### **1. IoT Stations (Trạm quan trắc)**
- **URI Pattern:** `urn:ngsi-ld:Device:Hanoi:station:{TênTrạm}`
- **Kiểu:** `sosa:Platform`, `ssn:System`
- **Thuộc tính:**
  - `rdfs:label`: Tên hiển thị của trạm.
  - `schema1:description`: Mô tả chức năng trạm.
  - `fiware:serialNumber`: Số serial định danh thiết bị.
  - `fiware:controlledAsset`: Khu vực/tài sản được giám sát.
  - `geo:hasGeometry`: Liên kết đến hình học không gian (Point).
  - `sosa:hosts`: Danh sách các cảm biến được lắp đặt tại trạm.

#### **2. Sensors (Cảm biến)**
- **URI Pattern:** `http://opendatafithou.org/sensor/{TênTrạm}:{LoạiCảmBiến}`
- **Kiểu:** `sosa:Sensor`, `ssn:System`
- **Thuộc tính:**
  - `rdfs:label`: Tên cảm biến.
  - `schema1:description`: Mô tả chức năng.
  - `sosa:isHostedBy`: Trạm lắp đặt cảm biến.
  - `sosa:observes`: Các thuộc tính quan sát được (nhiệt độ, độ ẩm, PM2.5, v.v.).
  - `fiware:controlledProperty`: Danh sách thuộc tính được giám sát.

#### **3. Observable Properties (Thuộc tính quan sát)**
- **URI Pattern:** `property:{TênThuộcTính}`
- **Kiểu:** `sosa:ObservableProperty`, `ssn:Property`
- **Các thuộc tính IoT:**
  - `property:Temperature`: Nhiệt độ (°C).
  - `property:Humidity`: Độ ẩm (%).
  - `property:WindSpeed`: Tốc độ gió (m/s).
  - `property:Rainfall`: Lượng mưa (mm).
  - `property:PM2.5`: Nồng độ bụi mịn PM2.5 (µg/m³).
  - `property:PM10`: Nồng độ bụi PM10 (µg/m³).
  - `property:AQI`: Chỉ số chất lượng không khí.
  - `property:NoiseLevel`: Mức độ ồn (dB).
  - `property:TrafficIntensity`: Mật độ giao thông (xe/phút).
  - `property:VehicleSpeed`: Tốc độ xe trung bình (km/h).
  - `property:WaterLevel`: Mực nước (cm).
  - `property:FloodRisk`: Mức độ rủi ro lũ lụt (low/medium/high).

#### **4. Geometry (Hình học không gian)**
- **URI Pattern:** `urn:ngsi-ld:Device:Hanoi:station:{TênTrạm}/geometry`
- **Kiểu:** `sf:Point`
- **Thuộc tính:**
  - `geo:asWKT`: Tọa độ WKT của trạm cảm biến.

### **Danh sách trạm IoT:**
1. **Cầu Giấy** (CauGiay) - Quận Cầu Giấy
2. **Hà Đông** (HaDong) - Quận Hà Đông
3. **Hồ Gươm** (HoGuom) - Quận Hoàn Kiếm
4. **Hoàng Mai** (HoangMai) - Quận Hoàng Mai
5. **Láng** (Lang) - Quận Đống Đa
6. **Long Biên** (LongBien) - Quận Long Biên
7. **Mỹ Đình** (MyDinh) - Quận Nam Từ Liêm
8. **Royal City** (RoyalCity) - Quận Thanh Xuân
9. **Tây Hồ** (TayHo) - Quận Tây Hồ
10. **Times City** (TimeCity) - Quận Hai Bà Trưng

---

## 📂 Dữ liệu IoT Coverage (iot_coverage.ttl)

### **Mô tả:**
File này định nghĩa mối quan hệ giữa các địa điểm (POI) và các trạm cảm biến IoT, xác định địa điểm nào được trạm nào phủ sóng.

### **Thuộc tính:**

- **`sosa:isSampledBy`**: Quan hệ "được lấy mẫu bởi" - chỉ ra một địa điểm được quan trắc bởi trạm cảm biến nào.
  - **Ví dụ:** ATM A được trạm Cầu Giấy quan trắc, Bệnh viện B được trạm Hồ Gươm quan trắc.
  - **Cú pháp:** `<địa_điểm> sosa:isSampledBy <trạm_cảm_biến>`

### **Ứng dụng:**
- Xác định dữ liệu IoT nào áp dụng cho địa điểm cụ thể.
- Phân tích môi trường xung quanh các địa điểm quan trọng.
- Cảnh báo khi có biến động môi trường ảnh hưởng đến các POI.
- Hỗ trợ ra quyết định dựa trên dữ liệu thời gian thực.

### **Thống kê phủ sóng:**
- Mỗi địa điểm được gán cho 1 trạm cảm biến gần nhất.
- Tổng số quan hệ coverage: 28,573 (tương ứng số POI trong dữ liệu).
- Trạm Hồ Gươm (trung tâm) có số POI phủ sóng nhiều nhất.

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