# Tài liệu Topology Relationships - Hệ thống Dữ liệu Thành phố Thông minh Hà Nội

## 📖 Giới thiệu

File `data_hanoi_topology.ttl` chứa **84,397 mối quan hệ không gian** (spatial relationships) giữa các tiện ích công cộng tại Hà Nội. Những mối quan hệ này được tạo tự động dựa trên khoảng cách địa lý thực tế, giúp hiểu được cấu trúc và kết nối của đô thị.

## 🎯 Mục đích

Topology này giúp trả lời các câu hỏi như:
- Trạm xe buýt nào phục vụ trường học này?
- Có nhà thuốc nào gần bệnh viện không?
- Những quán cà phê nào tạo thành cụm thương mại?
- Cơ sở khẩn cấp (cảnh sát, cứu hỏa) được kết nối như thế nào?

## 📊 Thống kê tổng quan

```
Tổng số mối quan hệ: 84,397
Số tiện ích được liên kết: 11,170

Phân bố theo khoảng cách:
├─ ≤ 50m (containedInPlace):     7,388 mối quan hệ (8.8%)
├─ 50-200m (isNextTo):          55,884 mối quan hệ (66.2%)
└─ >200m (domain-specific):     21,125 mối quan hệ (25.0%)
```

## 🔗 Ba loại Predicates chính

### 1. **schema:containedInPlace** (≤50m)
**Ý nghĩa**: Tiện ích nằm BÊN TRONG hoặc SÁT CẠNH nhau (trong vòng 50 mét)

**Ví dụ thực tế**:
```turtle
# ATM nằm trong trạm xăng
<atm:12895021294> schema:containedInPlace <fuel_station:729787543> .

# Nhà hàng và quán café trong cùng toà nhà
<restaurant:123> schema:containedInPlace <cafe:456> .
```

**Các cặp phổ biến**:
- ATM → Ngân hàng (383 trường hợp)
- ATM → Trạm xăng (nhiều trường hợp)
- Nhà hàng ↔ Quán café (2,372 trường hợp)

---

### 2. **schema:isNextTo** (50-200m)
**Ý nghĩa**: Tiện ích Ở GẦN nhau, trong phạm vi đi bộ ngắn (50-200 mét)

**Ví dụ thực tế**:
```turtle
# Nhà thuốc gần bệnh viện
<pharmacy:789> schema:isNextTo <hospital:321> .

# Ngân hàng gần ATM
<bank:555> schema:isNextTo <atm:888> .
```

**Đây là loại quan hệ phổ biến nhất** (66.2% tổng số)

---

### 3. **Predicates theo lĩnh vực** (>200m)
**Ý nghĩa**: Quan hệ chức năng đặc biệt dựa theo từng loại tiện ích

#### 🚌 **schema:amenityFeature** (Bus phục vụ các điểm)
```turtle
# Trạm xe buýt phục vụ trường học (trong vòng 500m)
<bus_stop:444394880> schema:amenityFeature <school:699218317> .

# Trạm xe buýt phục vụ bệnh viện
<bus_stop:123> schema:amenityFeature <hospital:456> .
```
**Số lượng**: 14,096 mối quan hệ

---

#### 🅿️ **schema:publicAccess** (Parking có quyền truy cập công cộng)
```turtle
# Bãi đỗ xe phục vụ quán café
<parking:10063035517> schema:publicAccess <cafe:10241471509> .

# Bãi đỗ xe phục vụ siêu thị
<parking:789> schema:publicAccess <supermarket:321> .
```
**Số lượng**: 2,552 mối quan hệ

---

#### 🎓 **ext:campusAmenity** (Tiện ích phục vụ khuôn viên trường đại học)
```turtle
# Quán café phục vụ sinh viên đại học
<cafe:123> ext:campusAmenity <university:699218352> .

# Nhà hàng gần trường đại học
<restaurant:456> ext:campusAmenity <university:699218352> .
```
**Số lượng**: 2,317 mối quan hệ

---

#### 📚 **ext:educationSupport** (Hỗ trợ giáo dục)
```turtle
# Thư viện hỗ trợ trường học
<library:123> ext:educationSupport <school:456> .

# Sân chơi gần trường học
<playground:789> ext:educationSupport <school:456> .
```
**Số lượng**: 1,501 mối quan hệ

---

#### 🛒 **ext:shoppingDistrict** (Khu thương mại)
```turtle
# Siêu thị trong khu thương mại với ngân hàng
<supermarket:123> ext:shoppingDistrict <bank:456> .

# Siêu thị gần nhà thuốc
<supermarket:789> ext:shoppingDistrict <pharmacy:321> .
```
**Số lượng**: 392 mối quan hệ

---

#### 📖 **ext:educationHub** (Trung tâm giáo dục)
```turtle
# Thư viện là trung tâm giáo dục cho trường học
<library:123> ext:educationHub <school:456> .

# Thư viện phục vụ đại học
<library:789> ext:educationHub <university:321> .
```
**Số lượng**: 102 mối quan hệ

---

#### 🚨 **ext:emergencyService** (Dịch vụ khẩn cấp)
```turtle
# Đồn cảnh sát liên kết với bệnh viện
<police:10234747087> ext:emergencyService <hospital:5808582515> .

# Trạm cứu hỏa liên kết với cảnh sát
<fire_station:123> ext:emergencyService <police:456> .
```
**Số lượng**: 89 mối quan hệ

**Mạng lưới khẩn cấp**:
- Cảnh sát ↔ Bệnh viện: 48 kết nối
- Cảnh sát ↔ Bưu điện: 33 kết nối
- Cứu hỏa ↔ Cảnh sát: 4 kết nối

---

#### 🏘️ **ext:communityHub** (Trung tâm cộng đồng)
```turtle
# Trung tâm văn hóa cộng đồng kết nối với công viên
<community_centre:1124152131> ext:communityHub <park:1124152135> .

# Trung tâm cộng đồng gần thư viện
<community_centre:789> ext:communityHub <library:321> .
```
**Số lượng**: 76 mối quan hệ

---

## 🗺️ Các cụm tiện ích quan trọng (Top Hubs)

Những tiện ích có nhiều kết nối nhất:

### Top 5 Điểm kết nối cao nhất:
1. **University 699218352**: 165 kết nối
2. **University 699218338**: 159 kết nối  
3. **University 699218317**: 144 kết nối
4. **Parking 1210480417**: 127 kết nối
5. **Cafe 3281664612**: 114 kết nối

→ Các trường đại học và bãi đỗ xe là những "hub" quan trọng của thành phố!

---

## 📐 Quy tắc tạo Topology

### Khoảng cách và Predicate
```
Khoảng cách thực tế              Predicate được sử dụng
─────────────────────────────────────────────────────────
0m    ────────────> 50m          schema:containedInPlace
                                 (Nằm trong/sát cạnh)

50m   ────────────> 200m         schema:isNextTo
                                 (Ở gần, đi bộ ngắn)

200m  ────────────> 500m         Predicate theo lĩnh vực
                                 (amenityFeature, publicAccess, 
                                  campusAmenity, etc.)
```

### Cấu hình theo lĩnh vực

#### 🚌 Giao thông
- **Bus stops** kết nối với: trường học, bệnh viện, chợ, siêu thị (≤500m)
- **Parking** kết nối với: công viên, chợ, bệnh viện, nhà hàng (≤300m)

#### ⚕️ Y tế
- **Pharmacies** gần: bệnh viện, phòng khám (≤100m)
- **Clinics** trong mạng lưới: bệnh viện, nhà thuốc (≤200m)

#### 🎓 Giáo dục
- **Schools** kết nối: sân chơi, thư viện, trạm bus, công viên (≤300m)
- **Kindergartens** gần: sân chơi, công viên (≤200m)
- **Universities** kết nối: thư viện, café, nhà hàng, bus (≤500m)

#### 🏪 Thương mại
- **Cafes** cụm với: nhà hàng, cửa hàng tiện lợi (≤200m)
- **Supermarkets** gần: nhà thuốc, ngân hàng, ATM (≤250m)

#### 🏛️ Dịch vụ công
- **Police** kết nối: trạm cứu hỏa, bệnh viện, bưu điện (≤300m)
- **Post offices** gần: ngân hàng, trung tâm cộng đồng (≤200m)

---

## 💡 Ví dụ sử dụng SPARQL

### 1. Tìm tất cả tiện ích trong vòng 50m
```sparql
PREFIX schema: <http://schema.org/>

SELECT ?source ?target WHERE {
    ?source schema:containedInPlace ?target .
}
```

### 2. Tìm trường học có trạm bus gần
```sparql
PREFIX schema: <http://schema.org/>

SELECT ?school ?bus_stop WHERE {
    ?bus_stop a schema:BusStop ;
              schema:amenityFeature ?school .
    ?school a schema:School .
}
```

### 3. Tìm mạng lưới y tế (bệnh viện - phòng khám - nhà thuốc)
```sparql
PREFIX schema: <http://schema.org/>
PREFIX ext: <http://opendatafithou.org/def/extension/>

SELECT ?clinic ?pharmacy ?hospital WHERE {
    ?clinic a schema:Clinic ;
            ext:healthcareNetwork ?hospital .
    ?pharmacy schema:isNextTo ?hospital .
    ?hospital a schema:Hospital .
}
```

### 4. Tìm các dịch vụ khẩn cấp liên kết
```sparql
PREFIX ext: <http://opendatafithou.org/def/extension/>

SELECT ?source ?target WHERE {
    ?source ext:emergencyService ?target .
}
```

### 5. Tìm bãi đỗ xe phục vụ quán café
```sparql
PREFIX schema: <http://schema.org/>

SELECT ?parking ?cafe WHERE {
    ?parking schema:publicAccess ?cafe .
    ?cafe a schema:Cafe .
}
```

---

## 🔧 Cách tạo lại Topology

File này được tạo tự động bởi script `generate_topology.py`:

```bash
# Chạy script tạo topology
python generate_topology.py

# Output: datav2/data_hanoi_topology.ttl
```

**Thời gian xử lý**: ~30 giây cho 13,146 tiện ích

**Công nghệ**:
- RDFlib: Xử lý RDF/Turtle
- Haversine formula: Tính khoảng cách địa lý chính xác
- Distance-based semantic predicates: Phân loại tự động

---

## 📁 Cấu trúc Namespace

```turtle
@prefix ext: <http://opendatafithou.org/def/extension/> .
@prefix schema: <http://schema.org/> .
```

- **schema:** - Các predicates chuẩn từ Schema.org
- **ext:** - Các predicates mở rộng đặc thù cho Hà Nội

---

## 🎓 Các khái niệm quan trọng

### Topology (Cấu trúc không gian)
Mô tả cách các đối tượng được sắp xếp và kết nối trong không gian địa lý.

### Predicate (Vị từ)
Quan hệ giữa hai tiện ích (ví dụ: "gần", "phục vụ", "nằm trong").

### Triple (Bộ ba)
Cấu trúc cơ bản của RDF: `<Chủ thể> <Vị từ> <Đối tượng>`

**Ví dụ**:
```turtle
<atm:123> schema:isNextTo <bank:456> .
   ↑           ↑              ↑
 Chủ thể    Vị từ        Đối tượng
```

### Spatial Relationship (Quan hệ không gian)
Mối liên hệ dựa trên khoảng cách và vị trí địa lý giữa các tiện ích.

---

## 🤝 Ứng dụng thực tế

### 1. **Quy hoạch đô thị**
- Phát hiện thiếu hụt tiện ích (vùng không có trạm bus, y tế)
- Tối ưu hóa vị trí dịch vụ công mới

### 2. **Ứng dụng di động**
- "Tìm nhà thuốc gần bệnh viện này"
- "Chỉ đường đến quán café gần nhất từ đại học"

### 3. **Phân tích cụm**
- Nhận diện các khu thương mại
- Tìm các "hub" quan trọng của thành phố

### 4. **Dịch vụ khẩn cấp**
- Mapping mạng lưới cảnh sát - cứu hỏa - bệnh viện
- Tối ưu thời gian phản ứng khẩn cấp

### 5. **Du lịch thông minh**
- Gợi ý điểm tham quan gần nhau
- Lên lịch di chuyển tối ưu

---

## 📞 Hỗ trợ

**Script tạo topology**: `generate_topology.py`  
**Script kiểm tra**: `verify_predicate_types.py`  
**Ví dụ queries**: `example_topology_queries.py`

**Documentation**: `docs/TOPOLOGY_GENERATOR.md`

---

## 📝 Ghi chú kỹ thuật

- Sử dụng **Haversine formula** để tính khoảng cách chính xác trên bề mặt Trái Đất
- Tọa độ từ **WKT POINT format**: `POINT(longitude latitude)`
- Tối ưu hóa: Load toàn bộ graphs vào RAM, cache coordinates
- Tránh O(N²): Chỉ kiểm tra các cặp được cấu hình

---

## ✨ Ví dụ trực quan

```
🏥 Bệnh viện Bạch Mai
    │
    ├─ (≤50m) ──→ 💊 Nhà thuốc 24h
    ├─ (100m) ──→ 🚑 Trạm cấp cứu
    ├─ (150m) ──→ 🏪 Cửa hàng tiện lợi
    └─ (250m) ──→ 🚌 Trạm xe buýt số 8

🎓 ĐH Bách Khoa Hà Nội
    │
    ├─ (50m) ───→ ☕ Highlands Coffee
    ├─ (100m) ──→ 🍜 Khu ăn uống sinh viên
    ├─ (200m) ──→ 📚 Thư viện khoa học
    ├─ (300m) ──→ 🅿️ Bãi đỗ xe
    └─ (400m) ──→ 🚌 Trạm bus Đại Cồ Việt
```

---

**Generated**: November 30, 2025  
**Version**: 1.0  
**Dataset**: Hanoi Smart City Open Data  
**Total Relationships**: 84,397
