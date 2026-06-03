"""
Data profiling functions for Data Analyst Pro.

Provides profile_dimensions, profile_fields, and profile_statistics
for comprehensive DataFrame analysis.
"""

import logging
from typing import Dict, Any

import pandas as pd
import numpy as np


logger = logging.getLogger(__name__)


def profile_dimensions(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Profile DataFrame dimensions (rows, columns, memory usage).

    Args:
        df: DataFrame to profile

    Returns:
        Dict with keys: rows, columns, memory_bytes, memory_mb

    Note:
        Uses deep=True for memory_usage to accurately count object/string columns.
        See RESEARCH.md Pitfall 3: Inaccurate Memory Reporting.
    """
    rows = len(df)
    columns = len(df.columns)
    memory_bytes = df.memory_usage(deep=True).sum()
    memory_mb = round(memory_bytes / 1024 / 1024, 2)

    logger.info(f'Dimensions: {rows} rows, {columns} columns, {memory_mb} MB')

    return {
        'rows': rows,
        'columns': columns,
        'memory_bytes': memory_bytes,
        'memory_mb': memory_mb
    }


def profile_fields(df: pd.DataFrame) -> Dict[str, Dict]:
    """
    Profile each field in DataFrame with dtype, null stats, and type-specific statistics.

    Args:
        df: DataFrame to profile

    Returns:
        Dict of field names to profile dicts with:
        - dtype: column data type
        - null_count: number of null values
        - null_rate: percentage of nulls (0-100)
        - unique_count: number of unique values
        - statistics: type-specific stats (numeric or categorical)

    Note:
        Numeric columns: min, max, mean, median, std
        Object columns: top_value, top_freq
    """
    fields = {}

    for col in df.columns:
        col_profile = {
            'dtype': str(df[col].dtype),
            'null_count': int(df[col].isna().sum()),
            'null_rate': round(df[col].isna().sum() / len(df) * 100, 4),
            'unique_count': int(df[col].nunique()),
        }

        # Type-specific statistics
        if df[col].dtype in ['int64', 'float64', 'int32', 'float32']:
            # Numeric columns
            if not df[col].isna().all():
                col_profile['statistics'] = {
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'std': float(df[col].std()),
                }
            else:
                # All values are NaN
                col_profile['statistics'] = {
                    'min': None,
                    'max': None,
                    'mean': None,
                    'median': None,
                    'std': None,
                }
        elif df[col].dtype == 'object' or str(df[col].dtype) == 'str':
            # String/categorical columns (pandas 2.x uses 'str', 1.x uses 'object')
            top_value = df[col].value_counts().head(1)
            col_profile['statistics'] = {
                'top_value': str(top_value.index[0]) if len(top_value) > 0 else None,
                'top_freq': int(top_value.values[0]) if len(top_value) > 0 else 0,
            }

        fields[col] = col_profile

    logger.info(f'Profiled {len(fields)} fields')

    return fields