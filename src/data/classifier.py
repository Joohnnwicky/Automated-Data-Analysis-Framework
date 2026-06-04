"""Data type classification module.

Provides heuristic-based data type detection (table/advertising/time-series)
and analysis method suggestions.
"""

import logging
from typing import List, Tuple

import pandas as pd

logger = logging.getLogger(__name__)


def detect_datetime_columns(df: pd.DataFrame) -> List[str]:
    """Detect datetime columns in DataFrame via name patterns and YYYYMMDD format.

    Args:
        df: Input DataFrame to analyze.

    Returns:
        List of column names identified as datetime columns.
    """
    datetime_patterns = ['day', 'date', 'time', 'timestamp', '日期', '时间']
    datetime_cols = []

    for col in df.columns:
        col_lower = col.lower()

        # Check name pattern
        if any(pattern in col_lower for pattern in datetime_patterns):
            datetime_cols.append(col)
        # Check YYYYMMDD format in object columns
        elif df[col].dtype == 'object':
            sample = df[col].dropna().head(10)
            if len(sample) > 0 and sample.astype(str).str.match(r'^\d{8}$').all():
                datetime_cols.append(col)

    logger.info(f'Detected {len(datetime_cols)} datetime columns: {datetime_cols}')
    return datetime_cols