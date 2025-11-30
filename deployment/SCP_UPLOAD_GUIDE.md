# 🚀 Hướng dẫn Upload bằng SCP Command - Chi tiết từng bước

**VPS của bạn:**
- IP: `160.250.5.179`
- SSH Port: `8686`

---

## 📋 Bước 1: Kiểm tra OpenSSH trên Windows

Mở PowerShell **BÌnh thường** (không cần Administrator):

```powershell
# Kiểm tra đã có ssh/scp chưa
ssh -V
```

**Nếu thấy output như:** `OpenSSH_for_Windows_8.x` → **OK, bỏ qua bước cài đặt**

**Nếu báo lỗi:** `ssh is not recognized` → Cần cài đặt:

### Cài đặt OpenSSH (chỉ khi cần):

Mở PowerShell **as Administrator**:

```powershell
# Cài OpenSSH Client
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0

# Kiểm tra lại
ssh -V
```

---

## 📋 Bước 2: Test kết nối VPS

Trước khi upload, test xem kết nối có OK không:

```powershell
# Test SSH connection
ssh -p 8686 root@160.250.5.179
```

**Lần đầu tiên sẽ hỏi:**
```
The authenticity of host '[160.250.5.179]:8686' can't be established.
ECDSA key fingerprint is SHA256:xxxxxx.
Are you sure you want to continue connecting (yes/no)?
```

→ Gõ `yes` và Enter

**Nhập password VPS** → Enter

**Nếu vào được VPS shell:**
```
root@vps:~#
```

→ **Kết nối OK!** Gõ `exit` để thoát về Windows

**Nếu báo lỗi:** "Connection refused" hoặc "Timeout"
- Kiểm tra IP và Port có đúng không
- Kiểm tra VPS có bật SSH không
- Kiểm tra firewall VPS có mở port 8686 không

---

## 📋 Bước 3: Tạo thư mục trên VPS

```powershell
# Tạo thư mục iot-collector trên VPS
ssh -p 8686 root@160.250.5.179 "mkdir -p ~/iot-collector"
```

Nhập password → Enter

**Không có output = thành công**

---

## 📋 Bước 4: Upload files bằng SCP

### Option A: Upload từng file (Dễ debug nếu lỗi)

Mở PowerShell tại thư mục deployment:

```powershell
cd D:\OpenDataFitHou\deployment-package
```

Upload từng file:

```powershell
# File 1: iot_collector.py
scp -P 8686 iot_collector.py root@160.250.5.179:~/iot-collector/

# File 2: requirements.txt
scp -P 8686 requirements.txt root@160.250.5.179:~/iot-collector/

# File 3: docker-compose.yml
scp -P 8686 docker-compose.yml root@160.250.5.179:~/iot-collector/

# File 4: Dockerfile
scp -P 8686 Dockerfile root@160.250.5.179:~/iot-collector/

# File 5: .env.template
scp -P 8686 .env.template root@160.250.5.179:~/iot-collector/

# File 6: deploy.sh
scp -P 8686 deploy.sh root@160.250.5.179:~/iot-collector/

# File 7: README.md
scp -P 8686 README.md root@160.250.5.179:~/iot-collector/
```

**Mỗi lần nhập password VPS**, bạn sẽ thấy progress:
```
iot_collector.py    100%   85KB   1.2MB/s   00:00
```

### Option B: Upload toàn bộ cùng lúc (Nhanh hơn)

```powershell
cd D:\OpenDataFitHou\deployment-package

# Upload tất cả
scp -P 8686 -r * root@160.250.5.179:~/iot-collector/
```

**CHÚ Ý:** Chỉ nhập password **1 lần** cho tất cả files

**Expected output:**
```
iot_collector.py       100%   85KB   1.2MB/s   00:00
requirements.txt       100%  123B   0.5KB/s   00:00
docker-compose.yml     100% 1234B   5.2KB/s   00:00
Dockerfile             100%  456B   2.1KB/s   00:00
.env.template          100%  789B   3.5KB/s   00:00
deploy.sh              100% 2345B   8.9KB/s   00:00
README.md              100% 5678B  12.3KB/s   00:00
```

---

## 📋 Bước 5: Kiểm tra files đã upload

```powershell
# SSH vào VPS
ssh -p 8686 root@160.250.5.179

# Kiểm tra files
cd ~/iot-collector
ls -la
```

**Phải thấy 7 files:**
```
-rw-r--r-- 1 root root  85123 Dec  1 10:00 iot_collector.py
-rw-r--r-- 1 root root    123 Dec  1 10:00 requirements.txt
-rw-r--r-- 1 root root   1234 Dec  1 10:00 docker-compose.yml
-rw-r--r-- 1 root root    456 Dec  1 10:00 Dockerfile
-rw-r--r-- 1 root root    789 Dec  1 10:00 .env.template
-rw-r--r-- 1 root root   2345 Dec  1 10:00 deploy.sh
-rw-r--r-- 1 root root   5678 Dec  1 10:00 README.md
```

**Nếu thiếu file nào:** Upload lại file đó (Option A)

---

## 📋 Bước 6: Cấu hình và chạy

Vẫn trong VPS shell:

```bash
# Set executable cho deploy.sh
chmod +x deploy.sh

# Tạo file .env
cp .env.template .env

# Edit file .env
nano .env
```

### Điền API keys:

Di chuyển cursor bằng mũi tên, điền 3 giá trị:

```env
# 1. Generate InfluxDB token
INFLUXDB_TOKEN=<paste output của lệnh: openssl rand -base64 32>

# 2. OpenWeatherMap API Key
OPENWEATHER_API_KEY=<API key từ https://openweathermap.org/api>

# 3. Admin password
INFLUXDB_ADMIN_PASSWORD=MySecurePassword123!

# 4. Optional: OpenAQ API Key (có thể để trống)
OPENAQ_API_KEY=

# 5. Collection interval (mặc định 300s = 5 phút)
COLLECTION_INTERVAL=300
```

**Generate InfluxDB token ngay trên VPS:**
```bash
openssl rand -base64 32
```
Copy output và paste vào `INFLUXDB_TOKEN=`

**Lưu file .env:**
- Nhấn `Ctrl+X`
- Nhấn `Y` (Yes)
- Nhấn `Enter`

### Chạy deployment:

```bash
./deploy.sh
```

**Lần đầu tiên:** Script sẽ cài Docker (mất 2-3 phút)

**Output:**
```
Installing Docker...
Docker installed. Please logout and login again, then run this script again.
```

→ **Logout và login lại:**
```bash
exit
ssh -p 8686 root@160.250.5.179
cd ~/iot-collector
./deploy.sh
```

**Lần 2:** Script sẽ start services:
```
Starting services...
[+] Running 2/2
 ✔ Container influxdb        Started
 ✔ Container iot-collector   Started

Deployment complete!

Check status: docker compose ps
View logs: docker compose logs -f iot-collector

InfluxDB UI: http://160.250.5.179:8086
```

---

## 📋 Bước 7: Xác minh hoạt động

```bash
# Kiểm tra containers
docker compose ps
```

**Expected:**
```
NAME            STATUS
influxdb        Up (healthy)
iot-collector   Up (healthy)
```

```bash
# Xem logs collector
docker compose logs -f iot-collector
```

**Expected (sau 5 phút):**
```
[INFO] [2025-12-01 10:00:00] Thu thập dữ liệu từ 10 trạm...
[INFO] [2025-12-01 10:00:05] ✅ Đã ghi 40 measurements vào InfluxDB
⏳ Waiting 300 seconds until next collection...
```

**Nhấn Ctrl+C để thoát logs**

---

## 📊 Bước 8: Truy cập InfluxDB UI

1. Mở browser trên Windows
2. Vào: `http://160.250.5.179:8086`
3. Login:
   - Username: `admin`
   - Password: `<INFLUXDB_ADMIN_PASSWORD từ file .env>`
4. Click **Data Explorer**
5. Chọn bucket: `smartcity`
6. Chọn measurement: `weather` hoặc `traffic`
7. Click **Submit** → Thấy dữ liệu được thu thập

---

## ❓ Troubleshooting

### Lỗi: "Connection refused"
```powershell
# Kiểm tra VPS có chạy không
ping 160.250.5.179

# Kiểm tra port 8686
Test-NetConnection -ComputerName 160.250.5.179 -Port 8686
```

### Lỗi: "Permission denied (publickey)"
→ VPS yêu cầu password authentication
```powershell
# Thêm option để force dùng password
scp -P 8686 -o PreferredAuthentications=password file.txt root@160.250.5.179:~/
```

### Upload bị "Broken pipe" hoặc timeout
→ File quá lớn hoặc mạng không ổn định
```powershell
# Upload file nhỏ hơn trước (requirements.txt)
scp -P 8686 requirements.txt root@160.250.5.179:~/iot-collector/

# Nếu OK, upload tiếp các file khác
```

### Docker không start
```bash
# Trên VPS, kiểm tra Docker
docker --version

# Restart Docker service
sudo systemctl restart docker
sudo systemctl status docker

# Chạy lại
./deploy.sh
```

### Container không healthy
```bash
# Xem logs chi tiết
docker compose logs influxdb
docker compose logs iot-collector

# Restart
docker compose restart
```

---

## 🎯 Summary Commands

```powershell
# === Trên Windows PowerShell ===

# 1. Test connection
ssh -p 8686 root@160.250.5.179

# 2. Tạo thư mục
ssh -p 8686 root@160.250.5.179 "mkdir -p ~/iot-collector"

# 3. Upload files
cd D:\OpenDataFitHou\deployment-package
scp -P 8686 -r * root@160.250.5.179:~/iot-collector/
```

```bash
# === Trên VPS (sau khi SSH vào) ===

# 4. Cấu hình
cd ~/iot-collector
chmod +x deploy.sh
cp .env.template .env
nano .env
# (Điền API keys)

# 5. Deploy
./deploy.sh

# 6. Kiểm tra
docker compose ps
docker compose logs -f iot-collector

# 7. Thoát logs: Ctrl+C
```

---

## 🔄 Update code sau này

**Trên Windows (khi sửa iot_collector.py):**
```powershell
cd D:\OpenDataFitHou\deployment-package
scp -P 8686 iot_collector.py root@160.250.5.179:~/iot-collector/
```

**Trên VPS:**
```bash
cd ~/iot-collector
docker compose build iot-collector
docker compose restart iot-collector
```

---

**Xong! Bây giờ bạn có thể bắt đầu upload rồi! 🚀**

Nếu gặp lỗi ở bước nào, cho tôi biết error message và tôi sẽ giúp bạn debug!
