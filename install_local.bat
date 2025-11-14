@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo 本地安装脚本（使用国内镜像源）
echo ========================================
echo.

cd /d %~dp0

echo [步骤 1/4] 检查 Python...
python --version
if errorlevel 1 (
    echo ❌ Python 未安装
    pause
    exit /b 1
)
echo ✅ Python 已安装

echo.
echo [步骤 2/4] 升级 pip...
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo [步骤 3/4] 安装基础依赖（使用清华镜像源）...
echo 正在安装 Gradio...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gradio --quiet --disable-pip-version-check
if errorlevel 1 (
    echo ⚠️  Gradio 安装可能有问题，继续...
)

echo 正在安装其他依赖...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple python-dotenv langdetect --quiet --disable-pip-version-check
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pymupdf PyPDF2 reportlab Pillow --quiet --disable-pip-version-check

echo.
echo [步骤 4/4] 验证安装...
python -c "import gradio; print('✅ Gradio 安装成功，版本:', gradio.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ Gradio 安装失败
    echo.
    echo 请尝试手动安装:
    echo   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gradio
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 安装完成！
echo ========================================
echo.
echo 现在可以运行:
echo   python test_gradio.py  (测试界面)
echo   或
echo   python main.py  (完整应用)
echo.

pause

