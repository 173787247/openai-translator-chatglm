# 故障排除指南

## 问题：无法访问 http://localhost:7860

### 检查步骤

#### 1. 检查应用是否在运行

```powershell
# 检查端口是否被占用
netstat -ano | findstr :7860
```

如果看到输出，说明有程序在使用 7860 端口。

#### 2. 检查依赖是否安装

```powershell
python -c "import gradio; print('OK')"
```

如果报错 `ModuleNotFoundError`，需要安装依赖。

#### 3. 安装依赖

**方法一：使用 pip（推荐）**

```powershell
pip install gradio python-dotenv langdetect
```

**方法二：使用 requirements.txt**

```powershell
pip install -r requirements.txt
```

**方法三：如果网络慢，使用国内镜像**

```powershell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gradio python-dotenv langdetect
```

#### 4. 测试 Gradio 是否能启动

运行测试脚本：

```powershell
python test_gradio.py
```

如果测试界面能打开，说明 Gradio 工作正常。

#### 5. 启动完整应用

```powershell
python main.py
```

### 常见问题

#### 问题 1: 端口被占用

**解决方案**：
- 修改 `config.py` 中的端口号
- 或关闭占用 7860 端口的程序

#### 问题 2: 依赖安装失败（网络问题）

**解决方案**：
- 使用国内镜像源
- 或使用代理
- 或手动下载 wheel 文件安装

#### 问题 3: ChatGLM 模型下载失败

**解决方案**：
- 首次运行需要下载模型（约 12GB）
- 确保网络连接稳定
- 可以使用 HuggingFace 镜像

#### 问题 4: GPU 不可用

**解决方案**：
- 检查 CUDA 是否安装
- 检查 PyTorch 是否安装了 CUDA 版本
- 如果 GPU 不可用，会自动使用 CPU（较慢）

### 快速诊断命令

```powershell
# 1. 检查 Python
python --version

# 2. 检查 Gradio
python -c "import gradio; print(gradio.__version__)"

# 3. 检查端口
netstat -ano | findstr :7860

# 4. 测试启动
python test_gradio.py
```

### 最小化启动（不依赖 ChatGLM）

如果 ChatGLM 相关依赖安装有问题，可以先测试 Gradio 界面：

```powershell
python test_gradio.py
```

这会启动一个简单的测试界面，验证 Gradio 是否正常工作。

### 联系支持

如果以上方法都无法解决，请检查：
1. Python 版本（需要 3.8+）
2. 网络连接
3. 防火墙设置
4. 错误日志信息

