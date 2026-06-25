---
name: automated-data-analysis
description: AI-powered data analysis framework with multi-expert analysis and professional report generation
---

# Automated Data Analysis Framework

> Claude Code Skill for AI-powered data analysis and professional report generation.

## What This Skill Does

When you provide a data file (Excel/CSV/JSON), this skill:
1. **Understands your data** — automatic profiling, type detection, encoding detection
2. **Analyzes with multiple expert perspectives** — 6 specialized roles analyze simultaneously
3. **Generates professional reports** — 11 design styles, HTML/PPT output

## Quick Start

### One-Line Install

```bash
npx skills add Joohnnwicky/Automated-Data-Analysis-Framework
```

Or install manually to your skills directory:
- Claude Code: `~/.claude/skills/`
- Cursor: `~/.cursor/skills/`
- Continue: `~/.continue/skills/`

### Usage in Claude Code

Once installed, just describe your analysis need in natural language:

```
> analyze this sales data and find growth trends

> generate a McKinsey-style PPT report

> what's the ROI trend in this advertising data?
```

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│  Phase 1: Business Clarification                        │
│  → Understand your goal, audience, key metrics          │
├─────────────────────────────────────────────────────────┤
│  Phase 2: Data Understanding                            │
│  → Load data, profile dimensions, detect type           │
│  → Initial insights: trends, anomalies                  │
├─────────────────────────────────────────────────────────┤
│  Phase 3: Multi-Expert Analysis                         │
│  → 6 experts analyze in parallel                        │
│  → Detect conflicts, validate conclusions               │
├─────────────────────────────────────────────────────────┤
│  Phase 4: Report Generation                             │
│  → Synthesize expert perspectives                       │
│  → Apply design style, output HTML/PPT                  │
└─────────────────────────────────────────────────────────┘
```

## Expert Roles

| Expert | Domain | Specializes In |
|--------|--------|----------------|
| Quantitative Analyst | Statistics | Distribution, correlation, anomalies |
| Valuation Expert | Finance | FCF, valuation metrics, risk |
| Growth Optimizer | Advertising | ROI, CTR, channel optimization |
| User Growth Expert | Growth | User behavior, funnel analysis |
| Industry Analyst | Strategy | Benchmarking, competitive analysis |
| Financial Analyst | Finance | Financial ratios, health assessment |

## Design Styles

11 professional styles: `ft`, `mckinsey`, `economist`, `goldman`, `swiss`, `wsj`, `bloomberg`, `reuters`, `morningstar`, `bcg`, `bain`

## Requirements

- Python 3.10+
- Supported formats: Excel (.xlsx), CSV, JSON

## User-Confirmed Report Defaults

When the user asks for a professional data-analysis report, apply these defaults unless they explicitly ask otherwise.

### 1. Report framing

- Do **not** assume the report should be a job-application, interview, résumé, JD, target-company, or candidate showcase deliverable.
- Only use recruitment/application language when the user explicitly asks for that framing.
- For government, enterprise, management, client-facing, or general business reports, use a neutral delivery framing such as:
  - analysis report
  - executive summary
  - business/management recommendations
  - project team / data service team
  - follow-up actions and limitations
- Replace “岗位匹配、面试展示、简历项目、目标公司、招聘公司所在地、JD 相关性” with neutral sections such as:
  - Background and report objective
  - Executive summary
  - Data understanding and methodology
  - Overall profile
  - Segmented analysis
  - Trend/comparison analysis
  - Risk/opportunity/priority ranking
  - Recommendations and next steps
  - Method limitations
  - Appendix: data dictionary and output files

### 2. Data workflow

For non-Excel sources or semi-structured files, adapt the workflow before analysis:

1. Extract raw content into UTF-8 intermediate files when console encoding or source formatting is unreliable.
2. Convert semi-structured content into a structured CSV/JSON layer before writing the report.
3. Preserve source traceability fields where possible, such as source file, period, category/section, entity, date, metric name, raw value, normalized value, unit, threshold/target, status flag, and notes.
4. For multi-period data, combine all periods into one consolidated dataset and one stats summary.
5. Make the primary analysis object match the user's request, and use other data sections only as context unless the user asks for equal treatment.

### 3. Derived metrics and interpretation

- Define derived metrics explicitly before using them in conclusions.
- For threshold/target-based analysis, include both absolute values and relative-to-threshold ratios when meaningful.
- Use risk/priority buckets only when the bucket thresholds are stated in the report.
- Disclose any normalization, censoring, missing-value handling, or threshold assumptions that could change interpretation.
- Do not over-claim causality from coverage changes, sample-size changes, or reporting-frequency changes.

### 4. HTML visualization requirement

Do not deliver an HTML report that only contains KPI cards and tables when the data supports charts. Add real visualizations by default.

Use offline inline SVG generated by Python rather than external Chart.js/CDN scripts unless the user explicitly asks for interactive charts. Reasons:

- single-file HTML works offline;
- no network dependency;
- suitable for enterprise archiving and printing;
- avoids browser/CDN/script compatibility issues.

Recommended generic chart set:

1. Composition chart for categories/sections.
2. Bar chart for top entities, regions, products, channels, or other key dimensions.
3. Donut/pie chart for distribution or bucket composition.
4. Trend chart for time-based record counts and key metrics.
5. Scatter plot for relationship/outlier analysis.
6. Heatmap for two-dimensional intersections, such as region × metric, category × period, or entity × indicator.

If the current report generator lacks these chart functions, add simple Python SVG helpers such as:

- `bar_svg(...)`
- `donut_svg(...)`
- `scatter_svg(...)`
- `heatmap_svg(...)`
- `trend_svg(...)`

Keep the Markdown report primarily textual/table-based. Insert the charts directly into the HTML generation stage so SVG is not escaped by a Markdown converter.

### 5. Verification checklist

After generating a professional report, verify:

- output Markdown and HTML files exist;
- HTML contains multiple `<svg` charts when data supports visualization, normally at least 5 for a full analytical report;
- HTML does not depend on `<script`, CDN, or Chart.js unless the user explicitly asks;
- recruitment/application terms are absent unless the user explicitly requested that framing, including `应聘`, `招聘`, `面试`, `简历`, `JD`, `目标公司`, `岗位`;
- key figures in the report match parsed CSV/JSON statistics;
- report language avoids unsupported causal claims;
- important assumptions and data-handling limitations are disclosed.

### 6. Word output

Do not prioritize Word layout work by default. If the user asks for Word output later, generate `.docx` as a separate optional export after the Markdown/HTML analytical report is correct.

## License

MIT