"""
交互式文档转换脚本 - pypandoc-converter
提供用户友好的转换选项选择
"""

import sys
import os
from pathlib import Path

# 添加 scripts 目录到路径
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from convert_to_markdown import (
    convert_to_markdown,
    convert_with_html_intermediate,
    batch_convert
)
from preprocess_html import validate_table_structure, preprocess_html_file


def analyze_file_complexity(input_file):
    """
    分析文件复杂度，提供转换建议

    Args:
        input_file (str): 输入文件路径

    Returns:
        dict: 分析结果和建议
    """
    input_path = Path(input_file)

    if not input_path.exists():
        raise FileNotFoundError(f"输入文件不存在: {input_file}")

    # 生成临时 HTML 用于分析
    from tempfile import NamedTemporaryFile
    import pypandoc

    print("[分析] 正在分析文件复杂度...")

    try:
        # 创建临时 HTML 文件
        with NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_file:
            temp_html_path = Path(temp_file.name)

        # 转换为 HTML
        pypandoc.convert_file(
            str(input_path),
            'html',
            outputfile=str(temp_html_path),
            extra_args=['--standalone']
        )

        # 读取 HTML
        with open(temp_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 验证表格结构
        validation = validate_table_structure(html_content)

        # 删除临时文件
        temp_html_path.unlink()

        # 分析结果
        analysis = {
            'table_count': validation['tables'],
            'has_issues': len(validation['issues']) > 0,
            'issues': validation['issues'],
            'colspan_count': sum(1 for w in validation['warnings'] if 'colspan' in w) if validation['warnings'] else 0,
            'rowspan_count': sum(1 for w in validation['warnings'] if 'rowspan' in w) if validation['warnings'] else 0,
        }

        # 提供建议
        recommendations = []

        if analysis['table_count'] == 0:
            recommendations.append({
                'method': '普通转换',
                'format': 'markdown',
                'reason': '文件中没有表格，使用普通转换即可'
            })
        elif analysis['colspan_count'] > 5 or analysis['rowspan_count'] > 5:
            recommendations.append({
                'method': '先转HTML再转管道表',
                'format': 'gfm',
                'reason': f'检测到 {analysis["colspan_count"]} 个合并单元格，建议使用两步法'
            })
            recommendations.append({
                'method': '转网格表',
                'format': 'markdown+grid_tables',
                'reason': '网格表对复杂表格支持更好'
            })
        elif analysis['table_count'] > 5:
            recommendations.append({
                'method': '转管道表 (GFM)',
                'format': 'gfm',
                'reason': f'检测到 {analysis["table_count"]} 个表格，GFM 格式支持较好'
            })
            recommendations.append({
                'method': '转网格表',
                'format': 'markdown+grid_tables',
                'reason': '多个表格，网格表更稳定'
            })
        else:
            recommendations.append({
                'method': '转管道表 (GFM)',
                'format': 'gfm',
                'reason': '简单表格，推荐 GFM 格式'
            })

        if analysis['has_issues']:
            recommendations.insert(0, {
                'method': '先转HTML再转管道表',
                'format': 'gfm',
                'reason': f'检测到问题: {", ".join(analysis["issues"])}'
            })

        return {
            'analysis': analysis,
            'recommendations': recommendations
        }

    except Exception as e:
        print(f"[警告] 无法分析文件复杂度: {e}")
        return {
            'analysis': None,
            'recommendations': [
                {'method': '普通转换', 'format': 'markdown', 'reason': '无法分析，使用默认方法'},
                {'method': '转管道表 (GFM)', 'format': 'gfm', 'reason': 'GFM 格式对表格支持较好'}
            ]
        }


def display_menu(title, options, show_back=False):
    """
    显示菜单并获取用户选择

    Args:
        title (str): 菜单标题
        options (list): 选项列表
        show_back (bool): 是否显示返回选项

    Returns:
        int: 用户选择的索引
    """
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")

    if show_back:
        print(f"  0. 返回上级菜单")

    print('='*60)

    while True:
        try:
            choice = input("  请选择 (输入数字): ").strip()
            if show_back and choice == '0':
                return 0
            choice = int(choice)
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print(f"  [错误] 请输入 1-{len(options)} 之间的数字")
        except ValueError:
            print("  [错误] 请输入有效的数字")


def single_file_conversion():
    """单文件转换流程"""
    input_file = input("\n  请输入要转换的文件路径: ").strip().strip('"')

    input_path = Path(input_file)
    if not input_path.exists():
        print(f"  [错误] 文件不存在: {input_file}")
        return

    # 分析文件复杂度
    result = analyze_file_complexity(input_path)
    analysis = result['analysis']
    recommendations = result['recommendations']

    # 显示分析结果
    if analysis:
        print(f"\n  [分析结果]")
        print(f"    表格数量: {analysis['table_count']}")
        if analysis['colspan_count'] > 0:
            print(f"    合并单元格: {analysis['colspan_count']}")
        if analysis['rowspan_count'] > 0:
            print(f"    跨行单元格: {analysis['rowspan_count']}")
        if analysis['has_issues']:
            print(f"    发现问题: {', '.join(analysis['issues'])}")

    # 显示推荐方案
    print(f"\n  [系统推荐]")
    for i, rec in enumerate(recommendations, 1):
        print(f"    {i}. {rec['method']} - {rec['reason']}")

    # 让用户选择转换方法
    options = [
        "普通转换 (标准 Markdown)",
        "转管道表 (GFM - GitHub Flavored Markdown)",
        "转网格表 (Grid Tables - 更稳定)",
        "先转HTML再转管道表 (两步法，处理复杂表格)",
        "系统自动建议 (基于文件分析)"
    ]

    print(f"\n  [选择转换方法]")
    choice = display_menu("选择转换方法", options, show_back=True)

    if choice == 0:
        return

    # 转换方法映射
    method_map = {
        0: ('markdown', False),
        1: ('gfm', False),
        2: ('markdown+grid_tables-simple_tables-pipe_tables-multiline_tables', False),
        3: ('gfm', True),
        4: (recommendations[0]['format'], recommendations[0]['method'] == '先转HTML再转管道表')
    }

    format_type, use_two_step = method_map[choice]

    # 获取输出文件路径
    default_output = input_path.with_suffix('.md')
    output_file = input(f"  输出文件路径 (默认: {default_output}): ").strip().strip('"')
    if not output_file:
        output_file = str(default_output)

    # 执行转换
    print(f"\n  [开始转换]")
    print(f"    输入: {input_path}")
    print(f"    输出: {output_file}")
    print(f"    格式: {format_type}")
    if use_two_step:
        print(f"    方法: 两步法 (HTML -> MD)")

    try:
        if use_two_step:
            # 网格表需要特殊处理
            if 'grid_tables' in format_type:
                # 网格表使用两步法
                convert_with_html_intermediate(
                    str(input_path),
                    output_file,
                    format_type='gfm',  # 先用 GFM
                    extra_args=['--wrap=none']
                )
                print(f"  [提示] 网格表已转换，可能需要手动调整")
            else:
                # 标准 GFM 两步法
                convert_with_html_intermediate(
                    str(input_path),
                    output_file,
                    format_type=format_type,
                    extra_args=['--wrap=none']
                )
        else:
            # 单步转换
            if 'grid_tables' in format_type:
                # 网格表需要直接使用 pandoc
                import pypandoc
                output_path = Path(output_file).absolute()
                output_path.parent.mkdir(parents=True, exist_ok=True)

                extra_args = [
                    '--wrap=none',
                    '--atx-headers'
                ]

                pypandoc.convert_file(
                    str(input_path),
                    'markdown+grid_tables-simple_tables-pipe_tables-multiline_tables',
                    outputfile=str(output_path),
                    extra_args=extra_args
                )
            else:
                convert_to_markdown(
                    str(input_path),
                    output_file,
                    format_type=format_type,
                    extra_args=['--wrap=none']
                )

        print(f"\n  [成功] 转换完成!")

    except Exception as e:
        print(f"\n  [错误] 转换失败: {e}")


def batch_file_conversion():
    """批量文件转换流程"""
    input_pattern = input("\n  请输入文件模式 (如: *.docx): ").strip().strip('"')
    output_dir = input("  请输入输出目录 (默认: ./output/): ").strip().strip('"')
    if not output_dir:
        output_dir = './output/'

    # 选择转换方法
    options = [
        "普通转换",
        "转管道表 (GFM)",
        "转网格表",
        "两步法 (先HTML再MD)"
    ]

    choice = display_menu("选择批量转换方法", options, show_back=True)

    if choice == 0:
        return

    method_map = {
        0: ('markdown', False),
        1: ('gfm', False),
        2: ('markdown+grid_tables-simple_tables-pipe_tables-multiline_tables', False),
        3: ('gfm', True)
    }

    format_type, use_two_step = method_map[choice]

    print(f"\n  [开始批量转换]")
    print(f"    模式: {input_pattern}")
    print(f"    输出: {output_dir}")
    print(f"    格式: {format_type}")
    if use_two_step:
        print(f"    方法: 两步法")

    try:
        batch_convert(
            input_pattern,
            output_dir,
            format_type=format_type,
            extra_args=['--wrap=none'],
            use_two_step=use_two_step
        )
        print(f"\n  [成功] 批量转换完成!")
    except Exception as e:
        print(f"\n  [错误] 批量转换失败: {e}")


def interactive_main():
    """交互式主菜单"""
    while True:
        options = [
            "单文件转换",
            "批量转换",
            "退出"
        ]

        choice = display_menu("Pypandoc 交互式转换工具", options)

        if choice == 0:
            # 单文件转换
            single_file_conversion()
        elif choice == 1:
            # 批量转换
            batch_file_conversion()
        elif choice == 2:
            # 退出
            print("\n  再见!")
            break


def main():
    """命令行入口"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("用法:")
        print("  python interactive_converter.py           # 交互式模式")
        print("  python convert_to_markdown.py <file>      # 直接转换模式")
        print("")
        print("交互式模式提供:")
        print("  - 文件复杂度分析")
        print("  - 智能转换建议")
        print("  - 多种表格格式选择（普通、GFM、网格表）")
        print("  - 两步法转换（处理复杂表格）")
        sys.exit(0)

    print("\n" + "="*60)
    print("  Pypandoc 交互式文档转换工具 v2.0")
    print("="*60)
    print("  支持格式: DOCX, PDF, PPT, HTML 等")
    print("  输出格式: Markdown, GFM, Grid Tables")
    print("  特色: 自动分析、智能建议、复杂表格处理")
    print("="*60)

    interactive_main()


if __name__ == '__main__':
    main()
