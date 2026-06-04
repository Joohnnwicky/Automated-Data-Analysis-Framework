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

    @pytest.mark.skip(reason="Wave 0 scaffold - src/report/synthesis.py not implemented")
    def test_generate_conclusion_title(self):
        """REP-05: Verify conclusion-style titles (not expert-attribute)."""
        from src.report.synthesis import generate_conclusion_title

        # Test with analysis content
        content = 'ROI increased by 15% compared to last quarter, driven by improved conversion rates.'

        title = generate_conclusion_title(content)

        # Verify title is conclusion-style, not expert-attributed
        assert isinstance(title, str)
        assert len(title) > 0
        # Title should NOT contain expert attribution patterns
        assert 'expert' not in title.lower()
        assert 'analyst' not in title.lower()
        # Title should be actionable/conclusive
        assert any(word in title for word in ['increased', 'improved', 'decreased', 'change', 'trend', 'result'])

    @pytest.mark.skip(reason="Wave 0 scaffold - src/report/synthesis.py not implemented")
    def test_manager_pov(self):
        """REP-06: Verify synthesis output contains no expert names."""
        from src.report.synthesis import generate_manager_pov_synthesis

        expert_outputs = [
            {'expert_id': 'quant_analyst', 'name': 'Quantitative Analyst', 'content': 'ROI increased by 15%.'},
            {'expert_id': 'growth_expert', 'name': 'Growth Expert', 'content': 'User growth improved.'}
        ]

        synthesis = generate_manager_pov_synthesis(expert_outputs)

        # Verify synthesis is generated
        assert isinstance(synthesis, str)
        assert len(synthesis) > 0

        # Verify no expert names or IDs appear in synthesis
        assert 'quant_analyst' not in synthesis
        assert 'Quantitative Analyst' not in synthesis
        assert 'growth_expert' not in synthesis
        assert 'Growth Expert' not in synthesis

        # Synthesis should present unified view
        assert 'ROI' in synthesis or 'growth' in synthesis.lower()