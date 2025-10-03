# Nhật ký thay đổi

Tất cả các thay đổi đáng chú ý của dự án này sẽ được ghi lại trong file này.

Định dạng dựa trên [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
và dự án này tuân thủ [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Chưa phát hành]

### Đã thêm
- Tuân thủ header bản quyền với các yêu cầu của giấy phép GPL-3.0
- CHANGELOG.md để theo dõi các thay đổi của dự án

### Đã thay đổi
- Cải thiện cấu trúc tài liệu

## [0.0.1] - 2025-10-03
- Phát hành ban đầu
- Thiết lập dự án và cấu trúc cơ bản

## [1.0.0] - 2025-10-03
### Đã thêm
- Tích hợp Overpass API để thu thập dữ liệu địa lý từ OpenStreetMap
- Chức năng chuyển đổi dữ liệu RDF/Turtle
- Hỗ trợ nhiều loại dữ liệu:
  - Vị trí ATM (`atm.geojson`, `atm_expanded_clean.ttl`)
  - Trạm xe buýt (`bus_stop.geojson`, `bus_stop_expanded_clean.ttl`)
  - Vòi nước uống (`drinking_water.geojson`, `drinking_water_expanded_clean.ttl`)
  - Bệnh viện (`hospital.geojson`, `hospital_expanded_clean.ttl`)
  - Sân chơi (`playground.geojson`, `playgrounds_expanded_clean.ttl`)
  - Trường học (`school.geojson`, `school_expanded_clean.ttl`)
  - Nhà vệ sinh công cộng (`toilets.geojson`, `toilets_expanded_clean.ttl`)
- Jupyter notebooks để xử lý dữ liệu:
  - `OverpassApi.ipynb` - Thu thập dữ liệu từ Overpass API
  - `ParseRDF.ipynb` - Phân tích và chuyển đổi RDF
- Thư mục dữ liệu có cấu trúc:
  - `data/` - Dữ liệu định dạng GeoJSON
  - `opendata_hanoi/` - Dữ liệu định dạng RDF/Turtle
- Tài liệu dự án:
  - `README.md` với tổng quan dự án và hướng dẫn sử dụng
  - File `LICENSE` với các điều khoản GNU GPL v3.0
  - `SECURITY.md` cho chính sách bảo mật

### Chi tiết kỹ thuật
- Phạm vi địa lý: Khu vực Hà Nội (vĩ độ: 20.9-21.2, kinh độ: 105.7-106.0)
- Hỗ trợ định dạng dữ liệu: GeoJSON, RDF/Turtle
- Tích hợp với điểm cuối SPARQL của Wikidata để làm phong phú dữ liệu
- Phương pháp thu thập dữ liệu dựa trên lưới để bao phủ toàn diện

### Phụ thuộc
- `requests` - Thư viện HTTP cho các cuộc gọi API
- `pandas` - Thao tác và phân tích dữ liệu
- `rdflib` - Thư viện xử lý RDF

---

## Các loại thay đổi

- **Đã thêm** cho các tính năng mới
- **Đã thay đổi** cho các thay đổi trong chức năng hiện có
- **Đã lỗi thời** cho các tính năng sắp bị loại bỏ
- **Đã xóa** cho các tính năng đã bị loại bỏ
- **Đã sửa** cho các sửa lỗi
- **Bảo mật** cho các sửa lỗi bảo mật

## Định dạng phiên bản

Dự án này sử dụng [Semantic Versioning](https://semver.org/):
- Phiên bản **CHÍNH** khi bạn thực hiện các thay đổi API không tương thích
- Phiên bản **PHỤ** khi bạn thêm chức năng theo cách tương thích ngược
- Phiên bản **VÁ** khi bạn thực hiện các sửa lỗi tương thích ngược

## Liên kết

- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html)
