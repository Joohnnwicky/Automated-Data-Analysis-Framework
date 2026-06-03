# tests/test_data_loader.py
"""
Test scaffolds for DATA-01 and UX-04 requirements.
Initially skipped - will pass after src/data/loader.py implementation.
"""

import pytest
from pathlib import Path


@pytest.mark.skip(reason="src/data/loader.py not implemented")
def test_load_excel():
    """DATA-01: Verify Excel file loading with pandas read_excel."""
    pass


@pytest.mark.skip(reason="src/data/loader.py not implemented")
def test_encoding_detection():
    """DATA-01: Verify charset-normalizer encoding detection for CSV files."""
    pass


@pytest.mark.skip(reason="src/data/loader.py not implemented")
def test_error_unsupported_format():
    """UX-04: Verify DataLoadError raised for unsupported file formats."""
    pass


@pytest.mark.skip(reason="src/data/loader.py not implemented")
def test_error_corrupted_file():
    """UX-04: Verify error handling for corrupted/unreadable files."""
    pass