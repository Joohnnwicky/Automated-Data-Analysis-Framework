# tests/test_chart_selector.py
"""
Test scaffolds for REP-09 requirement.
Initially skipped - will pass after src/report/chart_selector.py implementation.
"""

import pytest
import pandas as pd
from pathlib import Path


class TestChartSelector:
    """Tests for chart type selection based on data profile."""

    @pytest.mark.skip(reason="Wave 0 scaffold - src/report/chart_selector.py not implemented")
    def test_select_chart_type_time_series(self):
        """REP-09: Verify datetime columns → line chart selection."""
        from src.report.chart_selector import select_chart_type

        # Create data profile with datetime column
        data_profile = {
            'columns': {
                'date': {'dtype': 'datetime64[ns]', 'unique_count': 30},
                'value': {'dtype': 'float64', 'unique_count': 30}
            },
            'data_type': 'time_series'
        }

        chart_type = select_chart_type(data_profile)

        assert chart_type == 'line'

    @pytest.mark.skip(reason="Wave 0 scaffold - src/report/chart_selector.py not implemented")
    def test_select_chart_type_categorical(self):
        """REP-09: Verify numeric + categorical → bar chart selection."""
        from src.report.chart_selector import select_chart_type

        # Create data profile with categorical + numeric columns
        data_profile = {
            'columns': {
                'category': {'dtype': 'object', 'unique_count': 5},
                'value': {'dtype': 'float64', 'unique_count': 100}
            },
            'data_type': 'table'
        }

        chart_type = select_chart_type(data_profile)

        assert chart_type == 'bar'

    @pytest.mark.skip(reason="Wave 0 scaffold - src/report/chart_selector.py not implemented")
    def test_select_chart_type_scatter(self):
        """REP-09: Verify two numeric columns → scatter chart selection."""
        from src.report.chart_selector import select_chart_type

        # Create data profile with two numeric columns
        data_profile = {
            'columns': {
                'x_value': {'dtype': 'float64', 'unique_count': 50},
                'y_value': {'dtype': 'float64', 'unique_count': 50}
            },
            'data_type': 'table'
        }

        chart_type = select_chart_type(data_profile)

        assert chart_type == 'scatter'

    @pytest.mark.skip(reason="Wave 0 scaffold - src/report/chart_selector.py not implemented")
    def test_select_chart_type_fallback(self):
        """REP-09: Verify fallback → table selection."""
        from src.report.chart_selector import select_chart_type

        # Create data profile that doesn't match any pattern
        data_profile = {
            'columns': {
                'text': {'dtype': 'object', 'unique_count': 1000}
            },
            'data_type': 'table'
        }

        chart_type = select_chart_type(data_profile)

        assert chart_type == 'table'