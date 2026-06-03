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


@pytest.mark.skip(reason="src/data/profiler.py not implemented")
def test_numeric_stats():
    """DATA-02: Verify statistical summaries via pandas describe()."""
    pass


@pytest.mark.skip(reason="src/data/profiler.py not implemented")
def test_missing_value_report():
    """DATA-02: Verify missing value detection and strategy suggestions."""
    pass