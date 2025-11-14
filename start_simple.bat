@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo 启动简化测试版本
echo ========================================
echo.

cd /d %~dp0

echo 检查并安装 Gradio...
python -c "import gradio" 2>nul
if errorlevel 1 (
    echo 正在安装 Gradio（可能需要几分钟）...
    pip install gradio --quiet
)

echo.
echo 启动测试界面...
echo 浏览器将自动打开: http://localhost:7860
echo 按 Ctrl+C 停止
echo.

python test_gradio.py

pause

