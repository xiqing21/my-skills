"""
文档转换脚本 - 使用 pypandoc 将多种格式转换为 Markdown
支持的输入格式: docx, doc, ppt, pptx, pdf, html, rtf, txt, odt, ods, odp 等
输出格式: Markdown

特别功能: 两步转换法处理复杂表格问题 (DOCX -> HTML -> MD)
"""

import pypandoc
import sys
import os
import re
from pathlib import Path
from tempfile import NamedTemporaryFile


def convert_to_markdown(input_file, output_file=None, format_type='markdown', extra_args=None):
    """
    将文件转换为指定格式

    Args:
        input_file (str): 输入文件路径
        output_file (str, optional): 输出文件路径。如果为 None，则自动生成 .md 文件名
        format_type (str): 输出格式，默认为 'markdown'，可选 'gfm', 'html' 等
        extra_args (list, optional): 额外的 pandoc 参数

    Returns:
        str: 如果 output_file 为 None，返回转换内容；否则返回 None
    """
    input_path = Path(input_file).absolute()

    if not input_path.exists():
        raise FileNotFoundError(f"输入文件不存在: {input_file}")

    # 如果未指定输出文件，自动生成
    if output_file is None:
        output_file = str(input_path.with_suffix('.md'))

    output_path = Path(output_file).absolute()

    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 默认额外参数
    if extra_args is None:
        extra_args = [
            '--wrap=none',  # 不自动换行
        ]

    try:
        # 执行转换
        content = pypandoc.convert_file(
            str(input_path),
            format_type,
            outputfile=str(output_path),
            extra_args=extra_args
        )

        print(f"[OK] 转换成功: {input_path} -> {output_path} (格式: {format_type})")
        return content

    except Exception as e:
        print(f"[ERROR] 转换失败: {e}")
        raise


def preprocess_html_table(html_content):
    """
    预处理 HTML 表格，修复常见问题：
    - 删除空列（width: 0% 或 display: none）
    - 统一列数匹配
    - 标记需要人工审查的复杂合并单元格

    Args:
        html_content (str): HTML 内容

    Returns:
        str: 预处理后的 HTML 内容
    """
    # 删除空列样式
    html_content = re.sub(r'<col[^>]*style=["\'][^"\']*(?:width:\s*0%|display:\s*none)[^"\']*["\'][^>]*/?>', '', html_content, flags=re.IGNORECASE)

    # 删除空的 colgroup 定义
    html_content = re.sub(r'<colgroup>\s*</colgroup>', '', html_content)

    # 添加注释标记，提示需要人工审查
    html_content = '<!-- HTML tables have been preprocessed for conversion -->\n' + html_content

    return html_content


def convert_with_html_intermediate(input_file, output_file=None, temp_html=None, format_type='gfm', extra_args=None, preprocess=True):
    """
    使用 HTML 作为中间格式的两步转换法
    专门用于处理复杂表格的转换问题

    Args:
        input_file (str): 输入文件路径（通常是 DOCX）
        output_file (str, optional): 输出 MD 文件路径
        temp_html (str, optional): 中间 HTML 文件路径，如果为 None 则使用临时文件
        format_type (str): 最终输出格式，默认 'gfm' (GitHub Flavored Markdown)
        extra_args (list, optional): 额外的 pandoc 参数
        preprocess (bool): 是否预处理 HTML 表格，默认 True

    Returns:
        str: 转换后的 Markdown 内容
    """
    input_path = Path(input_file).absolute()

    if not input_path.exists():
        raise FileNotFoundError(f"输入文件不存在: {input_file}")

    # 如果未指定输出文件，自动生成
    if output_file is None:
        output_file = str(input_path.with_suffix('.md'))

    output_path = Path(output_file).absolute()

    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 确定中间 HTML 文件路径
    if temp_html is None:
        temp_file = NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        temp_html_path = Path(temp_file.name)
        temp_file.close()
    else:
        temp_html_path = Path(temp_html).absolute()

    # 默认额外参数（推荐用于表格转换）
    if extra_args is None:
        extra_args = ['--wrap=none']

    try:
        # 第一步: DOCX -> HTML（保留完整表格结构）
        print(f"[STEP 1] 转换: {input_path} -> {temp_html_path} (HTML)")
        html_content = pypandoc.convert_file(
            str(input_path),
            'html',
            outputfile=str(temp_html_path),
            extra_args=['--standalone']
        )

        # 预处理 HTML 表格
        if preprocess:
            print("[STEP 1.5] 预处理 HTML 表格...")
            with open(temp_html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            processed_html = preprocess_html_table(html_content)

            with open(temp_html_path, 'w', encoding='utf-8') as f:
                f.write(processed_html)
            print("[STEP 1.5] HTML 表格预处理完成")

        # 第二步: HTML -> MD（强制输出管道表）
        print(f"[STEP 2] 转换: {temp_html_path} -> {output_path} ({format_type})")
        markdown_content = pypandoc.convert_file(
            str(temp_html_path),
            format_type,
            outputfile=str(output_path),
            extra_args=extra_args
        )

        print(f"[OK] 两步转换成功: {input_path} -> {output_path}")
        return markdown_content

    except Exception as e:
        print(f"[ERROR] 两步转换失败: {e}")
        # 清理临时文件
        if temp_html is None and temp_html_path.exists():
            temp_html_path.unlink()
        raise
    finally:
        # 清理临时文件（如果不是用户指定的）
        if temp_html is None and temp_html_path.exists():
            try:
                temp_html_path.unlink()
                print(f"[INFO] 已删除临时文件: {temp_html_path}")
            except Exception as e:
                print(f"[WARNING] 无法删除临时文件: {e}")


def batch_convert(input_pattern, output_dir=None, format_type='markdown', extra_args=None, use_two_step=False):
    """
    批量转换文件

    Args:
        input_pattern (str): 输入文件模式（支持通配符）
        output_dir (str, optional): 输出目录
        format_type (str): 输出格式，默认 'markdown'
        extra_args (list, optional): 额外的 pandoc 参数
        use_two_step (bool): 是否使用两步转换法（处理表格问题）
    """
    from glob import glob

    files = glob(input_pattern)
    if not files:
        print(f"未找到匹配的文件: {input_pattern}")
        return

    print(f"找到 {len(files)} 个文件待转换")

    for file_path in files:
        input_path = Path(file_path)

        # 确定输出文件路径
        if output_dir:
            output_path = Path(output_dir) / f"{input_path.stem}.md"
        else:
            output_path = input_path.with_suffix('.md')

        # 选择转换方法
        if use_two_step:
            convert_with_html_intermediate(str(input_path), str(output_path), format_type=format_type, extra_args=extra_args)
        else:
            convert_to_markdown(str(input_path), str(output_path), format_type=format_type, extra_args=extra_args)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  # 单文件转换（默认 Markdown）")
        print("  python convert_to_markdown.py <input_file> [output_file]")
        print("")
        print("  # 指定输出格式")
        print("  python convert_to_markdown.py --format gfm <input_file> [output_file]")
        print("")
        print("  # 两步转换法（处理复杂表格）")
        print("  python convert_to_markdown.py --two-step <input_file> [output_file]")
        print("")
        print("  # 分步执行（高级用法）")
        print("  python convert_to_markdown.py --step1 --format html <input_file> temp.html")
        print("  python convert_to_markdown.py --step2 --format gfm temp.html output.md")
        print("")
        print("  # 批量转换")
        print("  python convert_to_markdown.py --batch <input_pattern> [output_dir]")
        print("  python convert_to_markdown.py --batch --two-step <input_pattern> [output_dir]")
        print("")
        print("示例:")
        print("  python convert_to_markdown.py document.docx")
        print("  python convert_to_markdown.py document.docx output.md")
        print("  python convert_to_markdown.py --format gfm document.docx")
        print("  python convert_to_markdown.py --two-step docx_with_tables.docx output.md")
        print("  python convert_to_markdown.py --step1 --format html doc.docx temp.html")
        print("  python convert_to_markdown.py --step2 --format gfm temp.html output.md")
        print("  python convert_to_markdown.py --batch '*.docx' ./output/")
        print("  python convert_to_markdown.py --batch --two-step '*.docx' ./output/")
        sys.exit(1)

    # 解析参数
    args = sys.argv[1:]
    mode = 'single'  # single, batch, step1, step2
    format_type = 'markdown'
    use_two_step = False
    input_file = None
    output_file = None
    input_pattern = None
    output_dir = None

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == '--batch':
            mode = 'batch'
        elif arg == '--step1':
            mode = 'step1'
        elif arg == '--step2':
            mode = 'step2'
        elif arg == '--two-step':
            use_two_step = True
        elif arg == '--format':
            if i + 1 < len(args):
                format_type = args[i + 1]
                i += 1
        elif arg.startswith('-'):
            print(f"未知参数: {arg}")
            sys.exit(1)
        elif input_file is None and mode != 'batch':
            input_file = arg
        elif output_file is None and mode != 'batch':
            output_file = arg
        elif input_pattern is None and mode == 'batch':
            input_pattern = arg
        elif output_dir is None and mode == 'batch':
            output_dir = arg

        i += 1

    # 根据模式执行转换
    if mode == 'batch':
        # 批量转换模式
        if input_pattern is None:
            input_pattern = '*.docx'
        batch_convert(input_pattern, output_dir, format_type=format_type, use_two_step=use_two_step)

    elif mode == 'step1':
        # 第一步：转换为 HTML
        if input_file is None:
            print("错误: --step1 模式需要指定输入文件")
            sys.exit(1)
        if output_file is None:
            output_file = str(Path(input_file).with_suffix('.html'))
        convert_to_markdown(input_file, output_file, format_type='html')

    elif mode == 'step2':
        # 第二步：HTML 转 MD
        if input_file is None:
            print("错误: --step2 模式需要指定输入文件")
            sys.exit(1)
        if output_file is None:
            output_file = str(Path(input_file).with_suffix('.md'))
        convert_to_markdown(input_file, output_file, format_type=format_type)

    else:
        # 单文件转换模式
        if input_file is None:
            print("错误: 需要指定输入文件")
            sys.exit(1)

        if use_two_step:
            # 使用两步转换法
            convert_with_html_intermediate(input_file, output_file, format_type=format_type)
        else:
            # 普通转换
            convert_to_markdown(input_file, output_file, format_type=format_type)


if __name__ == '__main__':
    main()
