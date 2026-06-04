# tests/test_expert_selector.py
"""
Test scaffolds for EXPT-01 and EXPT-04 requirements.
Tests for ExpertSelector class and selection algorithm.
"""

import pytest
from pathlib import Path


class TestExpertSelector:
    """Tests for ExpertSelector class and selection algorithm."""

    def test_select_returns_list(self):
        """EXPT-01: Verify select method returns list of ExpertRole objects."""
        from src.analysis.expert_selector import ExpertSelector
        from src.analysis.expert_roles import ExpertRole

        selector = ExpertSelector()
        result = selector.select(data_type='table')

        # Verify result is a list
        assert isinstance(result, list)

        # Verify each item is an ExpertRole
        for role in result:
            assert isinstance(role, ExpertRole)

        # Verify minimum experts enforced (default min_experts=3)
        assert len(result) >= 3

    def test_select_by_data_type(self):
        """EXPT-01: Verify selection filters by data_type."""
        from src.analysis.expert_selector import ExpertSelector
        from src.analysis.expert_roles import ExpertRole

        selector = ExpertSelector()

        # Select for advertising data type
        result_ad = selector.select(data_type='advertising')

        # Verify only advertising-compatible roles are returned
        for role in result_ad:
            assert 'advertising' in role.data_types

        # Verify specific advertising roles are included
        ad_role_ids = [r.id for r in result_ad]
        # growth_optimizer has data_types=['advertising']
        assert 'growth_optimizer' in ad_role_ids

    def test_select_with_business_context(self):
        """EXPT-01: Verify business context refines selection."""
        from src.analysis.expert_selector import ExpertSelector
        from src.analysis.expert_roles import ExpertRole

        selector = ExpertSelector()

        # Select with business context mentioning ROI
        result = selector.select(
            data_type='advertising',
            business_context={'metrics': ['ROI', 'conversion rate']}
        )

        # Verify advertising experts are selected
        assert len(result) >= 1
        # Verify advertising roles are present
        role_ids = [r.id for r in result]
        assert 'growth_optimizer' in role_ids

    def test_min_experts_enforced(self):
        """EXPT-01: Verify minimum 3 experts enforced even if fewer specific matches."""
        from src.analysis.expert_selector import ExpertSelector
        from src.analysis.expert_roles import ExpertRole

        selector = ExpertSelector()

        # Select for a type with fewer matches - 'time_series'
        # quant_analyst, valuation_expert, industry_analyst, financial_analyst have 'time_series'
        # That's 4 roles, so min_experts=3 should be satisfied
        result = selector.select(data_type='time_series', min_experts=3)

        # Should return at least 3 experts
        assert len(result) >= 3, "Minimum 3 experts should be enforced"

        # All should have 'time_series' or 'table' (fallback)
        for role in result:
            assert 'time_series' in role.data_types or 'table' in role.data_types

    def test_write_role_definitions(self):
        """EXPT-04: Verify write_role_definitions creates output file."""
        from src.analysis.expert_selector import ExpertSelector
        from src.analysis.expert_roles import EXPERT_ROLES
        from pathlib import Path

        selector = ExpertSelector()

        # Use actual EXPERT_ROLES
        selected = EXPERT_ROLES[:2]

        # Write role definitions
        output_path = selector.write_role_definitions(selected)

        # Verify file was created
        assert output_path is not None
        assert Path(output_path).exists()

        # Verify file contains role information
        content = Path(output_path).read_text(encoding='utf-8')
        # Check for role names (Chinese or English part)
        assert '量化分析师' in content or 'Quantitative' in content or 'quant_analyst' in content