# Pypandoc Converter - 快速参考卡

## 🎯 核心功能

将各种文档格式（DOCX, PDF, PPT, HTML 等）转换为 Markdown，特别优化了复杂表格的转换。

## ⚡ 快速开始

### 交互式转换（推荐新手）

```bash
python scripts/interactive_converter.py
```

**优势**:
- ✅ 自动分析文件复杂度
- ✅ 智能推荐转换方法
- ✅ 交互式选择界面
- ✅ 支持多种表格格式

### 基础转换

```bash
# 简单转换
python scripts/convert_to_markdown.py document.docx

# 指定输出文件
python scripts/convert_to_markdown.py document.docx output.md
```

### 处理复杂表格（推荐）

**方法 1: 交互式模式（最简单）**
```bash
python scripts/interactive_converter.py
# 系统会自动分析并推荐最佳方法
```

**方法 2: 两步转换法（自动）**
```bash
python scripts/convert_to_markdown.py --two-step document.docx output.md
```

**方法 3: 使用 GFM 格式**
```bash
python scripts/convert_to_markdown.py --format gfm --two-step document.docx output.md
```

**方法 4: 转换为网格表（最稳定）**
```bash
python scripts/convert_to_markdown.py --format "markdown+grid_tables-simple_tables-pipe_tables-multiline_tables" document.docx
```

### 批量转换

```bash
# 批量转换
python scripts/convert_to_markdown.py --batch "*.docx" ./output/

# 批量转换（使用两步法）
python scripts/convert_to_markdown.py --batch --two-step "*.docx" ./output/
```

## 📊 转换方法对比

| 方法 | 适用场景 | 复杂度 | 表格支持 | 推荐度 |
|------|----------|--------|----------|--------|
| **交互式模式** | 不确定用哪个方法 | 低 | 自动选择 | ⭐⭐⭐⭐⭐ |
| **普通转换** | 纯文本文档 | 最低 | 无 | ⭐⭐ |
| **GFM 管道表** | 简单表格 | 低 | 良好 | ⭐⭐⭐⭐ |
| **网格表** | 复杂表格 | 中 | 优秀 | ⭐⭐⭐⭐ |
| **两步法** | 非常复杂表格 | 中高 | 优秀 | ⭐⭐⭐⭐⭐ |

### 方法选择决策树

```
需要转换文档？
├─ 不确定用哪个方法？
│  └─ 使用交互式模式（推荐）
│
├─ 只有文本，没有表格？
│  └─ 普通转换
│
├─ 有简单表格？
│  └─ GFM 管道表
│
├─ 有复杂表格（合并单元格）？
│  ├─ 尝试网格表
│  └─ 或使用两步法
│
└─ 多个文件？
   └─ 批量转换 + 两步法
```

## 🔧 常用命令

### 单文件转换

```bash
# 默认 Markdown 格式
python scripts/convert_to_markdown.py input.docx

# GFM 格式（推荐用于表格）
python scripts/convert_to_markdown.py --format gfm input.docx

# 两步转换法（处理复杂表格）
python scripts/convert_to_markdown.py --two-step input.docx
```

### 分步转换（高级）

```bash
# 步骤 1: DOCX -> HTML
python scripts/convert_to_markdown.py --step1 --format html input.docx temp.html

# 预处理 HTML
python scripts/preprocess_html.py temp.html processed.html

# 步骤 2: HTML -> Markdown
python scripts/convert_to_markdown.py --step2 --format gfm processed.html output.md
```

### HTML 表格处理

```bash
# 验证 HTML 表格
python scripts/preprocess_html.py --validate temp.html

# 预处理 HTML 表格
python scripts/preprocess_html.py temp.html fixed.html
```

## 📊 表格问题解决方案

### 问题：表格列偏移（串列）

**解决方案**：使用两步转换法

```bash
python scripts/convert_to_markdown.py --two-step --format gfm doc.docx output.md
```

### 问题：表格识别失败

**解决方案**：先转 HTML，预处理后再转 MD

```bash
# 第一步：转 HTML
python scripts/convert_to_markdown.py --step1 --format html doc.docx temp.html

# 第二步：预处理
python scripts/preprocess_html.py temp.html fixed.html

# 第三步：转 MD
python scripts/convert_to_markdown.py --step2 --format gfm fixed.html output.md
```

### 问题：合并单元格错误

**解决方案**：手动修复 HTML 或禁用预处理中的合并处理

```python
from scripts.convert_to_markdown import convert_with_html_intermediate

convert_with_html_intermediate(
    'input.docx',
    'output.md',
    preprocess=False  # 禁用自动预处理，手动修复 HTML
)
```

## 🐍 Python API

### 基础转换

```python
from scripts.convert_to_markdown import convert_to_markdown

convert_to_markdown('input.docx', 'output.md')
```

### 复杂表格转换

```python
from scripts.convert_to_markdown import convert_with_html_intermediate

convert_with_html_intermediate(
    'input.docx',
    'output.md',
    format_type='gfm',
    extra_args=['--wrap=none']
)
```

### HTML 预处理

```python
from scripts.preprocess_html import preprocess_html_file, validate_table_structure

# 预处理 HTML
result = preprocess_html_file('temp.html', 'fixed.html')
print(f"修改: {result['changes']}")

# 验证表格
validation = validate_table_structure(html_content)
print(f"问题: {validation['issues']}")
```

## 📋 支持的格式

### 输入格式

- **Microsoft Office**: `.docx`, `.doc`, `.pptx`, `.ppt`
- **Adobe PDF**: `.pdf`
- **Web**: `.html`, `.htm`
- **其他**: `.rtf`, `.txt`, `.odt`, `.ods`, `.odp`, `.epub`, `.tex`

### 输出格式

- `markdown` - 标准 Markdown（默认）
- `gfm` - GitHub Flavored Markdown（推荐用于表格）
- `html` - HTML（中间格式）
- `markdown_github` - GitHub Markdown
- `markdown_mmd` - MultiMarkdown

## 🛠️ Pandoc 选项

| 选项 | 说明 | 推荐场景 |
|------|------|----------|
| `--wrap=none` | 禁用自动换行 | 表格转换（推荐） |
| `--toc` | 生成目录 | 长文档 |
| `--extract-media=dir` | 提取媒体文件 | 包含图片的文档 |
| `--standalone` | 生成独立 HTML | HTML 输出 |

## 📚 详细文档

- **SKILL.md** - 完整技能文档
- **references/table_conversion_guide.md** - 表格转换详细指南
- **examples/table_conversion_example.py** - 使用示例
- **references/supported_formats.md** - 支持格式列表
- **references/installation_guide.md** - 安装指南

## 🔍 故障排除

### Pandoc 未找到

```bash
# 安装 pandoc
# Windows (使用 Chocolatey)
choco install pandoc

# macOS (使用 Homebrew)
brew install pandoc

# Linux
sudo apt-get install pandoc
```

### 安装 pypandoc

```bash
pip install pypandoc
```

### 检查版本

```bash
pandoc --version  # 需要 2.0+
pip show pypandoc
```

## 💡 最佳实践

1. **处理表格**：始终使用 `--format gfm` 和 `--two-step`
2. **批量处理**：使用 `--batch` 选项提高效率
3. **提取媒体**：使用 `--extract-media` 保存图片
4. **验证 HTML**：转换前使用 `preprocess_html.py --validate` 检查
5. **保存中间文件**：调试时保留 HTML 中间文件

## 📞 获取帮助

```bash
# 查看帮助
python scripts/convert_to_markdown.py
python scripts/preprocess_html.py
```

---

**注意**：对于特别复杂的表格，可能需要手动修复 HTML 中间文件。详细步骤请参考 `references/table_conversion_guide.md`。
