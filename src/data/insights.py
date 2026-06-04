"""Initial insight generation module.

Provides InsightGenerator for generating 1-2 initial insights (trends or anomalies)
via code-executed statistics. All statistics computed via pandas/scipy - no LLM mental math.
"""

import logging
from typing import List, Dict, Optional

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def detect_anomalies(df: pd.DataFrame, col: str) -> Optional[Dict]:
    """Detect outliers using IQR method.

    Args:
        df: Input DataFrame to analyze.
        col: Column name to detect anomalies in.

    Returns:
        Insight dict if outlier_pct > 5%, else None.
        Dict contains: type, message, recommendation, statistics.
    """
    data = df[col].dropna()

    if len(data) < 10:
        logger.info(f'Insufficient data for anomaly detection in {col}: {len(data)} rows')
        return None

    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = data[(data < lower_bound) | (data > upper_bound)]
    outlier_count = len(outliers)
    outlier_pct = outlier_count / len(data) * 100

    if outlier_pct > 5:
        logger.info(f'Anomaly detected in {col}: {outlier_count} outliers ({outlier_pct:.1f}%)')
        return {
            'type': 'anomaly',
            'message': f'{col} 存在 {outlier_count} 个异常值（{outlier_pct:.1f}%），范围 [{lower_bound:.2f}, {upper_bound:.2f}]',
            'recommendation': '建议检查异常值成因，考虑使用中位数或截尾均值',
            'statistics': {
                'outlier_count': outlier_count,
                'outlier_pct': round(outlier_pct, 2),
                'bounds': [round(lower_bound, 2), round(upper_bound, 2)]
            }
        }

    logger.info(f'No significant anomalies detected in {col}: {outlier_pct:.1f}% outliers')
    return None