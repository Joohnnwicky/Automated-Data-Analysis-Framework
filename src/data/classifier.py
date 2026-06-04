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


def detect_advertising_keywords(df: pd.DataFrame) -> int:
    """Count advertising keyword matches in DataFrame column names.

    Args:
        df: Input DataFrame to analyze.

    Returns:
        Number of advertising keyword matches found.
    """
    advertising_keywords = [
        'ctr', 'click', 'impression', 'conversion',
        'roi', 'cost', 'cpm', 'cpc', 'cpa',
        '投放', '点击', '转化', '曝光', '花费'
    ]

    column_names = [col.lower() for col in df.columns]
    ad_matches = sum(1 for kw in advertising_keywords
                     if any(kw in col for col in column_names))

    logger.info(f'Advertising keywords detected: {ad_matches} matches')
    return ad_matches


def classify_data_type(df: pd.DataFrame) -> Tuple[str, List[str]]:
    """Classify data type and suggest analysis methods.

    Args:
        df: Input DataFrame to classify.

    Returns:
        Tuple of (data_type, suggested_methods) where:
        - data_type: 'advertising', 'time_series', or 'table'
        - suggested_methods: List of analysis method names
    """
    ad_matches = detect_advertising_keywords(df)
    datetime_cols = detect_datetime_columns(df)

    # Classification logic
    if ad_matches >= 3:
        data_type = 'advertising'
        suggested_methods = [
            'ROI analysis',
            'CTR trend analysis',
            'Channel comparison',
            'Conversion funnel',
            'Cost optimization'
        ]
    elif len(datetime_cols) >= 1 and df[datetime_cols[0]].nunique() > 10:
        data_type = 'time_series'
        suggested_methods = [
            'Trend analysis',
            'Seasonal decomposition',
            'Forecasting',
            'Anomaly detection',
            'Period comparison'
        ]
    else:
        data_type = 'table'
        suggested_methods = [
            'Distribution analysis',
            'Correlation analysis',
            'Group comparison',
            'Missing value handling',
            'Outlier detection'
        ]

    logger.info(f'Classified as {data_type} with {len(suggested_methods)} method suggestions')
    return data_type, suggested_methods