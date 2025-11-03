# 1. Giới Thiệu

## Mục Đích
Dự án này được phát triển nhằm xây dựng một hệ thống thông tin địa lý thông minh tích hợp dữ liệu từ nhiều nguồn mở (OpenStreetMap, Wikidata, RDF/SPARQL) để cung cấp các dịch vụ tra cứu, phân tích và quản lý thông tin địa điểm tại Việt Nam. Hệ thống sử dụng AI chatbot để tương tác tự nhiên với người dùng, giúp:
- **Tra cứu tiện ích xung quanh:** Tìm kiếm nhanh các địa điểm như nhà vệ sinh, ATM, bệnh viện, trạm xe buýt, nước uống, sân chơi trong bán kính nhất định.
- **Quản lý dữ liệu địa lý:** Lấy thông tin chi tiết về các thực thể địa lý, tính toán diện tích, phân tích dân số.
- **Tích hợp dữ liệu ngữ nghĩa:** Kết nối với Wikidata và RDF triple store để truy xuất thông tin có cấu trúc.
- **Xuất dữ liệu đa định dạng:** Hỗ trợ xuất dữ liệu dưới dạng XML và RDF/XML để tương thích với các hệ thống khác.

## Phạm Vi
- **Tên sản phẩm:** Opendatamap  
- **Mục tiêu chính:**
  - Cung cấp tra cứu địa điểm và tiện ích xung quanh theo vị trí.
  - Tích hợp dữ liệu mở (OSM, Wikidata, RDF/SPARQL) để tra cứu giàu ngữ nghĩa.
  - Hỗ trợ phân tích địa lý cơ bản phục vụ quản lý và ra quyết định.
  - Xuất dữ liệu và tích hợp dễ dàng với hệ thống bên ngoài.

**Những gì sản phẩm sẽ làm:**
- Tìm kiếm nhanh các tiện ích (nhà vệ sinh, ATM, bệnh viện, trạm xe buýt, nước uống, sân chơi) theo bán kính.
- Tra cứu chi tiết thực thể từ Wikidata/OSM (tọa độ, mô tả, hình ảnh, ranh giới).
- Thực thi truy vấn SPARQL, nạp/truy xuất dữ liệu RDF và xuất XML/RDF.
- Cung cấp giao diện chatbot để hỏi đáp tự nhiên về dữ liệu địa lý.

---

# 2. Mô Tả Tổng Quan (Overall Description)

## Bối cảnh sản phẩm (Product Perspective)
- **Kiến trúc:** Dịch vụ web độc lập có khả năng tích hợp vào hệ thống lớn hơn qua API/exports.
- **Tích hợp với bên thứ ba:** OpenStreetMap (OSM) để lấy địa hình và ranh giới, Wikidata để lấy dữ liệu ngữ nghĩa, RDF triple store / SPARQL (Fuseki) để lưu/truy vấn dữ liệu có cấu trúc, mô-đun chatbot để tương tác người dùng.
- **Giao diện:** Cung cấp REST API và giao diện người dùng (web/chatbot). Hỗ trợ xuất dữ liệu (XML, RDF/XML) để tích hợp với hệ thống bên ngoài.
- **Triển khai:** Có thể chạy như dịch vụ độc lập trên máy chủ/cloud hoặc đóng gói thành thành phần trong hệ thống quản lý địa lý lớn hơn.

## Chức năng sản phẩm (Product Functions)
- Tìm kiếm địa điểm theo vị trí và theo bán kính (hỗ trợ các loại: nhà vệ sinh, ATM, bệnh viện, trạm xe buýt, nước uống, sân chơi).
- Tra cứu chi tiết thực thể từ Wikidata/OSM: tọa độ, mô tả, hình ảnh, thuộc tính, ranh giới hành chính.
- Phân tích địa lý cơ bản: tính diện tích đa giác, tổng hợp dân số/diện tích theo vùng hành chính.
- Quản lý dữ liệu ngữ nghĩa: nhập/xuất RDF, thực thi truy vấn SPARQL, nạp dữ liệu từ triple store.
- Giao tiếp tự nhiên: chatbot/API hỗ trợ truy vấn bằng ngôn ngữ tự nhiên và trả về kết quả địa lý.
- Xuất dữ liệu: hỗ trợ XML/RDF/XML và định dạng chuẩn để tích hợp.

## Đặc điểm người dùng (User Characteristics)
- **Người dùng cuối (công chúng):** Giao diện đơn giản, tìm kiếm nhanh theo vị trí; không yêu cầu kiến thức kỹ thuật.
- **Nhân viên quy hoạch / phân tích dữ liệu:** Sử dụng chức năng phân tích và báo cáo; cần hiểu biết cơ bản về GIS và dữ liệu không gian.
- **Quản trị hệ thống / DevOps:** Triển khai, cấu hình nguồn dữ liệu, quản lý triple store và endpoint; yêu cầu kỹ năng về server và dữ liệu RDF/SPARQL.
- **Nhà phát triển / tích hợp hệ thống:** Dùng API để tích hợp Opendatamap vào ứng dụng khác; cần hiểu REST, JSON, RDF.
- **Nhà nghiên cứu / chuyên gia dữ liệu mở:** Khai thác dữ liệu ngữ nghĩa và thực hiện phân tích nâng cao.

## Các ràng buộc (Constraints)
- **Ràng buộc kỹ thuật:** Ví dụ: Hệ thống phải được xây dựng bằng React và NestJS, sử dụng cơ sở dữ liệu RDF/SPARQL (Apache Jena Fuseki).
- **Ràng buộc nghiệp vụ:** Phải tuân thủ quy định về bảo mật dữ liệu và cấp phép dữ liệu mở.
- **Ràng buộc giao diện:** Phải tương thích với trình duyệt Chrome và Firefox phiên bản mới nhất.

## Giả định và Phụ thuộc (Assumptions and Dependencies)
- Người dùng có kết nối internet ổn định.
- Các nguồn dữ liệu mở (Wikidata, OSM) sẵn sàng và có thể truy cập qua API/SPARQL.
- Máy chủ Fuseki hoạt động ổn định để xử lý truy vấn RDF.

---

# 3. Các yêu cầu cụ thể (Specific Requirements)

## Yêu cầu chức năng (Functional Requirements)

| **Tên Use Case** | **Mô tả ngắn** | **Tác nhân chính** | **Độ ưu tiên** |
|-------------------|----------------|--------------------|----------------|
| Tìm kiếm tiện ích xung quanh vị trí | Tìm kiếm các tiện ích (ATM, bệnh viện, nhà vệ sinh...) quanh vị trí người dùng. | Người dùng | Cao |
| Tra cứu thông tin địa điểm | Hiển thị chi tiết thông tin một địa điểm được chọn. | Người dùng | Cao |
| Lấy ranh giới hành chính | Truy xuất và hiển thị ranh giới hành chính. | Người dùng | Trung bình |
| Truy vấn dữ liệu RDF với SPARQL | Gửi và thực thi truy vấn SPARQL trên Fuseki. | Nhà phát triển | Cao |
| Tương tác với AI Chatbot | Giao tiếp tự nhiên để hỏi thông tin địa lý. | Người dùng | Trung bình |
| Xuất dữ liệu dạng RDF/XML | Tải dữ liệu RDF/XML từ hệ thống. | Người dùng | Thấp |

### UC-1: Tìm kiếm tiện ích xung quanh vị trí

| Trường | Nội dung |
|--------|---------|
| Tên Use Case | Tìm kiếm tiện ích xung quanh vị trí |
| Mục tiêu (Goal) | Người dùng tìm nhanh các POI (ATM, nhà vệ sinh, bệnh viện, trạm xe buýt, nước uống, sân chơi...) trong bán kính cho trước quanh một tọa độ. |
| Tác nhân chính | Người dùng (end-user, web UI / mobile web) |
| Mô tả ngắn gọn | Frontend gửi yêu cầu chứa `lon`/`lat` và `radiusKm` tới backend; backend truy vấn Fuseki (SPARQL) với bounding box, parse kết quả, tính khoảng cách Haversine, lọc theo radius, sắp xếp theo khoảng cách và trả JSON. |
| Điều kiện tiên quyết (Preconditions) | - Backend và Fuseki đang hoạt động và có dữ liệu RDF nạp sẵn.<br>- Frontend có quyền CORS truy cập tới backend.<br>- Người dùng cung cấp hoặc cho phép truy cập vị trí (lon, lat). |
| Trigger | Người dùng nhấn nút "Tìm quanh đây" hoặc gọi chức năng tìm kiếm trong UI với lon/lat và bán kính. |
| Luồng chính (Main Flow) | 1. Frontend gửi `GET /fuseki/{category}/nearby?lon={lon}&lat={lat}&radiusKm={r}&limit={n}`.<br>2. Backend validate các tham số (numeric, range, category hợp lệ, limit ≤ max).<br>3. Backend tính bounding box (minLon,maxLon,minLat,maxLat) từ center + radius và xây dựng SPARQL (giới hạn bằng bbox và optional amenity filter).<br>4. Backend gọi Fuseki SPARQL endpoint; nhận SPARQL JSON result.<br>5. Backend chuyển bindings thành danh sách tạm thời, parse WKT → lon/lat nếu cần.<br>6. Backend tính khoảng cách Haversine cho từng item, lọc theo `radiusKm`, sắp xếp theo khoảng cách, apply `limit`.<br>7. Backend trả JSON: `{ center: {lon,lat}, radiusKm, count, items: [ {id,label,lon,lat,distanceKm,properties...} ] }`.<br>8. Frontend hiển thị markers, popup và danh sách kèm khoảng cách. |
| Luồng thay thế (Alternative Flow) | A1. Multi-amenity: frontend gửi nhiều loại (POST composite) hoặc gọi nhiều endpoint; backend trả từng tập kết quả hoặc hợp nhất theo cấu hình.<br>A2. Category không hỗ trợ → backend trả `400 Bad Request` với message: "Unsupported category". |
| Hậu điều kiện (Postconditions) | - Frontend hiển thị các POI phù hợp trên bản đồ.<br>- Người dùng có thể chọn POI để xem chi tiết. |
| Luồng ngoại lệ (Exception Flow) | E1. Thiếu/format sai `lon`/`lat`/`radiusKm` → `400 Bad Request`.<br>E2. Fuseki không phản hồi hoặc trả lỗi → `502 Bad Gateway` (kèm thông tin ngắn).<br>E3. Dataset quá lớn/timeout → trả lỗi timeout hoặc trả partial result với cờ `partial: true` và cảnh báo. |
| Phụ thuộc / Modules liên quan | Backend: `FusekiController` endpoints `/fuseki/{category}/nearby` (controller: `fuseki.controller.ts`, service: `fuseki.service.ts`).<br>SPARQL triplestore: Apache Jena Fuseki (ENV: `FUSEKI_QUERY_ENDPOINT`).<br>Frontend: `SimpleMap.tsx` (hiển thị), `nearbyApi.ts` (utils), `rdfParser.ts`. |
| Ghi chú bổ sung | - Backend nên dùng bounding box để giảm tập dữ liệu trả về trước khi tính Haversine.<br>- Backend giới hạn `limit` tối đa (ví dụ `<= 2000`) để bảo đảm hiệu năng.<br>- Trả về khoảng cách theo km, làm tròn hợp lý (ví dụ 2 chữ số thập phân). |

### UC-2: Tra cứu thông tin địa điểm

| Trường | Nội dung |
|-------:|---------|
| Tên Use Case | Tra cứu thông tin địa điểm |
| Mục tiêu (Goal) | Người dùng xem chi tiết một thực thể địa lý (label, tọa độ, thuộc tính RDF, identifiers, liên kết Wikidata, hình ảnh, câu trích dẫn). |
| Tác nhân chính | Người dùng (web UI / mobile web) |
| Mô tả ngắn gọn | Từ marker hoặc kết quả tìm kiếm, frontend yêu cầu chi tiết (có thể kèm identifiers); hiển thị InfoPanel; nếu là relation thì hiển thị ranh giới; gọi Wikidata/Overpass khi cần. |
| Điều kiện tiên quyết (Preconditions) | - Thực thể tồn tại trong RDF dataset hoặc có identifiers OSM/Wikidata.<br>- Backend/Overpass/Wikidata có thể truy cập từ client hoặc qua backend proxy. |
| Trigger | Người dùng click vào marker hoặc chọn kết quả tìm kiếm trên UI. |
| Luồng chính (Main Flow) | 1. Frontend nhận event chọn POI; nếu metadata đã có trong state (prefetch), gọi `handleSelectLocation` nội bộ và hiển thị ngay.<br>2. Nếu thiếu metadata, frontend gọi backend `POST /fuseki/query` (hoặc frontend gọi SPARQL/Wikidata/Overpass trực tiếp nếu cho phép) để lấy triples liên quan tới subject hoặc gọi các API phụ trợ (Overpass, Wikidata) theo identifiers.<br>3. Nếu có `osmRelationId`, gọi Overpass (ví dụ `fetchOutlineByOSMRelationId`) để lấy geometry và nối ways nếu cần.<br>4. Nếu cần thông tin population/area hoặc thuộc tính ngữ nghĩa khác, gọi Wikidata SPARQL endpoint.<br>5. Parse WKT → coords, gom statements và render InfoPanel với rows chi tiết, statements, identifiers, hình ảnh và các hành động (vẽ ranh giới, export, open on Wikidata). |
| Luồng thay thế (Alternative Flow) | A1. Nếu frontend thiếu metadata và không thể gọi trực tiếp, frontend gửi `POST /fuseki/query` tới backend để lấy các triples liên quan; backend trả bindings đã gom sẵn.<br>A2. Nếu người dùng yêu cầu thêm dữ liệu (ví dụ population), frontend hoặc backend gọi Wikidata SPARQL trực tiếp/qua proxy. |
| Hậu điều kiện (Postconditions) | - InfoPanel hiển thị thông tin chi tiết, có thể kèm ranh giới/geometries.<br>- Các thao tác bổ sung (export, open Wikidata) có thể thực hiện từ panel. |
| Luồng ngoại lệ (Exception Flow) | E1. Overpass hoặc Wikidata trả lỗi/timeout → frontend hiển thị thông báo lỗi và giữ trạng thái cục bộ.<br>E2. Không tìm thấy geometry → hiển thị thông báo "Không có ranh giới" hoặc chỉ hiển thị điểm tọa độ.<br>E3. SPARQL truy vấn trả lỗi → hiển thị lỗi từ backend (nội dung hợp lý, không leak internals). |
| Phụ thuộc / Modules liên quan | Frontend: `SimpleMap.tsx`, `InfoPanel` component, `Search` component.<br>Utils: `rdfParser.ts` (chuyển triples → POI), `overpass.ts` (fetch boundary), `wikidataUtils.ts`.<br>Backend: `POST /fuseki/query` (controller: `fuseki.controller.ts`, service: `fuseki.service.ts`) khi cần truy vấn RDF từ server. |
| Ghi chú bổ sung | - Frontend có thể ưu tiên dữ liệu cục bộ nếu đã prefetch để tránh gọi API thừa.<br>- Ranh giới hành chính thường lấy từ Overpass; cần xử lý rate-limit và partial geometries.<br>- Kiểm soát hiển thị metadata nhạy cảm (nếu có). |


### UC-3: Lấy ranh giới hành chính
### UC-3: Lấy ranh giới hành chính

| Trường | Nội dung |
|--------|---------|
| Tên Use Case | Lấy ranh giới hành chính |
| Mục tiêu (Goal) | Lấy và hiển thị polygon ranh giới hành chính (OSM relation) để tính diện tích và phân tích mật độ dân số/diện tích. |
| Tác nhân chính | Người dùng (web UI) hoặc hệ thống frontend |
| Mô tả ngắn gọn | Khi có `osmRelationId`, frontend (hoặc backend proxy) gọi Overpass API lấy geom members; nối các way bằng `connectWays`, dựng polygon, tính diện tích (calculatePolygonArea) và hiển thị GeoJSON; (tuỳ) bổ sung dân số từ Wikidata. |
| Điều kiện tiên quyết (Preconditions) | - Thực thể có `osmRelationId` hợp lệ hoặc có cách map tới relation OSM.<br>- Overpass API và Wikidata có thể truy cập từ client hoặc backend proxy. |
| Trigger | Người dùng chọn "Hiển thị ranh giới" hoặc chọn một vùng có `osmRelationId` từ kết quả tìm kiếm. |
| Luồng chính (Main Flow) | 1. Frontend gửi POST tới Overpass API với query `relation(<id>); out geom;` (hoặc gọi backend proxy).<br>2. Overpass trả `elements` (members: ways/nodes/relations) kèm geometry.<br>3. Frontend gom các way có role `outer`/`inner`, nối chuỗi way thành polygon bằng `connectWays` (có thể reverse order khi cần).<br>4. Nếu polygon đóng được, tính diện tích bằng `calculatePolygonArea` và tạo GeoJSON để hiển thị trên bản đồ.<br>5. (Tùy chọn) Gọi Wikidata SPARQL để lấy `population`/`officialArea` và tính mật độ dân số.
| Luồng thay thế (Alternative Flow) | A1. Nếu Overpass trả geometry không đầy đủ, frontend thử tải từng member riêng lẻ (node, way, relation) để bổ sung.<br>A2. Nếu client không được phép gọi Overpass trực tiếp, frontend gọi backend proxy (`/overpass/proxy`) nếu backend hỗ trợ. |
| Hậu điều kiện (Postconditions) | - Ranh giới hiển thị trên bản đồ (GeoJSON/Polygon).
- Thông tin diện tích/dân số (nếu có) được cập nhật trong InfoPanel. |
| Luồng ngoại lệ (Exception Flow) | E1. Overpass rate-limit/timeout → frontend hiển thị cảnh báo và không vẽ ranh giới.
E2. Không tìm thấy relation → thông báo "Không có ranh giới".
E3. Không nối được ways thành polygon → hiển thị outline partial hoặc thông báo lỗi. |
| Phụ thuộc / Modules liên quan | Frontend utils: `overpass.ts`, `SimpleMap.tsx` (functions: `connectWays`, `calculatePolygonArea`), `InfoPanel`.
| Ghi chú bổ sung | - Nối way có thể phức tạp nếu dữ liệu thiếu/rời rạc; frontend có heuristic nối và đảo chiều way khi cần.
- Tính mật độ dân số phụ thuộc vào dữ liệu Wikidata và diện tích tính được. |


### UC-4: Truy vấn dữ liệu RDF với SPARQL

| Trường | Nội dung |
|--------|---------|
| Tên Use Case | Truy vấn dữ liệu RDF với SPARQL |
| Mục tiêu (Goal) | Cho phép nhà phát triển hoặc người dùng nâng cao thực thi SPARQL SELECT trên dataset RDF và nhận kết quả JSON. |
| Tác nhân chính | Nhà phát triển / power-user (qua UI `Query` hoặc API client) |
| Mô tả ngắn gọn | Frontend `Query` gửi SPARQL SELECT trong body tới backend `POST /fuseki/query`; backend kiểm tra là SELECT, forward tới Fuseki, nhận SPARQL JSON, map bindings→plain values và trả `{ count, data }`. |
| Điều kiện tiên quyết (Preconditions) | - Fuseki SPARQL endpoint cấu hình đúng và sẵn sàng.<br>- Backend có ENV `FUSEKI_QUERY_ENDPOINT` hoặc (`FUSEKI_BASE_URL` + `FUSEKI_DATASET`).<br>- Người dùng có quyền (nếu endpoint có auth). |
| Trigger | Người dùng nhập SPARQL SELECT trong UI Query và nhấn "Thực thi" hoặc client gửi `POST /fuseki/query`. |
| Luồng chính (Main Flow) | 1. Frontend gửi `POST /fuseki/query` với body `{ query: "<SPARQL SELECT ...>" }`.<br>2. Backend validate: `query` không rỗng, chứa `SELECT` (regex/parse check), and length within acceptable limit.<br>3. Backend gọi Fuseki (GET `?query=...` hoặc POST) với header `Accept: application/sparql-results+json` và Authorization nếu cấu hình.<br>4. Fuseki trả SPARQL JSON; backend map kết quả về array of bindings → plain values (convert datatypes/lang tags) và trả `{ count, data }`.<br>5. Frontend hiển thị kết quả dạng table/JSON và hỗ trợ download/export. |
| Luồng thay thế (Alternative Flow) | A1. Người dùng yêu cầu LIMIT/OFFSET → họ chỉnh query và backend forward nguyên văn.<br>A2. Non-SELECT query (CONSTRUCT/ASK/UPDATE) → backend trả `400 Bad Request` theo design. |
| Hậu điều kiện (Postconditions) | Người dùng nhận kết quả SPARQL và có thể export/inspect. |
| Luồng ngoại lệ (Exception Flow) | E1. Nếu `query` không chứa `SELECT` → backend trả `400` với message "Chỉ hỗ trợ SELECT SPARQL".
E2. Fuseki trả lỗi / auth fail → backend trả `502` hoặc `401` tương ứng.
E3. SPARQL syntax error → backend chuyển lỗi từ Fuseki cho client (message user-friendly). |
| Phụ thuộc / Modules liên quan | Backend: `POST /fuseki/query` (controller/service: `src/fuseki/*`).
| Ghi chú bổ sung | - Backend chặn non-SELECT để tránh thao tác thay đổi dữ liệu.
- Service đã map `binding.value` → plain values; nên chuẩn hoá response schema (JSON Schema / OpenAPI). |



### UC-5: Tương tác với AI Chatbot

| Trường | Nội dung |
|--------|---------|
| Tên Use Case | Tương tác với AI Chatbot |
| Mục tiêu (Goal) | Người dùng tương tác bằng ngôn ngữ tự nhiên để hỏi về POI, ranh giới, thống kê — nhận câu trả lời dạng văn bản và (tuỳ chọn) các hành động trên bản đồ. |
| Tác nhân chính | Người dùng (chat UI) |
| Mô tả ngắn gọn | Người dùng gửi câu hỏi; chatbot phân tích intent, dịch sang truy vấn nội bộ (REST/SPARQL/Overpass), thu thập dữ liệu, và trả về câu trả lời có thể kèm link/marker/GeoJSON để frontend hiển thị. |
| Điều kiện tiên quyết (Preconditions) | - Mô-đun chatbot (nội bộ hoặc external LLM wrapper) được cấu hình và có quyền gọi API backend.<br>- Backend và Fuseki/Overpass/Wikidata sẵn sàng. |
| Trigger | Người dùng gửi tin nhắn qua giao diện chatbot. |
| Luồng chính (Main Flow) | 1. Frontend gửi message tới chatbot service (backend module hoặc external LLM wrapper).<br>2. Chatbot/NLU phân tích intent (ví dụ: "Tìm ATM gần tôi 500m").<br>3. Chatbot chuyển intent thành API call(s): gọi `/fuseki/atms/nearby` hoặc `POST /fuseki/query` hoặc Overpass tùy intent.<br>4. Chatbot thu thập kết quả, tổng hợp văn bản trả lời và có thể đính kèm dữ liệu (top N POI, GeoJSON).<br>5. Frontend nhận reply, hiển thị trong chat; nếu có geo data, frontend vẽ markers/polygons và cho phép tương tác. |
| Luồng thay thế (Alternative Flow) | A1. Nếu chatbot không tự động chuyển thành API calls, forward raw question cho backend để backend thực hiện NLU/NLP.<br>A2. Nếu cần xác nhận intent, chatbot hỏi lại user trước khi gọi API. |
| Hậu điều kiện (Postconditions) | - Người dùng nhận câu trả lời ngắn gọn và chính xác hoặc yêu cầu làm rõ.<br>- Bản đồ có thể cập nhật markers/outline theo yêu cầu. |
| Luồng ngoại lệ (Exception Flow) | E1. LLM/chat service trả lỗi hoặc quá tải → frontend hiển thị thông báo lỗi tạm thời.<br>E2. Intent không rõ → chatbot yêu cầu làm rõ.<br>E3. API phụ trợ trả lỗi → chatbot trả thông báo "không thể truy xuất dữ liệu". |
| Phụ thuộc / Modules liên quan | Chatbot module (nội bộ/external LLM wrapper); Backend endpoints: nearby endpoints, `POST /fuseki/query`; Frontend chat UI và `SimpleMap` để hiển thị kết quả. |
| Ghi chú bổ sung | - Repo đề cập chatbot trong SRS/README nhưng không có module cụ thể; cần triển khai riêng hoặc tích hợp dịch vụ LLM ngoài với proxy backend để bảo mật.<br>- Cần kiểm soát rate limit và bảo mật khi gọi LLM/third-party APIs. |

### UC-6: Xuất dữ liệu dạng RDF/XML

| Trường | Nội dung |
|--------|---------|
| Tên Use Case | Xuất dữ liệu dạng RDF/XML |
| Mục tiêu (Goal) | Người dùng (hoặc hệ thống) xuất dữ liệu RDF hiện có sang định dạng RDF/XML (hoặc XML) để chia sẻ hoặc tích hợp với hệ thống khác. |
| Tác nhân chính | Người dùng (power-user) hoặc hệ thống tích hợp |
| Mô tả ngắn gọn | Dữ liệu RDF có thể được xuất trực tiếp từ file `.ttl` (offline) hoặc trích xuất từ Fuseki và chuyển đổi sang RDF/XML bằng công cụ (Fuseki export, rdflib); kết quả trả về là file RDF/XML để tải về. |
| Điều kiện tiên quyết (Preconditions) | - Dữ liệu đã được nạp vào Fuseki hoặc có file `.ttl` trong `opendata_hanoi`.<br>- Hệ thống có công cụ/chức năng chuyển đổi Turtle → RDF/XML (rdflib script hoặc Fuseki export). |
| Trigger | Người dùng chọn "Export RDF/XML" trong UI hoặc gọi API export. |
| Luồng chính (Main Flow) | Option A (offline): Admin tải file `.ttl` từ `opendata_hanoi` và dùng script (rdflib) để convert sang RDF/XML, rồi cung cấp link download.<br>Option B (via Fuseki): Frontend/backend gọi Fuseki admin/export hoặc thực hiện SPARQL `CONSTRUCT` để trích graph; backend convert sang RDF/XML và trả file (Content-Type: `application/rdf+xml`).<br>Client nhận file và tải về. |
| Luồng thay thế (Alternative Flow) | A1. Nếu backend không có chức năng convert, cung cấp file `.ttl` thô để user xử lý offline.<br>A2. Nếu dataset quá lớn, backend cung cấp export theo phân đoạn hoặc stream. |
| Hậu điều kiện (Postconditions) | Người dùng nhận file RDF/XML tương thích; có thể download link hoặc stream. |
| Luồng ngoại lệ (Exception Flow) | E1. Conversion thất bại → trả lỗi `500` với lý do; E2. Fuseki không cho phép export → trả `403/401`; E3. File quá lớn → trả `413` hoặc cung cấp phân đoạn/stream. |
| Phụ thuộc / Modules liên quan | Data sources: `opendata_hanoi/*.ttl`, Fuseki triplestore (admin/export).<br>Backend: cần endpoint export (ví dụ `GET /fuseki/export?format=rdfxml`) hoặc script trong `tools` để convert. |
| Ghi chú bổ sung | - Repo hiện chứa `.ttl` files nhưng không có endpoint export; đề xuất thêm `GET /fuseki/export?format=rdfxml` hoặc script chuyển đổi trong `tools`.<br>- Kiểm soát quyền truy cập export nếu dữ liệu nhạy cảm. |


---

## Yêu cầu phi chức năng (Non-Functional Requirements)
- **Hiệu năng:** Truy vấn SPARQL phản hồi dưới 3 giây cho dataset trung bình.  
- **Khả năng mở rộng:** Cho phép mở rộng dữ liệu và triển khai thêm các tỉnh/thành khác.  
- **Bảo mật:** Chỉ định quyền truy cập API; không cho phép sửa dữ liệu RDF công khai.  
- **Khả năng tương thích:** Hoạt động tốt trên các trình duyệt phổ biến (Chrome, Firefox, Edge).  
- **Mã nguồn mở:** Phát hành dưới giấy phép MIT, công khai trên GitHub.

## Yêu cầu giao diện bên ngoài (External Interface Requirements)
- **Giao diện người dùng (UI):** Giao diện bản đồ sử dụng Leaflet.js; bố cục trực quan, hiển thị marker và panel thông tin.  
- **Giao diện phần mềm (API):** REST API cho các chức năng: tìm kiếm tiện ích, truy vấn SPARQL, xuất RDF/XML, tương tác chatbot.  
- **Cơ sở dữ liệu:** Apache Jena Fuseki triple store lưu dữ liệu RDF, hỗ trợ SPARQL endpoint.

---

*Phiên bản: 1.0.0*  
*Tài liệu SRS cho hệ thống Opendatamap*

