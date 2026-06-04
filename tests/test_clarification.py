# tests/test_clarification.py
"""
Test scaffolds for CLAR requirements (CLAR-01 through CLAR-05).
Initially skipped - will pass after src/analysis/clarification.py implementation.
"""

import pytest
import pandas as pd
from pathlib import Path


class TestBusinessClarifier:
    """Tests for BusinessClarifier class and clarification flow."""

    def test_should_trigger_returns_bool(self):
        """CLAR-01: Verify should_trigger returns boolean for complexity check."""
        from src.analysis.clarification import BusinessClarifier

        # Simple dataset profile should not trigger
        profile_simple = {
            'dimensions': {'rows': 100, 'columns': 5},
            'data_type': 'table'
        }
        clarifier = BusinessClarifier()
        result = clarifier.should_trigger(profile_simple)
        assert isinstance(result, bool)

        # Complex dataset profile should trigger
        profile_complex = {
            'dimensions': {'rows': 1000, 'columns': 15},
            'data_type': 'advertising'
        }
        result_complex = clarifier.should_trigger(profile_complex)
        assert isinstance(result_complex, bool)

    def test_trigger_high_complexity(self):
        """CLAR-05: Verify high complexity (large dataset + complex type) triggers clarification."""
        from src.analysis.clarification import BusinessClarifier

        # High complexity profile: large rows + advertising data type
        # columns > 10 (+1), rows > 500 (+1), data_type='advertising' (+1) = score 3
        profile = {
            'dimensions': {'rows': 1000, 'columns': 12},
            'data_type': 'advertising'
        }

        clarifier = BusinessClarifier()
        result = clarifier.should_trigger(profile)

        assert result is True, "High complexity dataset should trigger clarification"

    def test_trigger_low_complexity(self):
        """CLAR-05: Verify low complexity (small dataset + simple type) does not trigger."""
        from src.analysis.clarification import BusinessClarifier

        # Low complexity profile: small rows + simple table data type
        # columns <= 10 (+0), rows <= 500 (+0), data_type='table' (+0) = score 0
        profile = {
            'dimensions': {'rows': 50, 'columns': 5},
            'data_type': 'table'
        }

        clarifier = BusinessClarifier()
        result = clarifier.should_trigger(profile)

        assert result is False, "Low complexity dataset should not trigger clarification"

    def test_ask_questions_returns_dict_or_none(self):
        """CLAR-02: Verify ask_questions returns dict with goal/audience/metrics or None if skipped."""
        from src.analysis.clarification import BusinessClarifier, ask_clarification_questions

        clarifier = BusinessClarifier()

        # Test helper function returns dict with correct keys
        # (In production, AskUserQuestion tool would be used)
        # For testing, function returns predefined answers
        result = ask_clarification_questions()

        # Verify structure when not None
        if result is not None:
            assert isinstance(result, dict)
            assert 'goal' in result
            assert 'audience' in result
            assert 'metrics' in result
            # Verify values are strings
            assert isinstance(result['goal'], str)
            assert isinstance(result['audience'], str)
            assert isinstance(result['metrics'], str)

    def test_write_context_creates_file(self, project_root):
        """CLAR-03: Verify write_context creates .planning/context.md file."""
        from src.analysis.clarification import BusinessClarifier, write_business_context

        # Test data with Chinese content for UTF-8 verification
        answers = {
            'goal': 'ROI优化',
            'audience': '管理层',
            'metrics': 'ROI, CTR'
        }

        # Write context file using helper function
        output_path = write_business_context(answers)

        # Verify file was created
        assert output_path is not None
        assert isinstance(output_path, Path)
        assert output_path.exists()
        assert output_path.name == 'context.md'
        assert '.planning' in str(output_path)

        # Verify file content has Chinese labels (UTF-8 encoding)
        content = output_path.read_text(encoding='utf-8')
        assert '分析目标' in content
        assert 'ROI优化' in content
        assert '报告受众' in content
        assert '管理层' in content
        assert '核心指标' in content
        assert 'ROI, CTR' in content

        # Cleanup test file
        if output_path.exists():
            output_path.unlink()

    def test_skip_option_available(self):
        """CLAR-04: Verify skip option allows proceeding without clarification."""
        from src.analysis.clarification import BusinessClarifier

        clarifier = BusinessClarifier()

        # Verify skip flag/option is available
        assert hasattr(clarifier, 'skip') or hasattr(clarifier, 'enable_skip')

        # When skip is enabled, clarification should not trigger
        clarifier_skip = BusinessClarifier(skip=True)
        profile = {'dimensions': {'rows': 1000, 'columns': 15}, 'data_type': 'advertising'}
        result = clarifier_skip.should_trigger(profile)
        assert result is False, "Skip option should prevent clarification trigger"