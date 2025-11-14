@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo 启动完整应用（ChatGLM 翻译功能）
echo ========================================
echo.

cd /d %~dp0

echo [提示] 首次运行需要下载 ChatGLM2-6B 模型（约 12GB）
echo [提示] 下载可能需要较长时间，请耐心等待
echo [提示] 模型下载后会自动缓存，下次启动无需重新下载
echo.

echo 检查依赖...
python -c "import gradio" 2>nul
if errorlevel 1 (
    echo [ERROR] Gradio 未安装
    echo 请先运行: install_local.bat
    pause
    exit /b 1
)

echo [OK] 依赖检查通过
echo.
echo ========================================
echo 正在启动完整应用...
echo ========================================
echo.
echo 访问地址: http://localhost:7860
echo.
echo 注意：
echo   - 首次运行需要下载模型（约 12GB）
echo   - 下载完成后会自动加载模型
echo   - 加载完成后即可使用翻译功能
echo.
echo 按 Ctrl+C 停止服务
echo.

python main.py

pause

