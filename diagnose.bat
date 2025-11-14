@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo 诊断脚本
echo ========================================
echo.

cd /d %~dp0

echo [1] 检查 Python...
python --version
if errorlevel 1 (
    echo ❌ Python 未安装
    goto :end
) else (
    echo ✅ Python 已安装
)

echo.
echo [2] 检查 Gradio...
python -c "import gradio; print('✅ Gradio 版本:', gradio.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ Gradio 未安装
    echo.
    echo 正在尝试安装 Gradio（使用清华镜像源）...
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gradio --quiet
    python -c "import gradio; print('✅ Gradio 安装成功，版本:', gradio.__version__)" 2>nul
    if errorlevel 1 (
        echo ❌ Gradio 安装失败
        echo.
        echo 请手动安装: pip install gradio
        echo 或使用镜像: pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gradio
    )
) else (
    echo ✅ Gradio 已安装
)

echo.
echo [3] 检查端口 7860...
netstat -ano | findstr :7860 >nul
if errorlevel 1 (
    echo ✅ 端口 7860 可用
) else (
    echo ⚠️  端口 7860 已被占用
    netstat -ano | findstr :7860
)

echo.
echo [4] 检查其他依赖...
python -c "import dotenv; print('✅ python-dotenv 已安装')" 2>nul || echo ❌ python-dotenv 未安装
python -c "import langdetect; print('✅ langdetect 已安装')" 2>nul || echo ❌ langdetect 未安装

echo.
echo ========================================
echo 诊断完成
echo ========================================
echo.
echo 如果所有检查都通过，可以运行:
echo   python main.py
echo 或
echo   python test_gradio.py  (测试版本)
echo.

:end
pause

