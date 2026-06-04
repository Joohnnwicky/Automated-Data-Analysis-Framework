"""Initial insight generation module.

Provides InsightGenerator for generating 1-2 initial insights (trends or anomalies)
via code-executed statistics. All statistics computed via pandas/scipy - no LLM mental math.
"""

import logging
from typing import List, Dict, Optional

import pandas as pd
import numpy as np
from scipy import stats

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


def detect_trend(df: pd.DataFrame, time_col: str, metric_col: str) -> Optional[Dict]:
    """Detect trend by comparing first/last period averages.

    Args:
        df: Input DataFrame to analyze.
        time_col: Column name containing datetime values.
        metric_col: Column name containing metric values.

    Returns:
        Insight dict if change_pct > 20%, else None.
        Dict contains: type, message, recommendation, statistics.
    """
    df_time = df.copy()

    try:
        df_time[time_col] = pd.to_datetime(df_time[time_col], errors='coerce')
        df_time = df_time.dropna(subset=[time_col, metric_col])
    except Exception:
        logger.warning(f'Failed to parse datetime column: {time_col}')
        return None

    if len(df_time) < 20:
        logger.info(f'Insufficient data for trend detection: {len(df_time)} rows')
        return None

    # Sort by time and split into quarters
    df_time = df_time.sort_values(time_col)
    n = len(df_time)
    first_quarter = df_time.iloc[:n//4]
    last_quarter = df_time.iloc[-n//4:]

    first_mean = first_quarter[metric_col].mean()
    last_mean = last_quarter[metric_col].mean()

    if first_mean == 0:
        change_pct = 0
    else:
        change_pct = (last_mean - first_mean) / first_mean * 100

    if abs(change_pct) > 20:
        direction = '上升' if change_pct > 0 else '下降'
        logger.info(f'Trend detected: {direction} {abs(change_pct):.1f}%')
        return {
            'type': 'trend',
            'message': f'{metric_col} 趋势{direction} {abs(change_pct):.1f}%（首期均值 {first_mean:.2f} -> 末期均值 {last_mean:.2f}）',
            'recommendation': f'建议进一步分析{direction}原因',
            'statistics': {
                'change_pct': round(change_pct, 2),
                'first_period_mean': round(first_mean, 2),
                'last_period_mean': round(last_mean, 2)
            }
        }

    logger.info(f'No significant trend detected: {change_pct:.1f}% change')
    return None


def generate_distribution_insight(df: pd.DataFrame, col: str) -> Dict:
    """Generate distribution insight based on skew calculation.

    Args:
        df: Input DataFrame to analyze.
        col: Column name to analyze distribution for.

    Returns:
        Insight dict with distribution analysis.
        Dict contains: type, message, recommendation (if skewed).
    """
    data = df[col].dropna()
    median_val = data.median()
    mean_val = data.mean()
    std_val = data.std()

    # Use scipy.stats.skew for proper skewness coefficient
    skew = stats.skew(data) if len(data) > 0 else 0

    if abs(skew) > 1:
        logger.info(f'Skewed distribution detected in {col}: skew={skew:.2f}')
        return {
            'type': 'distribution',
            'message': f'{col} 分布偏斜（偏度={skew:.2f}），中位数={median_val:.2f}，均值={mean_val:.2f}',
            'recommendation': '建议使用中位数而非均值作为代表值'
        }

    logger.info(f'Symmetric distribution detected in {col}: mean={mean_val:.2f}, std={std_val:.2f}')
    return {
        'type': 'distribution',
        'message': f'{col} 分布较为对称，均值={mean_val:.2f}，标准差={std_val:.2f}'
    }


def generate_initial_insights(df: pd.DataFrame, data_type: str) -> List[Dict]:
    """Generate 1-2 initial insights from data.

    Args:
        df: Input DataFrame to analyze.
        data_type: Type of data ('table', 'time_series', 'advertising').

    Returns:
        List of insight dicts (max 2).
        Each dict contains: type, message, recommendation, statistics.
    """
    insights = []

    # Extract numeric columns for trend/anomaly detection
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_cols:
        logger.info('No numeric columns for insight generation')
        return [{'type': 'info', 'message': '数据无数值字段，建议查看分类分布'}]

    # Trend insight: For time_series/advertising data
    if data_type in ['time_series', 'advertising']:
        from src.data.classifier import detect_datetime_columns

        datetime_cols = detect_datetime_columns(df)
        if datetime_cols:
            time_col = datetime_cols[0]
            for metric_col in numeric_cols[:3]:
                if time_col in df.columns and metric_col in df.columns:
                    trend_insight = detect_trend(df, time_col, metric_col)
                    if trend_insight:
                        insights.append(trend_insight)
                        break

    # Anomaly insight: If no trend or less than 2 insights
    if len(insights) < 2 and numeric_cols:
        primary_col = numeric_cols[0]
        anomaly_insight = detect_anomalies(df, primary_col)
        if anomaly_insight:
            insights.append(anomaly_insight)

    # Fallback distribution insight if still no insights
    if not insights:
        distribution_insight = generate_distribution_insight(df, numeric_cols[0])
        insights.append(distribution_insight)

    logger.info(f'Generated {len(insights)} initial insights')
    return insights[:2]  # Return max 2 insights