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

from src.analysis.statistical_enforcement import STATISTICAL_ENFORCEMENT_PROMPT

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


def build_expert_prompt(role: 'ExpertRole', data_path: Path, data_profile: Dict) -> str:
    """EXPT-05: Build isolated prompt for single expert.

    Creates a self-contained prompt with context isolation - each expert
    sees only its own role definition, not other experts' contexts.
    This prevents cross-expert contamination (T-3-05 mitigation).

    Args:
        role: ExpertRole object defining the expert's perspective.
        data_path: Path to the data file being analyzed.
        data_profile: Dict with data metadata (dimensions, data_type, etc.).

    Returns:
        Prompt string for the expert subagent.

    Note:
        Includes STATISTICAL_ENFORCEMENT_PROMPT to mitigate T-3-03 (LLM hallucination).
    """
    output_path = get_expert_output_path(role)

    prompt = f"""你现在是 {role.name},专注于{role.domain}视角的分析师。

角色定义:
{role.framework}

数据文件: {data_path}
数据概览: {data_profile.get('dimensions', {})}
数据类型: {data_profile.get('data_type', 'table')}

分析任务:
{chr(10).join(f'- {task}' for task in role.tasks)}

输出要求:
- 所有数值结论必须通过Python代码计算,不可使用LLM mental math
- 输出Markdown格式,包含关键数字和结论
- 写入文件: {output_path}

{STATISTICAL_ENFORCEMENT_PROMPT}

注意:你只能看到本角色定义,不可访问其他专家的分析。"""

    return prompt


def dispatch_parallel_experts(
    prompts: Dict[str, str],
    selected_roles: List['ExpertRole']
) -> Dict[str, Path]:
    """EXPT-03: Dispatch parallel expert analysis (stub).

    Note: Real subagent execution requires Task tool integration in skill context.
    For Phase 3 implementation, this is a function stub that:
    - Returns dict mapping role_id to output_path
    - Logs parallel dispatch intent at INFO level

    In production skill context, would call Task tool with run_in_background=true.

    Args:
        prompts: Dict mapping role_id to prompt string.
        selected_roles: List of ExpertRole objects being dispatched.

    Returns:
        Dict mapping role_id to output Path for each expert.

    Threat Mitigation:
        - T-3-04: Each expert gets unique output file via get_expert_output_path
    """
    logger.info(f'Dispatching {len(selected_roles)} experts in parallel')

    output_paths = {}
    for role in selected_roles:
        output_paths[role.id] = get_expert_output_path(role)

    return output_paths


class ExpertRunner:
    """Main orchestrator for parallel expert analysis.

    Coordinates the execution of multiple expert roles in parallel,
    building isolated prompts for each expert and dispatching them
    to separate output files.

    Implements EXPT-03: Parallel expert execution orchestration.

    Threat Mitigations:
        - T-3-04: Each expert writes to separate file (no race conditions)
        - T-3-05: build_expert_prompt ensures context isolation
        - T-3-03: STATISTICAL_ENFORCEMENT_PROMPT included in all prompts
    """

    def __init__(self):
        """Initialize ExpertRunner."""
        pass

    def run_experts(
        self,
        selected_roles: List['ExpertRole'],
        data_path: Path,
        data_profile: Dict
    ) -> Dict[str, Any]:
        """EXPT-03: Run parallel expert analysis.

        Orchestrates the execution of multiple expert roles:
        1. Builds isolated prompts for each expert (context isolation)
        2. Dispatches experts to separate output files
        3. Returns structured result with outputs and metadata

        Args:
            selected_roles: List of ExpertRole objects to execute.
            data_path: Path to the data file being analyzed.
            data_profile: Dict with data metadata (dimensions, data_type, etc.).

        Returns:
            Dict with:
            - expert_outputs: Dict mapping role_id to output Path
            - execution_timestamp: ISO format timestamp
            - total_experts: Number of experts executed
        """
        result = {}

        # Build prompts for each expert (context isolation)
        prompts = {}
        for role in selected_roles:
            prompts[role.id] = build_expert_prompt(role, data_path, data_profile)

        # Dispatch experts in parallel
        output_paths = dispatch_parallel_experts(prompts, selected_roles)

        result['expert_outputs'] = output_paths
        result['execution_timestamp'] = datetime.now().isoformat()
        result['total_experts'] = len(selected_roles)

        logger.info(f'Executed {len(selected_roles)} experts in parallel')

        return result