"""
测试 Gradio 是否能正常启动
"""
import sys
import os

# 设置 UTF-8 编码
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')

try:
    import gradio as gr
    print("[OK] Gradio 已安装")
except ImportError:
    print("[ERROR] Gradio 未安装")
    print("正在尝试安装...")
    os.system("pip install gradio --quiet")
    try:
        import gradio as gr
        print("[OK] Gradio 安装成功")
    except ImportError:
        print("[ERROR] Gradio 安装失败，请手动安装: pip install gradio")
        sys.exit(1)

# 创建简单的测试界面
def test_function(text):
    return f"你输入了: {text}"

with gr.Blocks(title="测试界面") as app:
    gr.Markdown("# 测试界面")
    gr.Markdown("如果能看到这个界面，说明 Gradio 工作正常")
    
    with gr.Row():
        input_text = gr.Textbox(label="输入文本", placeholder="输入一些文字...")
        output_text = gr.Textbox(label="输出", interactive=False)
    
    btn = gr.Button("测试")
    btn.click(fn=test_function, inputs=input_text, outputs=output_text)
    
    gr.Markdown("### 状态")
    gr.Markdown("✅ Gradio 运行正常")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("启动测试界面...")
    print("="*50)
    print("\n如果成功，浏览器将自动打开: http://localhost:7860")
    print("按 Ctrl+C 停止\n")
    
    try:
        app.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            inbrowser=True
        )
    except Exception as e:
        print(f"[ERROR] 启动失败: {str(e)}")
        print("\n可能的原因:")
        print("1. 端口 7860 已被占用")
        print("2. 防火墙阻止")
        print("3. 其他错误")
        sys.exit(1)

