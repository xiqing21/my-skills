# pypandoc 支持的文档格式

## 输入格式（常见）

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| docx | .docx | Microsoft Word 2007+ |
| doc | .doc | Microsoft Word 97-2003（需 pandoc 2.0+） |
| pptx | .pptx | Microsoft PowerPoint 2007+ |
| ppt | .ppt | Microsoft PowerPoint 97-2003 |
| pdf | .pdf | Portable Document Format（需安装 LaTeX） |
| html | .html, .htm | HyperText Markup Language |
| rtf | .rtf | Rich Text Format |
| txt | .txt | 纯文本 |
| odt | .odt | OpenDocument Text |
| ods | .ods | OpenDocument Spreadsheet |
| odp | .odp | OpenDocument Presentation |
| md | .md, .markdown | Markdown |
| latex | .tex, .latex | LaTeX |
| epub | .epub | EPUB 电子书 |

## 输出格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| markdown | .md | Markdown |
| html | .html | HTML |
| docx | .docx | Microsoft Word |
| pdf | .pdf | Portable Document Format（需安装 LaTeX） |
| latex | .tex | LaTeX |
| rtf | .rtf | Rich Text Format |
| epub | .epub | EPUB 电子书 |
| plain | .txt | 纯文本 |

## 获取完整格式列表

在 Python 中执行：
```python
import pypandoc
input_formats, output_formats = pypandoc.get_pandoc_formats()
print("输入格式:", input_formats)
print("输出格式:", output_formats)
```

或在命令行执行：
```bash
pandoc --list-input-formats
pandoc --list-output-formats
```

## 注意事项

1. **PDF 输入**: 需要安装额外的工具（如 `pdf2xml`），且转换效果取决于 PDF 的结构
2. **PDF 输出**: 需要安装 LaTeX 引擎（如 TeX Live 或 MiKTeX）
3. **DOC 文件**: 旧版 .doc 格式支持有限，建议先转换为 .docx
4. **PPT 文件**: PowerPoint 文件转换可能丢失部分格式和布局
