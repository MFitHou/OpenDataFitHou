# OpenDataFitHou
Ứng dụng dữ liệu mở liên kết phục vụ chuyển đổi số - OLP PMNM 2025

## 📌 Giới thiệu
**OpenDataFitHou** là repo thu thập và xử lý **dữ liệu mở** từ nhiều nguồn khác nhau nhằm phục vụ nghiên cứu và ứng dụng trong **chuyển đổi số**.  

## 📂 Cấu trúc repo
Repo gồm các thành phần chính:
- `*.ipynb` : Notebook Jupyter dùng để xử lý, chuyển đổi và trực quan hóa dữ liệu.
- `data/` : Thư mục chứa dữ liệu **GeoJSON** thu thập từ Overpass API (OpenStreetMap).
- `opendata_hanoi/` : Các file dữ liệu đã chuyển đổi sang dạng **RDF (.ttl)**.

## 🌐 Nguồn dữ liệu
- **Overpass API (OpenStreetMap)**: Thu thập dữ liệu địa lý mở (ATM, trường học, bệnh viện, bến xe bus, v.v.).
- **Wikidata**: Trích xuất thông tin qua SPARQL Endpoint để bổ sung thông tin cho địa điểm địa lý đã thu tập được từ Overpass API.
- Các nguồn mở khác (cập nhật thêm sau).

## 🚀 Mục tiêu
- Chuẩn hóa dữ liệu mở thu thập được.
- Chuyển đổi sang **RDF/Linked Data** để dễ dàng tích hợp và liên kết.
- Phục vụ các bài toán nghiên cứu, trực quan hóa, và ứng dụng trong **chuyển đổi số**.

## 📖 Hướng dẫn sử dụng
1. Clone repo:
   ```bash
   git clone https://github.com/<username>/OpenDataFitHou.git
   cd OpenDataFitHou
