"""Intent detection module for UX-01 and UX-02.

Provides keyword-based intent matching for skill invocation and quick response mode.
Users can invoke skill with natural keywords like "analyze data",
"make report", "make PPT", "Excel", "advertising analysis".

Threat Model:
- T-5-01: Whitelist keywords in INTENT_KEYWORDS, no regex injection
- T-5-03: Sanitize query before logging (truncate to 100 chars)
- T-5-05: Quick response is lightweight; no memory risk for small datasets (<100 rows)
"""

import logging
from dataclasses import dataclass
from typing import List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

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


# Quick mode thresholds (UX-02)
QUICK_MODE_THRESHOLD: Dict[str, Any] = {
    'max_rows': 100,
    'max_columns': 5,
    'complex_types': ['advertising', 'time_series']
}


def should_use_quick_mode(data_profile: Dict, intent: IntentMatch) -> bool:
    """UX-02: Determine if quick response mode should be used.

    Args:
        data_profile: Profile from DataProfiler with dimensions and data_type
        intent: Detected intent from detect_intent

    Returns:
        True if quick mode appropriate

    Note:
        Quick mode bypasses multi-expert workflow.
        Triggered by: small data, simple intent, or explicit quick keyword.
    """
    # Explicit quick intent bypasses all thresholds
    if intent.suggested_workflow == 'quick':
        logger.info('Quick mode: explicit quick intent')
        return True

    # Check data complexity thresholds
    rows = data_profile.get('dimensions', {}).get('rows', 0)
    columns = data_profile.get('dimensions', {}).get('columns', 0)
    data_type = data_profile.get('data_type', 'table')

    if rows > QUICK_MODE_THRESHOLD['max_rows']:
        logger.info(f'Quick mode: rows exceed threshold ({rows} > {QUICK_MODE_THRESHOLD["max_rows"]})')
        return False

    if columns > QUICK_MODE_THRESHOLD['max_columns']:
        logger.info(f'Quick mode: columns exceed threshold ({columns} > {QUICK_MODE_THRESHOLD["max_columns"]})')
        return False

    if data_type in QUICK_MODE_THRESHOLD['complex_types']:
        logger.info(f'Quick mode: complex data type ({data_type})')
        return False

    logger.info('Quick mode: simple dataset, quick mode enabled')
    return True


def quick_response(df: 'pd.DataFrame', query: str) -> str:
    """UX-02: Generate quick response without multi-expert workflow.

    Args:
        df: Loaded DataFrame
        query: User's original query

    Returns:
        Quick analysis result as formatted string

    Note:
        Uses DataProfiler for basic stats only.
        No expert dispatch, no report generation.
    """
    from src.data.profiler import DataProfiler

    profiler = DataProfiler()
    profile = profiler.profile(df)

    # Format quick output (Chinese-first)
    rows = profile.get('dimensions', {}).get('rows', 0)
    columns = profile.get('dimensions', {}).get('columns', 0)
    data_type = profile.get('data_type', 'table')

    output = f"数据概览：{rows}行 × {columns}列\n"
    output += f"数据类型：{data_type}\n"

    # Add basic statistics for numeric columns
    fields = profile.get('fields', {})
    for field, info in fields.items():
        dtype = info.get('dtype', '')
        if dtype in ['int64', 'float64', 'int32', 'float32']:
            mean_val = info.get('mean', 'N/A')
            min_val = info.get('min', 'N/A')
            max_val = info.get('max', 'N/A')
            output += f"{field}: 均值={mean_val}, 范围=[{min_val}, {max_val}]\n"

    logger.info(f'Quick response generated for query: {query[:50]}')
    return output