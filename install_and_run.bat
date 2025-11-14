@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo OpenAI-Translator v2.0 安装并启动
echo ========================================
echo.

cd /d %~dp0

echo [步骤 1/3] 检查 Python...
python --version
if errorlevel 1 (
    echo 错误: Python 未安装
    pause
    exit /b 1
)

echo.
echo [步骤 2/3] 安装必要依赖（这可能需要几分钟）...
echo 正在安装 Gradio...
pip install gradio --quiet --disable-pip-version-check
if errorlevel 1 (
    echo 警告: Gradio 安装可能失败，继续尝试...
)

echo 正在安装其他基础依赖...
pip install python-dotenv langdetect --quiet --disable-pip-version-check

echo.
echo [步骤 3/3] 启动应用...
echo.
echo ========================================
echo 应用正在启动...
echo 请稍候，首次运行可能需要下载模型
echo ========================================
echo.
echo 应用地址: http://localhost:7860
echo 按 Ctrl+C 停止服务
echo.

python main.py

pause

