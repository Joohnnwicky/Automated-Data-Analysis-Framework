# tests/test_chart_generator.py
"""
Test scaffolds for REP-01 and REP-04 requirements.
Initially skipped - will pass after src/report/chart_generator.py implementation.
"""

import pytest
import pandas as pd
from pathlib import Path


class TestChartGenerator:
    """Tests for Plotly chart generation and Chinese font rendering."""

    def test_generate_line_chart(self):
        """REP-01: Verify Plotly line chart generation."""
        from src.report.chart_generator import generate_line_chart
        from src.report.styles import get_design_style

        # Create sample data
        df = pd.DataFrame({
            'date': ['2023-01', '2023-02', '2023-03'],
            'value': [100, 150, 200]
        })

        style = get_design_style('ft')
        chart = generate_line_chart(df, x_col='date', y_col='value', title='Sales Trend', style=style)

        # Verify chart is a Plotly figure
        assert chart is not None
        assert hasattr(chart, 'data')
        assert len(chart.data) > 0

        # Verify line chart type
        assert chart.data[0].type == 'scatter' or hasattr(chart.data[0], 'mode')

    def test_generate_bar_chart(self):
        """REP-01: Verify Plotly bar chart generation."""
        from src.report.chart_generator import generate_bar_chart
        from src.report.styles import get_design_style

        # Create sample data
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [10, 20, 15]
        })

        style = get_design_style('ft')
        chart = generate_bar_chart(df, x_col='category', y_col='value', title='Sales by Category', style=style)

        # Verify chart is a Plotly figure
        assert chart is not None
        assert hasattr(chart, 'data')
        assert len(chart.data) > 0

        # Verify bar chart type
        assert chart.data[0].type == 'bar'

    def test_chinese_font(self):
        """REP-04: Verify Plotly chart uses Noto Sans SC font for Chinese text."""
        from src.report.chart_generator import generate_line_chart
        from src.report.styles import get_design_style

        # Create sample data with Chinese labels
        df = pd.DataFrame({
            '日期': ['2023-01', '2023-02', '2023-03'],
            '销售额': [100, 150, 200]
        })

        style = get_design_style('ft')
        chart = generate_line_chart(df, x_col='日期', y_col='销售额', title='月度销售趋势', style=style)

        # Verify chart font configuration
        assert chart is not None

        # Check title font - should contain Noto Sans SC
        if hasattr(chart, 'layout'):
            # Title font is stored in layout.title.font.family
            title_obj = chart.layout.title
            if hasattr(title_obj, 'font') and hasattr(title_obj.font, 'family'):
                title_font_family = title_obj.font.family
                assert title_font_family is not None and 'Noto' in title_font_family

            # Check layout font family
            font_obj = chart.layout.font
            if hasattr(font_obj, 'family'):
                font_family = font_obj.family
                # Font should be Noto Sans SC or similar Chinese-capable font
                assert font_family is not None and ('Noto' in font_family or 'sans' in font_family.lower())

    def test_embed_chart_as_svg(self):
        """REP-01: Verify chart exports as SVG string for embedding."""
        from src.report.chart_generator import generate_line_chart, embed_chart_as_svg
        from src.report.styles import get_design_style

        df = pd.DataFrame({
            'date': ['2023-01', '2023-02', '2023-03'],
            'value': [100, 150, 200]
        })

        style = get_design_style('ft')
        chart = generate_line_chart(df, x_col='date', y_col='value', title='Sales Trend', style=style)
        svg_string = embed_chart_as_svg(chart)

        # Verify SVG output
        assert svg_string is not None
        assert isinstance(svg_string, str)
        assert '<svg' in svg_string or '<!--' in svg_string  # Kaleido may output SVG or comment wrapper
        assert len(svg_string) > 100  # SVG should be substantial