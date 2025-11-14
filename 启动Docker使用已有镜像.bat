@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo 使用已有镜像启动（RTX 5080）
echo ========================================
echo.

cd /d %~dp0

echo [检查] 使用已有镜像: pytorch/pytorch:2.7.0-cuda12.8-cudnn9-devel
echo [检查] 该镜像支持 CUDA 12.8，完全兼容 RTX 5080
echo.

echo [步骤 1/2] 检查 Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker 未运行
    echo 请启动 Docker Desktop
    pause
    exit /b 1
)
echo [OK] Docker 运行中

echo.
echo [步骤 2/2] 启动容器...
echo 注意: 首次运行需要安装依赖，可能需要几分钟
echo.

docker-compose up -d

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

echo 等待服务就绪（首次需要安装依赖）...
timeout /t 10 >nul

echo 正在打开浏览器...
start http://localhost:7860

echo.
pause

