# PDF 中文字体修复说明

## 问题描述

翻译后的 PDF 文件中，中文文本显示为黑色矩形块，无法正常阅读。

## 问题原因

PDF 生成代码使用了 `Helvetica` 字体，该字体不支持中文字符。当 ReportLab 尝试渲染中文字符时，如果字体不支持，就会显示为黑色矩形块。

## 修复方案

### 1. 添加中文字体支持

使用 ReportLab 的 `UnicodeCIDFont` 来注册中文字体：

```python
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics

# 尝试注册中文字体
try:
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    font_name = 'STSong-Light'
except:
    try:
        pdfmetrics.registerFont(UnicodeCIDFont('STHeiti-Light'))
        font_name = 'STHeiti-Light'
    except:
        # 使用默认字体（可能不支持中文）
        font_name = 'Helvetica'
```

### 2. 改进文本绘制

- 添加了错误处理机制
- 改进了中文文本的换行逻辑
- 优化了编码处理

### 3. 两种 PDF 生成方法都修复

- **高级方法**（SimpleDocTemplate）：使用支持中文的字体
- **简单方法**（Canvas）：也添加了中文字体支持

## 修复后的效果

- ✅ 中文文本可以正常显示
- ✅ 不再出现黑色矩形块
- ✅ 支持中英文混合文本
- ✅ 改进了文本换行和布局

## 测试建议

1. 重新上传 PDF 文件
2. 选择源语言和目标语言（例如：English → Chinese）
3. 点击 Submit 开始翻译
4. 下载翻译后的 PDF 文件
5. 检查中文文本是否正常显示

## 注意事项

- 如果系统没有安装中文字体，ReportLab 会尝试使用内置的 CID 字体
- 某些特殊字符可能仍然无法显示（取决于字体支持）
- 如果仍有问题，可能需要安装额外的中文字体文件

