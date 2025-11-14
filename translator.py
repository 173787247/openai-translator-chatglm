"""
基于 ChatGLM2-6B 的翻译引擎
"""
import torch
from transformers import AutoTokenizer, AutoModel
from typing import Optional, Dict, Any
import logging
import os

logger = logging.getLogger(__name__)


class ChatGLMTranslator:
    """基于 ChatGLM2-6B 的翻译器"""
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        device: Optional[str] = None
    ):
        """
        初始化翻译器
        
        Args:
            model_path: 模型路径或 HuggingFace 模型名称
            device: 设备类型 (cuda 或 cpu)
        """
        from config import MODEL_PATH, DEVICE
        
        self.model_path = model_path or MODEL_PATH
        self.device = device or DEVICE
        
        # 检查设备可用性
        if self.device == "cuda" and not torch.cuda.is_available():
            logger.warning("CUDA 不可用，使用 CPU")
            self.device = "cpu"
        
        self.tokenizer = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """加载模型"""
        try:
            logger.info(f"正在加载模型: {self.model_path}")
            logger.info(f"使用设备: {self.device}")
            
            # 加载 tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            
            # 修复 tokenizer 兼容性问题
            # ChatGLM2-6B 的 tokenizer 与新版 transformers 不兼容，需要修复 _pad 方法
            if hasattr(self.tokenizer, 'pad_token') and self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # 修复 _pad 方法，移除不支持的 padding_side 参数
            if hasattr(self.tokenizer, '_pad'):
                original_pad = self.tokenizer._pad
                def patched_pad(encoded_inputs, max_length=None, padding_strategy=None, pad_to_multiple_of=None, return_attention_mask=None, **kwargs):
                    # 移除 padding_side 参数（ChatGLM tokenizer 不支持）
                    kwargs.pop('padding_side', None)
                    # 调用原始方法
                    try:
                        return original_pad(
                            encoded_inputs,
                            max_length=max_length,
                            padding_strategy=padding_strategy,
                            pad_to_multiple_of=pad_to_multiple_of,
                            return_attention_mask=return_attention_mask,
                            **kwargs
                        )
                    except TypeError:
                        # 如果还是出错，尝试更简单的调用
                        return original_pad(encoded_inputs, max_length=max_length, **kwargs)
                self.tokenizer._pad = patched_pad
                logger.info("已修复 tokenizer _pad 方法兼容性问题")
            
            # 加载模型
            self.model = AutoModel.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                device_map="auto" if self.device == "cuda" else None
            )
            
            if self.device == "cpu":
                self.model = self.model.float()
            
            self.model.eval()
            logger.info("模型加载成功")
            
        except Exception as e:
            logger.error(f"模型加载失败: {str(e)}")
            raise
    
    def translate(
        self,
        text: str,
        source_language: str = "English",
        target_language: str = "Chinese",
        max_length: Optional[int] = None,
        top_p: Optional[float] = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        翻译文本
        
        Args:
            text: 待翻译的文本
            source_language: 源语言
            target_language: 目标语言
            max_length: 最大生成长度
            top_p: top_p 参数
            temperature: temperature 参数
            
        Returns:
            包含翻译结果的字典
        """
        if not text or not text.strip():
            return {
                "success": False,
                "error": "文本为空",
                "translated_text": ""
            }
        
        if not self.model or not self.tokenizer:
            return {
                "success": False,
                "error": "模型未加载",
                "translated_text": ""
            }
        
        try:
            from config import MAX_LENGTH, TOP_P, TEMPERATURE
            
            max_length = max_length or MAX_LENGTH
            top_p = top_p or TOP_P
            temperature = temperature or TEMPERATURE
            
            # 构建翻译提示词（优化版）
            # 根据目标语言选择不同的提示词格式
            if target_language == "Korean":
                prompt = f"""You must translate the following English text into Korean language (한국어). 
IMPORTANT: You must output ONLY Korean text. Do NOT output Chinese. Do NOT output English. Only Korean.

English:
{text}

Korean (한국어 only):"""
            elif target_language == "Japanese":
                prompt = f"""You must translate the following English text into Japanese language (日本語). 
IMPORTANT: You must output ONLY Japanese text. Do NOT output Chinese. Do NOT output English. Only Japanese.

English:
{text}

Japanese (日本語 only):"""
            else:
                prompt = f"""你是一位专业的翻译专家。请将以下{source_language}文本准确翻译成{target_language}。

要求：
1. 翻译要准确、自然、流畅
2. 保持原文的语气和风格
3. 保留原文的格式（如换行、段落等）
4. 如果是技术术语，请使用通用的翻译
5. 只返回翻译结果，不要添加任何解释、注释或额外说明
6. 不要包含原文或任何注释

原文：
{text}

翻译："""
            
            # 使用 ChatGLM 进行生成
            # 捕获可能的 tokenizer 错误并重试
            try:
                response, history = self.model.chat(
                    self.tokenizer,
                    prompt,
                    history=[],
                    max_length=max_length,
                    top_p=top_p,
                    temperature=temperature
                )
            except TypeError as e:
                if 'padding_side' in str(e):
                    # 如果还是出现 padding_side 错误，尝试更彻底的修复
                    logger.warning(f"检测到 padding_side 错误，尝试修复: {str(e)}")
                    # 重新修复 tokenizer
                    if hasattr(self.tokenizer, '_pad'):
                        original_pad = self.tokenizer._pad
                        def patched_pad(*args, **kwargs):
                            kwargs.pop('padding_side', None)
                            return original_pad(*args, **kwargs)
                        self.tokenizer._pad = patched_pad
                    # 重试
                    response, history = self.model.chat(
                        self.tokenizer,
                        prompt,
                        history=[],
                        max_length=max_length,
                        top_p=top_p,
                        temperature=temperature
                    )
                else:
                    raise
            
            translated_text = response.strip()
            
            # 清理翻译结果，移除可能的提示词或注释
            if target_language == "Japanese":
                # 检查是否包含日文字符（平假名、片假名、汉字）
                has_japanese = any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' or '\u4E00' <= char <= '\u9FAF' for char in translated_text)
                has_chinese = any('\u4e00' <= char <= '\u9fff' for char in translated_text)
                # 检查是否包含日文特有的假名
                has_hiragana_katakana = any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' for char in translated_text)
                
                # 如果包含中文但没有日文假名，说明可能混入了中文
                if has_chinese and not has_hiragana_katakana:
                    logger.warning(f"翻译结果包含中文但没有日文假名，可能混入了中文")
                    # 尝试从结果中提取日文部分
                    lines = translated_text.split('\n')
                    japanese_lines = []
                    for line in lines:
                        line = line.strip()
                        # 优先保留包含日文假名的行
                        if any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' for char in line):
                            japanese_lines.append(line)
                        # 如果包含汉字但没有假名，可能是中文，跳过
                        elif any('\u4e00' <= char <= '\u9fff' for char in line) and not any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' for char in line):
                            # 检查是否主要是中文（没有日文假名）
                            continue
                        # 保留其他非ASCII字符的行（可能是日文）
                        elif not all(c.isascii() or c.isspace() or c in '.,;:!?()[]{}' for c in line):
                            japanese_lines.append(line)
                    
                    if japanese_lines:
                        translated_text = '\n'.join(japanese_lines)
                    else:
                        logger.warning(f"清理后没有找到日文内容，使用原始结果")
                
                # 移除可能的英文提示词
                lines = translated_text.split('\n')
                cleaned_lines = []
                skip_keywords = ['Translation', 'Original text', 'Requirements', 'Note', '翻译', '原文', '要求', 'English', 'Japanese', '日本語']
                
                for line in lines:
                    line = line.strip()
                    # 跳过明显的提示词行
                    if any(keyword in line for keyword in skip_keywords):
                        continue
                    # 跳过空行或只有标点的行
                    if not line or line in ['：', ':', '-', '—']:
                        continue
                    # 优先保留包含日文假名的行
                    if any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' for char in line):
                        cleaned_lines.append(line)
                    # 如果整行主要是非ASCII字符（可能是日文），也保留
                    elif not all(c.isascii() or c.isspace() or c in '.,;:!?()[]{}' for c in line):
                        # 检查是否主要是非ASCII字符
                        non_ascii_ratio = sum(1 for c in line if not c.isascii() and not c.isspace()) / max(len(line), 1)
                        if non_ascii_ratio > 0.5:  # 至少50%是非ASCII字符
                            cleaned_lines.append(line)
                
                if cleaned_lines:
                    translated_text = '\n'.join(cleaned_lines)
                else:
                    # 如果清理后没有内容，使用原始结果但移除明显的提示词
                    translated_text = response.strip()
                    # 移除开头的提示词
                    for keyword in ['Translation', '翻译结果', 'Translation (Japanese):', 'Translation (日本語):', 'Japanese (日本語 only):']:
                        if translated_text.startswith(keyword):
                            translated_text = translated_text[len(keyword):].strip()
                            if translated_text.startswith(':'):
                                translated_text = translated_text[1:].strip()
            
            elif target_language == "Korean":
                # 检查是否包含韩文字符
                has_korean = any('\uAC00' <= char <= '\uD7A3' for char in translated_text)
                has_chinese = any('\u4e00' <= char <= '\u9fff' for char in translated_text)
                
                # 如果包含中文但没有韩文，说明翻译错误，尝试重新翻译或标记为失败
                if has_chinese and not has_korean:
                    logger.warning(f"翻译结果包含中文但没有韩文，可能翻译方向错误")
                    # 尝试从结果中提取可能的韩文部分
                    lines = translated_text.split('\n')
                    korean_lines = []
                    for line in lines:
                        line = line.strip()
                        # 只保留包含韩文字符的行
                        if any('\uAC00' <= char <= '\uD7A3' for char in line):
                            korean_lines.append(line)
                    if korean_lines:
                        translated_text = '\n'.join(korean_lines)
                    else:
                        # 如果没有韩文，标记为翻译失败
                        logger.error(f"翻译结果没有韩文内容，返回空结果")
                        return {
                            "success": False,
                            "error": "翻译结果不包含韩文，可能模型返回了错误的语言",
                            "translated_text": ""
                        }
                
                # 移除可能的英文提示词
                lines = translated_text.split('\n')
                cleaned_lines = []
                skip_keywords = ['Translation', 'Original text', 'Requirements', 'Note', '翻译', '原文', '要求', 'English', 'Korean']
                
                for line in lines:
                    line = line.strip()
                    # 跳过明显的提示词行
                    if any(keyword in line for keyword in skip_keywords):
                        continue
                    # 跳过空行或只有标点的行
                    if not line or line in ['：', ':', '-', '—']:
                        continue
                    # 优先保留包含韩文字符的行
                    if any('\uAC00' <= char <= '\uD7A3' for char in line):
                        cleaned_lines.append(line)
                    # 如果整行主要是非ASCII字符（可能是韩文），也保留
                    elif not all(c.isascii() or c.isspace() or c in '.,;:!?()[]{}' for c in line):
                        # 检查是否主要是非ASCII字符
                        non_ascii_ratio = sum(1 for c in line if not c.isascii() and not c.isspace()) / max(len(line), 1)
                        if non_ascii_ratio > 0.5:  # 至少50%是非ASCII字符
                            cleaned_lines.append(line)
                
                if cleaned_lines:
                    translated_text = '\n'.join(cleaned_lines)
                else:
                    # 如果清理后没有内容，使用原始结果但移除明显的提示词
                    translated_text = response.strip()
                    # 移除开头的提示词
                    for keyword in ['Translation', '翻译结果', 'Translation (Korean):', 'Translation (한국어):', 'Korean (한국어 only):']:
                        if translated_text.startswith(keyword):
                            translated_text = translated_text[len(keyword):].strip()
                            if translated_text.startswith(':'):
                                translated_text = translated_text[1:].strip()
            
            return {
                "success": True,
                "translated_text": translated_text,
                "source_language": source_language,
                "target_language": target_language
            }
            
        except Exception as e:
            logger.error(f"翻译失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "translated_text": ""
            }
    
    def translate_batch(
        self,
        texts: list,
        source_language: str = "English",
        target_language: str = "Chinese"
    ) -> list:
        """
        批量翻译文本
        
        Args:
            texts: 待翻译的文本列表
            source_language: 源语言
            target_language: 目标语言
            
        Returns:
            翻译结果列表
        """
        results = []
        for text in texts:
            result = self.translate(
                text,
                source_language=source_language,
                target_language=target_language
            )
            results.append(result)
        return results

