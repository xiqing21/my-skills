# 表格转换指南 - 复杂表格问题解决方案

## 问题概述

在将 DOCX 文件转换为 Markdown 时，复杂表格经常出现以下问题：

1. **列偏移（串列问题）**: 表格数据出现在错误的列中
2. **表格识别失败**: 表格被识别为纯文本
3. **合并单元格处理不当**: `colspan` 或 `rowspan` 导致列数计算错误
4. **空列干扰**: 隐藏的零宽度列导致列对齐错误

## 核心原因分析

### 1. HTML 表格结构混乱

**问题表现**:
- `<colgroup>` 定义的列数与实际单元格列数不匹配
- 存在 `width: 0%` 的隐藏空列
- 表头和表体的列数不一致

**示例**:
```html
<!-- 错误：colgroup 定义 12 列，但实际只有 11 列 -->
<colgroup>
  <col style="width: 8.33%" />
  <col style="width: 0%" />  <!-- 问题：零宽度空列 -->
  <col style="width: 8.33%" />
  <!-- ... 更多列 -->
</colgroup>
```

### 2. 合并单元格冲突

**问题表现**:
- `colspan="2"` 导致列数计算错误
- 多级表头中不同层的合并策略冲突
- 嵌套的合并单元格造成解析困难

**示例**:
```html
<!-- 问题：colspan 导致列偏移 -->
<tr>
  <th colspan="3">430 抢装</th>
  <th colspan="3">531 抢装</th>  <!-- 同比列 colspan="2"，但总列数计算错误 -->
  <th colspan="3">新能源全量</th>
</tr>
```

### 3. Pandoc 解析限制

**问题表现**:
- Pandoc 无法正确处理复杂的 HTML 表格结构
- 自动列调整算法在遇到合并单元格时失效
- 默认的 `markdown` 格式对表格支持有限

## 解决方案

### 方案一：两步转换法（推荐）

#### 步骤 1: DOCX → HTML

保留完整的表格结构，使用 HTML 作为中间格式：

```bash
pandoc -f docx -t html -o temp.html "input.docx"
```

或使用 Python 脚本：

```python
from scripts.convert_to_markdown import convert_to_markdown

convert_to_markdown('input.docx', 'temp.html', format_type='html')
```

#### 步骤 2: 预处理 HTML（关键）

修复 HTML 表格中的问题：

```bash
python scripts/preprocess_html.py temp.html processed.html
```

或在 Python 中：

```python
from scripts.preprocess_html import preprocess_html_file

preprocess_html_file('temp.html', 'processed.html')
```

预处理会自动：
- 删除零宽度空列
- 删除空的 `<colgroup>` 标签
- 标准化空白字符

#### 步骤 3: HTML → Markdown

使用 GFM 格式强制输出管道表：

```bash
pandoc -f html -t gfm --wrap=none -o output.md processed.html
```

或使用 Python 脚本：

```python
from scripts.convert_to_markdown import convert_to_markdown

extra_args = ['--wrap=none']
convert_to_markdown('processed.html', 'output.md', format_type='gfm', extra_args=extra_args)
```

### 方案二：一键两步转换（更简单）

使用 Python 脚本的内置两步转换功能：

```bash
python scripts/convert_to_markdown.py --two-step input.docx output.md
```

这会自动执行：
1. DOCX → HTML 转换
2. HTML 预处理
3. HTML → GFM Markdown 转换

### 方案三：手动 HTML 修复（高级）

对于特别复杂的表格，可能需要手动修复 HTML：

#### 修复要点

1. **统一列数**:
   ```html
   <!-- 确保所有行的列数一致 -->
   <table>
     <colgroup>
       <col style="width: 25%" />
       <col style="width: 25%" />
       <col style="width: 25%" />
       <col style="width: 25%" />
     </colgroup>
     <tr>
       <td>数据 1</td>
       <td>数据 2</td>
       <td>数据 3</td>
       <td>数据 4</td>
     </tr>
   </table>
   ```

2. **删除 colspan/rowspan**:
   ```html
   <!-- 避免：合并单元格 -->
   <td colspan="2">合并内容</td>

   <!-- 推荐：拆分为独立单元格 -->
   <td>合并内容</td>
   <td></td>
   ```

3. **删除空列**:
   ```html
   <!-- 避免：零宽度列 -->
   <col style="width: 0%" />

   <!-- 推荐：完全删除 -->
   <!-- （无此行） -->
   ```

#### 手动修复流程

1. 在浏览器中打开 `temp.html`，使用开发者工具检查表格结构
2. 使用文本编辑器打开 `temp.html`，搜索 `<table>` 标签
3. 逐个检查并修复表格问题
4. 保存后重新执行步骤 3 的转换

## 最佳实践

### 1. 使用 GFM 格式

GitHub Flavored Markdown 对表格支持最好：

```bash
pandoc -f html -t gfm --wrap=none
```

### 2. 禁用自动换行

自动换行可能导致单元格内容被错误分割：

```bash
pandoc --wrap=none
```

### 3. 提取媒体文件

如果表格包含图片，提取到单独目录：

```bash
pandoc --extract-media=images
```

### 4. 批量处理

批量转换多个 DOCX 文件：

```bash
python scripts/convert_to_markdown.py --batch --two-step "*.docx" ./output/
```

## 故障排除

### 问题 1: 转换后表格仍是乱序

**原因**: HTML 预处理未完全修复问题

**解决**:
```bash
# 验证 HTML 表格
python scripts/preprocess_html.py --validate temp.html

# 手动修复 HTML 后再转换
```

### 问题 2: 表格数据丢失

**原因**: Pandoc 版本过旧

**解决**:
```bash
# 升级 pandoc
pandoc --version  # 检查版本，需要 2.0+

# 升级 pypandoc
pip install --upgrade pypandoc
```

### 问题 3: 转换速度慢

**原因**: 大文件或复杂表格

**解决**:
```bash
# 使用 --quiet 参数减少输出
pandoc --quiet -f html -t gfm input.html output.md
```

## 实际案例

### 案例：营销数据报表转换

**问题描述**:
- DOCX 文件包含 3 个复杂表格
- 表格有多级表头，包含合并单元格
- 直接转换出现列偏移问题

**解决步骤**:
```bash
# 1. 两步转换
python scripts/convert_to_markdown.py --two-step \
  "营销基础数据\管理看板内容.docx" output.md

# 2. 检查输出
cat output.md

# 3. 如有问题，手动修复中间 HTML
python scripts/preprocess_html.py temp.html fixed.html
python scripts/convert_to_markdown.py --step2 --format gfm fixed.html output.md
```

**结果**:
- 表格结构完整保留
- 列对齐正确
- 数据无误

## 工具参考

### Python API

```python
from scripts.convert_to_markdown import convert_with_html_intermediate

# 基本用法
markdown = convert_with_html_intermediate(
    'input.docx',
    'output.md',
    format_type='gfm'
)

# 高级用法
markdown = convert_with_html_intermediate(
    'input.docx',
    'output.md',
    temp_html='custom_temp.html',  # 自定义中间文件
    format_type='gfm',
    extra_args=['--wrap=none', '--extract-media=images'],
    preprocess=True  # 启用自动预处理
)
```

### 命令行工具

```bash
# 单文件转换
python scripts/convert_to_markdown.py document.docx output.md

# 指定格式
python scripts/convert_to_markdown.py --format gfm document.docx output.md

# 两步转换
python scripts/convert_to_markdown.py --two-step document.docx output.md

# 批量转换
python scripts/convert_to_markdown.py --batch --two-step "*.docx" ./output/

# 分步转换（高级）
python scripts/convert_to_markdown.py --step1 --format html doc.docx temp.html
python scripts/preprocess_html.py temp.html processed.html
python scripts/convert_to_markdown.py --step2 --format gfm processed.html output.md

# 验证 HTML 表格
python scripts/preprocess_html.py --validate temp.html
```

## 总结

**核心原则**:
1. 优先使用两步转换法（DOCX → HTML → MD）
2. HTML 预处理是解决表格问题的关键
3. 使用 GFM 格式获得最佳表格支持
4. 对复杂表格，可能需要手动修复 HTML

**快速决策树**:
```
是否是 DOCX 文件？
├─ 是 → 是否有复杂表格？
│   ├─ 是 → 使用两步转换法
│   └─ 否 → 普通转换
└─ 否 → 直接转换
```
