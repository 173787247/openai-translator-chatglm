@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo 修复 pip 并安装依赖
echo ========================================
echo.

cd /d %~dp0

echo [步骤 1/3] 修复 pip...
python -m ensurepip --upgrade
python -m pip install --upgrade pip --user -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo [步骤 2/3] 验证 pip...
python -m pip --version
if errorlevel 1 (
    echo ❌ pip 仍然有问题
    echo 请尝试: python -m ensurepip --upgrade
    pause
    exit /b 1
)
echo ✅ pip 正常

echo.
echo [步骤 3/3] 安装依赖（使用清华镜像源）...
echo.
echo 安装 Gradio...
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gradio --user

echo.
echo 安装其他依赖...
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple python-dotenv langdetect --user
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pymupdf PyPDF2 reportlab Pillow --user

echo.
echo 验证安装...
python -c "import gradio; print('✅ Gradio 安装成功，版本:', gradio.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ 验证失败，但可能已安装
    echo 请尝试运行: python test_gradio.py
) else (
    echo ✅ 所有依赖安装成功！
    echo.
    echo 现在可以运行:
    echo   python test_gradio.py  (测试)
    echo   或
    echo   python main.py  (完整应用)
)

echo.
pause

