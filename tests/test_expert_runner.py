# tests/test_expert_runner.py
"""
Tests for EXPT-03, EXPT-05, EXPT-06 requirements.
Tests for ExpertRunner class and expert orchestration.
"""

import pytest
import pandas as pd
from pathlib import Path
from datetime import datetime


class TestGetExpertOutputPath:
    """Tests for get_expert_output_path function (EXPT-06)."""

    def test_returns_path_with_role_id(self):
        """EXPT-06: Verify get_expert_output_path returns Path ending with {role_id}.md."""
        from src.analysis.expert_runner import get_expert_output_path
        from src.analysis.expert_roles import EXPERT_ROLES

        role = EXPERT_ROLES[0]
        path = get_expert_output_path(role)

        assert isinstance(path, Path)
        assert str(path).endswith(f'{role.id}.md')

    def test_different_roles_get_different_paths(self):
        """EXPT-06: Verify different roles get different output paths."""
        from src.analysis.expert_runner import get_expert_output_path
        from src.analysis.expert_roles import EXPERT_ROLES

        role1 = EXPERT_ROLES[0]
        role2 = EXPERT_ROLES[1]

        path1 = get_expert_output_path(role1)
        path2 = get_expert_output_path(role2)

        assert path1 != path2

    def test_all_paths_unique(self):
        """EXPT-06: Verify paths for 3 roles are all unique."""
        from src.analysis.expert_runner import get_expert_output_path
        from src.analysis.expert_roles import EXPERT_ROLES

        roles = EXPERT_ROLES[:3]
        paths = [get_expert_output_path(role) for role in roles]

        assert len(set(paths)) == len(paths), "Each expert should have unique output path"

    def test_path_in_output_experts_directory(self):
        """EXPT-06: Verify path is in output/experts directory."""
        from src.analysis.expert_runner import get_expert_output_path
        from src.analysis.expert_roles import EXPERT_ROLES

        role = EXPERT_ROLES[0]
        path = get_expert_output_path(role)

        path_str = str(path)
        assert 'experts' in path_str, f"Path should contain 'experts' directory: {path_str}"


class TestBuildExpertPrompt:
    """Tests for build_expert_prompt function (EXPT-05)."""

    def test_prompt_contains_role_name(self):
        """EXPT-05: Verify prompt contains role.name."""
        from src.analysis.expert_runner import build_expert_prompt
        from src.analysis.expert_roles import EXPERT_ROLES

        role = EXPERT_ROLES[0]
        prompt = build_expert_prompt(role, Path('data.csv'), {})

        assert role.name in prompt

    def test_prompt_contains_role_framework(self):
        """EXPT-05: Verify prompt contains role.framework."""
        from src.analysis.expert_runner import build_expert_prompt
        from src.analysis.expert_roles import EXPERT_ROLES

        role = EXPERT_ROLES[0]
        prompt = build_expert_prompt(role, Path('data.csv'), {})

        assert role.framework in prompt

    def test_prompt_contains_statistical_enforcement(self):
        """EXPT-07: Verify prompt contains STATISTICAL_ENFORCEMENT_PROMPT key phrases."""
        from src.analysis.expert_runner import build_expert_prompt
        from src.analysis.expert_roles import EXPERT_ROLES

        role = EXPERT_ROLES[0]
        prompt = build_expert_prompt(role, Path('data.csv'), {})

        # Check for key phrases from STATISTICAL_ENFORCEMENT_PROMPT
        assert 'Python' in prompt or 'python' in prompt
        assert '代码' in prompt or '计算' in prompt

    def test_prompt_does_not_contain_other_expert_names(self):
        """EXPT-05: Verify prompt does NOT contain other expert names (context isolation)."""
        from src.analysis.expert_runner import build_expert_prompt
        from src.analysis.expert_roles import EXPERT_ROLES

        quant_role = EXPERT_ROLES[0]  # quant_analyst
        val_role = EXPERT_ROLES[1]    # valuation_expert

        quant_prompt = build_expert_prompt(quant_role, Path('data.csv'), {})

        # Quant analyst prompt should NOT contain valuation expert info
        assert val_role.name not in quant_prompt

    def test_prompt_contains_output_path(self):
        """EXPT-06: Verify prompt contains output path for expert."""
        from src.analysis.expert_runner import build_expert_prompt
        from src.analysis.expert_roles import EXPERT_ROLES

        role = EXPERT_ROLES[0]
        prompt = build_expert_prompt(role, Path('data.csv'), {})

        assert f'{role.id}.md' in prompt


class TestDispatchParallelExperts:
    """Tests for dispatch_parallel_experts function (EXPT-03, EXPT-06)."""

    def test_returns_dict_with_role_id_keys(self):
        """EXPT-03: Verify function returns dict with role_id keys."""
        from src.analysis.expert_runner import dispatch_parallel_experts
        from src.analysis.expert_roles import EXPERT_ROLES

        roles = EXPERT_ROLES[:2]
        prompts = {role.id: f'prompt for {role.id}' for role in roles}

        result = dispatch_parallel_experts(prompts, roles)

        assert isinstance(result, dict)
        assert all(role.id in result for role in roles)

    def test_each_role_maps_to_unique_path(self):
        """EXPT-06: Verify each role_id maps to unique Path."""
        from src.analysis.expert_runner import dispatch_parallel_experts
        from src.analysis.expert_roles import EXPERT_ROLES

        roles = EXPERT_ROLES[:2]
        prompts = {role.id: f'prompt for {role.id}' for role in roles}

        result = dispatch_parallel_experts(prompts, roles)

        paths = list(result.values())
        assert len(set(paths)) == len(paths), "Each role should have unique output path"

    def test_all_paths_in_output_experts_directory(self):
        """EXPT-06: Verify all paths are in output/experts directory."""
        from src.analysis.expert_runner import dispatch_parallel_experts
        from src.analysis.expert_roles import EXPERT_ROLES

        roles = EXPERT_ROLES[:2]
        prompts = {role.id: f'prompt for {role.id}' for role in roles}

        result = dispatch_parallel_experts(prompts, roles)

        for path in result.values():
            assert 'experts' in str(path)

    def test_accepts_prompts_dict_and_selected_roles_list(self):
        """EXPT-03: Verify function accepts prompts dict and selected_roles list."""
        from src.analysis.expert_runner import dispatch_parallel_experts
        from src.analysis.expert_roles import EXPERT_ROLES

        roles = EXPERT_ROLES[:2]
        prompts = {role.id: f'prompt for {role.id}' for role in roles}

        # Should not raise
        result = dispatch_parallel_experts(prompts, roles)

        assert isinstance(result, dict)


class TestExpertRunner:
    """Tests for ExpertRunner class (EXPT-03)."""

    def test_run_experts_returns_dict(self):
        """EXPT-03: Verify run_experts returns dict with expert_outputs, execution_timestamp, total_experts."""
        from src.analysis.expert_runner import ExpertRunner
        from src.analysis.expert_roles import EXPERT_ROLES

        roles = EXPERT_ROLES[:2]
        data_path = Path('test_data.csv')
        data_profile = {'dimensions': {'rows': 100, 'columns': 5}, 'data_type': 'table'}

        runner = ExpertRunner()
        result = runner.run_experts(roles, data_path, data_profile)

        # Verify result structure
        assert isinstance(result, dict)
        assert 'expert_outputs' in result
        assert 'execution_timestamp' in result
        assert 'total_experts' in result

        # Verify expert_outputs is a dict
        assert isinstance(result['expert_outputs'], dict)

        # Verify total_experts matches role count
        assert result['total_experts'] == len(roles)

        # Verify timestamp is valid ISO format
        try:
            datetime.fromisoformat(result['execution_timestamp'])
        except ValueError:
            assert False, "execution_timestamp should be valid ISO format"

    def test_expert_outputs_dict_maps_role_id_to_path(self):
        """EXPT-03: Verify expert_outputs is dict mapping role_id to Path."""
        from src.analysis.expert_runner import ExpertRunner
        from src.analysis.expert_roles import EXPERT_ROLES

        roles = EXPERT_ROLES[:2]
        data_path = Path('test_data.csv')
        data_profile = {'dimensions': {'rows': 100, 'columns': 5}, 'data_type': 'table'}

        runner = ExpertRunner()
        result = runner.run_experts(roles, data_path, data_profile)

        expert_outputs = result['expert_outputs']

        for role in roles:
            assert role.id in expert_outputs
            assert isinstance(expert_outputs[role.id], Path)