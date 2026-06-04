"""
Data loading module for Data Analyst Pro.

Provides data loading, encoding detection, and user-friendly error handling.
"""

import logging
from pathlib import Path
from typing import Optional

import pandas as pd
from charset_normalizer import from_bytes

from src.data.memory import estimate_memory, MEMORY_THRESHOLD_BYTES

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


def load_excel_safe(filepath: Path) -> pd.DataFrame:
    """
    Load Excel file with openpyxl engine.

    Args:
        filepath: Path to the Excel file to load

    Returns:
        pandas DataFrame with the loaded data

    Raises:
        DataLoadError: If the file is empty or malformed

    Note:
        Uses openpyxl engine for .xlsx and .xls files.
    """
    try:
        df = pd.read_excel(filepath, engine='openpyxl')
        logger.info(f'Loaded Excel: {len(df)} rows from {filepath}')
        return df
    except pd.errors.EmptyDataError as e:
        raise DataLoadError(
            message=f'文件为空或格式错误：{filepath.name}',
            technical_detail=f'EmptyDataError: {str(e)}'
        )


def load_json_safe(filepath: Path) -> pd.DataFrame:
    """
    Load JSON file with UTF-8 encoding.

    Args:
        filepath: Path to the JSON file to load

    Returns:
        pandas DataFrame with the loaded data

    Raises:
        DataLoadError: If the file is malformed or cannot be parsed

    Note:
        Uses UTF-8 encoding for JSON files.
    """
    try:
        df = pd.read_json(filepath, encoding='utf-8')
        logger.info(f'Loaded JSON: {len(df)} rows from {filepath}')
        return df
    except ValueError as e:
        raise DataLoadError(
            message=f'JSON格式错误：{filepath.name}。请检查文件是否符合JSON规范',
            technical_detail=f'ValueError: {str(e)}'
        )


def load_file(filepath: Path) -> pd.DataFrame:
    """
    Load data file with comprehensive security validation.

    Performs security checks before loading:
    1. File existence validation
    2. Format whitelist validation (.xlsx, .xls, .csv, .json)
    3. File size limit validation (500MB maximum)

    Args:
        filepath: Path to the data file to load

    Returns:
        pandas DataFrame with the loaded data

    Raises:
        DataLoadError: If file doesn't exist, format unsupported,
                       file too large, or loading fails

    Note:
        Routes to format-specific loaders based on file extension.
        User messages in Chinese (UX-04), technical details in English.
    """
    # Check file existence
    if not filepath.exists():
        raise DataLoadError(
            message=f'文件不存在：{filepath.name}',
            technical_detail=f'Path not found: {filepath.resolve()}'
        )

    # Check file format (whitelist)
    suffix = filepath.suffix.lower()
    supported_formats = ['.xlsx', '.xls', '.csv', '.json']

    if suffix not in supported_formats:
        raise DataLoadError(
            message=f'不支持该文件格式：{suffix}。支持格式：Excel (.xlsx/.xls)、CSV、JSON',
            technical_detail=f'Unsupported format: {suffix}'
        )

    # Check file size (500MB limit)
    file_size_mb = filepath.stat().st_size / 1024 / 1024
    if file_size_mb > 500:
        raise DataLoadError(
            message=f'文件过大（{file_size_mb:.1f}MB），建议使用采样模式或分块处理',
            technical_detail=f'File size: {file_size_mb:.2f}MB exceeds 500MB limit'
        )

    # Memory estimation check for CSV files (chunking suggestion)
    if suffix == '.csv':
        estimated_memory = estimate_memory(filepath)
        estimated_memory_mb = estimated_memory / 1024 / 1024

        # Already handled by file size limit above if >= 500MB
        # Log warning for files > 50MB suggesting chunked processing
        if estimated_memory > 50 * 1024 * 1024:
            logger.warning(
                f'Large file detected ({estimated_memory_mb:.1f}MB estimated), '
                'consider using chunked processing'
            )

    # Route to format-specific loader
    try:
        if suffix in ['.xlsx', '.xls']:
            return load_excel_safe(filepath)
        elif suffix == '.csv':
            return load_csv_safe(filepath)
        elif suffix == '.json':
            return load_json_safe(filepath)
    except pd.errors.EmptyDataError as e:
        raise DataLoadError(
            message=f'文件为空或格式错误：{filepath.name}',
            technical_detail=f'EmptyDataError: {str(e)}'
        )
    except UnicodeDecodeError as e:
        raise DataLoadError(
            message=f'文件编码错误：{filepath.name}。请检查是否为中文编码（GB2312/GBK）或 UTF-8',
            technical_detail=f'UnicodeDecodeError: {str(e)}'
        )
    except Exception as e:
        logger.exception(f'Unexpected error loading {filepath}')
        raise DataLoadError(
            message=f'文件读取失败：{filepath.name}。请检查文件是否损坏',
            technical_detail=f'{type(e).__name__}: {str(e)}'
        )


class DataLoader:
    """
    Public interface for data loading operations.

    Provides a clean wrapper for load_file function with logging.

    Usage:
        loader = DataLoader()
        df = loader.load(Path('data.csv'))
    """

    def __init__(self) -> None:
        """Initialize DataLoader instance."""
        pass

    def load(self, filepath: Path) -> pd.DataFrame:
        """
        Load data file and return DataFrame.

        Args:
            filepath: Path to the data file to load

        Returns:
            pandas DataFrame with the loaded data

        Raises:
            DataLoadError: If file loading fails

        Note:
            Logs loading operations for debugging.
            Delegates to load_file for actual loading.
        """
        logger.info(f'Loading file: {filepath}')
        df = load_file(filepath)
        logger.info(f'File loaded successfully: {len(df)} rows')
        return df