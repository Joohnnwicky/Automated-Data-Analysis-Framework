"""
Chart type auto-selection based on data characteristics.

REP-09: Automatic chart type selection from Phase 2 DataProfiler output.
Follows data-to-viz.com heuristics for chart type matching.

Usage:
    from src.report.chart_selector import select_chart_type

    data_profile = {
        'datetime_columns': ['date'],
        'numeric_columns': ['value'],
        'categorical_columns': []
    }

    chart_type, rationale = select_chart_type(data_profile)

Precedence Order:
    1. datetime + numeric → line (time-series takes highest priority)
    2. numeric + categorical → bar (most efficient comparison)
    3. two numeric → scatter (relationship analysis)
    4. single numeric → histogram (distribution)
    5. fallback → table (no clear pattern)

Reference:
    https://www.data-to-viz.com — Chart type selection heuristics
"""

from typing import Tuple, Dict, List


def select_chart_type(data_profile: Dict) -> Tuple[str, str]:
    """
    Select chart type based on data characteristics from DataProfiler.

    Heuristics from data-to-viz.com:
    - Time-series (datetime column detected) → Line chart
    - One numeric + one categorical → Bar chart
    - Two numeric variables → Scatter plot
    - Single numeric → Histogram (distribution)
    - Fallback → Table

    Args:
        data_profile: Dict containing:
            - datetime_columns: List[str] of datetime column names
            - numeric_columns: List[str] of numeric column names
            - categorical_columns: List[str] of categorical column names

    Returns:
        Tuple[str, str]: (chart_type, rationale) where rationale is Chinese
        explanation for the selection.

    Examples:
        >>> select_chart_type({'datetime_columns': ['date'], 'numeric_columns': ['value'], 'categorical_columns': []})
        ('line', '时序数据，展示趋势变化')

        >>> select_chart_type({'datetime_columns': [], 'numeric_columns': ['sales'], 'categorical_columns': ['category']})
        ('bar', '数值与分类变量关系，最高效展示')
    """
    datetime_cols: List[str] = data_profile.get('datetime_columns', [])
    numeric_cols: List[str] = data_profile.get('numeric_columns', [])
    categorical_cols: List[str] = data_profile.get('categorical_columns', [])

    # Rule 1: Time-series data → Line chart (highest priority)
    # datetime columns indicate time dimension, best shown as line for trend
    if len(datetime_cols) > 0 and len(numeric_cols) > 0:
        return ('line', '时序数据，展示趋势变化')

    # Rule 2: Numeric + Categorical → Bar chart
    # Most efficient for comparing values across categories
    if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
        return ('bar', '数值与分类变量关系，最高效展示')

    # Rule 3: Two numeric variables → Scatter chart
    # Relationship analysis between two continuous variables
    if len(numeric_cols) >= 2 and len(datetime_cols) == 0:
        return ('scatter', '双数值变量关系分析')

    # Rule 4: Single numeric → Histogram (distribution analysis)
    if len(numeric_cols) == 1 and len(categorical_cols) == 0 and len(datetime_cols) == 0:
        return ('histogram', '单变量分布分析')

    # Fallback: Unable to determine best chart type
    return ('table', '无法确定最佳图表类型，使用表格展示')


__all__ = ['select_chart_type']