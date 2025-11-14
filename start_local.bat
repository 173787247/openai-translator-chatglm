@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo OpenAI-Translator v2.0 启动脚本
echo ========================================
echo.

cd /d %~dp0

echo [1/3] 检查 Python 环境...
python --version
if errorlevel 1 (
    echo 错误: Python 未安装或不在 PATH 中
    pause
    exit /b 1
)

echo.
echo [2/3] 检查依赖...
python -c "import gradio; import torch; print('依赖检查通过')" 2>nul
if errorlevel 1 (
    echo 警告: 部分依赖可能未安装
    echo 正在安装依赖...
    pip install -r requirements.txt
)

echo.
echo [3/3] 启动应用...
echo.
echo 应用将在浏览器中自动打开: http://localhost:7860
echo 按 Ctrl+C 停止服务
echo.

python main.py

pause

