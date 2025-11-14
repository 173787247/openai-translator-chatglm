"""
PDF 处理模块
支持 PDF 翻译并保留布局
"""
import fitz  # PyMuPDF
from typing import Dict, Optional
import os
import logging
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
import io

logger = logging.getLogger(__name__)


class PDFProcessor:
    """PDF 处理器"""
    
    def __init__(self, translator=None):
        """
        初始化 PDF 处理器
        
        Args:
            translator: 翻译器实例
        """
        self.translator = translator
    
    def extract_text_from_pdf(self, pdf_path: str) -> Dict:
        """
        从 PDF 提取文本
        
        Args:
            pdf_path: PDF 文件路径
            
        Returns:
            包含文本和页面信息的字典
        """
        try:
            doc = fitz.open(pdf_path)
            pages_data = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                pages_data.append({
                    "page_number": page_num + 1,
                    "text": text,
                    "width": page.rect.width,
                    "height": page.rect.height
                })
            
            doc.close()
            
            return {
                "success": True,
                "pages": pages_data,
                "total_pages": len(pages_data)
            }
            
        except Exception as e:
            logger.error(f"提取 PDF 文本失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "pages": []
            }
    
    def translate_pdf(
        self,
        pdf_path: str,
        output_path: str,
        source_language: str = "English",
        target_language: str = "Chinese",
        progress_callback=None
    ) -> Dict:
        """
        翻译 PDF 文件
        
        Args:
            pdf_path: 输入 PDF 文件路径
            output_path: 输出 PDF 文件路径
            source_language: 源语言
            target_language: 目标语言
            
        Returns:
            处理结果字典
        """
        if not self.translator:
            return {
                "success": False,
                "error": "翻译器未初始化"
            }
        
        try:
            # 提取文本
            extract_result = self.extract_text_from_pdf(pdf_path)
            if not extract_result["success"]:
                return extract_result
            
            pages_data = extract_result["pages"]
            
            # 翻译每一页
            translated_pages = []
            total_pages = len(pages_data)
            
            for idx, page_data in enumerate(pages_data, 1):
                # 更新进度
                if progress_callback:
                    progress_callback(idx, total_pages, f"正在翻译第 {idx}/{total_pages} 页...")
                
                text = page_data["text"]
                if not text or not text.strip():
                    translated_pages.append({
                        "page_number": page_data["page_number"],
                        "translated_text": "",
                        "width": page_data["width"],
                        "height": page_data["height"]
                    })
                    continue
                
                # 如果文本太长，分段处理
                max_chunk_length = 2000
                if len(text) > max_chunk_length:
                    # 分段翻译
                    chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
                    translated_chunks = []
                    
                    for chunk_idx, chunk in enumerate(chunks):
                        logger.info(f"正在翻译第 {idx} 页，第 {chunk_idx+1}/{len(chunks)} 段: {source_language} → {target_language}")
                        result = self.translator.translate(
                            text=chunk,
                            source_language=source_language,
                            target_language=target_language
                        )
                        if result["success"]:
                            translated_chunks.append(result["translated_text"])
                            logger.info(f"第 {idx} 页第 {chunk_idx+1} 段翻译成功")
                        else:
                            error_msg = result.get("error", "未知错误")
                            logger.error(f"第 {idx} 页第 {chunk_idx+1} 段翻译失败: {error_msg}，使用原文")
                            translated_chunks.append(chunk)
                    
                    translated_text = "\n".join(translated_chunks)
                else:
                    # 直接翻译
                    logger.info(f"正在翻译第 {idx} 页: {source_language} → {target_language}")
                    result = self.translator.translate(
                        text=text,
                        source_language=source_language,
                        target_language=target_language
                    )
                    
                    if result["success"]:
                        translated_text = result["translated_text"]
                        # 清理翻译结果（移除可能的注释或原文）
                        translated_text = translated_text.strip()
                        
                        # 如果翻译结果包含明显的原文（可能是模型错误），尝试提取
                        if source_language == "English" and target_language == "Japanese":
                            # 检查是否包含英文原文或中文，如果有则尝试提取日文部分
                            lines = translated_text.split('\n')
                            japanese_lines = []
                            skip_patterns = ['原文', 'Original', 'Translation', '翻译', '要求', 'Requirements', '事项', 'Matters', 'English', 'Japanese']
                            
                            for line in lines:
                                line = line.strip()
                                # 跳过明显的提示词行
                                if any(pattern in line for pattern in skip_patterns):
                                    continue
                                # 跳过空行或只有标点的行
                                if not line or line in ['：', ':', '-', '—', '1.', '2.', '3.', '4.', '5.', '6.']:
                                    continue
                                # 优先保留包含日文假名（平假名、片假名）的行
                                if any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' for char in line):
                                    japanese_lines.append(line)
                                # 如果包含汉字但没有假名，可能是中文，跳过
                                elif any('\u4e00' <= char <= '\u9fff' for char in line) and not any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' for char in line):
                                    # 检查是否主要是中文（没有日文假名）
                                    continue
                                # 如果整行都不是英文ASCII字符，可能是日文
                                elif not all(c.isascii() or c.isspace() or c in '.,;:!?()[]{}' for c in line):
                                    # 检查是否主要是非ASCII字符
                                    non_ascii_count = sum(1 for c in line if not c.isascii() and not c.isspace())
                                    if non_ascii_count > len(line) * 0.3:  # 至少30%是非ASCII字符
                                        japanese_lines.append(line)
                            
                            if japanese_lines:
                                translated_text = '\n'.join(japanese_lines)
                                logger.info(f"第 {idx} 页已清理翻译结果，提取了 {len(japanese_lines)} 行日文")
                            else:
                                logger.warning(f"第 {idx} 页清理后没有找到日文内容，使用原始结果")
                        
                        elif source_language == "English" and target_language == "Korean":
                            # 检查是否包含英文原文，如果有则尝试提取韩文部分
                            lines = translated_text.split('\n')
                            korean_lines = []
                            skip_patterns = ['原文', 'Original', 'Translation', '翻译', '要求', 'Requirements', '事项', 'Matters']
                            
                            for line in lines:
                                line = line.strip()
                                # 跳过明显的提示词行
                                if any(pattern in line for pattern in skip_patterns):
                                    continue
                                # 跳过空行或只有标点的行
                                if not line or line in ['：', ':', '-', '—', '1.', '2.', '3.', '4.', '5.', '6.']:
                                    continue
                                # 检查是否主要是韩文字符
                                if any('\uAC00' <= char <= '\uD7A3' for char in line):
                                    korean_lines.append(line)
                                # 检查是否包含韩文字符（即使混合其他字符）
                                elif any('\uAC00' <= char <= '\uD7A3' for char in line):
                                    # 提取包含韩文的部分
                                    korean_part = ''.join(c for c in line if '\uAC00' <= c <= '\uD7A3' or c.isspace() or c in '.,;:!?()[]{}')
                                    if korean_part.strip():
                                        korean_lines.append(korean_part.strip())
                                # 如果整行都不是英文ASCII字符，可能是韩文
                                elif not all(c.isascii() or c.isspace() or c in '.,;:!?()[]{}' for c in line):
                                    # 检查是否主要是非ASCII字符
                                    non_ascii_count = sum(1 for c in line if not c.isascii() and not c.isspace())
                                    if non_ascii_count > len(line) * 0.3:  # 至少30%是非ASCII字符
                                        korean_lines.append(line)
                            
                            if korean_lines:
                                translated_text = '\n'.join(korean_lines)
                                logger.info(f"第 {idx} 页已清理翻译结果，提取了 {len(korean_lines)} 行韩文")
                            else:
                                logger.warning(f"第 {idx} 页清理后没有找到韩文内容，使用原始结果")
                        
                        logger.info(f"第 {idx} 页翻译成功，长度: {len(translated_text)} 字符")
                        # 验证翻译结果不是原文
                        if translated_text == text or translated_text == text.strip():
                            logger.warning(f"第 {idx} 页翻译结果与原文相同，可能翻译失败")
                        # 检查是否包含中文（如果目标是日文）
                        if target_language == "Japanese" and any('\u4e00' <= char <= '\u9fff' for char in translated_text):
                            chinese_count = sum(1 for c in translated_text if '\u4e00' <= c <= '\u9fff')
                            japanese_hiragana_katakana = sum(1 for c in translated_text if '\u3040' <= c <= '\u309F' or '\u30A0' <= c <= '\u30FF')
                            if chinese_count > japanese_hiragana_katakana * 2:  # 如果中文数量远大于日文假名，可能混入了中文
                                logger.warning(f"第 {idx} 页翻译结果包含大量中文，可能混入了中文而非纯日文")
                        # 检查是否包含中文（如果目标是韩文）
                        elif target_language == "Korean" and any('\u4e00' <= char <= '\u9fff' for char in translated_text):
                            chinese_count = sum(1 for c in translated_text if '\u4e00' <= c <= '\u9fff')
                            korean_count = sum(1 for c in translated_text if '\uAC00' <= c <= '\uD7A3')
                            if chinese_count > korean_count:
                                logger.warning(f"第 {idx} 页翻译结果包含大量中文，可能翻译方向错误")
                    else:
                        # 翻译失败，记录错误并使用原文
                        error_msg = result.get("error", "未知错误")
                        logger.error(f"第 {idx} 页翻译失败: {error_msg}，使用原文")
                        translated_text = text
                
                translated_pages.append({
                    "page_number": page_data["page_number"],
                    "translated_text": translated_text,
                    "width": page_data["width"],
                    "height": page_data["height"]
                })
            
            # 记录翻译统计
            translated_count = sum(1 for p in translated_pages if p["translated_text"] and p["translated_text"].strip())
            logger.info(f"翻译完成: 共 {len(translated_pages)} 页，其中 {translated_count} 页有翻译内容")
            logger.info(f"翻译方向: {source_language} → {target_language}")
            
            # 生成翻译后的 PDF
            self._create_translated_pdf(translated_pages, output_path)
            
            return {
                "success": True,
                "output_path": output_path,
                "pages_translated": len(translated_pages),
                "translated_count": translated_count
            }
            
        except Exception as e:
            logger.error(f"翻译 PDF 失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_translated_pdf(self, pages_data: list, output_path: str):
        """
        创建翻译后的 PDF 文件（优化版，更好的布局保留）
        
        Args:
            pages_data: 包含翻译文本的页面数据
            output_path: 输出文件路径
        """
        try:
            from reportlab.lib.colors import black
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.units import inch
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            
            # 创建 PDF 文档
            doc = SimpleDocTemplate(
                output_path,
                pagesize=(pages_data[0]["width"], pages_data[0]["height"]) if pages_data else A4
            )
            
            # 注册中文字体（使用 ReportLab 内置的 CID 字体）
            # 尝试注册中文字体
            font_name = 'Helvetica'
            try:
                # 尝试使用系统字体或 ReportLab 内置的 CID 字体
                # 首先尝试注册 CID 字体（支持中文）
                try:
                    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
                    font_name = 'STSong-Light'
                    logger.info("已注册中文字体: STSong-Light")
                except:
                    # 如果失败，尝试其他中文字体
                    try:
                        pdfmetrics.registerFont(UnicodeCIDFont('STHeiti-Light'))
                        font_name = 'STHeiti-Light'
                        logger.info("已注册中文字体: STHeiti-Light")
                    except:
                        # 如果都失败，使用默认字体（可能不支持中文）
                        logger.warning("无法注册中文字体，可能无法正确显示中文")
            except Exception as e:
                logger.warning(f"注册中文字体时出错: {str(e)}，使用默认字体")
            
            # 获取样式
            styles = getSampleStyleSheet()
            
            # 创建自定义样式
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=12,
                leading=16,
                spaceAfter=12,
                fontName=font_name,
                encoding='utf-8'
            )
            
            # 构建内容
            story = []
            
            for page_data in pages_data:
                text = page_data["translated_text"]
                if text:
                    # 处理文本，保留换行
                    paragraphs = text.split('\n')
                    for para in paragraphs:
                        if para.strip():
                            # 处理特殊字符
                            para = para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                            story.append(Paragraph(para, normal_style))
                            story.append(Spacer(1, 6))
                
                # 添加分页
                story.append(Spacer(1, 0.2*inch))
            
            # 生成 PDF
            doc.build(story)
            
        except Exception as e:
            logger.error(f"创建 PDF 失败: {str(e)}")
            # 如果失败，使用简单方法
            try:
                from reportlab.lib.colors import black
                c = canvas.Canvas(output_path)
                
                for page_data in pages_data:
                    width = page_data["width"]
                    height = page_data["height"]
                    c.setPageSize((width, height))
                    
                    text = page_data["translated_text"]
                    if text:
                        # 使用支持中文的字体
                        try:
                            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
                            from reportlab.pdfbase import pdfmetrics
                            try:
                                pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
                                c.setFont("STSong-Light", 12)
                            except:
                                try:
                                    pdfmetrics.registerFont(UnicodeCIDFont('STHeiti-Light'))
                                    c.setFont("STHeiti-Light", 12)
                                except:
                                    # 如果都失败，尝试使用支持 Unicode 的方法
                                    c.setFont("Helvetica", 12)
                        except:
                            c.setFont("Helvetica", 12)
                        
                        lines = text.split('\n')
                        y_position = height - 50
                        
                        for line in lines:
                            if y_position < 50:
                                break
                            # 处理长行，自动换行（对中文和英文都适用）
                            max_chars = 60  # 中文字符数
                            if len(line) > max_chars:
                                # 对中文和英文混合文本进行智能分割
                                chunks = []
                                current_chunk = ""
                                for char in line:
                                    if len(current_chunk) >= max_chars:
                                        chunks.append(current_chunk)
                                        current_chunk = char
                                    else:
                                        current_chunk += char
                                if current_chunk:
                                    chunks.append(current_chunk)
                                
                                for chunk in chunks:
                                    if y_position < 50:
                                        break
                                    try:
                                        c.drawString(50, y_position, chunk)
                                        y_position -= 20
                                    except Exception as e:
                                        logger.warning(f"绘制文本失败: {str(e)}")
                                        # 如果绘制失败，尝试编码处理
                                        try:
                                            chunk_encoded = chunk.encode('utf-8', 'ignore').decode('utf-8')
                                            c.drawString(50, y_position, chunk_encoded)
                                            y_position -= 20
                                        except:
                                            y_position -= 20
                            else:
                                try:
                                    c.drawString(50, y_position, line)
                                    y_position -= 20
                                except Exception as e:
                                    logger.warning(f"绘制文本失败: {str(e)}")
                                    try:
                                        line_encoded = line.encode('utf-8', 'ignore').decode('utf-8')
                                        c.drawString(50, y_position, line_encoded)
                                        y_position -= 20
                                    except:
                                        y_position -= 20
                    
                    c.showPage()
                
                c.save()
            except Exception as e2:
                logger.error(f"简单 PDF 创建也失败: {str(e2)}")
                raise

