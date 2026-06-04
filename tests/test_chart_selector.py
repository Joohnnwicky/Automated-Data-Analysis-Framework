# tests/test_chart_selector.py
"""
Test scaffolds for REP-09 requirement.
Chart type auto-selection based on data profile from Phase 2 DataProfiler.
"""

import pytest
from typing import Tuple


class TestChartSelector:
    """Tests for chart type selection based on data profile."""

    def test_select_chart_type_time_series(self):
        """REP-09: Verify datetime columns → line chart selection."""
        from src.report.chart_selector import select_chart_type

        # Create data profile matching Phase 2 DataProfiler output
        data_profile = {
            'datetime_columns': ['date'],
            'numeric_columns': ['value'],
            'categorical_columns': []
        }

        chart_type, rationale = select_chart_type(data_profile)

        assert chart_type == 'line'
        assert '时序' in rationale or '趋势' in rationale

    def test_select_chart_type_categorical(self):
        """REP-09: Verify numeric + categorical → bar chart selection."""
        from src.report.chart_selector import select_chart_type

        # Create data profile with categorical + numeric columns
        data_profile = {
            'datetime_columns': [],
            'numeric_columns': ['sales'],
            'categorical_columns': ['category']
        }

        chart_type, rationale = select_chart_type(data_profile)

        assert chart_type == 'bar'
        assert '分类' in rationale or '数值' in rationale

    @pytest.mark.skip(reason="Wave 0 scaffold - src/report/chart_selector.py not implemented")
    def test_select_chart_type_scatter(self):
        """REP-09: Verify two numeric columns → scatter chart selection."""
        from src.report.chart_selector import select_chart_type

        # Create data profile with two numeric columns (no datetime)
        data_profile = {
            'datetime_columns': [],
            'numeric_columns': ['x_value', 'y_value'],
            'categorical_columns': []
        }

        chart_type, rationale = select_chart_type(data_profile)

        assert chart_type == 'scatter'
        assert '双数值' in rationale or '关系' in rationale

    @pytest.mark.skip(reason="Wave 0 scaffold - src/report/chart_selector.py not implemented")
    def test_select_chart_type_fallback(self):
        """REP-09: Verify fallback → table selection."""
        from src.report.chart_selector import select_chart_type

        # Create data profile that doesn't match any pattern
        data_profile = {
            'datetime_columns': [],
            'numeric_columns': [],
            'categorical_columns': ['text']
        }

        chart_type, rationale = select_chart_type(data_profile)

        assert chart_type == 'table'
        assert '无法' in rationale or '表格' in rationale