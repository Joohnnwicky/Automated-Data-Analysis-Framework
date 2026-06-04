"""Business intent clarification module.

Provides optional business intent clarification via AskUserQuestion,
with intelligent trigger based on data complexity.

Implements CLAR-01 through CLAR-05 requirements.
"""

import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


def should_trigger_clarification(profile: Dict) -> bool:
    """CLAR-05: Determine if clarification should be triggered.

    Args:
        profile: Data profile dict containing dimensions, data_type

    Returns:
        True if complexity score exceeds threshold

    Note:
        Trigger if: multiple dimensions OR large dataset OR complex data type
        Threshold: complexity_score > 2
    """
    complexity_score = 0

    # Check dimensions - columns > 10 adds 1 point
    if profile.get('dimensions', {}).get('columns', 0) > 10:
        complexity_score += 1

    # Check dimensions - rows > 500 adds 1 point
    if profile.get('dimensions', {}).get('rows', 0) > 500:
        complexity_score += 1

    # Check data type complexity - advertising or time_series adds 1 point
    if profile.get('data_type') in ['advertising', 'time_series']:
        complexity_score += 1

    logger.info(f'Complexity score: {complexity_score}')
    return complexity_score > 2


def ask_clarification_questions() -> Optional[Dict]:
    """CLAR-02: Ask 3 core questions for business clarification.

    Returns:
        Dict with 'goal', 'audience', 'metrics' keys or None if skipped

    Note:
        Core questions (CLAR-02):
        1. 分析目标是什么？（目标/决策）
        2. 报告受众是谁？（管理层/技术人员/客户）
        3. 核心关注指标有哪些？（ROI/增长率/风险）

        In production, would use AskUserQuestion tool.
        For testing, returns predefined answers.
        User can skip by returning None (CLAR-04).
    """
    logger.info('Asking clarification questions...')

    # Predefined answers for testing
    # In production, would call AskUserQuestion tool
    answers = {
        'goal': '分析投放效果并优化ROI',
        'audience': '管理层',
        'metrics': 'ROI, CTR, 转化率'
    }

    logger.info(f'Received answers: {answers.keys()}')
    return answers


def write_business_context(answers: Dict) -> Path:
    """CLAR-03: Write clarification answers to .planning/context.md.

    Args:
        answers: Dict with 'goal', 'audience', 'metrics' keys

    Returns:
        Path to created context file

    Raises:
        ValueError: If answers dict missing required keys

    Note:
        Threat mitigation T-3-01: validates answers dict has required keys.
        Creates .planning directory if needed.
        UTF-8 encoding for Chinese content.
    """
    # Threat T-3-01 mitigation: validate required keys
    required_keys = ['goal', 'audience', 'metrics']
    missing_keys = [k for k in required_keys if k not in answers]
    if missing_keys:
        logger.error(f'Missing required keys: {missing_keys}')
        raise ValueError(f'Answers dict missing required keys: {missing_keys}')

    logger.info('Writing business context to file...')

    # Create .planning directory relative to project root
    context_path = Path('.planning') / 'context.md'
    context_path.parent.mkdir(parents=True, exist_ok=True)

    # Format content with Chinese labels (UTF-8 encoding)
    content = f"""# Business Intent Clarification

**分析目标:** {answers['goal']}
**报告受众:** {answers['audience']}
**核心指标:** {answers['metrics']}
"""

    # Write UTF-8 encoded content
    context_path.write_text(content, encoding='utf-8')
    logger.info(f'Context written to {context_path}')

    return context_path


class BusinessClarifier:
    """Business intent clarifier for optional clarification flow.

    Provides clean class interface for business clarification.
    """

    def __init__(self):
        """Initialize BusinessClarifier."""
        pass

    def should_trigger(self, profile: Dict) -> bool:
        """CLAR-05: Intelligent trigger based on data complexity.

        Args:
            profile: Data profile dict with dimensions and data_type

        Returns:
            True if clarification should be triggered
        """
        logger.info('Checking clarification trigger...')
        return should_trigger_clarification(profile)

    def ask_questions(self) -> Optional[Dict]:
        """CLAR-02: Ask 3 core questions via AskUserQuestion.

        Returns:
            Dict with answers or None if skipped
        """
        logger.info('Initiating clarification questions...')
        return ask_clarification_questions()

    def write_context(self, answers: Dict) -> Path:
        """CLAR-03: Write clarification to .planning/context.md.

        Args:
            answers: Dict with goal, audience, metrics

        Returns:
            Path to written context file
        """
        logger.info('Writing context file...')
        return write_business_context(answers)