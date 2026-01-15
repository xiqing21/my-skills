"""
表格转换示例
演示如何处理 DOCX 文件中的复杂表格转换问题
"""

from scripts.convert_to_markdown import (
    convert_to_markdown,
    convert_with_html_intermediate,
    batch_convert
)
from scripts.preprocess_html import (
    preprocess_html_file,
    validate_table_structure,
    preprocess_html_table
)
from pathlib import Path


def example_1_simple_conversion():
    """示例 1: 简单的 DOCX 转 Markdown"""
    print("\n=== 示例 1: 简单转换 ===")

    input_file = "简单文档.docx"
    output_file = "简单文档.md"

    try:
        convert_to_markdown(input_file, output_file)
        print(f"✓ 转换成功: {input_file} -> {output_file}")
    except Exception as e:
        print(f"✗ 转换失败: {e}")


def example_2_gfm_format():
    """示例 2: 使用 GFM 格式转换（推荐用于表格）"""
    print("\n=== 示例 2: GFM 格式转换 ===")

    input_file = "包含表格的文档.docx"
    output_file = "包含表格的文档.md"

    try:
        convert_to_markdown(
            input_file,
            output_file,
            format_type='gfm',
            extra_args=['--wrap=none']
        )
        print(f"✓ 转换成功 (GFM): {input_file} -> {output_file}")
    except Exception as e:
        print(f"✗ 转换失败: {e}")


def example_3_two_step_conversion():
    """示例 3: 两步转换法（处理复杂表格）"""
    print("\n=== 示例 3: 两步转换法 ===")

    input_file = "复杂表格文档.docx"
    output_file = "复杂表格文档.md"

    try:
        # 方法 A: 自动两步转换（推荐）
        convert_with_html_intermediate(
            input_file,
            output_file,
            format_type='gfm',
            extra_args=['--wrap=none'],
            preprocess=True
        )
        print(f"✓ 两步转换成功: {input_file} -> {output_file}")

    except Exception as e:
        print(f"✗ 两步转换失败: {e}")


def example_4_manual_two_step():
    """示例 4: 手动两步转换（更多控制）"""
    print("\n=== 示例 4: 手动两步转换 ===")

    input_file = "营销数据.docx"
    temp_html = "temp.html"
    processed_html = "processed.html"
    output_file = "营销数据.md"

    try:
        # 步骤 1: DOCX -> HTML
        print(f"步骤 1: {input_file} -> {temp_html}")
        convert_to_markdown(
            input_file,
            temp_html,
            format_type='html'
        )

        # 步骤 2: 预处理 HTML
        print(f"步骤 2: 预处理 HTML 表格")
        result = preprocess_html_file(temp_html, processed_html)
        print(f"  修改: {', '.join(result['changes']) if result['changes'] else '无'}")

        # 步骤 3: HTML -> Markdown
        print(f"步骤 3: {processed_html} -> {output_file}")
        convert_to_markdown(
            processed_html,
            output_file,
            format_type='gfm',
            extra_args=['--wrap=none']
        )

        print(f"✓ 手动两步转换成功: {input_file} -> {output_file}")

    except Exception as e:
        print(f"✗ 手动两步转换失败: {e}")


def example_5_validate_html():
    """示例 5: 验证 HTML 表格结构"""
    print("\n=== 示例 5: 验证 HTML 表格 ===")

    html_file = "temp.html"

    try:
        if Path(html_file).exists():
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            validation = validate_table_structure(html_content)

            print(f"表格数量: {validation['tables']}")

            if validation['issues']:
                print("\n⚠️  发现的问题:")
                for issue in validation['issues']:
                    print(f"  - {issue}")

            if validation['warnings']:
                print("\nℹ️  注意事项:")
                for warning in validation['warnings']:
                    print(f"  - {warning}")

            if not validation['issues'] and not validation['warnings']:
                print("✓ 未发现明显问题")

        else:
            print(f"✗ 文件不存在: {html_file}")

    except Exception as e:
        print(f"✗ 验证失败: {e}")


def example_6_batch_conversion():
    """示例 6: 批量转换（使用两步法）"""
    print("\n=== 示例 6: 批量转换 ===")

    input_pattern = "*.docx"
    output_dir = "./output/"

    try:
        # 使用两步法批量转换
        batch_convert(
            input_pattern,
            output_dir,
            format_type='gfm',
            extra_args=['--wrap=none'],
            use_two_step=True
        )
        print(f"✓ 批量转换完成: {input_pattern} -> {output_dir}")

    except Exception as e:
        print(f"✗ 批量转换失败: {e}")


def example_7_html_preprocessing_api():
    """示例 7: 使用 HTML 预处理 API"""
    print("\n=== 示例 7: HTML 预处理 API ===")

    html_content = """
    <table>
      <colgroup>
        <col style="width: 0%" />
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
    """

    try:
        result = preprocess_html_table(html_content, verbose=True)

        print("\n处理后的 HTML:")
        print(result['processed_html'])

        print(f"\n修改记录:")
        for change in result['changes']:
            print(f"  - {change}")

    except Exception as e:
        print(f"✗ HTML 预处理失败: {e}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("表格转换示例")
    print("=" * 60)

    # 运行示例（取消注释以执行）
    # example_1_simple_conversion()
    # example_2_gfm_format()
    # example_3_two_step_conversion()
    # example_4_manual_two_step()
    # example_5_validate_html()
    # example_6_batch_conversion()
    example_7_html_preprocessing_api()

    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
