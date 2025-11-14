"""
Gradio 图形界面
基于 ChatGLM2-6B 的 PDF 电子书翻译工具
"""
import gradio as gr
import logging
import os
from translator import ChatGLMTranslator
from pdf_processor import PDFProcessor
from utils import get_pdf_info, format_file_size
from config import (
    SUPPORTED_LANGUAGES,
    GRADIO_SERVER_NAME,
    GRADIO_SERVER_PORT,
    GRADIO_SHARE,
    TEMP_DIR,
    OUTPUT_DIR
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化翻译器和 PDF 处理器
translator = None
pdf_processor = None

try:
    logger.info("正在初始化 ChatGLM2-6B 翻译器...")
    translator = ChatGLMTranslator()
    pdf_processor = PDFProcessor(translator=translator)
    logger.info("初始化成功")
except Exception as e:
    logger.error(f"初始化失败: {str(e)}")
    translator = None
    pdf_processor = None


def translate_pdf(
    pdf_file,
    source_language: str,
    target_language: str,
    progress=gr.Progress()
):
    """
    翻译 PDF 文件（带进度显示）
    
    Args:
        pdf_file: 上传的 PDF 文件
        source_language: 源语言
        target_language: 目标语言
        progress: Gradio 进度对象
        
    Returns:
        (输出文件路径, 状态信息)
    """
    if not pdf_processor:
        return None, "❌ 错误: PDF 处理器未初始化"
    
    if pdf_file is None:
        return None, "⚠️ 请上传 PDF 文件"
    
    try:
        # 获取上传的文件路径
        input_path = pdf_file.name if hasattr(pdf_file, 'name') else pdf_file
        
        # 生成输出文件路径
        import time
        timestamp = int(time.time())
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}_translated_{timestamp}{ext}"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # 定义进度回调
        def progress_callback(current, total, message):
            if progress:
                progress(current / total, desc=message)
        
        # 翻译 PDF
        result = pdf_processor.translate_pdf(
            pdf_path=input_path,
            output_path=output_path,
            source_language=source_language,
            target_language=target_language,
            progress_callback=progress_callback
        )
        
        if result["success"]:
            status = f"✅ 翻译完成！共翻译 {result['pages_translated']} 页\n文件已保存到: {output_filename}"
            return output_path, status
        else:
            error_msg = result.get("error", "未知错误")
            return None, f"❌ 翻译失败: {error_msg}"
            
    except Exception as e:
        logger.error(f"PDF 翻译异常: {str(e)}")
        return None, f"❌ 翻译异常: {str(e)}"


def translate_text(
    text: str,
    source_language: str,
    target_language: str
):
    """
    翻译文本
    
    Args:
        text: 待翻译文本
        source_language: 源语言
        target_language: 目标语言
        
    Returns:
        (翻译结果, 状态信息)
    """
    if not translator:
        return "", "❌ 错误: 翻译器未初始化"
    
    if not text or not text.strip():
        return "", "⚠️ 请输入要翻译的文本"
    
    try:
        result = translator.translate(
            text=text,
            source_language=source_language,
            target_language=target_language
        )
        
        if result["success"]:
            status = f"✅ 翻译完成: {source_language} → {target_language}"
            return result["translated_text"], status
        else:
            error_msg = result.get("error", "未知错误")
            return "", f"❌ 翻译失败: {error_msg}"
            
    except Exception as e:
        logger.error(f"文本翻译异常: {str(e)}")
        return "", f"❌ 翻译异常: {str(e)}"


# 构建 Gradio 界面
with gr.Blocks(
    title="OpenAI-Translator v2.0 (PDF电子书翻译工具)",
    theme=gr.themes.Monochrome()
) as app:
    
    gr.Markdown(
        """
        <div style="text-align: center;">
            <h1>OpenAI-Translator v2.0 (PDF电子书翻译工具)</h1>
        </div>
        """,
        elem_classes="title"
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📄 上传PDF文件")
            pdf_input = gr.File(
                label="上传PDF文件",
                file_types=[".pdf"],
                type="filepath",
                height=300
            )
            pdf_info = gr.Markdown(
                value="等待上传文件...",
                visible=True
            )
        
        with gr.Column(scale=1):
            gr.Markdown("### 📥 下载翻译文件")
            pdf_output = gr.File(
                label="下载翻译文件",
                type="filepath",
                interactive=False,
                height=300
            )
    
    # 更新 PDF 信息
    def update_pdf_info(file):
        if file is None:
            return gr.update(value="等待上传文件...", visible=True)
        
        try:
            input_path = file.name if hasattr(file, 'name') else file
            info = get_pdf_info(input_path)
            if info["success"]:
                info_text = f"""
                **文件信息**:
                - 文件名: {info['file_name']}
                - 总页数: {info['total_pages']} 页
                - 文件大小: {info['file_size']}
                """
                return gr.update(value=info_text, visible=True)
            else:
                return gr.update(value=f"⚠️ 无法读取文件信息: {info.get('error', '未知错误')}", visible=True)
        except Exception as e:
            return gr.update(value=f"⚠️ 错误: {str(e)}", visible=True)
    
    pdf_input.change(
        fn=update_pdf_info,
        inputs=[pdf_input],
        outputs=[pdf_info]
    )
    
    with gr.Row():
        with gr.Column():
            source_lang = gr.Dropdown(
                label="源语言 (默认: 英文)",
                choices=list(SUPPORTED_LANGUAGES.keys()),
                value="English",
                info="选择源语言"
            )
        
        with gr.Column():
            target_lang = gr.Dropdown(
                label="目标语言 (默认: 中文)",
                choices=list(SUPPORTED_LANGUAGES.keys()),
                value="Chinese",
                info="选择目标语言"
            )
    
    with gr.Row():
        clear_btn = gr.Button("Clear", variant="secondary", scale=1)
        submit_btn = gr.Button("Submit", variant="primary", scale=1)
    
    status_text = gr.Textbox(
        label="状态",
        interactive=False,
        value="就绪",
        lines=3
    )
    
    # 模型状态显示
    model_status = gr.Markdown(
        value=f"""
        ### 🔧 系统状态
        - **翻译器**: {'✅ 已加载' if translator else '❌ 未初始化'}
        - **PDF 处理器**: {'✅ 已加载' if pdf_processor else '❌ 未初始化'}
        - **设备**: {translator.device if translator else 'N/A'}
        """
    )
    
    # 文本翻译区域（可选）
    with gr.Accordion("文本翻译", open=False):
        with gr.Row():
            with gr.Column():
                text_input = gr.Textbox(
                    label="输入文本",
                    lines=5,
                    placeholder="请输入要翻译的文本..."
                )
            
            with gr.Column():
                text_output = gr.Textbox(
                    label="翻译结果",
                    lines=5,
                    interactive=False
                )
        
        text_translate_btn = gr.Button("翻译文本", variant="primary")
    
    # 绑定事件
    submit_btn.click(
        fn=translate_pdf,
        inputs=[pdf_input, source_lang, target_lang],
        outputs=[pdf_output, status_text],
        show_progress=True
    )
    
    clear_btn.click(
        fn=lambda: (None, None, "English", "Chinese", "等待上传文件...", "已清空"),
        outputs=[pdf_input, pdf_output, source_lang, target_lang, pdf_info, status_text]
    )
    
    # 添加示例
    gr.Examples(
        examples=[
            ["English", "Chinese"],
            ["English", "Japanese"],
            ["Japanese", "Chinese"],
        ],
        inputs=[source_lang, target_lang],
        label="快速选择语言组合"
    )
    
    text_translate_btn.click(
        fn=translate_text,
        inputs=[text_input, source_lang, target_lang],
        outputs=[text_output, status_text]
    )
    
    gr.Markdown(
        """
        ### 💡 使用说明
        
        1. **PDF 翻译**：
           - 点击"上传PDF文件"区域上传 PDF 文件
           - 设置源语言和目标语言（默认：英文 → 中文）
           - 点击 "Submit" 开始翻译
           - 翻译完成后，在右侧下载翻译文件
        
        2. **文本翻译**：
           - 展开"文本翻译"区域
           - 输入要翻译的文本
           - 点击"翻译文本"按钮
        
        3. **支持的语言**：
           - English, Chinese, Japanese, Korean, French, German, Spanish, Italian, Portuguese, Russian, Arabic, Thai, Vietnamese, Hindi, Turkish 等
        
        ### ⚠️ 注意事项
        
        - 首次运行需要下载 ChatGLM2-6B 模型，可能需要较长时间
        - 建议使用 GPU 加速（如果可用）
        - 大型 PDF 文件翻译可能需要较长时间
        """
    )


def main():
    """启动 Gradio 应用"""
    if not translator:
        print("⚠️  警告: 翻译器未初始化")
        print("请检查模型路径和设备配置")
        print("应用仍将启动，但翻译功能将不可用")
    
    app.launch(
        server_name=GRADIO_SERVER_NAME,
        server_port=GRADIO_SERVER_PORT,
        share=GRADIO_SHARE
    )


if __name__ == "__main__":
    main()

