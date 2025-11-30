# Setup Script - Prepare Deployment Package

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "OpenDataFitHou Deployment Setup" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

$deploymentDir = "D:\OpenDataFitHou\deployment"
$packageDir = "D:\OpenDataFitHou\deployment-package"

# Tạo thư mục package
Write-Host "[1/3] Creating deployment package directory..." -ForegroundColor Yellow
if (Test-Path $packageDir) {
    Remove-Item -Recurse -Force $packageDir
}
New-Item -ItemType Directory -Path $packageDir | Out-Null

# Copy 7 files
Write-Host "[2/3] Copying files..." -ForegroundColor Yellow
$files = @(
    "iot_collector.py",
    "requirements.txt",
    "docker-compose.yml",
    "Dockerfile",
    ".env.template",
    "deploy.sh",
    "README.md"
)

foreach ($file in $files) {
    $sourcePath = Join-Path $deploymentDir $file
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination $packageDir
        Write-Host "  OK Copied: $file" -ForegroundColor Green
    } else {
        Write-Host "  X Missing: $file" -ForegroundColor Red
    }
}

# Tạo file ZIP
Write-Host "[3/3] Creating ZIP file..." -ForegroundColor Yellow
$zipPath = "D:\OpenDataFitHou\iot-collector-deployment.zip"
if (Test-Path $zipPath) {
    Remove-Item -Force $zipPath
}
Compress-Archive -Path "$packageDir\*" -DestinationPath $zipPath -CompressionLevel Optimal

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "OK Deployment package ready!" -ForegroundColor Green
Write-Host "================================`n" -ForegroundColor Cyan

Write-Host "Package location:" -ForegroundColor Yellow
Write-Host "  Folder: $packageDir" -ForegroundColor White
Write-Host "  ZIP:    $zipPath`n" -ForegroundColor White

Write-Host "Your VPS Info:" -ForegroundColor Yellow
Write-Host "  IP:   160.250.5.179" -ForegroundColor White
Write-Host "  Port: 8686`n" -ForegroundColor White

Write-Host "Upload via WinSCP:" -ForegroundColor Yellow
Write-Host "  1. Download WinSCP: https://winscp.net" -ForegroundColor White
Write-Host "  2. Connect to: 160.250.5.179:8686" -ForegroundColor White
Write-Host "  3. Create folder: ~/iot-collector" -ForegroundColor White
Write-Host "  4. Upload 7 files from: $packageDir`n" -ForegroundColor White

Write-Host "Upload via SCP command:" -ForegroundColor Yellow
Write-Host "  scp -P 8686 -r $packageDir\* root@160.250.5.179:~/iot-collector/`n" -ForegroundColor Cyan

Write-Host "Upload ZIP file:" -ForegroundColor Yellow
Write-Host "  scp -P 8686 $zipPath root@160.250.5.179:~/" -ForegroundColor Cyan
Write-Host "  ssh -p 8686 root@160.250.5.179" -ForegroundColor Cyan
Write-Host "  unzip iot-collector-deployment.zip -d ~/iot-collector" -ForegroundColor Cyan
Write-Host "  cd ~/iot-collector; chmod +x deploy.sh; ./deploy.sh`n" -ForegroundColor Cyan

Write-Host "See UPLOAD_TO_YOUR_VPS.md for detailed instructions!" -ForegroundColor Green
Write-Host ""
