# 📂 Thư mục `opendata_hanoi`

Thư mục này chứa **dữ liệu RDF** (đuôi `.ttl`) được chuyển đổi từ các file GeoJSON trong thư mục [`data/`](../data).  
Dữ liệu được chuẩn hóa theo dạng **Linked Open Data (LOD)**, giúp dễ dàng tích hợp và truy vấn bằng **SPARQL**.

---

## 🗂 Nội dung
Mỗi file `.ttl` tương ứng với một loại đối tượng tại Hà Nội được trích xuất từ OpenStreetMap:
- `bus_stop.ttl` → dữ liệu bến xe bus.  
- `atm.ttl` → dữ liệu cây ATM.  
- `school.ttl` → dữ liệu trường học.  
- `hospital.ttl` → dữ liệu bệnh viện.  
- `playground.ttl` → dữ liệu sân chơi.  
- `toilets.ttl` → dữ liệu nhà vệ sinh công cộng.  
- `drinking_water.ttl` → dữ liệu điểm lấy nước uống.  

---

## 📌 Chuẩn RDF
- **Ngôn ngữ**: Turtle (`.ttl`).  
- **Namespace chính**:  
  - `http://opendatafithou.com/ontology/` (ontology tùy chỉnh).  
  - `rdfs`, `rdf`, `xsd` cho các khái niệm chuẩn.  

Ví dụ một resource trong RDF:
```turtle
<http://opendatafithou.com/resource/bus_stop/123456>
    a <http://opendatafithou.com/ontology/BusStop> ;
    rdfs:label "Bến xe buýt Trần Duy Hưng"@vi ;
    <http://opendatafithou.com/ontology/latitude> "21.01234"^^xsd:float ;
    <http://opendatafithou.com/ontology/longitude> "105.81234"^^xsd:float .
```
⚙️ Cách sử dụng

Load dữ liệu RDF bằng Python (rdflib):
```
from rdflib import Graph
g = Graph()
g.parse("opendata_hanoi/bus_stop.ttl", format="turtle")
print(len(g), "triples")
```

Truy vấn SPARQL ví dụ:
```
qres = g.query(
    """
    SELECT ?s ?label WHERE {
        ?s a <http://opendatafithou.com/ontology/BusStop> ;
           rdfs:label ?label .
    } LIMIT 10
    """
)
for row in qres:
    print(row)
```

Có thể nạp dữ liệu .ttl vào triplestore (Fuseki, GraphDB, Blazegraph, …) để khai thác nâng cao.

📖 Ghi chú

Dữ liệu được chuẩn hóa từ GeoJSON → RDF để phục vụ chuyển đổi số.

Các file .ttl có thể mở trực tiếp bằng editor (VSCode, Notepad++) hoặc import vào công cụ RDF.

Cấu trúc ontology có thể mở rộng khi bổ sung thêm loại dữ liệu mới.
