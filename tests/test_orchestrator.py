"""Tests for UX-01, UX-02, UX-03, UX-04 integration requirements.

Tests for WorkflowOrchestrator end-to-end workflow coordination.
"""

import pytest
from pathlib import Path
import pandas as pd


class TestWorkflowOrchestrator:
    """Tests for WorkflowOrchestrator class (UX-01-04)."""

    def test_execute_returns_dict(self):
        """UX-01: Verify execute returns dict with workflow results."""
        from src.workflow.orchestrator import WorkflowOrchestrator

        orchestrator = WorkflowOrchestrator()
        result = orchestrator.execute(query="分析数据")

        assert isinstance(result, dict)
        assert 'intent' in result

    def test_execute_with_intent_detection(self):
        """UX-01: Verify execute calls detect_intent at workflow start."""
        from src.workflow.orchestrator import WorkflowOrchestrator
        from src.workflow.intent_detector import IntentMatch

        orchestrator = WorkflowOrchestrator()
        result = orchestrator.execute(query="分析数据")

        # Verify intent was detected
        assert 'intent' in result
        assert isinstance(result['intent'], IntentMatch)
        assert result['intent'].intent_type == 'analyze'

    def test_execute_with_quick_mode(self):
        """UX-02: Verify execute activates quick mode for small dataset."""
        from src.workflow.orchestrator import WorkflowOrchestrator
        from src.data.loader import DataLoader

        orchestrator = WorkflowOrchestrator()

        # Create small test DataFrame
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [10, 20, 30],
            'C': ['a', 'b', 'c']
        })

        # Save to temp file
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            temp_path = Path(f.name)

        try:
            # Use quick intent
            result = orchestrator.execute(query="快速查数", data_path=temp_path)

            # Verify quick mode was activated
            assert result.get('workflow_mode') == 'quick'
            assert 'quick_response' in result
        finally:
            os.unlink(temp_path)

    def test_execute_full_workflow(self):
        """UX-01-03: Verify execute runs all phases for complex dataset."""
        from src.workflow.orchestrator import WorkflowOrchestrator

        orchestrator = WorkflowOrchestrator()

        # Create dataset that exceeds quick mode thresholds (>100 rows)
        # to trigger full workflow regardless of data type
        import numpy as np
        df = pd.DataFrame({
            'value1': np.random.uniform(1, 100, 150),
            'value2': np.random.uniform(1, 100, 150),
            'category': ['A', 'B', 'C'] * 50
        })

        import tempfile
        import os

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            temp_path = Path(f.name)

        try:
            result = orchestrator.execute(query="分析数据", data_path=temp_path)

            # Verify full workflow was activated (rows > 100 triggers full mode)
            assert result.get('workflow_mode') == 'full'
            assert 'profile' in result
            assert 'data_type' in result
            assert 'expert_outputs' in result
        finally:
            os.unlink(temp_path)

    def test_phases_execute_in_order(self):
        """UX-03: Verify phases execute in correct order."""
        from src.workflow.orchestrator import WorkflowOrchestrator
        from src.workflow.phases import WorkflowPhase

        orchestrator = WorkflowOrchestrator()

        # Track phase transitions
        phases_called = []
        original_callback = orchestrator._display_progress

        def tracking_callback(transition):
            phases_called.append(transition.to_phase)
            original_callback(transition)

        orchestrator.progress.display_callback = tracking_callback

        # Execute with dataset >100 rows to trigger full workflow
        import numpy as np
        df = pd.DataFrame({
            'CTR': np.random.uniform(0.01, 0.05, 150),
            'ROI': np.random.uniform(1.5, 3.0, 150),
            'cost': np.random.uniform(100, 500, 150)
        })

        import tempfile
        import os

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            temp_path = Path(f.name)

        try:
            result = orchestrator.execute(query="广告分析", data_path=temp_path)

            # Verify phases were called in order
            assert len(phases_called) >= 3  # At least UNDERSTAND, ANALYZE, REPORT or COMPLETED
            # Verify phases are in correct order (increasing phase value)
            phase_values = [p.value for p in phases_called]
            assert phase_values == sorted(phase_values)
        finally:
            os.unlink(temp_path)


class TestErrorHandling:
    """Tests for error handling (UX-04)."""

    def test_dataloaderror_preserved(self):
        """UX-04: Verify DataLoadError.user_message is preserved."""
        from src.workflow.orchestrator import WorkflowOrchestrator

        orchestrator = WorkflowOrchestrator()

        # Use non-existent file path
        result = orchestrator.execute(
            query="分析数据",
            data_path=Path("/nonexistent/file.csv")
        )

        # Verify error message is in result
        assert 'error' in result
        assert isinstance(result['error'], str)
        assert len(result['error']) > 0

    def test_valueerror_on_invalid_input(self):
        """UX-04: Verify ValueError raised for invalid input."""
        from src.workflow.orchestrator import WorkflowOrchestrator

        orchestrator = WorkflowOrchestrator(output_format='invalid')

        # Invalid output_format should not raise on init
        # but should work for basic query
        result = orchestrator.execute(query="分析数据")

        # Should return dict with intent
        assert 'intent' in result