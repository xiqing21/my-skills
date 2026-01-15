---
name: pypandoc-converter
description: This skill should be used when converting various document formats (PDF, DOCX, DOC, PPT, PPTX, HTML, etc.) to Markdown. It provides enhanced conversion scripts using pypandoc for reliable format conversion, with a two-step method (DOCX → HTML → MD) specifically designed to handle complex tables and column misalignment issues, and supports both single-file and batch processing.
allowed-tools:
disable: false
---

# Pypandoc Converter

## Overview

This skill enables conversion of multiple document formats to Markdown using pypandoc, a Python wrapper for the universal document converter pandoc. It supports common office formats (DOCX, DOC, PPT, PPTX), PDF, HTML, and others, providing a reliable and efficient way to extract content from various document types.

## Quick Start

To convert a document to Markdown:

1. Verify pypandoc is installed:
   ```bash
   pip install pypandoc
   ```

2. Use the conversion script:
   ```bash
   python .codebuddy/skills/pypandoc-converter/scripts/convert_to_markdown.py <input_file>
   ```

3. The converted Markdown file will be saved in the same directory with `.md` extension.

## Supported Input Formats

Common formats supported for conversion:

- **Microsoft Office**: `.docx`, `.doc`, `.pptx`, `.ppt`
- **Adobe PDF**: `.pdf`
- **Web**: `.html`, `.htm`
- **Other**: `.rtf`, `.txt`, `.odt`, `.ods`, `.odp`, `.epub`, `.tex`

See `references/supported_formats.md` for complete format list.

## Usage Patterns

### Interactive Conversion (Recommended)

Use the interactive converter for automatic analysis and smart recommendations:

```bash
python scripts/interactive_converter.py
```

The interactive tool will:
1. Analyze your file complexity
2. Detect table issues
3. Provide smart recommendations
4. Guide you through method selection
5. Execute the conversion

### Single File Conversion

Convert a specific document to Markdown:

```bash
python scripts/convert_to_markdown.py document.docx
python scripts/convert_to_markdown.py presentation.pptx output.md
```

### Single File with Custom Format

Specify output format for better compatibility:

```bash
python scripts/convert_to_markdown.py --format gfm document.docx
python scripts/convert_to_markdown.py --format gfm document.docx output.md
```

### Grid Tables Conversion

Use grid tables for better complex table support:

```bash
python scripts/convert_to_markdown.py --format "markdown+grid_tables-simple_tables-pipe_tables-multiline_tables" document.docx
```

### Two-Step Conversion for Complex Tables

Handle documents with complex table structures:

```bash
# Automatic two-step conversion
python scripts/convert_to_markdown.py --two-step "docx_with_tables.docx" output.md

# Manual two-step conversion (more control)
python scripts/convert_to_markdown.py --step1 --format html input.docx temp.html
python scripts/convert_to_markdown.py --step2 --format gfm temp.html output.md
```

### Preprocess HTML Tables

Validate and fix HTML table issues:

```bash
# Validate HTML table structure
python scripts/preprocess_html.py --validate temp.html

# Preprocess and fix HTML tables
python scripts/preprocess_html.py temp.html fixed.html
```

### Batch Conversion

Convert multiple files matching a pattern:

```bash
# Regular batch conversion
python scripts/convert_to_markdown.py --batch "*.docx" ./output/

# Batch conversion with two-step method for tables
python scripts/convert_to_markdown.py --batch --two-step "*.docx" ./output/

# Batch conversion with custom format
python scripts/convert_to_markdown.py --batch --format gfm "*.docx" ./output/
```

### Python API Usage

Use the script as a Python module for programmatic conversion:

```python
from scripts.convert_to_markdown import convert_to_markdown, convert_with_html_intermediate
from scripts.preprocess_html import preprocess_html_file, validate_table_structure

# Convert single file
convert_to_markdown('document.docx', 'output.md')

# Convert with custom pandoc options
extra_args = ['--wrap=none', '--toc', '--number-sections']
convert_to_markdown('document.docx', extra_args=extra_args)

# Two-step conversion for complex tables
convert_with_html_intermediate(
    'document_with_tables.docx',
    'output.md',
    format_type='gfm',
    extra_args=['--wrap=none']
)

# Preprocess HTML tables
result = preprocess_html_file('temp.html', 'processed.html')
print(f"Changes made: {result['changes']}")

# Validate HTML table structure
validation = validate_table_structure(html_content)
print(f"Issues found: {validation['issues']}")
```

## Workflow Decision Tree

When a user requests document conversion:

### Option 1: Interactive Mode (Recommended)

1. **Launch interactive converter** - `python scripts/interactive_converter.py`
2. **System analyzes file** - Automatic complexity detection
3. **Review recommendations** - Smart suggestions based on file content
4. **Choose method** - Select from recommended options
5. **Execute conversion** - Automatic processing
6. **Verify output** - Check results

### Option 2: Direct Command Line

1. **Identify input format** - Check file extension or confirm with user
2. **Choose conversion method**:
   - Single file → Use `convert_to_markdown()`
   - Multiple files → Use `batch_convert()`
   - Tables with issues → Use two-step method (DOCX → HTML → MD)
3. **Handle special cases**:
   - PDF conversion may require LaTeX installation
   - DOC format (older) may have limited support
   - PPT conversion may lose some formatting
   - **Complex tables** - Use HTML intermediate format for better table recognition
4. **Verify output** - Check if Markdown content meets user expectations
5. **Apply post-processing** if needed (e.g., cleanup, formatting adjustments)

### Decision Guide

```
Need to convert document?
├─ Prefer interactive guidance?
│  └─ Use: python scripts/interactive_converter.py
│
├─ Simple document, no tables?
│  └─ Use: python scripts/convert_to_markdown.py input.docx
│
├─ Simple tables only?
│  └─ Use: python scripts/convert_to_markdown.py --format gfm input.docx
│
├─ Complex tables with merged cells?
│  └─ Use: python scripts/convert_to_markdown.py --two-step --format gfm input.docx
│
└─ Multiple files?
   └─ Use: python scripts/convert_to_markdown.py --batch --two-step "*.docx" ./output/
```

## Complex Table Handling

### Problem: Table Recognition Issues

When converting DOCX files with complex tables, pandoc may:
- Misidentify table structures
- Create column misalignment (串列问题)
- Fail to properly handle merged cells (colspan/rowspan)
- Produce tables with incorrect column counts

### Solution: Two-Step Conversion (DOCX → HTML → MD)

For documents with table recognition issues, use the two-step conversion method:

#### Method 1: Using Conversion Scripts

```bash
# Step 1: DOCX to HTML (preserves complete table structure)
python .codebuddy/skills/pypandoc-converter/scripts/convert_to_markdown.py \
  --step1 --format html "doc\营销基础数据\管理看板内容.docx" temp.html

# Step 2: HTML to Markdown with GFM (forces pipe tables)
python .codebuddy/skills/pypandoc-converter/scripts/convert_to_markdown.py \
  --step2 --format gfm temp.html output.md
```

#### Method 2: Using Pandoc Directly

```bash
# Step 1: DOCX to HTML
pandoc -f docx -t html -o temp.html "doc\营销基础数据\管理看板内容.docx"

# Step 2: HTML to GFM (forces pipe tables, disables automatic column adjustment)
pandoc -f html -t gfm --wrap=none -o output.md temp.html
```

### Root Causes of Table Issues

1. **Column count mismatch**: HTML tables define different column counts in `<colgroup>` vs actual cells
2. **Merged cells**: `colspan="2"` or `rowspan="2"` attributes confuse the parser
3. **Empty columns**: Hidden or zero-width columns (e.g., `<col style="width: 0%" />`) create offset errors
4. **Complex headers**: Multi-level headers with varying column spans cause alignment problems

### Best Practices for Table Conversion

**Pre-processing HTML** (before conversion to MD):
- Remove empty columns with `width: 0%` or `display: none`
- Eliminate or flatten `colspan` and `rowspan` attributes
- Ensure column counts match between `<colgroup>` and actual table cells
- Validate table structure using HTML validator

**Conversion parameters**:
- Always use `-t gfm` (GitHub Flavored Markdown) for best table support
- Add `--wrap=none` to prevent automatic line breaks that cause column offsets
- Consider `--strip-comments` to remove HTML comments that might interfere

**Example complete workflow**:
```bash
# Convert with table-safe parameters
python scripts/convert_to_markdown.py \
  --two-step \
  --format gfm \
  --extra-args "--wrap=none --extract-media=images" \
  "input.docx" "output.md"
```

## Interactive Conversion Mode

The interactive converter provides a user-friendly interface with automatic analysis and smart recommendations.

### Usage

```bash
python scripts/interactive_converter.py
```

### Features

1. **Automatic File Analysis**
   - Detects table count
   - Identifies merged cells (colspan/rowspan)
   - Finds common table issues

2. **Smart Recommendations**
   - Suggests optimal conversion method
   - Provides reasoning for each recommendation
   - Highlights potential issues

3. **Method Selection Options**

   **Standard Conversion**
   - Basic Markdown format
   - Fast and simple
   - Best for documents without tables

   **Pipe Tables (GFM)**
   - GitHub Flavored Markdown
   - Good for simple tables
   - Widely compatible

   **Grid Tables**
   - Most stable for complex tables
   - Handles merged cells better
   - May need manual formatting adjustments

   **Two-Step (HTML → MD)**
   - Best for complex tables
   - HTML intermediate format
   - Automatic preprocessing

   **Auto-Suggested**
   - System analyzes file
   - Chooses best method
   - Most reliable option

### Interactive Workflow

1. Launch interactive converter
2. Select single-file or batch conversion
3. Enter input file path
4. View analysis results
5. Review system recommendations
6. Choose conversion method
7. Specify output location
8. Wait for conversion to complete

### Example Session

```
============================================================
  Pypandoc 交互式转换工具 v2.0
============================================================

============================================================
  主菜单
============================================================
  1. 单文件转换
  2. 批量转换
  3. 退出
============================================================
  请选择 (输入数字): 1

  请输入要转换的文件路径: doc/营销基础数据/管理看板内容.docx

[分析] 正在分析文件复杂度...

  [分析结果]
    表格数量: 17
    合并单元格: 28
    跨行单元格: 12
    发现问题: 检测到 1 个零宽度列

  [系统推荐]
    1. 先转HTML再转管道表 - 检测到问题: 检测到 1 个零宽度列
    2. 转网格表 - 网格表对复杂表格支持更好

============================================================
  选择转换方法
============================================================
  1. 普通转换 (标准 Markdown)
  2. 转管道表 (GFM - GitHub Flavored Markdown)
  3. 转网格表 (Grid Tables - 更稳定)
  4. 先转HTML再转管道表 (两步法，处理复杂表格)
  5. 系统自动建议 (基于文件分析)
  0. 返回上级菜单
============================================================
  请选择 (输入数字): 5

  输出文件路径 (默认: doc/营销基础数据/管理看板内容.md):

  [开始转换]
    输入: doc/营销基础数据/管理看板内容.docx
    输出: doc/营销基础数据/管理看板内容.md
    格式: gfm
    方法: 两步法 (HTML -> MD)

[STEP 1] 转换: ... -> ... (HTML)
[STEP 1.5] 预处理 HTML 表格...
[STEP 1.5] HTML 表格预处理完成
[STEP 2] 转换: ... -> ... (gfm)
[OK] 两步转换成功: ... -> ...

  [成功] 转换完成!
```

### Conversion Method Comparison

| Method | Best For | Complexity | Output Format |
|--------|----------|------------|---------------|
| Standard | Text-only documents | Low | Markdown |
| GFM Pipe | Simple tables | Low-Medium | GFM |
| Grid Tables | Complex tables, merged cells | High | Grid Tables |
| Two-Step | Very complex tables | High | GFM/Custom |
| Auto-Suggested | Any document | Auto | Auto |

### Troubleshooting Table Issues

If tables still have issues after two-step conversion:

1. **Inspect HTML intermediate**: Open `temp.html` in a browser to verify table structure
2. **Manual HTML correction**: Edit HTML to fix column counts and remove problematic attributes
3. **Alternative formats**: Try `-t markdown_github` or `-t markdown_mmd`
4. **Post-processing**: Use regex or custom scripts to fix table alignment in output MD

### Python API for Two-Step Conversion

```python
from scripts.convert_to_markdown import convert_with_html_intermediate

# Two-step conversion for tables with issues
convert_with_html_intermediate(
    'input.docx',
    'output.md',
    temp_html='temp.html',
    extra_args=['--wrap=none']
)
```

## Common Pandoc Options

Useful extra arguments for conversion:

- `--wrap=none` - Disable automatic line wrapping (recommended for tables)
- `--toc` - Generate table of contents
- `--number-sections` - Number sections in output
- `--extract-media=dir` - Extract embedded media to directory
- `--smart` - Enable smart punctuation
- `--standalone` - Produce standalone HTML with header/footer

Example:
```python
extra_args = ['--wrap=none', '--toc', '--extract-media=images']
convert_to_markdown('input.docx', extra_args=extra_args)
```

## Format Types

Supported output formats for conversion:

- `markdown` - Standard Markdown (default)
- `gfm` - GitHub Flavored Markdown (recommended for tables)
- `markdown_github` - Alternative GitHub Markdown
- `html` - HTML (useful as intermediate format)
- `markdown_mmd` - MultiMarkdown
- `commonmark` - CommonMark specification

For complex tables, always use `gfm` format for best results.

## Troubleshooting

### Pandoc Not Found

If encountering "No pandoc was found" error:

1. Install pandoc system-wide (see `references/installation_guide.md`)
2. Or use `pypandoc_binary` instead of `pypandoc`
3. Or set environment variable:
   ```python
   import os
   os.environ['PYPANDOC_PANDOC'] = '/path/to/pandoc'
   ```

### PDF Conversion Issues

PDF conversion quality depends on:
- PDF structure (text-based vs image-based)
- Pandoc version (use 2.0+ for better PDF support)
- LaTeX installation (required for PDF output)

For scanned/image-based PDFs, consider OCR tools first.

### Encoding Issues

For non-UTF-8 documents:
```python
convert_to_markdown('input.docx', encoding='gbk')  # or other encoding
```

### Table Column Misalignment (串列问题)

**Symptoms**: Table data appears in wrong columns after conversion.

**Solution**: Use two-step conversion method described in "Complex Table Handling" section above.

**Common causes**:
- HTML tables with inconsistent column counts
- Merged cells (colspan/rowspan) not properly handled
- Hidden or zero-width columns causing offset errors

**Quick fix**:
```bash
# Two-step conversion with GFM
python scripts/convert_to_markdown.py --two-step --format gfm input.docx output.md
```

## Resources

### scripts/

**interactive_converter.py** - Interactive conversion tool providing:
- Automatic file complexity analysis
- Smart conversion recommendations
- Interactive method selection menu
- Support for multiple table formats (standard, GFM, Grid, Two-Step)
- User-friendly prompts and guidance
- Best choice for beginners and uncertain users

**convert_to_markdown.py** - Main conversion script providing:
- Single file conversion (`convert_to_markdown()`)
- Batch conversion (`batch_convert()`)
- Two-step conversion for complex tables (`convert_with_html_intermediate()`)
- Command-line interface with `--step1`, `--step2`, `--two-step`, `--format` options
- Custom pandoc argument support
- Format type specification (markdown, gfm, html, etc.)

**preprocess_html.py** - HTML table preprocessing tool providing:
- Automatic removal of empty columns (width: 0%, display: none)
- Validation of HTML table structure
- Detection of merged cells (colspan/rowspan)
- Command-line interface for standalone use
- Python API for programmatic processing

### references/

**table_conversion_guide.md** - Comprehensive guide for handling complex table conversion issues, including:
- Root cause analysis of table misalignment problems
- Step-by-step solutions for two-step conversion method
- Best practices for HTML preprocessing
- Troubleshooting common table conversion issues
- Real-world examples and case studies

**supported_formats.md** - Complete list of supported input and output formats, including format descriptions and usage notes.

**installation_guide.md** - Detailed installation instructions for pypandoc and pandoc, troubleshooting common issues, and verification steps.

### assets/

This skill does not require asset files. Delete this directory if present.
