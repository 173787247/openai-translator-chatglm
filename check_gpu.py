"""
GPU 检查脚本
用于验证 GPU 和 CUDA 是否可用
"""
import sys
import os
# 设置 UTF-8 编码
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')

def check_gpu():
    """检查 GPU 和 CUDA 支持"""
    print("=" * 50)
    print("GPU 和 CUDA 检查")
    print("=" * 50)
    
    # 检查 PyTorch
    try:
        import torch
        print(f"✅ PyTorch 版本: {torch.__version__}")
    except ImportError:
        print("❌ PyTorch 未安装")
        return False
    
    # 检查 CUDA 可用性
    cuda_available = torch.cuda.is_available()
    print(f"CUDA 可用: {'✅ 是' if cuda_available else '❌ 否'}")
    
    if cuda_available:
        # GPU 信息
        print(f"CUDA 版本: {torch.version.cuda}")
        print(f"cuDNN 版本: {torch.backends.cudnn.version()}")
        print(f"GPU 数量: {torch.cuda.device_count()}")
        
        for i in range(torch.cuda.device_count()):
            print(f"\nGPU {i}:")
            print(f"  名称: {torch.cuda.get_device_name(i)}")
            print(f"  显存: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.2f} GB")
            print(f"  计算能力: {torch.cuda.get_device_properties(i).major}.{torch.cuda.get_device_properties(i).minor}")
        
        # 测试 GPU 计算
        try:
            x = torch.randn(3, 3).cuda()
            y = torch.randn(3, 3).cuda()
            z = x @ y
            print("\n✅ GPU 计算测试通过")
        except Exception as e:
            print(f"\n❌ GPU 计算测试失败: {str(e)}")
            return False
    else:
        print("\n⚠️  警告: CUDA 不可用，将使用 CPU 模式")
        print("   如果您的设备有 GPU，请检查：")
        print("   1. NVIDIA 驱动是否已安装")
        print("   2. CUDA 工具包是否已安装")
        print("   3. PyTorch 是否安装了 CUDA 版本")
    
    print("=" * 50)
    return cuda_available

if __name__ == "__main__":
    success = check_gpu()
    sys.exit(0 if success else 1)

