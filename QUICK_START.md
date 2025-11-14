# 快速启动指南（RTX 5080 + Docker Desktop）

## 🚀 一键启动（推荐）

### 步骤 1: 验证 Docker GPU 支持

```bash
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

如果能看到 GPU 信息，说明配置正确 ✅

### 步骤 2: 启动服务

```bash
cd openai-translator-chatglm
docker-compose up -d --build
```

### 步骤 3: 查看日志

```bash
docker-compose logs -f
```

等待看到 "Running on local URL: http://0.0.0.0:7860" 表示启动成功 ✅

### 步骤 4: 访问应用

打开浏览器访问：**http://localhost:7860**

## 📋 完整流程

### 首次运行

1. **构建镜像**（首次需要，后续可跳过）
   ```bash
   docker-compose build
   ```

2. **启动服务**
   ```bash
   docker-compose up -d
   ```

3. **等待模型下载**（首次运行）
   - 查看日志：`docker-compose logs -f`
   - 模型约 12GB，下载需要一些时间
   - 下载完成后会自动加载模型

4. **访问界面**
   - 浏览器打开：http://localhost:7860
   - 界面加载后即可使用

### 日常使用

```bash
# 启动
docker-compose up -d

# 停止
docker-compose down

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

## 🔧 配置调整

### 修改环境变量

编辑 `docker-compose.yml` 或创建 `.env` 文件：

```env
MODEL_PATH=THUDM/chatglm2-6b
DEVICE=cuda
MAX_LENGTH=2048
TOP_P=0.7
TEMPERATURE=0.95
```

然后重启：

```bash
docker-compose down
docker-compose up -d
```

## 🐛 故障排除

### 问题 1: GPU 不可用

**检查**：
```bash
docker exec openai-translator-chatglm nvidia-smi
```

**解决**：
- 确保 Docker Desktop 已启用 GPU 支持
- 检查 NVIDIA 驱动是否最新
- 重启 Docker Desktop

### 问题 2: 端口被占用

**解决**：修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "7861:7860"  # 改为其他端口
```

### 问题 3: 模型下载失败

**解决**：
- 检查网络连接
- 使用 HuggingFace 镜像
- 手动下载模型到 `./models` 目录

### 问题 4: 内存不足

**解决**：
- 增加 Docker Desktop 内存分配
- 使用量化模型
- 减少 `MAX_LENGTH` 参数

## 📊 性能监控

### 查看 GPU 使用情况

```bash
docker exec openai-translator-chatglm nvidia-smi
```

### 查看容器资源使用

```bash
docker stats openai-translator-chatglm
```

### 查看应用日志

```bash
docker-compose logs -f translator
```

## 🎯 RTX 5080 优化建议

RTX 5080 有充足的显存，可以：

1. **使用完整模型**（无需量化）
2. **增加 MAX_LENGTH**（支持更长文本）
3. **批量处理**（同时处理多个任务）

在 `docker-compose.yml` 中调整：

```yaml
environment:
  - MAX_LENGTH=4096  # 增加到 4096
  - DEVICE=cuda
```

## ✅ 验证清单

启动后检查：

- [ ] 容器运行正常：`docker-compose ps`
- [ ] GPU 可用：`docker exec openai-translator-chatglm nvidia-smi`
- [ ] 界面可访问：http://localhost:7860
- [ ] 可以上传 PDF
- [ ] 翻译功能正常

## 📚 更多信息

- 详细 Docker 指南：查看 [DOCKER_GUIDE.md](DOCKER_GUIDE.md)
- 完整文档：查看 [README.md](README.md)
- 项目总结：查看 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

**祝使用愉快！** 🎉

