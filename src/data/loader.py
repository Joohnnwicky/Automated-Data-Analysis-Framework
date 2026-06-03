"""
Data loading module for Data Analyst Pro.

Provides data loading, encoding detection, and user-friendly error handling.
"""

import logging
from pathlib import Path
from typing import Optional

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