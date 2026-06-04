"""Tests for UX-02 quick response mode requirements.

Tests for should_use_quick_mode and quick_response functions.
"""

import pytest
from pathlib import Path
import pandas as pd


class TestShouldUseQuickMode:
    """Tests for should_use_quick_mode function (UX-02)."""

    def test_returns_true_for_small_dataset(self):
        """UX-02: Verify quick mode triggered for small dataset (< 100 rows)."""
        from src.workflow.intent_detector import should_use_quick_mode, IntentMatch

        profile = {
            'dimensions': {'rows': 50, 'columns': 3},
            'data_type': 'table'
        }
        intent = IntentMatch(
            intent_type='analyze',
            confidence=0.8,
            matched_keywords=['分析'],
            suggested_workflow='full'
        )

        result = should_use_quick_mode(profile, intent)
        assert result is True

    def test_returns_false_for_large_dataset(self):
        """UX-02: Verify quick mode NOT triggered for large dataset (> 100 rows)."""
        from src.workflow.intent_detector import should_use_quick_mode, IntentMatch

        profile = {
            'dimensions': {'rows': 200, 'columns': 5},
            'data_type': 'table'
        }
        intent = IntentMatch(
            intent_type='analyze',
            confidence=0.8,
            matched_keywords=['分析'],
            suggested_workflow='full'
        )

        result = should_use_quick_mode(profile, intent)
        assert result is False

    def test_returns_true_for_quick_intent(self):
        """UX-02: Verify quick mode triggered by explicit quick intent."""
        from src.workflow.intent_detector import should_use_quick_mode, IntentMatch

        # Large dataset but quick intent
        profile = {
            'dimensions': {'rows': 500, 'columns': 10},
            'data_type': 'table'
        }
        intent = IntentMatch(
            intent_type='quick',
            confidence=0.9,
            matched_keywords=['快速'],
            suggested_workflow='quick'
        )

        result = should_use_quick_mode(profile, intent)
        assert result is True  # Quick intent bypasses thresholds

    def test_returns_false_for_complex_type(self):
        """UX-02: Verify quick mode NOT triggered for advertising/time_series data."""
        from src.workflow.intent_detector import should_use_quick_mode, IntentMatch

        profile = {
            'dimensions': {'rows': 50, 'columns': 3},
            'data_type': 'advertising'
        }
        intent = IntentMatch(
            intent_type='analyze',
            confidence=0.8,
            matched_keywords=['分析'],
            suggested_workflow='full'
        )

        result = should_use_quick_mode(profile, intent)
        assert result is False


class TestQuickResponse:
    """Tests for quick_response function (UX-02)."""

    def test_quick_response_returns_string(self):
        """UX-02: Verify quick_response returns formatted string."""
        from src.workflow.intent_detector import quick_response

        # Create small test DataFrame
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50],
            'C': ['a', 'b', 'c', 'd', 'e']
        })

        result = quick_response(df, "test query")

        assert isinstance(result, str)
        assert len(result) > 0

    def test_quick_response_includes_dimensions(self):
        """UX-02: Verify quick_response includes rows and columns."""
        from src.workflow.intent_detector import quick_response

        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [10, 20, 30]
        })

        result = quick_response(df, "test")

        assert '行' in result  # Chinese for rows
        assert '列' in result  # Chinese for columns
        assert '3' in result   # Row count

    def test_quick_response_includes_numeric_stats(self):
        """UX-02: Verify quick_response includes mean and range for numeric fields."""
        from src.workflow.intent_detector import quick_response

        df = pd.DataFrame({
            'price': [100, 200, 300],
            'quantity': [1, 2, 3],
            'name': ['a', 'b', 'c']
        })

        result = quick_response(df, "test")

        # Should include numeric field statistics
        assert '均值' in result or 'mean' in result.lower()  # Chinese for mean
        assert '范围' in result or 'range' in result.lower()  # Chinese for range
        # Should include price field
        assert 'price' in result.lower()