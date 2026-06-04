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


# Significant threshold for conclusion-style titles (REP-05)
_SIGNIFICANT_THRESHOLD = 10  # |change_pct| > 10% considered significant


def generate_conclusion_title(metrics: Dict[str, Dict[str, Any]]) -> str:
    """Generate conclusion-style title from key metrics.

    REP-05: Creates titles like "ROI增长15%, CTR下降3%" instead of
    topic-style titles like "ROI分析报告".

    Args:
        metrics: Dict mapping metric name to dict with 'value' and 'change_pct'.

    Returns:
        Conclusion-style title string, or "数据概览" fallback.

    Note:
        Only metrics with |change_pct| > 10% threshold are included.
        Top 2 significant metrics are used for title.
    """
    significant_metrics = []

    for metric_name, data in metrics.items():
        change_pct = data.get('change_pct', 0)
        if abs(change_pct) > _SIGNIFICANT_THRESHOLD:
            direction = '增长' if change_pct > 0 else '下降'
            significant_metrics.append({
                'name': metric_name,
                'direction': direction,
                'magnitude': abs(change_pct)
            })

    # Sort by magnitude, take top 2
    significant_metrics.sort(key=lambda x: x['magnitude'], reverse=True)
    top_2 = significant_metrics[:2]

    if len(top_2) == 0:
        return "数据概览"  # Fallback

    # Generate conclusion-style title
    title_parts = []
    for m in top_2:
        title_parts.append(f"{m['name']}{m['direction']}{int(m['magnitude'])}%")

    return ', '.join(title_parts)


# Expert attribution patterns to remove (T-4-06 mitigation)
_EXPERT_ATTRIBUTION_PATTERNS = [
    r'分析师认为',
    r'根据.*分析师',
    r'分析师.*建议',
    r'expert.*:',
    r'analyst.*:',
    r'Analyst:',
    r'Expert:',
]


def generate_manager_pov_synthesis(themes: Dict[str, List[Dict[str, Any]]]) -> str:
    """Generate manager-POV synthesis without visible expert names.

    REP-06: Transforms theme-organized findings into cohesive narrative
    without expert attribution. All findings presented as unified
    manager perspective: "数据显示..." instead of "分析师认为...".

    Args:
        themes: Dict mapping theme name to list of findings.

    Returns:
        Complete synthesis markdown string with theme sections.

    Threat Mitigation:
        - T-4-06: Regex removes all expert attribution patterns
    """
    synthesis_lines = []

    for theme_name, findings in themes.items():
        # Add theme section header
        synthesis_lines.append(f"## {theme_name}\n\n")

        # Process each finding
        for finding in findings:
            # Get finding content
            finding_text = _get_finding_content(finding)

            # Remove expert attribution patterns (T-4-06)
            finding_text = _remove_expert_attribution(finding_text)

            # Rewrite as manager-POV statement
            if finding_text:
                # Use "数据显示" prefix for metrics
                metrics_text = _extract_metrics_text(finding)
                if metrics_text:
                    synthesis_lines.append(f"数据显示{metrics_text}\n")

                # Add recommendations as bullet points
                for rec in finding.get('recommendations', []):
                    clean_rec = _remove_expert_attribution(rec)
                    if clean_rec:
                        synthesis_lines.append(f"- {clean_rec}\n")

        synthesis_lines.append("\n")  # Section separator

    return ''.join(synthesis_lines)


def _remove_expert_attribution(text: str) -> str:
    """Remove expert attribution patterns from text.

    T-4-06 mitigation: Strips patterns like "分析师认为", "根据...分析师".

    Args:
        text: Input text with potential expert attribution.

    Returns:
        Cleaned text without expert attribution.
    """
    for pattern in _EXPERT_ATTRIBUTION_PATTERNS:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # Clean up whitespace and awkward phrasing
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'^应该', '', text)  # Remove "应该" prefix after attribution removal

    return text


def _extract_metrics_text(finding: Dict[str, Any]) -> str:
    """Extract metrics as readable text for manager-POV synthesis.

    Args:
        finding: Finding dict with 'metrics' key.

    Returns:
        Concatenated metrics context string.
    """
    metrics = finding.get('metrics', [])
    if not metrics:
        return ''

    parts = []
    for metric in metrics:
        context = metric.get('context', '')
        if context:
            # Clean up context for readability
            clean_context = _remove_expert_attribution(context)
            parts.append(clean_context)

    return ', '.join(parts) if parts else ''


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