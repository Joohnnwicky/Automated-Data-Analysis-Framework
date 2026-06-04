#!/usr/bin/env python3
"""
CLI entry point for Automated Data Analysis Framework.

Usage:
    analyze <data_file> [--format html|ppt] [--style ft|mckinsey|...] [--query "分析任务"]

Examples:
    analyze data/sales.xlsx
    analyze data/advertising.csv --format ppt --style mckinsey
    analyze data/revenue.json --query "找出ROI下降原因"
"""

import argparse
import sys
from pathlib import Path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Automated Data Analysis Framework - AI-powered data analysis tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  analyze data/sales.xlsx                    # Basic analysis, HTML output
  analyze data/sales.xlsx --format ppt       # Generate PowerPoint report
  analyze data/sales.xlsx --style mckinsey   # Use McKinsey design style
  analyze data/sales.xlsx --query "找出趋势"  # Specific analysis query

Design Styles:
  ft, mckinsey, economist, goldman, swiss, wsj, bloomberg, reuters, morningstar, bcg, bain
        '''
    )

    parser.add_argument(
        'data_file',
        type=str,
        nargs='?',
        help='Path to data file (Excel, CSV, or JSON)'
    )

    parser.add_argument(
        '--format', '-f',
        type=str,
        choices=['html', 'ppt'],
        default='html',
        help='Output format: html (default) or ppt'
    )

    parser.add_argument(
        '--style', '-s',
        type=str,
        default='ft',
        help='Design style: ft, mckinsey, economist, goldman, swiss, wsj, bloomberg, reuters, morningstar, bcg, bain'
    )

    parser.add_argument(
        '--query', '-q',
        type=str,
        default='分析这份数据',
        help='Analysis query in natural language'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        default='output',
        help='Output directory (default: output)'
    )

    parser.add_argument(
        '--quick',
        action='store_true',
        help='Use quick mode (no full multi-expert analysis)'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Automated Data Analysis Framework v1.0'
    )

    args = parser.parse_args()

    # No data file provided - show help
    if not args.data_file:
        parser.print_help()
        print('\nError: Please provide a data file path.')
        print('Example: analyze data/sales.xlsx')
        sys.exit(1)

    # Resolve data file path
    data_path = Path(args.data_file)
    if not data_path.exists():
        print(f'\nError: File not found: {data_path}')
        sys.exit(1)

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Import and run analysis
    try:
        # Add project root to path
        project_root = Path(__file__).parent.parent.parent
        sys.path.insert(0, str(project_root))

        from src.data.loader import DataLoader, DataLoadError
        from src.data.profiler import DataProfiler
        from src.workflow.orchestrator import WorkflowOrchestrator

        print(f'\n加载数据: {data_path}')

        # Load data
        loader = DataLoader()
        df = loader.load_file(data_path)

        print(f'  ✓ 加载完成: {len(df)} 行, {len(df.columns)} 列')

        # Quick mode - just show profile
        if args.quick:
            profiler = DataProfiler(df)
            profile = profiler.profile()

            print('\n' + '='*60)
            print('数据画像')
            print('='*60)
            print(f'维度: {profile["dimensions"]["rows"]} 行, {profile["dimensions"]["columns"]} 列')
            print(f'缺失率: {profile["quality"]["missing_rate"]:.2%}')
            print(f'质量评分: {profile["quality"]["quality_score"]}')
            print('\n字段概览:')
            for field in profile['fields'][:10]:
                print(f'  - {field["name"]}: {field["type"]} (缺失 {field["missing_rate"]:.1%})')
            print('='*60)
            return

        # Full analysis workflow
        print(f'\n启动分析流程...')
        print(f'  输出格式: {args.format}')
        print(f'  设计风格: {args.style}')
        print(f'  分析任务: {args.query}')

        orchestrator = WorkflowOrchestrator(
            output_format=args.format,
            style=args.style
        )

        result = orchestrator.execute(
            query=args.query,
            data_path=data_path,
            skip_clarification=args.quick
        )

        # Print results
        print('\n' + '='*60)
        print('分析完成')
        print('='*60)

        if 'report_path' in result:
            print(f'报告已生成: {result["report_path"]}')

        if args.format == 'html':
            print('\n提示: 按 Ctrl/Cmd + P 可导出 PDF')

        print('='*60)

    except DataLoadError as e:
        print(f'\n错误: {e.user_message}')
        if e.technical_detail:
            print(f'详情: {e.technical_detail}')
        sys.exit(1)

    except Exception as e:
        print(f'\n错误: {str(e)}')
        sys.exit(1)


if __name__ == '__main__':
    main()