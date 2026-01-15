# pypandoc 安装指南

## 安装方法

### 方法 1: 使用 pip 安装 pypandoc（需单独安装 pandoc）

```bash
pip install pypandoc
```

然后安装 pandoc：

**Windows:**
- 下载安装包: https://pandoc.org/installing.html
- 或使用 chocolatey: `choco install pandoc`
- 或使用 pypandoc 自动下载:
  ```python
  from pypandoc.pandoc_download import download_pandoc
  download_pandoc()
  ```

**macOS:**
```bash
brew install pandoc
```

**Linux:**
```bash
sudo apt-get install pandoc  # Ubuntu/Debian
sudo dnf install pandoc        # Fedora
```

### 方法 2: 使用 pypandoc_binary（推荐新手）

```bash
pip install pypandoc_binary
```

注意: `pypandoc_binary` 内置了 pandoc，但仅支持 Windows 和 macOS（64位），Linux 需自行构建。

### 方法 3: 使用 conda 安装（自动安装 pandoc）

```bash
conda install -c conda-forge pypandoc
```

## 验证安装

```python
import pypandoc

# 检查 pandoc 版本
version = pypandoc.get_pandoc_version()
print(f"Pandoc 版本: {version}")

# 检查支持的格式
input_formats, output_formats = pypandoc.get_pandoc_formats()
print(f"支持 {len(input_formats)} 种输入格式, {len(output_formats)} 种输出格式")
```

## 常见问题

### 1. 找不到 pandoc 错误

```
OSError: No pandoc was found
```

**解决方案:**
- 确认 pandoc 已正确安装
- 设置环境变量 `PYPANDOC_PANDOC` 指向 pandoc 可执行文件:
  ```python
  import os
  os.environ['PYPANDOC_PANDOC'] = '/path/to/pandoc'
  ```

### 2. PDF 转换失败

**解决方案:**
- 安装 LaTeX 引擎（TeX Live 或 MiKTeX）
- Windows 下载: https://tug.org/texlive/
- macOS: `brew install --cask mactex`

### 3. 中文文档乱码

**解决方案:**
- 指定输入编码:
  ```python
  pypandoc.convert_file('input.docx', 'md', encoding='utf-8')
  ```
- 使用额外参数:
  ```python
  extra_args=['--wrap=none', '--toc']
  pypandoc.convert_file('input.docx', 'md', extra_args=extra_args)
  ```
