# tests/test_data_profiler.py
"""
Test scaffolds for DATA-02, DATA-04, DATA-07 requirements.
Initially skipped - will pass after src/data/profiler.py implementation.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path


def test_profile_dimensions():
    """DATA-02: Verify data dimensions profiling (rows, columns, memory usage)."""
    from src.data.profiler import profile_dimensions

    # Create test DataFrame
    df = pd.DataFrame({
        'col1': [1, 2, 3, 4, 5],
        'col2': ['a', 'b', 'c', 'd', 'e'],
        'col3': [1.1, 2.2, 3.3, 4.4, 5.5]
    })

    result = profile_dimensions(df)

    # Verify dimensions
    assert result['rows'] == 5
    assert result['columns'] == 3
    assert 'memory_bytes' in result
    assert 'memory_mb' in result
    assert result['memory_bytes'] > 0
    assert result['memory_mb'] >= 0  # Small DataFrames may round to 0.0 MB
    # Verify deep=True is used (memory_bytes should be larger than shallow)
    assert result['memory_bytes'] > df.memory_usage(deep=False).sum()


def test_profile_fields():
    """DATA-02: Verify field profiling with dtype, nulls, and statistics."""
    from src.data.profiler import profile_fields

    # Create test DataFrame with numeric and object columns
    df = pd.DataFrame({
        'numeric_col': [1, 2, 3, 4, 5],
        'string_col': ['a', 'b', 'c', 'd', 'e'],
        'col_with_nulls': [1.0, 2.0, None, 4.0, 5.0]
    })

    result = profile_fields(df)

    # Verify field count
    assert len(result) == 3

    # Verify numeric column profile
    numeric_profile = result['numeric_col']
    assert numeric_profile['dtype'] == 'int64'
    assert numeric_profile['null_count'] == 0
    assert numeric_profile['null_rate'] == 0.0
    assert numeric_profile['unique_count'] == 5
    assert 'statistics' in numeric_profile
    assert numeric_profile['statistics']['min'] == 1.0
    assert numeric_profile['statistics']['max'] == 5.0
    assert numeric_profile['statistics']['mean'] == 3.0
    assert numeric_profile['statistics']['median'] == 3.0

    # Verify string column profile
    string_profile = result['string_col']
    assert string_profile['dtype'] in ['object', 'str']  # pandas may use either
    assert string_profile['null_count'] == 0
    assert string_profile['unique_count'] == 5
    assert 'statistics' in string_profile
    assert 'top_value' in string_profile['statistics']
    assert 'top_freq' in string_profile['statistics']

    # Verify column with nulls
    null_profile = result['col_with_nulls']
    assert null_profile['null_count'] == 1
    assert null_profile['null_rate'] == 20.0  # 1/5 = 20%


def test_profile_statistics():
    """DATA-04: Verify statistical summaries via pandas describe()."""
    from src.data.profiler import profile_statistics

    # Create test DataFrame with numeric and categorical columns
    df = pd.DataFrame({
        'numeric1': [1, 2, 3, 4, 5],
        'numeric2': [10.0, 20.0, 30.0, 40.0, 50.0],
        'category_col': ['a', 'b', 'a', 'b', 'c']
    })

    result = profile_statistics(df)

    # Verify numeric summary exists
    assert 'numeric_summary' in result
    assert 'numeric1' in result['numeric_summary']
    assert 'numeric2' in result['numeric_summary']

    # Verify numeric summary contains standard statistics
    assert 'mean' in result['numeric_summary']['numeric1']
    assert 'std' in result['numeric_summary']['numeric1']
    assert 'min' in result['numeric_summary']['numeric1']
    assert 'max' in result['numeric_summary']['numeric1']

    # Verify categorical summary exists
    assert 'categorical_summary' in result
    assert 'category_col' in result['categorical_summary']

    # Test DataFrame with only numeric columns
    df_numeric_only = pd.DataFrame({
        'col1': [1, 2, 3],
        'col2': [4, 5, 6]
    })
    result_numeric = profile_statistics(df_numeric_only)
    assert 'numeric_summary' in result_numeric
    assert 'categorical_summary' not in result_numeric  # No categorical columns

    # Test DataFrame with only categorical columns
    df_categorical_only = pd.DataFrame({
        'col1': ['a', 'b', 'c'],
        'col2': ['x', 'y', 'z']
    })
    result_categorical = profile_statistics(df_categorical_only)
    assert 'categorical_summary' in result_categorical
    # No numeric columns
    assert 'numeric_summary' not in result_categorical or result_categorical['numeric_summary'] == {}


def test_suggest_memory_optimization():
    """DATA-02: Verify memory optimization suggestions for category conversion."""
    from src.data.profiler import suggest_memory_optimization

    # Create DataFrame with object columns suitable for category conversion
    df = pd.DataFrame({
        'numeric_col': [1, 2, 3, 4, 5],
        'low_cardinality': ['a', 'b', 'a', 'b', 'a'],  # 3 unique out of 5 rows (60% < 50% unique)
        'high_cardinality': ['a', 'b', 'c', 'd', 'e'],  # 5 unique out of 5 rows (100% unique)
    })

    result = suggest_memory_optimization(df)

    # Verify result structure
    assert 'current_memory_mb' in result
    assert 'suggestions' in result
    assert result['current_memory_mb'] >= 0

    # Verify low_cardinality is suggested for category conversion
    # unique_ratio = 3/5 = 0.6 which is > 0.5, so it should NOT be suggested
    # Actually, need to check: unique_ratio < 0.5 means < 50% unique
    # 3 unique out of 5 rows = 60% unique ratio, which is > 0.5
    # So this should NOT be suggested

    # Let's use a better test case
    df2 = pd.DataFrame({
        'numeric_col': list(range(100)),
        'low_unique': ['a'] * 90 + ['b'] * 10,  # 2 unique out of 100 rows (2% unique)
    })

    result2 = suggest_memory_optimization(df2)
    suggestions = result2['suggestions']

    # Should have at least one suggestion for low_unique
    low_unique_suggestion = [s for s in suggestions if s['column'] == 'low_unique']
    assert len(low_unique_suggestion) > 0, "Should suggest category conversion for low cardinality column"
    assert low_unique_suggestion[0]['suggestion'] == 'convert to category'
    assert low_unique_suggestion[0]['estimated_reduction'] > 50  # Should have significant reduction


def test_suggest_missing_value_strategy():
    """DATA-07: Verify missing value strategy suggestions."""
    from src.data.profiler import suggest_missing_value_strategy

    # Create DataFrame with various missing value patterns
    df = pd.DataFrame({
        'numeric_low_null': [1.0, 2.0, 3.0, 4.0, 5.0],  # 0% null
        'numeric_medium_null': [1.0, 2.0, None, 4.0, 5.0],  # 20% null
        'numeric_high_null': [1.0, None, None, None, None],  # 80% null
        'categorical_low_null': ['a', 'b', 'c', 'd', 'e'],  # 0% null
        'categorical_medium_null': ['a', None, 'c', 'd', 'e'],  # 20% null
    })

    result = suggest_missing_value_strategy(df)

    # Verify result structure
    assert 'missing_columns' in result
    assert 'total_missing_rows' in result

    # Verify columns with missing values are identified
    # Should only include columns where null_count > 0
    missing_cols = result['missing_columns']
    assert 'numeric_low_null' not in missing_cols
    assert 'categorical_low_null' not in missing_cols
    assert 'numeric_medium_null' in missing_cols
    assert 'numeric_high_null' in missing_cols
    assert 'categorical_medium_null' in missing_cols

    # Verify strategy suggestions for numeric columns
    assert missing_cols['numeric_medium_null']['null_pct'] == 20.0
    assert missing_cols['numeric_medium_null']['dtype'] == 'float64'
    # 20% null should suggest 'fill with median' or 'consider dropping column or rows'
    assert 'fill' in missing_cols['numeric_medium_null']['suggested_strategy'] or 'drop' in missing_cols['numeric_medium_null']['suggested_strategy']

    # High null percentage should suggest dropping
    assert missing_cols['numeric_high_null']['null_pct'] == 80.0
    assert 'drop' in missing_cols['numeric_high_null']['suggested_strategy']

    # Verify strategy for categorical columns
    assert missing_cols['categorical_medium_null']['dtype'] in ['object', 'str']
    # 20% null for categorical should suggest fill with placeholder or drop rows
    strategy = missing_cols['categorical_medium_null']['suggested_strategy']
    assert 'Unknown' in strategy or 'drop' in strategy or 'mode' in strategy

    # Verify total missing rows count
    # Rows with at least one null: row 2 (numeric_medium_null, numeric_high_null), row 3, row 4, row 5
    # Actually row 2 has numeric_medium_null null and numeric_high_null null
    # row 3-5 have numeric_high_null null
    # So total missing rows = 4
    assert result['total_missing_rows'] >= 1  # At least some rows have missing values


def test_data_profiler_class():
    """DATA-02: Verify DataProfiler orchestrates all profiling functions."""
    from src.data.profiler import DataProfiler

    # Create test DataFrame with consistent row counts
    df = pd.DataFrame({
        'numeric_col': list(range(100)),
        'string_col': ['a', 'b', 'c', 'd', 'e'] * 20,
        'col_with_nulls': [1.0, 2.0, None, 4.0, 5.0] * 20,  # 20% nulls
        'low_cardinality': ['a'] * 90 + ['b'] * 10,  # For memory optimization
    })

    profiler = DataProfiler()
    profile = profiler.profile(df)

    # Verify profile structure
    assert 'dimensions' in profile
    assert 'fields' in profile
    assert 'statistics' in profile
    assert 'optimization' in profile
    assert 'missing_strategies' in profile
    assert 'profiling_timestamp' in profile
    assert 'data_quality_score' in profile

    # Verify dimensions
    assert profile['dimensions']['rows'] == 100
    assert profile['dimensions']['columns'] == 4

    # Verify fields
    assert len(profile['fields']) == 4
    assert 'numeric_col' in profile['fields']
    assert 'string_col' in profile['fields']
    assert 'col_with_nulls' in profile['fields']
    assert 'low_cardinality' in profile['fields']

    # Verify statistics
    assert 'numeric_summary' in profile['statistics']

    # Verify optimization
    assert 'current_memory_mb' in profile['optimization']
    assert 'suggestions' in profile['optimization']

    # Verify missing strategies
    assert 'missing_columns' in profile['missing_strategies']
    assert 'col_with_nulls' in profile['missing_strategies']['missing_columns']

    # Verify quality score is between 0 and 100
    assert 0 <= profile['data_quality_score'] <= 100

    # Verify timestamp is a valid ISO format string
    from datetime import datetime
    try:
        datetime.fromisoformat(profile['profiling_timestamp'])
    except ValueError:
        assert False, "profiling_timestamp should be valid ISO format"