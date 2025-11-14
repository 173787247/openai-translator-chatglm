"""
工具函数
"""
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 文件大小（字节）
        
    Returns:
        格式化后的文件大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_pdf_info(pdf_path: str) -> dict:
    """
    获取 PDF 文件信息
    
    Args:
        pdf_path: PDF 文件路径
        
    Returns:
        包含文件信息的字典
    """
    try:
        import fitz
        
        doc = fitz.open(pdf_path)
        file_size = os.path.getsize(pdf_path)
        
        info = {
            "success": True,
            "total_pages": len(doc),
            "file_size": format_file_size(file_size),
            "file_name": os.path.basename(pdf_path)
        }
        
        doc.close()
        return info
        
    except Exception as e:
        logger.error(f"获取 PDF 信息失败: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def validate_language(language: str) -> bool:
    """
    验证语言是否支持
    
    Args:
        language: 语言名称
        
    Returns:
        是否支持
    """
    from config import SUPPORTED_LANGUAGES
    return language in SUPPORTED_LANGUAGES

