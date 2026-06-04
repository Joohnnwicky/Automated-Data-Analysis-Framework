# tests/test_conflict_detector.py
"""
Test scaffolds for EXPT-08 requirement.
Initially skipped - will pass after src/analysis/conflict_detector.py implementation.
"""

import pytest
import pandas as pd
from pathlib import Path


class TestConflictDetector:
    """Tests for ConflictDetector class and conflict detection logic."""

    def test_detect_numerical_conflicts(self):
        """EXPT-08: Verify detect_numerical_conflicts returns conflict list when values differ >10%."""
        from src.analysis.conflict_detector import detect_numerical_conflicts

        # Create expert outputs with conflicting numerical claims (List[Dict] structure)
        expert_outputs = [
            {
                'expert_id': 'quant_analyst',
                'metrics': {
                    'ROI': 45.5,
                    'conversion_rate': 0.05,
                    'engagement': 100.0
                }
            },
            {
                'expert_id': 'growth_expert',
                'metrics': {
                    'ROI': 60.0,        # 32% difference > 10% - should conflict
                    'conversion_rate': 0.052,  # 4% difference < 10% - no conflict
                    'engagement': 102.0  # 2% difference < 10% - no conflict
                }
            }
        ]

        result = detect_numerical_conflicts(expert_outputs)

        # Should detect conflicts for values differing > 10%
        assert isinstance(result, list)

        # Should have exactly 1 conflict (ROI)
        assert len(result) == 1

        # Verify conflict structure
        conflict = result[0]
        assert conflict['type'] == 'numerical'
        assert conflict['metric'] == 'ROI'
        assert conflict['values'] == [45.5, 60.0]
        assert conflict['experts'] == ['quant_analyst', 'growth_expert']
        assert conflict['threshold'] == '10%'

    def test_detect_recommendation_conflicts(self):
        """EXPT-08: Verify detect_recommendation_conflicts returns conflict when directions oppose."""
        pytest.skip("Wave 0 scaffold - implementation pending")

        from src.analysis.conflict_detector import detect_recommendation_conflicts

        # Create expert outputs with opposing recommendations
        expert_outputs = {
            'quant_analyst': {
                'recommendations': [
                    'Increase advertising spend',
                    'Focus on high-value customers',
                    'Reduce marketing budget'
                ]
            },
            'ad_optimizer': {
                'recommendations': [
                    'Decrease advertising spend',  # Opposes 'Increase advertising spend'
                    'Focus on conversion rate',
                    'Expand marketing budget'      # Opposes 'Reduce marketing budget'
                ]
            }
        }

        result = detect_recommendation_conflicts(expert_outputs)

        # Should detect opposing directions
        assert isinstance(result, dict)

        # Should flag 'Increase' vs 'Decrease' conflict
        assert len(result) > 0

        # Verify conflict contains direction opposition
        has_direction_conflict = False
        for key, conflict in result.items():
            if 'increase' in conflict.get('directions', []) and 'decrease' in conflict.get('directions', []):
                has_direction_conflict = True
            elif 'expand' in conflict.get('directions', []) and 'reduce' in conflict.get('directions', []):
                has_direction_conflict = True

        assert has_direction_conflict, "Should detect opposing direction conflicts"

    def test_no_conflict_same_values(self):
        """EXPT-08: Verify no conflict when values differ <10%."""
        from src.analysis.conflict_detector import detect_numerical_conflicts

        # Create expert outputs with similar values (within 10%)
        expert_outputs = [
            {
                'expert_id': 'quant_analyst',
                'metrics': {
                    'ROI': 45.5,
                    'conversion_rate': 0.05,
                    'engagement': 100.0
                }
            },
            {
                'expert_id': 'growth_expert',
                'metrics': {
                    'ROI': 46.0,        # 1% difference < 10%
                    'conversion_rate': 0.052,  # 4% difference < 10%
                    'engagement': 102.0  # 2% difference < 10%
                }
            }
        ]

        result = detect_numerical_conflicts(expert_outputs)

        # Should NOT detect conflicts when values are within 10%
        assert isinstance(result, list)
        assert len(result) == 0, "No conflicts should be detected for values within 10%"

    def test_flag_conflicts_for_review(self):
        """EXPT-08: Verify flag_conflicts_for_review writes output/conflicts.md file."""
        pytest.skip("Wave 0 scaffold - implementation pending")

        from src.analysis.conflict_detector import flag_conflicts_for_review

        # Create sample conflicts
        conflicts = {
            'mean_value': {
                'experts': ['quant_analyst', 'growth_expert'],
                'values': [100.0, 150.0],
                'difference_pct': 50.0,
                'recommendation': 'Review statistical methodology'
            },
            'ad_spend_direction': {
                'experts': ['quant_analyst', 'ad_optimizer'],
                'directions': ['increase', 'decrease'],
                'recommendation': 'Align advertising strategy'
            }
        }

        output_path = flag_conflicts_for_review(conflicts, output_dir='output')

        # Verify file was created
        assert output_path is not None
        assert Path(output_path).exists()
        assert Path(output_path).name == 'conflicts.md'

        # Verify file contains conflict information
        content = Path(output_path).read_text(encoding='utf-8')
        assert 'mean_value' in content or 'Mean' in content
        assert 'recommendation' in content.lower() or '建议' in content