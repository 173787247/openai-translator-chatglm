@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo 安装 CUDA 版本的 PyTorch (RTX 5080)
echo ========================================
echo.

cd /d %~dp0

echo [步骤 1/3] 卸载 CPU 版本的 PyTorch...
pip uninstall -y torch torchvision torchaudio

echo.
echo [步骤 2/3] 安装 CUDA 12.1 版本的 PyTorch...
echo 注意: 这将下载较大的文件，请耐心等待
echo.
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

if errorlevel 1 (
    echo.
    echo [ERROR] 安装失败
    echo 请检查网络连接或使用国内镜像源
    pause
    exit /b 1
)

echo.
echo [步骤 3/3] 验证安装...
python check_cuda_local.py

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 如果 CUDA 可用，现在可以运行:
echo   python main.py
echo.

pause

