"""Tests for UX-01 intent detection requirements.

Tests for detect_intent, IntentMatch, and keyword matching.
"""

import pytest
from pathlib import Path


class TestDetectIntent:
    """Tests for detect_intent function (UX-01)."""

    def test_detect_intent_returns_intent_match(self):
        """UX-01: Verify detect_intent returns IntentMatch for recognized keywords."""
        from src.workflow.intent_detector import detect_intent, IntentMatch

        result = detect_intent("分析数据")

        assert isinstance(result, IntentMatch)
        assert result.intent_type == 'analyze'
        assert result.confidence > 0
        assert len(result.matched_keywords) > 0

    def test_multi_intent_aggregation(self):
        """UX-01: Verify multi-keyword matches increase confidence."""
        from src.workflow.intent_detector import detect_intent

        # Single keyword match
        result1 = detect_intent("分析")

        # Multiple keyword matches
        result2 = detect_intent("分析数据 做数据分析")

        assert result2.confidence >= result1.confidence

    def test_unknown_intent_fallback(self):
        """UX-01: Verify unknown intent defaults to 'clarify_only' workflow."""
        from src.workflow.intent_detector import detect_intent

        result = detect_intent("hello world xyz")

        assert result.intent_type == 'unknown'
        assert result.confidence == 0.0
        assert result.suggested_workflow == 'clarify_only'
        assert len(result.matched_keywords) == 0

    def test_quick_workflow_detection(self):
        """UX-01: Verify quick keywords trigger 'quick' workflow."""
        from src.workflow.intent_detector import detect_intent

        result = detect_intent("快速查数")

        assert result.suggested_workflow == 'quick'

    def test_ppt_workflow_detection(self):
        """UX-01: Verify PPT keywords trigger 'full_ppt' workflow."""
        from src.workflow.intent_detector import detect_intent

        result = detect_intent("做PPT报告")

        assert result.suggested_workflow == 'full_ppt'


class TestIntentMatch:
    """Tests for IntentMatch dataclass (UX-01)."""

    def test_dataclass_fields(self):
        """UX-01: Verify IntentMatch has 4 fields: intent_type, confidence, matched_keywords, suggested_workflow."""
        from src.workflow.intent_detector import IntentMatch

        match = IntentMatch(
            intent_type='analyze',
            confidence=0.8,
            matched_keywords=['分析'],
            suggested_workflow='full'
        )

        assert hasattr(match, 'intent_type')
        assert hasattr(match, 'confidence')
        assert hasattr(match, 'matched_keywords')
        assert hasattr(match, 'suggested_workflow')
        assert match.intent_type == 'analyze'
        assert match.confidence == 0.8
        assert match.matched_keywords == ['分析']
        assert match.suggested_workflow == 'full'

    def test_dataclass_instantiation(self):
        """UX-01: Verify IntentMatch can be instantiated with valid values."""
        from src.workflow.intent_detector import IntentMatch

        match = IntentMatch(
            intent_type='report',
            confidence=0.5,
            matched_keywords=['报告', 'report'],
            suggested_workflow='full'
        )

        assert match.intent_type == 'report'
        assert isinstance(match.confidence, float)
        assert isinstance(match.matched_keywords, list)


class TestIntentKeywords:
    """Tests for INTENT_KEYWORDS constant (UX-01)."""

    def test_keyword_sets_defined(self):
        """UX-01: Verify INTENT_KEYWORDS has 6 intent types."""
        from src.workflow.intent_detector import INTENT_KEYWORDS

        assert isinstance(INTENT_KEYWORDS, dict)
        assert len(INTENT_KEYWORDS) == 6
        assert 'analyze' in INTENT_KEYWORDS
        assert 'report' in INTENT_KEYWORDS
        assert 'ppt' in INTENT_KEYWORDS
        assert 'excel' in INTENT_KEYWORDS
        assert 'advertising' in INTENT_KEYWORDS
        assert 'quick' in INTENT_KEYWORDS

    def test_analyze_keywords(self):
        """UX-01: Verify 'analyze' intent has Chinese and English keywords."""
        from src.workflow.intent_detector import INTENT_KEYWORDS

        analyze_keywords = INTENT_KEYWORDS['analyze']

        assert isinstance(analyze_keywords, list)
        assert len(analyze_keywords) >= 4
        # Check for Chinese keywords
        assert any('分析' in kw for kw in analyze_keywords)
        # Check for English keywords
        assert any('analyze' in kw.lower() for kw in analyze_keywords)