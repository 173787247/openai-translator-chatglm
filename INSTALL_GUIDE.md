# 安装指南

## 当前状态诊断

根据检查，您的环境：
- ✅ Python 3.13.7 已安装
- ❌ Gradio 未安装
- ✅ 端口 7860 可用

## 快速安装步骤

### 方法一：使用国内镜像源（推荐，速度快）

```powershell
cd C:\Users\rchua\Desktop\AIFullStackDevelopment\openai-translator-chatglm

# 安装基础依赖
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gradio python-dotenv langdetect

# 如果需要完整功能，安装所有依赖
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### 方法二：使用官方源

```powershell
pip install gradio python-dotenv langdetect
```

### 方法三：使用诊断脚本

运行诊断脚本，它会自动尝试安装：

```powershell
diagnose.bat
```

## 启动应用

### 步骤 1: 测试 Gradio（推荐先测试）

```powershell
python test_gradio.py
```

如果测试界面能打开（http://localhost:7860），说明 Gradio 工作正常。

### 步骤 2: 启动完整应用

```powershell
python main.py
```

**注意**：首次运行会下载 ChatGLM2-6B 模型（约 12GB），需要：
- 稳定的网络连接
- 足够的磁盘空间
- 可能需要较长时间

## 如果网络很慢

### 使用代理

```powershell
# 设置代理（如果使用）
set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890

pip install gradio python-dotenv langdetect
```

### 手动下载安装包

1. 访问 https://pypi.org/project/gradio/
2. 下载 wheel 文件
3. 本地安装：`pip install gradio-*.whl`

## 验证安装

运行诊断脚本：

```powershell
diagnose.bat
```

或手动检查：

```powershell
python -c "import gradio; print('Gradio 版本:', gradio.__version__)"
```

## 常见问题

### Q: pip install 一直超时

**A**: 使用国内镜像源：
```powershell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gradio
```

### Q: 安装后还是无法访问

**A**: 
1. 检查应用是否真的在运行
2. 查看是否有错误信息
3. 尝试使用 `test_gradio.py` 测试

### Q: 端口被占用

**A**: 修改 `config.py` 中的 `GRADIO_SERVER_PORT` 为其他端口（如 7861）

## 下一步

安装完成后：
1. 运行 `diagnose.bat` 验证环境
2. 运行 `python test_gradio.py` 测试界面
3. 运行 `python main.py` 启动完整应用

