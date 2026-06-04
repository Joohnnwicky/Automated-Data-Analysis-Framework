"""Synthesis engine for manager-POV narrative generation.

Transforms multi-expert analysis into cohesive executive-ready narrative.
Implements REP-05 and REP-06 requirements.

Threat Model:
- T-4-02: Use markdown library + BeautifulSoup(html, 'html.parser') for sanitization
- T-4-06: generate_manager_pov_synthesis removes expert attribution patterns
"""

import re
import logging
from pathlib import Path
from typing import List, Dict, Any

import markdown
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def parse_expert_files(expert_outputs_dir: Path) -> List[Dict[str, Any]]:
    """Parse expert markdown files and extract findings.

    REP-05: Reads expert output files from Phase 3, extracts metrics
    and recommendations for synthesis.

    Args:
        expert_outputs_dir: Path to directory containing expert .md files.

    Returns:
        List of dicts with 'source_file', 'metrics', 'recommendations' keys.

    Threat Mitigation:
        - T-4-02: BeautifulSoup(html, 'html.parser') sanitizes parsed HTML
    """
    findings = []

    # Glob *.md files, skip roles.md (role definitions, not analysis)
    for md_file in expert_outputs_dir.glob('*.md'):
        if md_file.name == 'roles.md':
            continue

        content = md_file.read_text(encoding='utf-8')

        # Parse markdown to HTML
        html = markdown.markdown(content)

        # Parse HTML with BeautifulSoup (T-4-02: sanitization)
        soup = BeautifulSoup(html, 'html.parser')

        # Extract metrics: numbers with %, $, or unit patterns
        metrics = _extract_metrics(soup, content)

        # Extract recommendations: list items, action keywords
        recommendations = _extract_recommendations(soup)

        findings.append({
            'source_file': md_file.name,
            'metrics': metrics,
            'recommendations': recommendations
        })

        logger.debug(f"Parsed {md_file.name}: {len(metrics)} metrics, {len(recommendations)} recommendations")

    return findings


def _extract_metrics(soup: BeautifulSoup, raw_content: str) -> List[Dict[str, Any]]:
    """Extract numerical metrics from parsed content.

    Finds numbers with:
    - Percentage patterns: 15%, 12.5%
    - Currency patterns: $1.2M, $500K
    - Unit patterns: 100k, 2.5M

    Args:
        soup: BeautifulSoup parsed HTML.
        raw_content: Raw markdown content for regex matching.

    Returns:
        List of metric dicts with 'value', 'unit', 'context' keys.
    """
    metrics = []

    # Regex patterns for metric extraction
    patterns = [
        # Percentage: 15%, 12.5%
        r'(\d+\.?\d*)%',
        # Currency: $1.2M, $500K, $1,200
        r'\$(\d+\.?\d*[KMB]?)',
        r'\$([\d,]+)',
        # Unit suffix: 100k, 2.5M
        r'(\d+\.?\d*)[KMB]',
    ]

    text = soup.get_text()

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            # Clean up match
            value = match.replace(',', '') if isinstance(match, str) else match

            # Find context (surrounding words)
            context_match = re.search(
                rf'([^\n]*{re.escape(match)}[^\n]*)',
                raw_content,
                re.IGNORECASE
            )
            context = context_match.group(1).strip() if context_match else match

            metrics.append({
                'value': value,
                'unit': _infer_unit(match, pattern),
                'context': context
            })

    return metrics


def _infer_unit(match: str, pattern: str) -> str:
    """Infer unit type from match and pattern.

    Args:
        match: The matched string.
        pattern: The regex pattern used.

    Returns:
        Unit string: 'percent', 'currency', or 'count'.
    """
    if '%' in pattern:
        return 'percent'
    if '$' in pattern:
        return 'currency'
    if any(suffix in pattern.lower() for suffix in ['k', 'm', 'b']):
        return 'count'
    return 'unknown'


def _extract_recommendations(soup: BeautifulSoup) -> List[str]:
    """Extract recommendations from parsed content.

    Finds:
    - List items (<li> elements)
    - Paragraphs with action keywords: increase, decrease, focus, improve

    Args:
        soup: BeautifulSoup parsed HTML.

    Returns:
        List of recommendation strings.
    """
    recommendations = []

    # Extract list items
    for li in soup.find_all('li'):
        text = li.get_text().strip()
        if text:
            recommendations.append(text)

    # Extract paragraphs with action keywords
    action_keywords = [
        'increase', 'decrease', 'focus', 'improve', 'reduce',
        'optimize', 'enhance', '调整', '优化', '提升', '减少', '增加'
    ]

    for p in soup.find_all('p'):
        text = p.get_text().strip()
        if any(kw in text.lower() for kw in action_keywords):
            recommendations.append(text)

    return recommendations