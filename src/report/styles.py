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
DESIGN_STYLES: List[DesignStyle] = []