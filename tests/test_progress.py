"""Tests for UX-03 progress indicator requirements.

Tests for WorkflowPhase enum, PhaseTransition dataclass, and ProgressIndicator class.
"""

import pytest
from pathlib import Path


class TestWorkflowPhase:
    """Tests for WorkflowPhase enum (UX-03)."""

    def test_enum_values(self):
        """UX-03: Verify WorkflowPhase has 5 values: CLARIFY, UNDERSTAND, ANALYZE, REPORT, COMPLETED."""
        from src.workflow.phases import WorkflowPhase

        assert hasattr(WorkflowPhase, 'CLARIFY')
        assert hasattr(WorkflowPhase, 'UNDERSTAND')
        assert hasattr(WorkflowPhase, 'ANALYZE')
        assert hasattr(WorkflowPhase, 'REPORT')
        assert hasattr(WorkflowPhase, 'COMPLETED')

        # Verify it's an enum with 5 members
        members = list(WorkflowPhase)
        assert len(members) == 5

    def test_phase_order(self):
        """UX-03: Verify phase values are in correct order."""
        from src.workflow.phases import WorkflowPhase

        phases = [
            WorkflowPhase.CLARIFY,
            WorkflowPhase.UNDERSTAND,
            WorkflowPhase.ANALYZE,
            WorkflowPhase.REPORT,
            WorkflowPhase.COMPLETED
        ]

        # Verify each phase has increasing value
        values = [p.value for p in phases]
        assert values == sorted(values)


class TestPhaseTransition:
    """Tests for PhaseTransition dataclass (UX-03)."""

    def test_dataclass_fields(self):
        """UX-03: Verify PhaseTransition has 4 fields."""
        from src.workflow.progress import PhaseTransition
        from src.workflow.phases import WorkflowPhase

        transition = PhaseTransition(
            from_phase=WorkflowPhase.CLARIFY,
            to_phase=WorkflowPhase.UNDERSTAND,
            progress_percent=40.0,
            message="Phase 2/4: Data Understanding"
        )

        assert hasattr(transition, 'from_phase')
        assert hasattr(transition, 'to_phase')
        assert hasattr(transition, 'progress_percent')
        assert hasattr(transition, 'message')

    def test_transition_to_returns_transition(self):
        """UX-03: Verify transition_to returns PhaseTransition object."""
        from src.workflow.progress import ProgressIndicator, PhaseTransition
        from src.workflow.phases import WorkflowPhase

        indicator = ProgressIndicator()
        transition = indicator.transition_to(WorkflowPhase.UNDERSTAND)

        assert isinstance(transition, PhaseTransition)
        assert transition.to_phase == WorkflowPhase.UNDERSTAND


class TestProgressIndicator:
    """Tests for ProgressIndicator class (UX-03)."""

    def test_init_default_phase(self):
        """UX-03: Verify ProgressIndicator initializes with CLARIFY phase."""
        from src.workflow.progress import ProgressIndicator
        from src.workflow.phases import WorkflowPhase

        indicator = ProgressIndicator()

        assert indicator.current_phase == WorkflowPhase.CLARIFY
        assert indicator.progress == 0.0

    def test_transition_to_updates_phase(self):
        """UX-03: Verify transition_to updates current_phase."""
        from src.workflow.progress import ProgressIndicator
        from src.workflow.phases import WorkflowPhase

        indicator = ProgressIndicator()

        # Transition to UNDERSTAND
        indicator.transition_to(WorkflowPhase.UNDERSTAND)
        assert indicator.current_phase == WorkflowPhase.UNDERSTAND

        # Transition to ANALYZE
        indicator.transition_to(WorkflowPhase.ANALYZE)
        assert indicator.current_phase == WorkflowPhase.ANALYZE

    def test_progress_percent_calculation(self):
        """UX-03: Verify progress_percent increases with each phase."""
        from src.workflow.progress import ProgressIndicator
        from src.workflow.phases import WorkflowPhase

        indicator = ProgressIndicator()

        # CLARIFY = 20%
        t1 = indicator.transition_to(WorkflowPhase.CLARIFY)
        assert t1.progress_percent == 20.0

        # UNDERSTAND = 40%
        t2 = indicator.transition_to(WorkflowPhase.UNDERSTAND)
        assert t2.progress_percent == 40.0

        # ANALYZE = 60%
        t3 = indicator.transition_to(WorkflowPhase.ANALYZE)
        assert t3.progress_percent == 60.0

        # REPORT = 80%
        t4 = indicator.transition_to(WorkflowPhase.REPORT)
        assert t4.progress_percent == 80.0

        # COMPLETED = 100%
        t5 = indicator.transition_to(WorkflowPhase.COMPLETED)
        assert t5.progress_percent == 100.0

    def test_display_callback_called(self):
        """UX-03: Verify display_callback is invoked on transition."""
        from src.workflow.progress import ProgressIndicator, PhaseTransition
        from src.workflow.phases import WorkflowPhase

        # Track callback invocations
        callbacks = []
        def callback(t: PhaseTransition):
            callbacks.append(t)

        indicator = ProgressIndicator(display_callback=callback)
        indicator.transition_to(WorkflowPhase.UNDERSTAND)

        assert len(callbacks) == 1
        assert callbacks[0].to_phase == WorkflowPhase.UNDERSTAND

    def test_get_current_message(self):
        """UX-03: Verify get_current_message returns correct message."""
        from src.workflow.progress import ProgressIndicator
        from src.workflow.phases import WorkflowPhase

        indicator = ProgressIndicator()

        # Initial message
        msg = indicator.get_current_message()
        assert "Clarification" in msg or "CLARIFY" in msg or "Phase 1" in msg

        # After transition
        indicator.transition_to(WorkflowPhase.UNDERSTAND)
        msg = indicator.get_current_message()
        assert "Understanding" in msg or "UNDERSTAND" in msg or "Phase 2" in msg