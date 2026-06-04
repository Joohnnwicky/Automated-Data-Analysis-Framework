# tests/test_insights.py
"""
Test scaffolds for DATA-05 requirement.
Initially skipped - will pass after src/data/insights.py implementation.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path


def test_detect_anomalies_with_outliers():
    """Task 1: Verify detect_anomalies finds outliers using IQR method."""
    from src.data.insights import detect_anomalies

    # Create data with clear outliers
    df = pd.DataFrame({'value': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100]})

    result = detect_anomalies(df, 'value')

    # Should detect outlier (100 is far outside IQR bounds)
    assert result is not None
    assert result['type'] == 'anomaly'
    assert 'value' in result['message']
    assert '异常值' in result['message']
    assert 'outlier_count' in result['statistics']
    assert result['statistics']['outlier_count'] == 1
    assert 'bounds' in result['statistics']


def test_detect_anomalies_no_outliers():
    """Task 1: Verify detect_anomalies returns None when outliers < 5%."""
    from src.data.insights import detect_anomalies

    # Create data with no significant outliers
    df = pd.DataFrame({'value': list(range(1, 101))})

    result = detect_anomalies(df, 'value')

    # Should return None (no outliers > 5%)
    assert result is None


def test_detect_anomalies_insufficient_data():
    """Task 1: Verify detect_anomalies returns None for small datasets."""
    from src.data.insights import detect_anomalies

    # Create small dataset (< 10 rows)
    df = pd.DataFrame({'value': [1, 2, 3, 4, 5]})

    result = detect_anomalies(df, 'value')

    # Should return None (insufficient data)
    assert result is None


def test_detect_trend_significant_increase():
    """Task 2: Verify detect_trend detects increasing trend (>20%)."""
    from src.data.insights import detect_trend

    # Create time series with clear upward trend
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    values = list(range(1, 101))  # Steady increase
    df = pd.DataFrame({'date': dates, 'value': values})

    result = detect_trend(df, 'date', 'value')

    # Should detect increasing trend
    assert result is not None
    assert result['type'] == 'trend'
    assert 'value' in result['message']
    assert '上升' in result['message']
    assert 'change_pct' in result['statistics']
    assert result['statistics']['change_pct'] > 20


def test_detect_trend_no_significant_change():
    """Task 2: Verify detect_trend returns None when change < 20%."""
    from src.data.insights import detect_trend

    # Create time series with minimal change
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    values = [50 + np.random.randn() for _ in range(100)]  # Around 50
    df = pd.DataFrame({'date': dates, 'value': values})

    result = detect_trend(df, 'date', 'value')

    # Should return None (no significant trend)
    assert result is None


def test_detect_trend_insufficient_data():
    """Task 2: Verify detect_trend returns None for small datasets."""
    from src.data.insights import detect_trend

    # Create small time series (< 20 rows)
    dates = pd.date_range('2024-01-01', periods=15, freq='D')
    values = list(range(1, 16))
    df = pd.DataFrame({'date': dates, 'value': values})

    result = detect_trend(df, 'date', 'value')

    # Should return None (insufficient data)
    assert result is None


def test_generate_distribution_insight_skewed():
    """Task 3: Verify generate_distribution_insight detects skewed distribution."""
    from src.data.insights import generate_distribution_insight

    # Create heavily skewed distribution using exponential
    # Exponential distribution has theoretical skewness = 2
    np.random.seed(42)
    df = pd.DataFrame({'value': np.random.exponential(scale=10, size=100)})

    result = generate_distribution_insight(df, 'value')

    # Should detect skewed distribution (skew > 1)
    assert result is not None
    assert result['type'] == 'distribution'
    assert 'value' in result['message']
    assert '偏斜' in result['message']
    assert '建议使用中位数' in result['recommendation']


def test_generate_distribution_insight_symmetric():
    """Task 3: Verify generate_distribution_insight for symmetric distribution."""
    from src.data.insights import generate_distribution_insight

    # Create symmetric distribution (normal)
    np.random.seed(42)
    df = pd.DataFrame({'value': np.random.normal(50, 10, 100)})

    result = generate_distribution_insight(df, 'value')

    # Should detect symmetric distribution
    assert result is not None
    assert result['type'] == 'distribution'
    assert 'value' in result['message']
    assert '对称' in result['message'] or '均值' in result['message']


@pytest.mark.skip(reason="Waiting for Task 4: generate_initial_insights")
def test_generate_insights():
    """DATA-05: Verify generation of 1-2 insights (trends or anomalies)."""
    pass


@pytest.mark.skip(reason="Waiting for Task 4: generate_initial_insights")
def test_no_mental_math():
    """DATA-05: Verify all statistics computed via code execution (PITFALL-01: no LLM mental math)."""
    pass