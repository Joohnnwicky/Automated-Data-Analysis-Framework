# tests/test_synthesis.py
"""
Test scaffolds for REP-05 and REP-06 requirements.
Initially skipped - will pass after src/report/synthesis.py implementation.
"""

import pytest
from pathlib import Path


class TestSynthesis:
    """Tests for synthesis engine and manager-POV synthesis generation."""

    def test_parse_expert_files(self, tmp_path):
        """REP-05: Verify expert file parsing from output/experts/ directory."""
        from src.report.synthesis import parse_expert_files

        # Create mock expert output files
        experts_dir = tmp_path / 'experts'
        experts_dir.mkdir()

        expert_file = experts_dir / 'quant_analyst.md'
        expert_file.write_text(
            '# Quantitative Analyst\n\n'
            '## Analysis\n\n'
            'ROI increased by 15%.\n\n'
            'Revenue: $1.2M.\n\n'
            '## Recommendations\n\n'
            '- Increase marketing spend\n'
            '- Focus on retention\n',
            encoding='utf-8'
        )

        # Skip roles.md if present
        roles_file = experts_dir / 'roles.md'
        roles_file.write_text('# Role definitions\n', encoding='utf-8')

        result = parse_expert_files(experts_dir)

        # Verify parsing returns list of findings dicts
        assert isinstance(result, list)
        assert len(result) == 1  # Only quant_analyst.md, roles.md skipped
        assert 'source_file' in result[0]
        assert 'metrics' in result[0]
        assert 'recommendations' in result[0]

    def test_organize_by_theme(self):
        """REP-05: Verify theme organization from parsed expert outputs."""
        from src.report.synthesis import organize_by_theme

        # Findings from parse_expert_files
        findings = [
            {'source_file': 'quant_analyst.md', 'metrics': [{'value': '15', 'unit': 'percent', 'context': 'ROI increased by 15%'}], 'recommendations': ['Increase marketing spend']},
            {'source_file': 'growth_expert.md', 'metrics': [{'value': '20', 'unit': 'percent', 'context': 'User growth improved significantly'}], 'recommendations': []},
            {'source_file': 'risk_analyst.md', 'metrics': [{'value': '8', 'unit': 'percent', 'context': 'Risk volatility decreased by 8%'}], 'recommendations': []},
            {'source_file': 'ops_expert.md', 'metrics': [{'value': '12', 'unit': 'percent', 'context': 'Operational efficiency improved by 12%'}], 'recommendations': []},
            {'source_file': 'market_expert.md', 'metrics': [{'value': '5', 'unit': 'percent', 'context': 'Market share increased by 5%'}], 'recommendations': []}
        ]

        themes = organize_by_theme(findings)

        # Verify themes are organized into 5 categories
        assert isinstance(themes, dict)
        expected_themes = ['财务健康度', '增长趋势', '风险指标', '运营效率', '市场表现']
        for theme in expected_themes:
            assert theme in themes

    def test_generate_conclusion_title(self):
        """REP-05: Verify conclusion-style titles (not topic-style)."""
        from src.report.synthesis import generate_conclusion_title

        # Test with metrics dict containing significant changes
        metrics = {
            'ROI': {'value': 15.2, 'change_pct': 15},
            'CTR': {'value': 3.1, 'change_pct': -3},
            'Revenue': {'value': 1000, 'change_pct': 5}  # Below 10% threshold
        }

        title = generate_conclusion_title(metrics)

        # Verify title is conclusion-style
        assert isinstance(title, str)
        assert len(title) > 0

        # Title should be like "ROI增长15%, CTR下降3%"
        assert 'ROI' in title
        assert '增长' in title or '下降' in title

        # Title should NOT be topic-style like "ROI分析报告"
        assert '分析' not in title
        assert '报告' not in title

        # Title should NOT contain expert attribution
        assert 'expert' not in title.lower()
        assert 'analyst' not in title.lower()

    def test_generate_conclusion_title_fallback(self):
        """REP-05: Verify fallback title when no significant metrics."""
        from src.report.synthesis import generate_conclusion_title

        # Test with no significant metrics (all below 10% threshold)
        metrics = {
            'Revenue': {'value': 1000, 'change_pct': 5},
            'Users': {'value': 500, 'change_pct': 2}
        }

        title = generate_conclusion_title(metrics)

        # Fallback to "数据概览"
        assert title == '数据概览'

    def test_manager_pov(self):
        """REP-06: Verify synthesis output contains no expert names."""
        from src.report.synthesis import generate_manager_pov_synthesis

        # Themes dict from organize_by_theme
        themes = {
            '财务健康度': [
                {'source_file': 'quant_analyst.md', 'metrics': [{'value': '15', 'context': 'ROI increased by 15%'}], 'recommendations': ['分析师认为应该增加投入']}
            ],
            '增长趋势': [
                {'source_file': 'growth_expert.md', 'metrics': [{'value': '20', 'context': 'User growth improved'}], 'recommendations': ['根据量化分析师的建议']}
            ]
        }

        synthesis = generate_manager_pov_synthesis(themes)

        # Verify synthesis is generated
        assert isinstance(synthesis, str)
        assert len(synthesis) > 0

        # Verify output organized by theme sections
        assert '## 财务健康度' in synthesis
        assert '## 增长趋势' in synthesis

        # Verify no expert names or IDs appear in synthesis
        assert 'quant_analyst' not in synthesis
        assert 'growth_expert' not in synthesis

        # Verify no expert attribution patterns (T-4-06)
        assert '分析师认为' not in synthesis
        assert '根据.*分析师' not in synthesis
        assert 'analyst' not in synthesis.lower()

        # Synthesis should use manager-POV language: "数据显示..."
        assert '数据显示' in synthesis or '发现' in synthesis