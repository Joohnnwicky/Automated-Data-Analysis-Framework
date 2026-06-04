"""
Data loading module for Data Analyst Pro.

Provides data loading, encoding detection, and user-friendly error handling.
"""

import logging
from pathlib import Path
from typing import Optional

import pandas as pd
from charset_normalizer import from_bytes

logger = logging.getLogger(__name__)


class DataLoadError(Exception):
    """
    Custom exception with user-friendly error messages.

    Attributes:
        user_message: User-friendly error message (Chinese for UX-04)
        technical_detail: Optional technical detail (English)
    """

    def __init__(self, message: str, technical_detail: Optional[str] = None):
        """
        Initialize DataLoadError with message and optional technical detail.

        Args:
            message: User-friendly error message
            technical_detail: Optional technical detail for debugging
        """
        self.user_message = message
        self.technical_detail = technical_detail
        super().__init__(message)


def detect_encoding(filepath: Path, sample_size: int = 10000) -> str:
    """
    Detect file encoding using charset-normalizer.

    Args:
        filepath: Path to the file to detect encoding for
        sample_size: Number of bytes to read for detection (default: 10000)

    Returns:
        Detected encoding string (e.g., 'utf-8', 'gb2312', 'gbk')

    Note:
        Falls back to 'utf-8' if detection fails.
    """
    with open(filepath, 'rb') as f:
        sample = f.read(sample_size)

    result = from_bytes(sample)
    if result and result.best():
        encoding = result.best().encoding
        coherence = result.best().coherence
        logger.info(f'Detected encoding: {encoding} (coherence: {coherence:.2f})')
        return encoding

    # Fallback to UTF-8 if detection fails
    logger.warning('Encoding detection failed, using UTF-8 fallback')
    return 'utf-8'


def load_csv_safe(filepath: Path) -> pd.DataFrame:
    """
    Load CSV file with automatic encoding detection and fallback chain.

    Args:
        filepath: Path to the CSV file to load

    Returns:
        pandas DataFrame with the loaded data

    Raises:
        ValueError: If the file cannot be decoded with any encoding

    Note:
        Uses charset-normalizer for initial encoding detection,
        then falls back to utf-8, latin-1, cp1252 on UnicodeDecodeError.
    """
    encoding = detect_encoding(filepath)

    try:
        df = pd.read_csv(filepath, encoding=encoding)
        logger.info(f'Loaded CSV: {len(df)} rows from {filepath}')
        return df
    except UnicodeDecodeError:
        # Fallback chain: try alternative encodings
        for fallback_enc in ['utf-8', 'latin-1', 'cp1252']:
            try:
                df = pd.read_csv(filepath, encoding=fallback_enc)
                logger.warning(f'Used fallback encoding: {fallback_enc}')
                return df
            except UnicodeDecodeError:
                continue

        raise ValueError(f'Cannot decode file {filepath} with any encoding')