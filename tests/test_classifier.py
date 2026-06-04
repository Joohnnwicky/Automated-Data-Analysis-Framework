# tests/test_classifier.py
"""
Test scaffolds for DATA-03 requirement.
Initially skipped - will pass after src/data/classifier.py implementation.
"""

import pytest
import pandas as pd
from pathlib import Path


class TestDetectDatetimeColumns:
    """Tests for detect_datetime_columns helper function."""

    def test_detect_datetime_by_name_pattern(self):
        """Verify detection of datetime columns by name patterns."""
        from src.data.classifier import detect_datetime_columns

        df = pd.DataFrame({
            'date': ['20230101', '20230102'],
            'value': [1, 2]
        })
        result = detect_datetime_columns(df)
        assert 'date' in result

    def test_detect_datetime_by_yyyymmdd_format(self):
        """Verify detection of YYYYMMDD format in object columns."""
        from src.data.classifier import detect_datetime_columns

        df = pd.DataFrame({
            'transaction_date': ['20230101', '20230102', '20230103'],
            'amount': [100, 200, 300]
        })
        result = detect_datetime_columns(df)
        assert 'transaction_date' in result

    def test_no_datetime_columns(self):
        """Verify empty list when no datetime columns present."""
        from src.data.classifier import detect_datetime_columns

        df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'age': [30, 25]
        })
        result = detect_datetime_columns(df)
        assert result == []

    def test_chinese_datetime_keywords(self):
        """Verify detection of Chinese datetime keywords."""
        from src.data.classifier import detect_datetime_columns

        df = pd.DataFrame({
            '日期': ['20230101', '20230102'],
            'value': [1, 2]
        })
        result = detect_datetime_columns(df)
        assert '日期' in result


@pytest.mark.skip(reason="src/data/classifier.py not implemented")
def test_classify_advertising():
    """DATA-03: Verify advertising data detection via keyword heuristics."""
    pass


@pytest.mark.skip(reason="src/data/classifier.py not implemented")
def test_suggest_methods():
    """DATA-03: Verify analysis method suggestions per data type."""
    pass