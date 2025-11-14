@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo 查看容器日志
echo ========================================
echo.
echo 按 Ctrl+C 退出日志查看
echo.

cd /d %~dp0
docker-compose logs -f

