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


@pytest.mark.skip(reason="src/data/profiler.py not implemented")
def test_numeric_stats():
    """DATA-02: Verify statistical summaries via pandas describe()."""
    pass


@pytest.mark.skip(reason="src/data/profiler.py not implemented")
def test_missing_value_report():
    """DATA-02: Verify missing value detection and strategy suggestions."""
    pass