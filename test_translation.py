#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试翻译功能"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from translator import ChatGLMTranslator

def test_translation():
    print("正在初始化翻译器...")
    translator = ChatGLMTranslator()
    
    print("\n测试翻译: 'Hello, how are you?' -> 中文")
    result = translator.translate(
        text="Hello, how are you?",
        source_language="English",
        target_language="Chinese"
    )
    
    if result["success"]:
        print(f"✅ 翻译成功!")
        print(f"翻译结果: {result['translated_text']}")
    else:
        print(f"❌ 翻译失败: {result.get('error', '未知错误')}")
    
    return result["success"]

if __name__ == "__main__":
    success = test_translation()
    sys.exit(0 if success else 1)

