"""
HTML 表格预处理工具
用于修复 DOCX 转换为 HTML 后的表格问题，确保正确转换为 Markdown
"""

import re
from pathlib import Path


def preprocess_html_table(html_content, verbose=False):
    """
    预处理 HTML 表格，修复常见问题：
    1. 删除空列（width: 0% 或 display: none）
    2. 删除多余的空格和换行
    3. 添加处理标记

    Args:
        html_content (str): HTML 内容
        verbose (bool): 是否显示详细处理信息

    Returns:
        dict: {
            'processed_html': 预处理后的 HTML 内容,
            'changes': 修改记录列表
        }
    """
    changes = []

    # 1. 删除空列（width: 0% 或 display: none）
    empty_col_pattern = r'<col[^>]*style=["\'][^"\']*(?:width:\s*0%|display:\s*none)[^"\']*["\'][^>]*/?>'
    removed_cols = re.findall(empty_col_pattern, html_content, flags=re.IGNORECASE)
    if removed_cols:
        html_content = re.sub(empty_col_pattern, '', html_content, flags=re.IGNORECASE)
        changes.append(f"删除了 {len(removed_cols)} 个空列")

    # 2. 删除空的 colgroup 定义
    if re.search(r'<colgroup>\s*</colgroup>', html_content):
        html_content = re.sub(r'<colgroup>\s*</colgroup>', '', html_content)
        changes.append("删除了空的 colgroup 标签")

    # 3. 标准化空白字符
    original_length = len(html_content)
    html_content = re.sub(r'>\s+<', '><', html_content)
    if len(html_content) != original_length:
        changes.append("标准化了标签间的空白字符")

    # 4. 添加处理标记
    header_comment = f"<!-- HTML 预处理: {', '.join(changes) if changes else '无需修改'} -->\n"
    html_content = header_comment + html_content

    if verbose:
        print("\n[HTML 预处理报告]")
        for change in changes:
            print(f"  - {change}")
        if not changes:
            print("  - 未发现需要修复的问题")

    return {
        'processed_html': html_content,
        'changes': changes
    }


def validate_table_structure(html_content):
    """
    验证 HTML 表格结构，检测潜在问题

    Args:
        html_content (str): HTML 内容

    Returns:
        dict: {
            'tables': 表格数量,
            'issues': 检测到的问题列表,
            'warnings': 警告列表
        }
    """
    issues = []
    warnings = []

    # 统计表格数量
    tables = re.findall(r'<table[^>]*>', html_content, flags=re.IGNORECASE)

    # 检测 colspan
    colspan_cells = re.findall(r'<td[^>]*colspan=["\'](\d+)["\'][^>]*>', html_content, flags=re.IGNORECASE)
    if colspan_cells:
        warnings.append(f"检测到 {len(colspan_cells)} 个合并单元格 (colspan)")

    # 检测 rowspan
    rowspan_cells = re.findall(r'<td[^>]*rowspan=["\'](\d+)["\'][^>]*>', html_content, flags=re.IGNORECASE)
    if rowspan_cells:
        warnings.append(f"检测到 {len(rowspan_cells)} 个合并单元格 (rowspan)")

    # 检测空的 colgroup
    empty_colgroups = re.findall(r'<colgroup>\s*</colgroup>', html_content, flags=re.IGNORECASE)
    if empty_colgroups:
        issues.append(f"检测到 {len(empty_colgroups)} 个空的 colgroup 标签")

    # 检测零宽度列
    zero_width_cols = re.findall(r'<col[^>]*style=["\'][^"\']*width:\s*0%[^"\']*["\'][^>]*/?>', html_content, flags=re.IGNORECASE)
    if zero_width_cols:
        issues.append(f"检测到 {len(zero_width_cols)} 个零宽度列")

    return {
        'tables': len(tables),
        'issues': issues,
        'warnings': warnings
    }


def preprocess_html_file(input_file, output_file=None, verbose=True):
    """
    预处理 HTML 文件

    Args:
        input_file (str): 输入 HTML 文件路径
        output_file (str, optional): 输出 HTML 文件路径。如果为 None，则覆盖原文件
        verbose (bool): 是否显示详细信息

    Returns:
        dict: 处理结果
    """
    input_path = Path(input_file).absolute()

    if not input_path.exists():
        raise FileNotFoundError(f"输入文件不存在: {input_file}")

    # 确定输出文件路径
    if output_file is None:
        output_path = input_path
    else:
        output_path = Path(output_file).absolute()

    # 读取文件
    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 验证表格结构
    if verbose:
        print(f"\n[验证表格结构] {input_path.name}")
        validation = validate_table_structure(html_content)
        if validation['tables'] > 0:
            print(f"  检测到 {validation['tables']} 个表格")
            if validation['issues']:
                print("  发现的问题:")
                for issue in validation['issues']:
                    print(f"    [!] {issue}")
            if validation['warnings']:
                print("  注意事项:")
                for warning in validation['warnings']:
                    print(f"    [i] {warning}")
        else:
            print("  未检测到表格")

    # 预处理
    result = preprocess_html_table(html_content, verbose=verbose)

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result['processed_html'])

    if verbose:
        if output_path != input_path:
            print(f"\n[完成] 已保存到: {output_path}")
        else:
            print(f"\n[完成] 已覆盖原文件")

    return result


def main():
    """命令行入口"""
    import sys

    if len(sys.argv) < 2:
        print("用法:")
        print("  python preprocess_html.py <input_html> [output_html]")
        print("  python preprocess_html.py --validate <input_html>")
        print("")
        print("示例:")
        print("  python preprocess_html.py temp.html")
        print("  python preprocess_html.py temp.html processed.html")
        print("  python preprocess_html.py --validate temp.html")
        sys.exit(1)

    if sys.argv[1] == '--validate':
        # 仅验证模式
        input_file = sys.argv[2]
        input_path = Path(input_file).absolute()

        if not input_path.exists():
            print(f"错误: 文件不存在: {input_file}")
            sys.exit(1)

        with open(input_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        validation = validate_table_structure(html_content)
        print(f"\n[表格验证报告] {input_path.name}")
        print(f"表格数量: {validation['tables']}")

        if validation['issues']:
            print("\n[!] 发现的问题:")
            for issue in validation['issues']:
                print(f"  - {issue}")

        if validation['warnings']:
            print("\n[i] 注意事项:")
            for warning in validation['warnings']:
                print(f"  - {warning}")

        if not validation['issues'] and not validation['warnings']:
            print("\n[OK] 未发现明显问题")

    else:
        # 预处理模式
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None

        try:
            preprocess_html_file(input_file, output_file)
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()
