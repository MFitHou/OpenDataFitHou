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

## � Yêu cầu hệ thống
- **Python**: 3.8 hoặc mới hơn
- **Jupyter**: Để chạy các notebook
- **Git**: Để clone repository

## �📖 Hướng dẫn cài đặt và sử dụng

### 1️⃣ Clone Repository
```bash
git clone https://github.com/MFitHou/OpenDataFitHou.git
cd OpenDataFitHou
```

### 2️⃣ Thiết lập môi trường Python

#### Sử dụng Virtual Environment (Khuyến nghị)
```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### Hoặc sử dụng Conda
```bash
# Tạo môi trường conda mới
conda create -n opendatafit python=3.9
conda activate opendatafit
```

### 3️⃣ Cài đặt Dependencies
```bash
# Cài đặt tất cả packages cần thiết
pip install -r requirements.txt

# Hoặc cài đặt từng package:
pip install requests pandas rdflib jupyter notebook matplotlib folium geopandas
```

### 4️⃣ Chạy Jupyter Notebooks

#### Khởi động Jupyter Notebook
```bash
jupyter notebook
```

#### Hoặc sử dụng Jupyter Lab
```bash
pip install jupyterlab
jupyter lab
```

### 5️⃣ Sử dụng dữ liệu

#### A. Thu thập dữ liệu mới
1. Mở `OverpassApi.ipynb`
2. Chạy từng cell để thu thập dữ liệu từ Overpass API
3. Dữ liệu GeoJSON sẽ được lưu trong thư mục `data/`

#### B. Chuyển đổi sang RDF
1. Mở `ParseRDF.ipynb`  
2. Chạy notebook để chuyển đổi GeoJSON thành RDF/Turtle
3. Dữ liệu RDF sẽ được lưu trong thư mục `opendata_hanoi/`

#### C. Sử dụng dữ liệu RDF
```python
from rdflib import Graph

# Load dữ liệu RDF
g = Graph()
g.parse("opendata_hanoi/bus_stop_expanded_clean.ttl", format="turtle")

# Thực hiện truy vấn SPARQL
query = """
    SELECT ?name ?lat ?lon WHERE {
        ?stop a <http://example.org/BusStop> ;
              <http://example.org/name> ?name ;
              <http://example.org/latitude> ?lat ;
              <http://example.org/longitude> ?lon .
    }
    LIMIT 10
"""
results = g.query(query)
for row in results:
    print(f"Bus Stop: {row.name}, Lat: {row.lat}, Lon: {row.lon}")
```

## 🖥 Triển khai với Apache Jena Fuseki

### Cài đặt Fuseki Server
```bash
# Download Jena Fuseki
wget https://downloads.apache.org/jena/binaries/apache-jena-fuseki-4.9.0.tar.gz
tar -xzf apache-jena-fuseki-4.9.0.tar.gz
cd apache-jena-fuseki-4.9.0
```

### Khởi động Fuseki với dữ liệu
```bash
# Khởi động Fuseki server
./fuseki-server --update --mem /dataset

# Upload dữ liệu RDF qua web interface tại: http://localhost:3030
```

### Truy vấn SPARQL
Truy cập `http://localhost:3030` và sử dụng SPARQL endpoint để truy vấn dữ liệu.

## 📊 Cấu trúc dữ liệu có sẵn

### GeoJSON Files (thư mục `data/`)
- `atm.geojson` - Vị trí ATM
- `bus_stop.geojson` - Trạm xe bus  
- `drinking_water.geojson` - Điểm nước uống
- `hospital.geojson` - Bệnh viện
- `playground.geojson` - Sân chơi
- `school.geojson` - Trường học
- `toilets.geojson` - Nhà vệ sinh công cộng

### RDF/Turtle Files (thư mục `opendata_hanoi/`)
Tất cả dữ liệu GeoJSON đã được chuyển đổi sang định dạng RDF với suffix `_expanded_clean.ttl`

## 🔧 Script tự động hóa

### Cài đặt tự động
Dự án cung cấp các script để tự động hóa quá trình cài đặt:

#### Windows
```cmd
setup.bat
```

#### macOS/Linux  
```bash
chmod +x setup.sh
./setup.sh
```

### Khởi động nhanh
Sau khi cài đặt, sử dụng script khởi động nhanh:

#### Windows
```cmd
start.bat
```

#### macOS/Linux
```bash  
chmod +x start.sh
./start.sh
```

## 🐛 Xử lý sự cố

### Lỗi thường gặp

**1. Python không được tìm thấy**
- Đảm bảo Python 3.8+ đã được cài đặt
- Thêm Python vào PATH environment variable

**2. Pip install thất bại**  
```bash
# Nâng cấp pip lên phiên bản mới nhất
python -m pip install --upgrade pip

# Cài đặt với cache clear
pip install --no-cache-dir -r requirements.txt
```

**3. Jupyter không khởi động được**
```bash
# Cài đặt lại Jupyter
pip uninstall jupyter notebook
pip install jupyter notebook

# Hoặc sử dụng JupyterLab
pip install jupyterlab
jupyter lab
```

**4. Import error cho các package**
```bash
# Kiểm tra virtual environment đã được kích hoạt
# Windows: venv\Scripts\activate.bat  
# macOS/Linux: source venv/bin/activate

# Cài đặt lại dependencies
pip install -r requirements.txt
```

