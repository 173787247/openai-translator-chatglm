@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo 启动 OpenAI-Translator
echo ========================================
echo.

cd /d %~dp0

echo 检查依赖...
python -c "import gradio" 2>nul
if errorlevel 1 (
    echo ❌ Gradio 未安装
    echo.
    echo 请先运行: install_local.bat
    echo 或手动安装: pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gradio
    pause
    exit /b 1
)

echo ✅ 依赖检查通过
echo.
echo 启动应用...
echo 访问地址: http://localhost:7860
echo 按 Ctrl+C 停止
echo.

python main.py

pause

