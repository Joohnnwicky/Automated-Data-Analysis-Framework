"""HTML report generator with Jinja2 templates and embedded charts.

This module provides the HTMLReportGenerator class for creating
professional HTML reports with embedded visualizations, following
REP-01, REP-04, REP-05, REP-07, REP-10 requirements.

Usage:
    from src.report.html_report import HTMLReportGenerator

    generator = HTMLReportGenerator(style='ft')
    generator.generate(report_data, output_path)

Threat Model:
- T-4-01: XSS prevention via Jinja2 autoescape (select_autoescape)
"""

from pathlib import Path
from typing import Dict, Any, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.report.styles import get_design_style, DesignStyle


class HTMLReportGenerator:
    """Generate HTML reports with embedded charts and PDF hint.

    REP-01: HTML report generation with embedded visualizations
    REP-04: Chinese-first output with lang='zh-CN'
    REP-05: Conclusion-style titles from synthesis
    REP-07: Structure: Executive Summary -> Metrics -> Themes -> Conclusions
    REP-08: Single style source via CSS variables
    REP-10: PDF export hint in footer

    Attributes:
        template_dir: Directory containing Jinja2 templates
        style: DesignStyle object for colors and fonts
        env: Jinja2 Environment with autoescape enabled

    Example:
        >>> generator = HTMLReportGenerator(style='ft')
        >>> generator.generate({'title': '报告', ...}, Path('output.html'))
    """

    def __init__(
        self,
        template_dir: Optional[Path] = None,
        style: str = 'ft'
    ):
        """Initialize HTML report generator.

        Args:
            template_dir: Directory containing Jinja2 templates.
                         Defaults to src/report/templates/.
            style: Design style ID (e.g., 'ft', 'mckinsey', 'economist').
                   Defaults to 'ft' (Financial Times style).

        Raises:
            ValueError: If style_id is not recognized.
        """
        # Default template directory
        if template_dir is None:
            template_dir = Path(__file__).parent / 'templates'

        self.template_dir = template_dir

        # Load design style (REP-03, REP-08)
        self.style = get_design_style(style)

        # Create Jinja2 environment with autoescape (T-4-01 mitigation)
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def generate(
        self,
        report_data: Dict[str, Any],
        output_path: Path
    ) -> Path:
        """Generate HTML report and save to file.

        Args:
            report_data: Dictionary containing report content:
                - title: Report title (Chinese text supported)
                - metrics: Dict of metric name -> value
                - themes: Dict of theme name -> content dict
                - conclusions: List of conclusion strings
                - executive_summary: Optional executive summary text
                - metrics_panel: Optional metrics panel content
                - thematic_analysis: Optional thematic analysis content
                - charts: Optional dict of theme -> SVG chart string
            output_path: Path to save HTML file

        Returns:
            Path to the generated HTML file.

        Example:
            >>> generator.generate({'title': '报告', 'metrics': {...}}, Path('report.html'))
        """
        # Render template with data
        html = self.generate_report(report_data)

        # Write to file with UTF-8 encoding (REP-04)
        output_path.write_text(html, encoding='utf-8')

        return output_path

    def generate_report(
        self,
        synthesis_data: Dict[str, Any],
        charts: Optional[Dict[str, str]] = None
    ) -> str:
        """Generate HTML report as string.

        Args:
            synthesis_data: Dictionary containing synthesis content:
                - report_title or title: Report title
                - executive_summary: Executive summary text
                - metrics_panel: Metrics panel content
                - thematic_analysis: Thematic analysis content
                - conclusions: Conclusions content
            charts: Optional dict mapping theme name to SVG chart string.

        Returns:
            Complete HTML string ready for display or saving.

        Example:
            >>> html = generator.generate_report({'title': '报告', ...})
        """
        # Get base template
        template = self.env.get_template('base.html')

        # Extract title (support both 'title' and 'report_title' keys)
        report_title = synthesis_data.get('report_title') or synthesis_data.get('title', '数据分析报告')

        # Get CSS variables from style (REP-08)
        style_vars = self.style.to_css_vars()

        # Build sections content
        executive_summary = synthesis_data.get('executive_summary', '')
        if not executive_summary and 'themes' in synthesis_data:
            # Generate executive summary from themes if not provided
            executive_summary = self._build_executive_summary(synthesis_data)

        metrics_panel = synthesis_data.get('metrics_panel', '')
        if not metrics_panel and 'metrics' in synthesis_data:
            # Generate metrics panel from metrics dict
            metrics_panel = self._build_metrics_panel(synthesis_data.get('metrics', {}))

        thematic_analysis = synthesis_data.get('thematic_analysis', '')
        if not thematic_analysis and 'themes' in synthesis_data:
            # Generate thematic analysis from themes dict
            thematic_analysis = self._build_thematic_analysis(
                synthesis_data.get('themes', {}),
                charts or {}
            )

        conclusions = synthesis_data.get('conclusions', '')
        if not conclusions and 'conclusions' in synthesis_data:
            # Generate conclusions from conclusions list
            conclusions = self._build_conclusions(synthesis_data.get('conclusions', []))

        # Render template (REP-04: Chinese-first, REP-07: structure)
        html = template.render(
            report_title=report_title,
            style=style_vars,
            executive_summary=executive_summary,
            metrics_panel=metrics_panel,
            thematic_analysis=thematic_analysis,
            conclusions=conclusions,
            charts=charts or {},
            lang='zh-CN',
            pdf_hint='按 Ctrl/Cmd + P 可导出 PDF'  # REP-10
        )

        return html

    def _build_executive_summary(self, data: Dict[str, Any]) -> str:
        """Build executive summary section HTML.

        Args:
            data: Report data with themes and metrics.

        Returns:
            HTML string for executive summary section.
        """
        lines = []

        # Add title
        title = data.get('title', '数据分析报告')
        lines.append(f'<h2>执行摘要</h2>')
        lines.append(f'<p>{title}</p>')

        # Add key metrics summary
        metrics = data.get('metrics', {})
        if metrics:
            lines.append('<p>关键指标：</p>')
            lines.append('<ul>')
            for name, value in metrics.items():
                lines.append(f'<li>{name}: {value}</li>')
            lines.append('</ul>')

        return '\n'.join(lines)

    def _build_metrics_panel(self, metrics: Dict[str, Any]) -> str:
        """Build metrics panel section HTML.

        Args:
            metrics: Dict mapping metric name to value.

        Returns:
            HTML string for metrics panel section.
        """
        if not metrics:
            return ''

        lines = ['<h2>关键指标</h2>']
        lines.append('<div class="metrics-grid">')

        for name, value in metrics.items():
            lines.append(f'<div class="metric-card">')
            lines.append(f'<span class="metric-name">{name}</span>')
            lines.append(f'<span class="metric-value">{value}</span>')
            lines.append('</div>')

        lines.append('</div>')
        return '\n'.join(lines)

    def _build_thematic_analysis(
        self,
        themes: Dict[str, Any],
        charts: Dict[str, str]
    ) -> str:
        """Build thematic analysis section HTML.

        Args:
            themes: Dict mapping theme name to content dict.
            charts: Dict mapping theme name to SVG chart string.

        Returns:
            HTML string for thematic analysis section.
        """
        if not themes:
            return ''

        lines = ['<h2>主题分析</h2>']

        for theme_name, theme_content in themes.items():
            lines.append(f'<div class="theme-section">')

            # Theme title
            if isinstance(theme_content, dict):
                title = theme_content.get('title', theme_name)
                insights = theme_content.get('insights', [])
            else:
                title = theme_name
                insights = []

            lines.append(f'<h3>{title}</h3>')

            # Add chart if available
            if theme_name in charts:
                lines.append(f'<div class="chart-container">{charts[theme_name]}</div>')

            # Add insights
            if insights:
                lines.append('<ul>')
                for insight in insights:
                    lines.append(f'<li>{insight}</li>')
                lines.append('</ul>')

            lines.append('</div>')

        return '\n'.join(lines)

    def _build_conclusions(self, conclusions: list) -> str:
        """Build conclusions section HTML.

        Args:
            conclusions: List of conclusion strings.

        Returns:
            HTML string for conclusions section.
        """
        if not conclusions:
            return ''

        lines = ['<h2>综合结论与建议</h2>']
        lines.append('<ul>')

        for item in conclusions:
            lines.append(f'<li>{item}</li>')

        lines.append('</ul>')
        return '\n'.join(lines)


__all__ = ['HTMLReportGenerator']