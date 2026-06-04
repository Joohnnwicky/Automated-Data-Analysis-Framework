"""
Plotly chart generation with Chinese font support and SVG export.

This module provides functions to generate Plotly charts using design style
colors and Noto Sans SC font for Chinese text rendering.

REP-01: HTML report generation with embedded visualizations
REP-04: Chinese-first output with proper font rendering

Usage:
    from src.report.chart_generator import generate_line_chart, embed_chart_as_svg
    from src.report.styles import get_design_style

    style = get_design_style('ft')
    chart = generate_line_chart(df, x='date', y='value', title='Sales Trend', style=style)
    svg_string = embed_chart_as_svg(chart)

Threat Model:
- T-4-03: Chart data injection - pandas dtype enforcement, Plotly validates input
- T-4-04: Font licensing - Noto Sans SC is SIL open-source license
"""

import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from typing import Optional

from src.report.styles import DesignStyle


def generate_line_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    style: DesignStyle,
    y_label: Optional[str] = None
) -> go.Figure:
    """
    Generate a Plotly line chart for time-series data.

    Creates a line chart with markers using the design style's chart colors
    and Noto Sans SC font for Chinese text rendering (REP-04).

    Args:
        data: DataFrame containing the chart data
        x_col: Column name for x-axis (typically datetime or category)
        y_col: Column name for y-axis (numeric values)
        title: Chart title (supports Chinese text)
        style: DesignStyle object with chart_colors and font_family
        y_label: Optional label for y-axis (defaults to y_col name)

    Returns:
        Plotly Figure object ready for display or export

    Raises:
        ValueError: If DataFrame is empty or columns not found

    Examples:
        >>> df = pd.DataFrame({'date': ['2023-01', '2023-02'], 'value': [100, 150]})
        >>> style = get_design_style('ft')
        >>> fig = generate_line_chart(df, 'date', 'value', 'Sales Trend', style)
        >>> fig.data[0].type
        'scatter'
    """
    # Validate DataFrame is not empty
    if data.empty:
        raise ValueError("DataFrame is empty - cannot generate chart")

    # Validate columns exist
    if x_col not in data.columns:
        raise ValueError(f"Column '{x_col}' not found in DataFrame")
    if y_col not in data.columns:
        raise ValueError(f"Column '{y_col}' not found in DataFrame")

    fig = go.Figure()

    # Add line trace with markers
    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[y_col],
        mode='lines+markers',
        name=y_col,
        line=dict(
            color=style.chart_colors[0],
            width=2
        ),
        marker=dict(size=6)
    ))

    # Update layout with Chinese font and design style
    fig.update_layout(
        title=title,
        title_font_family='Noto Sans SC',
        title_font_size=16,
        font=dict(family=style.font_family),
        template='plotly_white',
        showlegend=True,
        xaxis_title=x_col,
        yaxis_title=y_label if y_label else y_col
    )

    return fig


def generate_bar_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    style: DesignStyle,
    y_label: Optional[str] = None
) -> go.Figure:
    """
    Generate a Plotly bar chart for categorical comparison.

    Creates a bar chart using the design style's chart colors
    and Noto Sans SC font for Chinese text rendering (REP-04).

    Args:
        data: DataFrame containing the chart data
        x_col: Column name for x-axis (categorical values)
        y_col: Column name for y-axis (numeric values)
        title: Chart title (supports Chinese text)
        style: DesignStyle object with chart_colors and font_family
        y_label: Optional label for y-axis (defaults to y_col name)

    Returns:
        Plotly Figure object ready for display or export

    Raises:
        ValueError: If DataFrame is empty or columns not found

    Examples:
        >>> df = pd.DataFrame({'category': ['A', 'B', 'C'], 'value': [10, 20, 15]})
        >>> style = get_design_style('ft')
        >>> fig = generate_bar_chart(df, 'category', 'value', 'Sales by Category', style)
        >>> fig.data[0].type
        'bar'
    """
    # Validate DataFrame is not empty
    if data.empty:
        raise ValueError("DataFrame is empty - cannot generate chart")

    # Validate columns exist
    if x_col not in data.columns:
        raise ValueError(f"Column '{x_col}' not found in DataFrame")
    if y_col not in data.columns:
        raise ValueError(f"Column '{y_col}' not found in DataFrame")

    fig = go.Figure()

    # Add bar trace
    fig.add_trace(go.Bar(
        x=data[x_col],
        y=data[y_col],
        name=y_col,
        marker=dict(color=style.chart_colors[0])
    ))

    # Update layout with Chinese font and design style
    fig.update_layout(
        title=title,
        title_font_family='Noto Sans SC',
        title_font_size=16,
        font=dict(family=style.font_family),
        template='plotly_white',
        showlegend=True,
        xaxis_title=x_col,
        yaxis_title=y_label if y_label else y_col
    )

    return fig


def embed_chart_as_svg(
    fig: go.Figure,
    width: int = 800,
    height: int = 400
) -> str:
    """
    Export Plotly chart as SVG string for HTML embedding.

    Uses kaleido for static image export (installed in Wave 0).
    SVG format is ideal for HTML embedding and PDF generation.

    Args:
        fig: Plotly Figure object to export
        width: Chart width in pixels (default: 800)
        height: Chart height in pixels (default: 400)

    Returns:
        SVG string ready for embedding in HTML

    Raises:
        ValueError: If kaleido is not installed or export fails

    Examples:
        >>> fig = generate_line_chart(df, 'date', 'value', 'Trend', style)
        >>> svg = embed_chart_as_svg(fig)
        >>> '<svg' in svg
        True
    """
    try:
        # Export as SVG bytes using kaleido
        svg_bytes = pio.to_image(fig, format='svg', width=width, height=height)
        # Decode to UTF-8 string
        return svg_bytes.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Failed to export chart as SVG: {e}")


__all__ = ['generate_line_chart', 'generate_bar_chart', 'embed_chart_as_svg']