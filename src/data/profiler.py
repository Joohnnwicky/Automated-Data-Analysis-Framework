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


def suggest_memory_optimization(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Suggest memory optimizations for DataFrame.

    Analyzes object columns for category conversion potential by comparing
    unique value ratios and memory reduction estimates.

    Args:
        df: DataFrame to analyze

    Returns:
        Dict with:
        - current_memory_mb: current memory usage in MB
        - suggestions: list of optimization suggestions

    Note:
        Only suggests category conversion if:
        - unique_ratio < 0.5 (less than 50% unique values)
        - estimated memory reduction > 50%
    """
    suggestions = []
    current_memory = df.memory_usage(deep=True).sum()

    # Handle both pandas 1.x 'object' and 2.x 'str' dtypes
    for col in df.select_dtypes(include=['object', 'str']).columns:
        unique_ratio = df[col].nunique() / len(df)
        if unique_ratio < 0.5:  # Less than 50% unique
            cat_memory = df[col].astype('category').memory_usage(deep=True)
            obj_memory = df[col].memory_usage(deep=True)
            reduction = (obj_memory - cat_memory) / obj_memory * 100
            if reduction > 50:
                suggestions.append({
                    'column': col,
                    'suggestion': 'convert to category',
                    'estimated_reduction': round(reduction, 1)
                })

    logger.info(f'Memory optimization: {len(suggestions)} suggestions found')

    return {
        'current_memory_mb': round(current_memory / 1024 / 1024, 2),
        'suggestions': suggestions
    }


def suggest_missing_value_strategy(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Suggest missing value handling strategies for DataFrame columns.

    Analyzes columns with missing values and suggests appropriate handling
    strategies based on data type and missing percentage.

    Args:
        df: DataFrame to analyze

    Returns:
        Dict with:
        - missing_columns: dict of column names to strategy recommendations
        - total_missing_rows: count of rows with at least one missing value

    Note:
        Strategy recommendations based on missing percentage:
        - Numeric < 5%: fill with mean
        - Numeric 5-20%: fill with median
        - Numeric >= 20%: consider dropping column or rows
        - Categorical < 5%: fill with mode
        - Categorical >= 5%: fill with placeholder "Unknown" or drop rows

        Implements DATA-07 (missing value report + strategy suggestions).
    """
    strategies = {}

    for col in df.columns:
        null_count = df[col].isna().sum()
        if null_count > 0:
            null_pct = null_count / len(df) * 100
            dtype = df[col].dtype

            # Determine strategy based on dtype and null percentage
            if dtype in ['int64', 'float64', 'int32', 'float32']:
                # Numeric columns
                if null_pct < 5:
                    strategy = 'fill with mean'
                elif null_pct < 20:
                    strategy = 'fill with median'
                else:
                    strategy = 'consider dropping column or rows'
            elif dtype == 'object' or str(dtype) == 'str':
                # String/categorical columns
                if null_pct < 5:
                    strategy = 'fill with mode'
                else:
                    strategy = 'fill with placeholder "Unknown" or drop rows'
            else:
                # Other types (datetime, etc.)
                strategy = 'investigate appropriate fill method'

            strategies[col] = {
                'null_pct': round(null_pct, 2),
                'dtype': str(dtype),
                'suggested_strategy': strategy
            }

    total_missing_rows = int(df.isna().any(axis=1).sum())
    logger.info(f'Missing value strategies: {len(strategies)} columns with missing values')

    return {
        'missing_columns': strategies,
        'total_missing_rows': total_missing_rows
    }


def profile_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate statistical summaries using pandas describe().

    Args:
        df: DataFrame to profile

    Returns:
        Dict with:
        - numeric_summary: describe() output for numeric columns
        - categorical_summary: describe() output for categorical columns

    Note:
        Uses pandas describe() for comprehensive statistics.
        Only includes keys if corresponding column types exist.
    """
    stats = {}

    # Numeric columns summary
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        stats['numeric_summary'] = df[numeric_cols].describe().to_dict()

    # Categorical columns summary (handle pandas 2.x 'str' dtype explicitly)
    # Include 'object', 'category', and 'str' dtypes to support both pandas 1.x and 2.x
    categorical_cols = df.select_dtypes(include=['object', 'category', 'str']).columns.tolist()

    if categorical_cols:
        stats['categorical_summary'] = df[categorical_cols].describe(include='all').to_dict()

    logger.info(f'Generated statistics summary for {len(numeric_cols)} numeric, {len(categorical_cols)} categorical columns')

    return stats