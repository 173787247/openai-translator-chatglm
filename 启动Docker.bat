@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo 使用 Docker 启动（RTX 5080 GPU 支持）
echo ========================================
echo.

cd /d %~dp0

echo [提示] 根据您的 RTX 5080 配置优化
echo [提示] 使用 PyTorch CUDA 12.1 镜像
echo.

echo [步骤 1/3] 检查 Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker 未安装或未运行
    echo 请启动 Docker Desktop
    pause
    exit /b 1
)
echo [OK] Docker 已安装

echo.
echo [步骤 2/3] 检查 GPU 支持...
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Docker GPU 支持可能未配置
    echo 但继续尝试启动...
) else (
    echo [OK] Docker GPU 支持正常
)

echo.
echo [步骤 3/3] 构建并启动容器...
echo 注意: 首次构建需要下载镜像，可能需要一些时间
echo.

docker-compose up -d --build

if errorlevel 1 (
    echo.
    echo [ERROR] 启动失败
    echo 查看日志: docker-compose logs
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] 容器已启动
echo ========================================
echo.
echo 查看日志: docker-compose logs -f
echo 停止服务: docker-compose down
echo 访问应用: http://localhost:7860
echo.

timeout /t 3 >nul
start http://localhost:7860

pause

