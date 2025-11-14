# OpenAI-Translator v2.0 (PDF电子书翻译工具)

基于 ChatGLM2-6B 的智能翻译工具，支持 PDF 电子书翻译和文本翻译，提供友好的图形化界面。

## ✨ 特性

- 🤖 **基于 ChatGLM2-6B**：使用强大的中文大语言模型
- 📚 **PDF 翻译**：支持 PDF 电子书翻译，保留文档结构
- 📝 **文本翻译**：支持单文本和多文本翻译
- 🌐 **多语言支持**：支持 15+ 种语言
- 💻 **图形化界面**：基于 Gradio 的现代化界面
- 🚀 **GPU 加速**：支持 CUDA 加速（如果可用）

## 📦 安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd openai-translator-chatglm
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

**注意**：如果使用 GPU，确保已安装 CUDA 版本的 PyTorch：

```bash
# CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 3. 配置环境变量（可选）

复制 `env.example` 为 `.env` 并修改配置：

```bash
cp env.example .env
```

编辑 `.env` 文件：

```
MODEL_PATH=THUDM/chatglm2-6b
DEVICE=cuda  # 或 cpu
```

## 🚀 使用方法

### 方式一：Docker 部署（推荐，支持 GPU）

#### 使用 Docker Compose

```bash
# 构建并启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

#### 使用 Docker 命令

```bash
# 构建镜像
docker build -t openai-translator-chatglm:latest .

# 运行容器（GPU 支持）
docker run -d \
  --name openai-translator-chatglm \
  --gpus all \
  -p 7860:7860 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/temp:/app/temp \
  -e DEVICE=cuda \
  openai-translator-chatglm:latest
```

详细 Docker 部署说明请查看 [DOCKER_GUIDE.md](DOCKER_GUIDE.md)

### 方式二：本地运行

#### 启动应用

```bash
python main.py
```

或者：

```bash
python gradio_app.py
```

#### 检查 GPU 支持

```bash
python check_gpu.py
```

应用将在浏览器中自动打开，默认地址：http://localhost:7860

### 使用步骤

#### PDF 翻译

1. 点击"上传PDF文件"区域
2. 选择要翻译的 PDF 文件
3. 设置源语言和目标语言（默认：英文 → 中文）
4. 点击 "Submit" 开始翻译
5. 翻译完成后，在右侧下载翻译文件

#### 文本翻译

1. 展开"文本翻译"区域
2. 输入要翻译的文本
3. 设置源语言和目标语言
4. 点击"翻译文本"按钮
5. 查看翻译结果

## 🎯 支持的语言

- English (英语)
- Chinese (中文)
- Japanese (日语)
- Korean (韩语)
- French (法语)
- German (德语)
- Spanish (西班牙语)
- Italian (意大利语)
- Portuguese (葡萄牙语)
- Russian (俄语)
- Arabic (阿拉伯语)
- Thai (泰语)
- Vietnamese (越南语)
- Hindi (印地语)
- Turkish (土耳其语)

## 🏗️ 项目结构

```
openai-translator-chatglm/
├── gradio_app.py          # Gradio 界面主文件
├── translator.py          # ChatGLM2-6B 翻译引擎
├── pdf_processor.py       # PDF 处理模块
├── config.py              # 配置文件
├── main.py                # 主入口文件
├── requirements.txt       # 依赖列表
├── env.example            # 环境变量示例
├── README.md              # 项目文档
├── temp/                  # 临时文件目录
└── output/                # 输出文件目录
```

## ⚙️ 配置说明

### 环境变量

- `MODEL_PATH`: 模型路径或 HuggingFace 模型名称（默认：THUDM/chatglm2-6b）
- `DEVICE`: 设备类型，cuda 或 cpu（默认：cuda）
- `MAX_LENGTH`: 最大生成长度（默认：2048）
- `TOP_P`: top_p 参数（默认：0.7）
- `TEMPERATURE`: temperature 参数（默认：0.95）
- `GRADIO_SERVER_NAME`: Gradio 服务器地址（默认：0.0.0.0）
- `GRADIO_SERVER_PORT`: Gradio 服务器端口（默认：7860）
- `GRADIO_SHARE`: 是否创建公共链接（默认：False）

### 模型下载

首次运行时会自动从 HuggingFace 下载 ChatGLM2-6B 模型，约 12GB。确保：
- 有足够的磁盘空间
- 网络连接稳定
- 可以访问 HuggingFace

如果下载缓慢，可以：
1. 使用镜像站点
2. 手动下载模型到本地
3. 修改 `MODEL_PATH` 指向本地路径

## 🔧 技术栈

- **Python 3.8+**
- **Gradio 4.0+** - 图形界面框架
- **Transformers** - HuggingFace 模型库
- **ChatGLM2-6B** - 中文大语言模型
- **PyTorch** - 深度学习框架
- **PyMuPDF** - PDF 处理
- **ReportLab** - PDF 生成

## 📝 注意事项

1. **首次运行**：需要下载 ChatGLM2-6B 模型（约 12GB），可能需要较长时间
2. **GPU 推荐**：建议使用 GPU 加速，CPU 模式会较慢
3. **内存要求**：至少需要 16GB RAM（GPU 模式）或 32GB RAM（CPU 模式）
4. **PDF 大小**：大型 PDF 文件翻译可能需要较长时间
5. **模型路径**：可以修改 `MODEL_PATH` 使用本地模型或量化版本

## 🚀 性能优化

### 使用量化模型

可以使用 4-bit 或 8-bit 量化版本以减少显存占用：

```python
# 在 translator.py 中修改模型加载方式
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

model = AutoModel.from_pretrained(
    model_path,
    quantization_config=quantization_config,
    trust_remote_code=True
)
```

### 使用本地模型

如果已下载模型到本地：

```bash
# 修改 .env 文件
MODEL_PATH=/path/to/local/chatglm2-6b
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- ChatGLM2-6B 模型由清华大学开发
- Gradio 提供优秀的界面框架
- HuggingFace 提供模型托管服务

---

**享受智能翻译的便利！** 🎉

