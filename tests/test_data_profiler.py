# tests/test_data_profiler.py
"""
Test scaffolds for DATA-02, DATA-04, DATA-07 requirements.
Initially skipped - will pass after src/data/profiler.py implementation.
"""

import pytest
from pathlib import Path


@pytest.mark.skip(reason="src/data/profiler.py not implemented")
def test_profile_dimensions():
    """DATA-02: Verify data dimensions profiling (rows, columns, memory usage)."""
    pass


@pytest.mark.skip(reason="src/data/profiler.py not implemented")
def test_numeric_stats():
    """DATA-02: Verify statistical summaries via pandas describe()."""
    pass


@pytest.mark.skip(reason="src/data/profiler.py not implemented")
def test_missing_value_report():
    """DATA-02: Verify missing value detection and strategy suggestions."""
    pass