"""Expert runner module for subagent orchestration.

Coordinates parallel expert execution via Task tool.
Implements EXPT-03, EXPT-05, EXPT-06 requirements.

Threat Model:
- T-3-04: Each expert writes to separate file (no shared writes)
- T-3-05: build_expert_prompt includes context isolation notice
- T-3-03: STATISTICAL_ENFORCEMENT_PROMPT included in all expert prompts
"""

import logging
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

# Output directory for expert analysis files
OUTPUT_DIR = Path(__file__).parent.parent.parent / 'output' / 'experts'


def get_expert_output_path(role: 'ExpertRole') -> Path:
    """EXPT-06: Get dedicated output file for expert.

    Each expert writes to a separate file to prevent race conditions
    and ensure isolation (T-3-04 mitigation).

    Args:
        role: ExpertRole object with id attribute.

    Returns:
        Path to expert output file: output/experts/{role_id}.md

    Note:
        Creates output/experts directory if it doesn't exist.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR / f'{role.id}.md'