# 🚀 DockerSetUp.md

## 1. Yêu cầu hệ thống
- Đã cài [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Đã cài [Git](https://git-scm.com/downloads) (khuyến nghị)
- Đã có Python 3.9+ (nếu phát triển code Python)

## 2. Khởi động các dịch vụ

```powershell
cd D:\OpenDataFitHou

docker-compose down -v   # (nếu muốn xóa dữ liệu cũ)
docker-compose up -d     # Khởi động toàn bộ dịch vụ
```

## 3. Truy cập các dịch vụ

| Dịch vụ      | Địa chỉ truy cập           | Tài khoản mặc định         |
|--------------|---------------------------|---------------------------|
| PostgreSQL   | localhost:5432            | user: postgres / pass: postgres123 |
| InfluxDB     | http://localhost:8086     | user: admin / pass: admin123456    |
| pgAdmin      | http://localhost:8000     | email: admin@example.com / pass: admin123 |

## 4. Kết nối PostgreSQL từ pgAdmin
- Add New Server
- Host: `postgres`  | Port: `5432`
- Username: `postgres` | Password: `postgres123`

## 5. Dừng dịch vụ
```powershell
docker-compose down
```

---
**Mọi thắc mắc, kiểm tra logs bằng:**
```powershell
docker-compose logs <service>
```
Ví dụ: `docker-compose logs pgadmin`
