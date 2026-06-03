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