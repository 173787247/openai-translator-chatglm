# 使用已有的 PyTorch CUDA 镜像（RTX 5080 支持 CUDA 12.8）
FROM pytorch/pytorch:2.7.0-cuda12.8-cudnn9-devel

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    git-lfs \
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip
RUN pip install --no-cache-dir --upgrade pip

# 设置 pip 使用清华镜像源（加速下载）
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 复制依赖文件
COPY requirements-docker.txt requirements.txt .

# 安装 Python 依赖（PyTorch 已在基础镜像中，只需安装其他依赖）
RUN pip install --no-cache-dir -r requirements-docker.txt || pip install --no-cache-dir -r requirements.txt

# 初始化 git lfs
RUN git lfs install

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p temp output

# 设置权限
RUN chmod +x run.sh || true

# 暴露端口
EXPOSE 7860

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# 启动命令
CMD ["python", "main.py"]

