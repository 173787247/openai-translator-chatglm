# Docker 部署指南

## 前置要求

1. **Docker Desktop** 已安装并运行
2. **NVIDIA GPU** 支持（RTX 5080）
3. **NVIDIA Container Toolkit** 已安装（Docker Desktop 通常已包含）

## 验证 GPU 支持

### 1. 检查 Docker GPU 支持

```bash
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

如果能看到 GPU 信息，说明 Docker GPU 支持正常。

### 2. 检查 Docker Desktop GPU 设置

在 Docker Desktop 中：
- Settings → Resources → Advanced
- 确保 "Use the WSL 2 based engine" 已启用（Windows）
- 确保 GPU 支持已启用

## 快速开始

### 方法一：使用 Docker Compose（推荐）

1. **构建并启动**

```bash
cd openai-translator-chatglm
docker-compose up -d --build
```

2. **查看日志**

```bash
docker-compose logs -f
```

3. **访问应用**

打开浏览器访问：http://localhost:7860

4. **停止服务**

```bash
docker-compose down
```

### 方法二：使用 Docker 命令

1. **构建镜像**

```bash
docker build -t openai-translator-chatglm:latest .
```

2. **运行容器**

```bash
docker run -d \
  --name openai-translator-chatglm \
  --gpus all \
  -p 7860:7860 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/temp:/app/temp \
  -e DEVICE=cuda \
  -e MODEL_PATH=THUDM/chatglm2-6b \
  openai-translator-chatglm:latest
```

3. **查看日志**

```bash
docker logs -f openai-translator-chatglm
```

4. **停止容器**

```bash
docker stop openai-translator-chatglm
docker rm openai-translator-chatglm
```

## 配置说明

### 环境变量

可以通过 `.env` 文件或 `docker-compose.yml` 配置：

```env
MODEL_PATH=THUDM/chatglm2-6b
DEVICE=cuda
MAX_LENGTH=2048
TOP_P=0.7
TEMPERATURE=0.95
GRADIO_SHARE=False
```

### 卷挂载

- `./models:/app/models` - 模型缓存目录（避免重复下载）
- `./output:/app/output` - 翻译输出文件
- `./temp:/app/temp` - 临时文件

### GPU 配置

`docker-compose.yml` 中已配置 GPU 支持：

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

## 常见问题

### 1. GPU 不可用

**问题**：容器内无法使用 GPU

**解决方案**：
- 确保 Docker Desktop 支持 GPU
- 检查 NVIDIA Container Toolkit 是否安装
- 验证 `nvidia-smi` 在容器内是否可用

```bash
docker exec openai-translator-chatglm nvidia-smi
```

### 2. 模型下载缓慢

**问题**：首次运行下载模型很慢

**解决方案**：
- 使用 HuggingFace 镜像站点
- 预先下载模型到本地，然后挂载：

```yaml
volumes:
  - /path/to/local/models:/app/local_models
```

### 3. 内存不足

**问题**：容器内存不足

**解决方案**：
- 增加 Docker Desktop 内存分配
- 使用量化模型
- 减少 `MAX_LENGTH` 参数

### 4. 端口冲突

**问题**：端口 7860 已被占用

**解决方案**：
修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "7861:7860"  # 使用 7861 端口
```

## 性能优化

### 1. 使用本地模型

如果已下载模型到本地：

```yaml
environment:
  - MODEL_PATH=/app/local_models/chatglm2-6b
volumes:
  - /path/to/models:/app/local_models
```

### 2. 调整 GPU 内存

RTX 5080 有足够的显存，可以：
- 增加 `MAX_LENGTH` 参数
- 使用更大的 batch size
- 不使用量化模型

### 3. 持久化模型缓存

模型会缓存在 `./models` 目录，下次启动无需重新下载。

## 监控和调试

### 查看容器状态

```bash
docker ps
docker stats openai-translator-chatglm
```

### 进入容器

```bash
docker exec -it openai-translator-chatglm bash
```

### 查看 GPU 使用情况

```bash
docker exec openai-translator-chatglm nvidia-smi
```

## 更新应用

```bash
# 停止当前容器
docker-compose down

# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build
```

## 清理

### 清理容器和镜像

```bash
docker-compose down
docker rmi openai-translator-chatglm:latest
```

### 清理模型缓存（谨慎操作）

```bash
rm -rf models/
```

## 生产环境建议

1. **使用环境变量文件**：创建 `.env` 文件管理配置
2. **设置资源限制**：在 `docker-compose.yml` 中设置内存和 CPU 限制
3. **启用日志轮转**：配置日志管理
4. **使用反向代理**：使用 Nginx 等反向代理
5. **定期备份**：备份模型和配置文件

---

**享受 Docker 部署的便利！** 🐳

