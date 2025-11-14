@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo 快速启动 - 使用 Docker Pull
echo ========================================
echo.

cd /d %~dp0

echo [1/4] 拉取 Python 基础镜像...
docker pull python:3.10-slim
if errorlevel 1 (
    echo 错误: 无法拉取镜像
    echo 请检查:
    echo   1. Docker Desktop 是否运行
    echo   2. 网络连接是否正常
    echo   3. Docker Hub 是否可访问
    pause
    exit /b 1
)
echo ✅ 镜像拉取成功

echo.
echo [2/4] 停止旧容器（如果存在）...
docker-compose -f docker-compose-pull.yml down 2>nul

echo.
echo [3/4] 启动服务...
echo 注意: 首次运行需要安装依赖，可能需要几分钟
echo.
docker-compose -f docker-compose-pull.yml up -d

if errorlevel 1 (
    echo 错误: 启动失败
    echo 查看日志: docker-compose -f docker-compose-pull.yml logs
    pause
    exit /b 1
)

echo.
echo [4/4] 等待服务就绪...
timeout /t 5 >nul

echo.
echo ========================================
echo ✅ 服务已启动
echo ========================================
echo.
echo 📍 访问地址: http://localhost:7860
echo.
echo 📋 常用命令:
echo   查看日志: docker-compose -f docker-compose-pull.yml logs -f
echo   停止服务: docker-compose -f docker-compose-pull.yml down
echo   重启服务: docker-compose -f docker-compose-pull.yml restart
echo   查看状态: docker-compose -f docker-compose-pull.yml ps
echo.
echo 正在打开浏览器...
timeout /t 2 >nul
start http://localhost:7860
echo.

pause

