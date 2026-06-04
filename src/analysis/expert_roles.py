"""Expert role definitions for multi-expert analysis.

This module defines the ExpertRole dataclass and the EXPERT_ROLES library
for the multi-expert analysis system. Each role represents a specialized
analytical perspective with specific domain expertise, framework, and tasks.

Threat Model:
- T-3-01: Role definitions are constants (immutable), no user input in EXPERT_ROLES
- T-3-05: Each role definition is self-contained, no cross-role references
"""

from dataclasses import dataclass
from typing import List


@dataclass
class ExpertRole:
    """Definition of an expert role for analysis.

    Attributes:
        id: Unique identifier for the role (snake_case)
        name: Display name (Chinese + English)
        domain: Expertise domain description
        framework: Analysis framework summary
        tasks: List of specific analysis tasks (3 items, Chinese)
        data_types: Compatible data types ['table', 'time_series', 'advertising']
    """
    id: str
    name: str
    domain: str
    framework: str
    tasks: List[str]
    data_types: List[str]