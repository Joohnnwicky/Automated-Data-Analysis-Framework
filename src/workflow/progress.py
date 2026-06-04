"""Progress indicator module for UX-03.

Provides phase transition notifications for workflow progress.
Uses ProgressIndicator class with display callback support.
"""

import logging
from dataclasses import dataclass
from typing import Optional, Callable

from src.workflow.phases import WorkflowPhase

logger = logging.getLogger(__name__)


@dataclass
class PhaseTransition:
    """Phase transition event for progress indicators.

    Attributes:
        from_phase: Phase before transition
        to_phase: Phase after transition
        progress_percent: Progress percentage (0-100)
        message: Human-readable progress message
    """
    from_phase: WorkflowPhase
    to_phase: WorkflowPhase
    progress_percent: float
    message: str


class ProgressIndicator:
    """UX-03: Progress indicator for workflow phases.

    Provides phase transition notifications with progress percentages.
    Optional display_callback for UI updates (e.g., print to console).

    Attributes:
        current_phase: Current workflow phase
        progress: Current progress percentage
        display_callback: Optional callback for progress updates
    """

    PHASE_MESSAGES = {
        WorkflowPhase.CLARIFY: "Phase 1/4: Business Intent Clarification",
        WorkflowPhase.UNDERSTAND: "Phase 2/4: Data Understanding",
        WorkflowPhase.ANALYZE: "Phase 3/4: Multi-Expert Analysis",
        WorkflowPhase.REPORT: "Phase 4/4: Report Generation",
        WorkflowPhase.COMPLETED: "Workflow Complete"
    }

    def __init__(self, display_callback: Optional[Callable[[PhaseTransition], None]] = None):
        """Initialize progress indicator.

        Args:
            display_callback: Optional function to call with progress updates
        """
        self.current_phase = WorkflowPhase.CLARIFY
        self.progress = 0.0
        self.display_callback = display_callback

    def transition_to(self, new_phase: WorkflowPhase) -> PhaseTransition:
        """Transition to new phase and emit progress notification.

        Args:
            new_phase: Target phase to transition to

        Returns:
            PhaseTransition event with details

        Note:
            UX-03: Emits progress message at each phase transition.
        """
        transition = PhaseTransition(
            from_phase=self.current_phase,
            to_phase=new_phase,
            progress_percent=self._calculate_progress(new_phase),
            message=self.PHASE_MESSAGES[new_phase]
        )

        self.current_phase = new_phase
        self.progress = transition.progress_percent

        # Log transition
        logger.info(f"Phase transition: {transition.message} ({transition.progress_percent:.0f}%)")

        # Emit display callback if provided
        if self.display_callback:
            self.display_callback(transition)

        return transition

    def _calculate_progress(self, phase: WorkflowPhase) -> float:
        """Calculate progress percentage for phase.

        Args:
            phase: Target phase

        Returns:
            Progress percentage (0-100)
        """
        phase_order = [
            WorkflowPhase.CLARIFY,
            WorkflowPhase.UNDERSTAND,
            WorkflowPhase.ANALYZE,
            WorkflowPhase.REPORT,
            WorkflowPhase.COMPLETED
        ]
        index = phase_order.index(phase)
        return (index + 1) / len(phase_order) * 100

    def get_current_message(self) -> str:
        """Get current phase message for display.

        Returns:
            Current phase progress message
        """
        return self.PHASE_MESSAGES[self.current_phase]