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

## License

MIT