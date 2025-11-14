@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo 使用 Docker 启动 OpenAI-Translator
echo ========================================
echo.

cd /d %~dp0

echo [步骤 1/3] 拉取 Python 基础镜像...
docker pull python:3.10-slim
if errorlevel 1 (
    echo ❌ 镜像拉取失败
    echo 尝试使用国内镜像源...
    echo 请检查网络连接或 Docker 配置
    pause
    exit /b 1
)

echo ✅ 镜像拉取成功
echo.

echo [步骤 2/3] 检查 GPU 支持...
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo ⚠️  GPU 可能不可用，将使用 CPU 模式
    echo 修改 docker-compose-simple.yml，移除 GPU 配置
) else (
    echo ✅ GPU 支持正常
)

echo.
echo [步骤 3/3] 启动服务...
echo.
echo 服务将在后台启动
echo 查看日志: docker-compose -f docker-compose-simple.yml logs -f
echo 停止服务: docker-compose -f docker-compose-simple.yml down
echo.

docker-compose -f docker-compose-simple.yml up -d

echo.
echo 等待服务启动（首次运行需要安装依赖，可能需要几分钟）...
timeout /t 10

echo.
echo 检查服务状态...
docker-compose -f docker-compose-simple.yml ps

echo.
echo ========================================
echo 如果服务运行正常，访问: http://localhost:7860
echo ========================================
echo.
echo 查看实时日志:
echo   docker-compose -f docker-compose-simple.yml logs -f
echo.

pause

