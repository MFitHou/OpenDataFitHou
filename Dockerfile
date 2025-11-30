# Sử dụng Python 3.9 slim để tối ưu dung lượng
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file requirements và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Thiết lập biến môi trường để Python log ra console ngay lập tức
ENV PYTHONUNBUFFERED=1
# Thêm thư mục hiện tại vào PYTHONPATH để import module dễ dàng
ENV PYTHONPATH=/app

# Lệnh chạy mặc định: Chạy scheduler
CMD ["python", "scheduler.py"]