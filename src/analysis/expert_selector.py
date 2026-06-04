"""Expert role selection module.

Provides algorithmic matching of expert roles based on data type
and business context. Implements EXPT-01, EXPT-04 requirements.

Threat Model:
- T-3-01: Validates data_type against whitelist to prevent injection
- T-3-05: Role definitions imported from constants (no user input)
"""

import logging
from typing import List, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


def select_experts(
    data_type: str,
    business_context: Optional[Dict] = None,
    min_experts: int = 3,
    max_experts: int = 5
) -> List['ExpertRole']:
    """EXPT-01: Select relevant experts based on data type and business context.

    Args:
        data_type: 'table', 'time_series', or 'advertising'
        business_context: Optional dict with 'goal', 'audience', 'metrics'
        min_experts: Minimum number of experts to select
        max_experts: Maximum number of experts to select

    Returns:
        List of selected ExpertRole objects

    Raises:
        ValueError: If data_type is not in whitelist ['table', 'time_series', 'advertising']

    Note:
        Filter by data_type first, then refine by business context.
        Ensure minimum coverage by adding generic experts if needed.
    """
    from src.analysis.expert_roles import EXPERT_ROLES, ExpertRole

    # T-3-01: Validate data_type against whitelist
    valid_types = ['table', 'time_series', 'advertising']
    if data_type not in valid_types:
        raise ValueError(f"Invalid data_type '{data_type}'. Must be one of {valid_types}")

    # Filter by data type
    eligible = [
        role for role in EXPERT_ROLES
        if data_type in role.data_types
    ]

    logger.info(f'{len(eligible)} eligible experts for {data_type}')

    # Business context refinement
    if business_context:
        goal = business_context.get('goal', '')
        metrics = business_context.get('metrics', [])

        # Prioritize advertising experts when ROI or '投放' mentioned
        if 'ROI' in metrics or '投放' in goal:
            eligible.sort(
                key=lambda r: 'advertising' in r.data_types,
                reverse=True
            )

    # Ensure minimum coverage and limit to max
    selected = eligible[:max_experts]

    if len(selected) < min_experts:
        # Add generic experts (roles with 'table' in data_types)
        generic = [r for r in EXPERT_ROLES if 'table' in r.data_types]
        for g in generic:
            if g not in selected:
                selected.append(g)
                if len(selected) >= min_experts:
                    break

    logger.info(f'Selected {len(selected)} experts')
    return selected[:max_experts]


def write_expert_definitions(selected: List['ExpertRole']) -> Path:
    """EXPT-04: Write role definitions to file for user confirmation.

    Args:
        selected: List of selected ExpertRole objects

    Returns:
        Path to written definitions file

    Note:
        Creates output/experts directory if needed.
        Uses UTF-8 encoding for Chinese content.
    """
    # Create output directory
    output_dir = Path(__file__).parent.parent.parent / 'output' / 'experts'
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / 'roles.md'

    # Build markdown content
    content = "# 专家角色定义\n\n"

    for role in selected:
        content += f"## {role.name}\n\n"
        content += f"**角色ID:** {role.id}\n"
        content += f"**专业领域:** {role.domain}\n"
        content += f"**分析框架:** {role.framework}\n"
        content += "**分析任务:**\n"
        for task in role.tasks:
            content += f"- {task}\n"
        content += f"**适用数据类型:** {', '.join(role.data_types)}\n\n"

    # Write with UTF-8 encoding
    output_path.write_text(content, encoding='utf-8')
    logger.info(f'Role definitions written to {output_path}')

    return output_path


class ExpertSelector:
    """Expert role selector for automatic expert matching.

    Provides a clean class interface for expert selection.
    """

    def __init__(self):
        """Initialize ExpertSelector."""
        pass

    def select(
        self,
        data_type: str,
        business_context: Optional[Dict] = None,
        min_experts: int = 3,
        max_experts: int = 5
    ) -> List['ExpertRole']:
        """Select experts for given data type and context.

        Args:
            data_type: 'table', 'time_series', or 'advertising'
            business_context: Optional dict with goal, audience, metrics
            min_experts: Minimum number of experts to select
            max_experts: Maximum number of experts to select

        Returns:
            List of ExpertRole objects
        """
        logger.info('Selecting expert roles...')
        return select_experts(data_type, business_context, min_experts, max_experts)

    def write_role_definitions(self, selected: List['ExpertRole']) -> Path:
        """EXPT-04: Write role definitions for user confirmation.

        Args:
            selected: List of selected ExpertRole objects

        Returns:
            Path to written definitions file
        """
        return write_expert_definitions(selected)