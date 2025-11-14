"""
检查本地 CUDA 支持（RTX 5080）
"""
import sys
import os

# 设置 UTF-8 编码
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')

print("=" * 60)
print("CUDA 和 GPU 检查（RTX 5080）")
print("=" * 60)
print()

# 检查 PyTorch
try:
    import torch
    print(f"[OK] PyTorch 版本: {torch.__version__}")
except ImportError:
    print("[ERROR] PyTorch 未安装")
    print()
    print("解决方案:")
    print("1. 安装 CUDA 版本的 PyTorch:")
    print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
    print()
    print("2. 或使用 Docker（推荐）:")
    print("   docker-compose up -d --build")
    sys.exit(1)

# 检查 CUDA
cuda_available = torch.cuda.is_available()
print(f"[{'OK' if cuda_available else 'WARNING'}] CUDA 可用: {cuda_available}")

if cuda_available:
    print(f"[OK] CUDA 版本: {torch.version.cuda}")
    print(f"[OK] cuDNN 版本: {torch.backends.cudnn.version()}")
    print(f"[OK] GPU 数量: {torch.cuda.device_count()}")
    print()
    
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}:")
        props = torch.cuda.get_device_properties(i)
        print(f"  名称: {props.name}")
        print(f"  显存: {props.total_memory / 1024**3:.2f} GB")
        print(f"  计算能力: {props.major}.{props.minor}")
    
    print()
    print("测试 GPU 计算...")
    try:
        x = torch.randn(3, 3).cuda()
        y = torch.randn(3, 3).cuda()
        z = x @ y
        print("[OK] GPU 计算测试通过")
        print()
        print("=" * 60)
        print("[SUCCESS] CUDA 配置正常，可以使用 GPU 加速！")
        print("=" * 60)
    except Exception as e:
        print(f"[ERROR] GPU 计算测试失败: {str(e)}")
        print()
        print("可能的原因:")
        print("1. PyTorch 安装的是 CPU 版本")
        print("2. CUDA 驱动版本不匹配")
        print("3. GPU 驱动未正确安装")
else:
    print()
    print("=" * 60)
    print("[WARNING] CUDA 不可用")
    print("=" * 60)
    print()
    print("可能的原因:")
    print("1. PyTorch 安装的是 CPU 版本（最常见）")
    print("2. NVIDIA 驱动未安装或版本不匹配")
    print("3. CUDA 工具包未安装")
    print()
    print("解决方案:")
    print()
    print("方案一：安装 CUDA 版本的 PyTorch（本地）")
    print("  pip uninstall torch torchvision torchaudio")
    print("  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
    print()
    print("方案二：使用 Docker（推荐，已配置好）")
    print("  docker-compose up -d --build")
    print()
    print("方案三：检查 NVIDIA 驱动")
    print("  运行: nvidia-smi")
    print("  如果无法运行，请安装最新 NVIDIA 驱动")

print()

