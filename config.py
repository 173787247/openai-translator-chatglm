"""
配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ChatGLM2-6B 配置
MODEL_PATH = os.getenv("MODEL_PATH", "THUDM/chatglm2-6b")
DEVICE = os.getenv("DEVICE", "cuda")  # cuda 或 cpu
MAX_LENGTH = int(os.getenv("MAX_LENGTH", "2048"))
TOP_P = float(os.getenv("TOP_P", "0.7"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.95"))

# Gradio 配置
GRADIO_SERVER_NAME = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
GRADIO_SERVER_PORT = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
GRADIO_SHARE = os.getenv("GRADIO_SHARE", "False").lower() == "true"

# 支持的语言列表
SUPPORTED_LANGUAGES = {
    "English": "英语",
    "Chinese": "中文",
    "Japanese": "日语",
    "Korean": "韩语",
    "French": "法语",
    "German": "德语",
    "Spanish": "西班牙语",
    "Italian": "意大利语",
    "Portuguese": "葡萄牙语",
    "Russian": "俄语",
    "Arabic": "阿拉伯语",
    "Thai": "泰语",
    "Vietnamese": "越南语",
    "Hindi": "印地语",
    "Turkish": "土耳其语",
}

# PDF 处理配置
PDF_DPI = 200
PDF_IMAGE_FORMAT = "PNG"
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# 创建临时目录
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

