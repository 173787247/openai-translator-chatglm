#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试英文到韩文翻译"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from translator import ChatGLMTranslator

def test_english_to_korean():
    print("正在初始化翻译器...")
    translator = ChatGLMTranslator()
    
    print("\n测试翻译: 'Hello, how are you?' -> 韩文")
    result = translator.translate(
        text="Hello, how are you?",
        source_language="English",
        target_language="Korean"
    )
    
    if result["success"]:
        print(f"✅ 翻译成功!")
        print(f"原文: Hello, how are you?")
        print(f"翻译结果: {result['translated_text']}")
    else:
        print(f"❌ 翻译失败: {result.get('error', '未知错误')}")
    
    print("\n测试翻译: 'This is a test document.' -> 韩文")
    result2 = translator.translate(
        text="This is a test document.",
        source_language="English",
        target_language="Korean"
    )
    
    if result2["success"]:
        print(f"✅ 翻译成功!")
        print(f"原文: This is a test document.")
        print(f"翻译结果: {result2['translated_text']}")
    else:
        print(f"❌ 翻译失败: {result2.get('error', '未知错误')}")
    
    return result["success"] and result2["success"]

if __name__ == "__main__":
    success = test_english_to_korean()
    sys.exit(0 if success else 1)

