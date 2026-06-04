# tests/test_expert_roles.py
"""
Test scaffolds for EXPT-02 requirement.
Initially skipped - will pass after src/analysis/expert_roles.py implementation.
"""

import pytest
import pandas as pd
from pathlib import Path


class TestExpertRole:
    """Tests for ExpertRole dataclass and role definitions."""

    def test_expert_role_dataclass_fields(self):
        """EXPT-02: Verify ExpertRole dataclass has id, name, domain, framework, tasks, data_types fields."""
        from src.analysis.expert_roles import ExpertRole

        # Create an expert role instance
        role = ExpertRole(
            id='quantitative_analyst',
            name='Quantitative Analyst',
            domain='Financial Analysis',
            framework='Statistical modeling and hypothesis testing',
            tasks=['Statistical analysis', 'Trend detection', 'Anomaly detection'],
            data_types=['table', 'time_series']
        )

        # Verify all required fields exist
        assert hasattr(role, 'id')
        assert hasattr(role, 'name')
        assert hasattr(role, 'domain')
        assert hasattr(role, 'framework')
        assert hasattr(role, 'tasks')
        assert hasattr(role, 'data_types')

        # Verify field types
        assert isinstance(role.id, str)
        assert isinstance(role.name, str)
        assert isinstance(role.domain, str)
        assert isinstance(role.framework, str)
        assert isinstance(role.tasks, list)
        assert isinstance(role.data_types, list)

    def test_expert_roles_list_defined(self):
        """EXPT-02: Verify EXPERT_ROLES list contains 6+ predefined roles."""
        pytest.skip("Wave 0 scaffold - implementation pending")

        from src.analysis.expert_roles import EXPERT_ROLES

        # Verify EXPERT_ROLES is a list
        assert isinstance(EXPERT_ROLES, list)

        # Verify at least 6 predefined roles
        assert len(EXPERT_ROLES) >= 6, "EXPERT_ROLES should contain at least 6 predefined expert roles"

        # Verify each item is an ExpertRole
        from src.analysis.expert_roles import ExpertRole
        for role in EXPERT_ROLES:
            assert isinstance(role, ExpertRole)

    def test_expert_role_data_types_coverage(self):
        """EXPT-02: Verify each role covers at least one data_type (table/time_series/advertising)."""
        pytest.skip("Wave 0 scaffold - implementation pending")

        from src.analysis.expert_roles import EXPERT_ROLES

        valid_data_types = {'table', 'time_series', 'advertising'}

        # Each role should support at least one valid data type
        for role in EXPERT_ROLES:
            assert len(role.data_types) >= 1, f"Role {role.id} should support at least one data type"
            for dt in role.data_types:
                assert dt in valid_data_types, f"Role {role.id} has invalid data type: {dt}"

        # Collect all supported data types across roles
        all_supported_types = set()
        for role in EXPERT_ROLES:
            all_supported_types.update(role.data_types)

        # Verify at least table and time_series are covered
        assert 'table' in all_supported_types, "At least one role should support 'table' data type"
        assert 'time_series' in all_supported_types, "At least one role should support 'time_series' data type"