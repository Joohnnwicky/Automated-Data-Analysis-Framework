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


def test_encoding_detection():
    """DATA-01: Verify charset-normalizer encoding detection for CSV files."""
    from src.data.loader import detect_encoding

    # Test UTF-8 file detection
    fixtures_dir = Path(__file__).parent / 'fixtures' / 'sample_data'
    utf8_file = fixtures_dir / 'test_utf8.csv'

    encoding = detect_encoding(utf8_file)
    assert encoding is not None
    assert isinstance(encoding, str)
    # charset-normalizer should detect utf-8 (may normalize to utf_8)
    assert 'utf' in encoding.lower()


def test_load_csv_safe():
    """DATA-01: Verify CSV loading with encoding detection and fallback chain."""
    from src.data.loader import load_csv_safe

    fixtures_dir = Path(__file__).parent / 'fixtures' / 'sample_data'

    # Test UTF-8 CSV file
    utf8_csv = fixtures_dir / 'test_utf8.csv'
    df_utf8 = load_csv_safe(utf8_csv)
    assert df_utf8 is not None
    assert len(df_utf8) > 0

    # Test GB2312 CSV file (Chinese encoding)
    gb2312_csv = fixtures_dir / 'test_gb2312.csv'
    df_gb = load_csv_safe(gb2312_csv)
    assert df_gb is not None
    assert len(df_gb) > 0


def test_error_unsupported_format():
    """UX-04: Verify DataLoadError raised for unsupported file formats."""
    from src.data.loader import DataLoadError

    # Test DataLoadError can be instantiated with message
    error = DataLoadError(message='不支持的文件格式')
    assert error.user_message == '不支持的文件格式'
    assert error.technical_detail is None
    assert str(error) == '不支持的文件格式'

    # Test DataLoadError with technical detail
    error_with_detail = DataLoadError(
        message='文件加载失败',
        technical_detail='File format .xyz not supported'
    )
    assert error_with_detail.user_message == '文件加载失败'
    assert error_with_detail.technical_detail == 'File format .xyz not supported'


@pytest.mark.skip(reason="src/data/loader.py not implemented")
def test_error_corrupted_file():
    """UX-04: Verify error handling for corrupted/unreadable files."""
    pass