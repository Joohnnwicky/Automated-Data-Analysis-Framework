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


# Theme classification keywords (REP-05)
_THEME_KEYWORDS = {
    '财务健康度': ['FCF', '现金流', '财务比率', 'CapEx', '负债', 'ROI', '利润', '营收', '财务'],
    '增长趋势': ['增长', '趋势', '同比', '环比', '预测', 'growth', 'improved', 'increased', '上升'],
    '风险指标': ['风险', '异常', '波动', '损失', '下降', 'risk', 'declined', 'decreased', '波动率'],
    '运营效率': ['效率', '转化', '留存', 'ROI', '成本', '效率', 'efficiency', 'conversion', '成本'],
    '市场表现': ['市场份额', '竞争', '行业', '对标', '定位', 'market', 'share', 'competitive', '市场']
}


def organize_by_theme(findings: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group findings by business theme (not by expert).

    REP-05: Organizes findings into 5 theme categories based on keyword
    classification. Each finding can appear in multiple themes if it
    contains keywords from multiple categories.

    Args:
        findings: List of finding dicts from parse_expert_files.

    Returns:
        Dict mapping theme name to list of findings.

    Note:
        Findings without matching keywords go to '综合分析' bucket.
    """
    themes = {
        '财务健康度': [],
        '增长趋势': [],
        '风险指标': [],
        '运营效率': [],
        '市场表现': [],
        '综合分析': []  # Fallback for unclassified findings
    }

    for finding in findings:
        # Extract text content for classification
        content_text = _get_finding_content(finding)

        # Classify by keyword matches
        matched_themes = set()
        for theme, keywords in _THEME_KEYWORDS.items():
            if theme == '综合分析':
                continue
            for keyword in keywords:
                if keyword.lower() in content_text.lower():
                    matched_themes.add(theme)
                    break

        # Add finding to matched themes (can be multiple)
        if matched_themes:
            for theme in matched_themes:
                themes[theme].append(finding)
        else:
            themes['综合分析'].append(finding)

    # Remove empty themes (except keep all 5 expected)
    # Keep the 5 expected themes even if empty
    final_themes = {}
    for theme in ['财务健康度', '增长趋势', '风险指标', '运营效率', '市场表现']:
        final_themes[theme] = themes[theme]

    return final_themes


def _get_finding_content(finding: Dict[str, Any]) -> str:
    """Extract all text content from a finding dict.

    Combines metric contexts and recommendations for classification.

    Args:
        finding: Finding dict with 'metrics' and 'recommendations'.

    Returns:
        Combined text string for keyword matching.
    """
    parts = []

    # Add metric contexts
    for metric in finding.get('metrics', []):
        if 'context' in metric:
            parts.append(metric['context'])

    # Add recommendations
    for rec in finding.get('recommendations', []):
        parts.append(rec)

    # Add source file name for classification hints
    parts.append(finding.get('source_file', ''))

    return ' '.join(parts)


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