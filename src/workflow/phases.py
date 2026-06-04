"""Workflow phase definitions for UX-03.

Provides WorkflowPhase enum for type-safe phase tracking.
"""

from enum import Enum, auto


class WorkflowPhase(Enum):
    """Workflow phase states for UX-03.

    Phases execute in order: CLARIFY -> UNDERSTAND -> ANALYZE -> REPORT -> COMPLETED
    """
    CLARIFY = auto()
    UNDERSTAND = auto()
    ANALYZE = auto()
    REPORT = auto()
    COMPLETED = auto()