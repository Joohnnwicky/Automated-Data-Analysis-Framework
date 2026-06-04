"""Design style definitions for professional report generation.

This module defines the DesignStyle dataclass and the DESIGN_STYLES library
for the report generation system. Each style represents a professional design
theme with colors, fonts, and chart color palettes.

Threat Model:
- T-4-04: Font licensing - use Noto Sans SC (SIL open-source license)
- T-4-08: Style drift prevention - single source via to_css_vars()
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class DesignStyle:
    """Definition of a professional design style for reports.

    Attributes:
        id: Unique identifier for the style (snake_case)
        name: Display name (English)
        primary_color: Primary color hex code
        secondary_color: Secondary/accent color hex code
        font_family: Font family for Chinese text
        font_family_en: Font family for English text
        chart_colors: List of chart color hex codes (3 colors minimum)
    """
    id: str
    name: str
    primary_color: str
    secondary_color: str
    font_family: str
    font_family_en: str
    chart_colors: List[str]

    def to_css_vars(self) -> Dict[str, str]:
        """Generate CSS custom properties for Jinja2 template.

        Returns:
            Dict mapping CSS custom property names to style values.
            Ensures single source of truth for all style values (REP-08).
        """
        css_vars = {
            '--primary-color': self.primary_color,
            '--secondary-color': self.secondary_color,
            '--font-family': self.font_family,
            '--font-family-en': self.font_family_en,
        }

        # Add chart colors with indexed names
        for i, color in enumerate(self.chart_colors[:3], start=1):
            css_vars[f'--chart-color-{i}'] = color

        return css_vars


# Design Style Library (REP-03)
# Each style defines a professional design theme
# T-4-04: All styles use Noto Sans SC for Chinese font (SIL open-source license)
DESIGN_STYLES: List[DesignStyle] = [
    # 1. Financial Times - classic newspaper aesthetic
    DesignStyle(
        id='ft',
        name='Financial Times',
        primary_color='#33302E',
        secondary_color='#E3120B',
        font_family='Noto Sans SC, serif',
        font_family_en='Georgia, serif',
        chart_colors=['#E3120B', '#33302E', '#9F8170']
    ),
    # 2. McKinsey - consulting firm blue-green
    DesignStyle(
        id='mckinsey',
        name='McKinsey',
        primary_color='#051C2C',
        secondary_color='#2DFF99',
        font_family='Noto Sans SC, sans-serif',
        font_family_en='Helvetica Neue, sans-serif',
        chart_colors=['#051C2C', '#2DFF99', '#4A4A4A']
    ),
    # 3. The Economist - red accent on dark
    DesignStyle(
        id='economist',
        name='The Economist',
        primary_color='#1D1D1B',
        secondary_color='#E3120B',
        font_family='Noto Sans SC, serif',
        font_family_en='Georgia, serif',
        chart_colors=['#E3120B', '#1D1D1B', '#0077C2']
    ),
    # 4. Goldman Sachs - corporate blue
    DesignStyle(
        id='goldman',
        name='Goldman Sachs',
        primary_color='#0033A0',
        secondary_color='#B9B9B9',
        font_family='Noto Sans SC, sans-serif',
        font_family_en='Arial, sans-serif',
        chart_colors=['#0033A0', '#B9B9B9', '#333333']
    ),
    # 5. Swiss Design - minimalist black-red
    DesignStyle(
        id='swiss',
        name='Swiss Design',
        primary_color='#000000',
        secondary_color='#FF0000',
        font_family='Noto Sans SC, sans-serif',
        font_family_en='Helvetica, sans-serif',
        chart_colors=['#FF0000', '#000000', '#666666']
    ),
    # 6. Wall Street Journal - business blue
    DesignStyle(
        id='wsj',
        name='Wall Street Journal',
        primary_color='#333333',
        secondary_color='#0066CC',
        font_family='Noto Sans SC, serif',
        font_family_en='Georgia, serif',
        chart_colors=['#0066CC', '#333333', '#999999']
    ),
    # 7. Bloomberg - orange accent
    DesignStyle(
        id='bloomberg',
        name='Bloomberg',
        primary_color='#FF6600',
        secondary_color='#000000',
        font_family='Noto Sans SC, sans-serif',
        font_family_en='Helvetica Neue, sans-serif',
        chart_colors=['#FF6600', '#000000', '#333333']
    ),
    # 8. Reuters - news agency orange
    DesignStyle(
        id='reuters',
        name='Reuters',
        primary_color='#FF8000',
        secondary_color='#333333',
        font_family='Noto Sans SC, sans-serif',
        font_family_en='Arial, sans-serif',
        chart_colors=['#FF8000', '#333333', '#666666']
    ),
    # 9. Morningstar - investment research gold
    DesignStyle(
        id='morningstar',
        name='Morningstar',
        primary_color='#FFD700',
        secondary_color='#333333',
        font_family='Noto Sans SC, sans-serif',
        font_family_en='Georgia, serif',
        chart_colors=['#FFD700', '#333333', '#006400']
    ),
    # 10. BCG - consulting blue-green (similar to McKinsey)
    DesignStyle(
        id='bcg',
        name='BCG',
        primary_color='#0033A0',
        secondary_color='#2DFF99',
        font_family='Noto Sans SC, sans-serif',
        font_family_en='Helvetica Neue, sans-serif',
        chart_colors=['#0033A0', '#2DFF99', '#4A4A4A']
    ),
    # 11. Bain & Company - deep blue-red
    DesignStyle(
        id='bain',
        name='Bain & Company',
        primary_color='#003366',
        secondary_color='#CC0000',
        font_family='Noto Sans SC, sans-serif',
        font_family_en='Georgia, serif',
        chart_colors=['#CC0000', '#003366', '#666666']
    ),
]


def get_design_style(style_id: str) -> DesignStyle:
    """Get a design style by its unique identifier.

    Args:
        style_id: The unique identifier of the style (e.g., 'ft', 'mckinsey')

    Returns:
        The DesignStyle object matching the given id

    Raises:
        ValueError: If no style with the given id exists

    Example:
        >>> style = get_design_style('ft')
        >>> style.name
        'Financial Times'
    """
    for style in DESIGN_STYLES:
        if style.id == style_id:
            return style

    raise ValueError(f"Unknown style: {style_id}")