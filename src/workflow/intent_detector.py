"""Intent detection module for UX-01.

Provides keyword-based intent matching for skill invocation.
Users can invoke skill with natural keywords like "analyze data",
"make report", "make PPT", "Excel", "advertising analysis".

Threat Model:
- T-5-01: Whitelist keywords in INTENT_KEYWORDS, no regex injection
- T-5-03: Sanitize query before logging (truncate to 100 chars)
"""

import logging
from dataclasses import dataclass
from typing import List, Dict

logger = logging.getLogger(__name__)


@dataclass
class IntentMatch:
    """Detected user intent from query.

    Attributes:
        intent_type: Primary intent ('analyze', 'report', 'ppt', 'excel', 'advertising', 'quick', 'unknown')
        confidence: Match confidence (0.0-1.0)
        matched_keywords: Keywords that matched the query
        suggested_workflow: Workflow path ('full', 'quick', 'full_ppt', 'clarify_only')
    """
    intent_type: str
    confidence: float
    matched_keywords: List[str]
    suggested_workflow: str


# Keyword sets for intent detection (UX-01)
INTENT_KEYWORDS: Dict[str, List[str]] = {
    'analyze': ['分析数据', '数据分析', 'analyze', '分析'],
    'report': ['做报告', '生成报告', 'make report', '报告', 'report'],
    'ppt': ['做PPT', 'PPT', '幻灯片', 'slides', 'presentation'],
    'excel': ['Excel', '表格', 'xlsx'],
    'advertising': ['投放分析', '广告分析', 'ROI', 'CTR', 'advertising'],
    'quick': ['查数', '看数据', '快速', 'simple', 'quick']
}


def detect_intent(query: str) -> IntentMatch:
    """UX-01: Detect user intent from natural language query.

    Args:
        query: User's natural language query string

    Returns:
        IntentMatch with detected intent, confidence, and workflow suggestion

    Note:
        Multi-keyword matches increase confidence.
        Unknown intent defaults to 'clarify_only' workflow.
    """
    # T-5-03: Sanitize query before processing
    query_lower = query.lower()[:100]  # Truncate to prevent log injection

    matched: Dict[str, List[str]] = {}

    # Find keyword matches for each intent type
    for intent_type, keywords in INTENT_KEYWORDS.items():
        matches = [kw for kw in keywords if kw.lower() in query_lower]
        if matches:
            matched[intent_type] = matches

    # No matches - return unknown intent
    if not matched:
        logger.info(f'No intent detected for query: {query_lower[:50]}')
        return IntentMatch(
            intent_type='unknown',
            confidence=0.0,
            matched_keywords=[],
            suggested_workflow='clarify_only'
        )

    # Determine primary intent (most keyword matches)
    primary_intent = max(matched.keys(), key=lambda k: len(matched[k]))

    # Calculate confidence (capped at 1.0)
    confidence = min(len(matched[primary_intent]) / 3.0, 1.0)

    # Determine workflow path
    if 'quick' in matched:
        workflow = 'quick'
    elif 'ppt' in matched:
        workflow = 'full_ppt'
    else:
        workflow = 'full'

    logger.info(f'Detected intent: {primary_intent} (workflow: {workflow}, confidence: {confidence:.2f})')

    return IntentMatch(
        intent_type=primary_intent,
        confidence=confidence,
        matched_keywords=matched[primary_intent],
        suggested_workflow=workflow
    )