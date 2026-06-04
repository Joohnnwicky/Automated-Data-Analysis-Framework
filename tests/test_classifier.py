# tests/test_classifier.py
"""
Test scaffolds for DATA-03 requirement.
Initially skipped - will pass after src/data/classifier.py implementation.
"""

import pytest
import pandas as pd
from pathlib import Path


class TestTypeClassifier:
    """Tests for TypeClassifier class."""

    def test_classify_method_returns_tuple(self):
        """Verify classify method returns (data_type, suggested_methods) tuple."""
        from src.data.classifier import TypeClassifier

        df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'age': [30, 25]
        })
        classifier = TypeClassifier()
        result = classifier.classify(df)

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[0] == 'table'
        assert isinstance(result[1], list)

    def test_classify_advertising_data(self):
        """Verify TypeClassifier correctly classifies advertising data."""
        from src.data.classifier import TypeClassifier

        df = pd.DataFrame({
            'ctr': [0.05, 0.06],
            'impression': [1000, 1200],
            'click': [50, 72],
            'conversion': [5, 7]
        })
        classifier = TypeClassifier()
        data_type, methods = classifier.classify(df)

        assert data_type == 'advertising'
        assert len(methods) == 5
        assert 'ROI analysis' in methods

    def test_classify_delegates_to_function(self):
        """Verify TypeClassifier.classify delegates to classify_data_type."""
        from src.data.classifier import TypeClassifier, classify_data_type

        df = pd.DataFrame({
            'date': ['20230101', '20230102'],
            'value': [100, 200]
        })

        classifier = TypeClassifier()
        classifier_result = classifier.classify(df)
        function_result = classify_data_type(df)

        assert classifier_result == function_result


class TestClassifyDataType:
    """Tests for classify_data_type function."""

    def test_classify_advertising_data(self):
        """Verify advertising classification with 3+ keywords."""
        from src.data.classifier import classify_data_type

        df = pd.DataFrame({
            'ctr': [0.05, 0.06],
            'impression': [1000, 1200],
            'click': [50, 72],
            'conversion': [5, 7]
        })
        data_type, methods = classify_data_type(df)
        assert data_type == 'advertising'
        assert 'ROI analysis' in methods
        assert 'CTR trend analysis' in methods

    def test_classify_time_series_data(self):
        """Verify time_series classification with datetime column and >10 unique values."""
        from src.data.classifier import classify_data_type

        dates = [f'2023010{i}' for i in range(12)]
        df = pd.DataFrame({
            'date': dates,
            'value': list(range(12))
        })
        data_type, methods = classify_data_type(df)
        assert data_type == 'time_series'
        assert 'Trend analysis' in methods
        assert 'Seasonal decomposition' in methods

    def test_classify_table_data(self):
        """Verify table classification as default fallback."""
        from src.data.classifier import classify_data_type

        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [30, 25, 35]
        })
        data_type, methods = classify_data_type(df)
        assert data_type == 'table'
        assert 'Distribution analysis' in methods
        assert 'Correlation analysis' in methods

    def test_advertising_priority_over_time_series(self):
        """Verify advertising takes priority when both indicators present."""
        from src.data.classifier import classify_data_type

        dates = [f'2023010{i}' for i in range(12)]
        df = pd.DataFrame({
            'date': dates,
            'ctr': [0.05] * 12,
            'impression': [1000] * 12,
            'click': [50] * 12
        })
        data_type, methods = classify_data_type(df)
        assert data_type == 'advertising'


class TestDetectAdvertisingKeywords:
    """Tests for detect_advertising_keywords helper function."""

    def test_detect_english_keywords(self):
        """Verify detection of English advertising keywords."""
        from src.data.classifier import detect_advertising_keywords

        df = pd.DataFrame({
            'ctr': [0.05, 0.06],
            'impression': [1000, 1200],
            'click': [50, 72]
        })
        result = detect_advertising_keywords(df)
        assert result == 3

    def test_detect_chinese_keywords(self):
        """Verify detection of Chinese advertising keywords."""
        from src.data.classifier import detect_advertising_keywords

        df = pd.DataFrame({
            '投放': ['A', 'B'],
            '点击': [100, 200],
            '曝光': [1000, 2000]
        })
        result = detect_advertising_keywords(df)
        assert result == 3

    def test_no_advertising_keywords(self):
        """Verify zero matches when no advertising keywords present."""
        from src.data.classifier import detect_advertising_keywords

        df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'age': [30, 25]
        })
        result = detect_advertising_keywords(df)
        assert result == 0


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