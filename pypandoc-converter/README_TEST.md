# pypandoc-converter Skill 测试指南

## 错误原因分析

### 问题 1: 不支持的 pandoc 选项

**错误信息**: `Unknown option --atx-headers`

**原因**: 
- `--atx-headers` 选项在较新版本的 pandoc 中已被移除或更名
- 当前 pandoc 版本: 3.8.3
- 该选项在 pandoc 2.x 版本中有效，但 3.x 版本已不再支持

**解决方案**:
- 已从脚本默认参数中移除 `--atx-headers` 选项
- pandoc 会自动使用合适的标题格式输出 Markdown

### 问题 2: Windows 控制台编码问题

**错误信息**: `UnicodeEncodeError: 'gbk' codec can't encode character '\u2717'`

**原因**:
- Windows 控制台默认使用 GBK 编码
- 脚本中使用了 Unicode 符号 `✓` 和 `✗`
- 这些符号无法在 GBK 编码的控制台中正确显示

**解决方案**:
- 将 Unicode 符号替换为 ASCII 字符: `[OK]` 和 `[ERROR]`
- 确保在所有平台（Windows/Linux/macOS）上都能正常显示

## 修复后的使用方法

### 方法 1: 直接使用 pypandoc API

```python
import pypandoc

# 简单转换
pypandoc.convert_file('input.docx', 'markdown', outputfile='output.md')

# 带额外参数
extra_args = ['--wrap=none', '--toc']
pypandoc.convert_file('input.docx', 'markdown', outputfile='output.md', extra_args=extra_args)
```

### 方法 2: 使用 skill 的转换脚本

```python
import sys
sys.path.insert(0, '.codebuddy/skills/pypandoc-converter/scripts')
from convert_to_markdown import convert_to_markdown

# 基本转换
convert_to_markdown('input.docx', 'output.md')

# 自定义参数
extra_args = ['--wrap=none', '--toc', '--number-sections']
convert_to_markdown('input.docx', extra_args=extra_args)
```

## 测试验证

运行以下命令测试转换功能：

```bash
python -c "import sys; sys.path.insert(0, '.codebuddy/skills/pypandoc-converter/scripts'); from convert_to_markdown import convert_to_markdown; convert_to_markdown('doc/管理看板内容.docx', 'doc/测试.md')"
```

## 优化建议

1. **pandoc 选项兼容性**: 使用前检查 pandoc 版本，只使用当前版本支持的选项
2. **跨平台编码**: 避免使用 Unicode 特殊字符，或设置正确的控制台编码
3. **错误处理**: 捕获并友好地显示 pandoc 执行错误
4. **版本检测**: 可选功能，自动检测 pandoc 版本并适配不同版本的选项

## Pandoc 版本兼容性检查

```python
import pypandoc

version = pypandoc.get_pandoc_version()
print(f"当前 pandoc 版本: {version}")

# 根据版本调整参数
major_version = int(version.split('.')[0])
if major_version >= 3:
    # pandoc 3.x 版本的参数
    extra_args = ['--wrap=none']
else:
    # pandoc 2.x 版本的参数
    extra_args = ['--wrap=none', '--atx-headers']
```
