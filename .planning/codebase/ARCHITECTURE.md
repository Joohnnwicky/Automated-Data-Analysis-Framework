---
last_mapped_commit: not a git repo
mapped_at: 2026-06-03
focus: arch
---

# Architecture Overview

## Architectural Pattern

**Script-based data analysis pipeline** with multi-expert methodology integration.

This project follows a **pipeline of standalone analysis scripts** pattern rather than a monolithic application. Each Python script performs a specific analysis type, reads from external data sources, and outputs results in multiple formats (HTML reports, JSON, CSV).

The `huashu-data-pro` skill provides a sophisticated multi-expert analysis workflow methodology that guides how analyses should be structured and presented.

## System Layers

```text
┌─────────────────────────────────────────────────────────────────┐
│                     Analysis Scripts Layer                       │
│  `analyze_data.py`  `behavior_analysis.py`  `statistical_analysis.py` │
│  `data_overview.py`  `母婴消费分析.py`                              │
│                                                                  │
│  Each script: Independent analysis workflow                      │
│  - Reads raw data from external paths                           │
│  - Performs domain-specific analysis                            │
│  - Outputs HTML reports + JSON/CSV results                      │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Skill/Methodology Layer                      │
│  `huashu-data-pro-extracted/huashu-data-pro/`                   │
│                                                                  │
│  - SKILL.md: Multi-expert analysis framework                    │
│  - references/: Design systems, style galleries, workflows      │
│  - scripts/: Utility scripts (read_excel.py, read_pptx.py)      │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Data Layer                                   │
│  External CSV/Excel sources (Downloads folder)                  │
│  Local data files:                                               │
│  - `*.json`: Processed/matched data outputs                     │
│  - `*.csv`: Intermediate analysis results                       │
│  - `*.xlsx`: Source Excel files (job recruitment data)          │
│  - `01 Titanic/input/`: Kaggle-style ML datasets                │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Output Layer                                 │
│  HTML reports: `*.html` (statistical_report.html, etc.)         │
│  JSON results: `analysis_result.json` (external path)           │
│  CSV exports: `matched_final.csv`, `final_matched.csv`          │
└─────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| Statistical Analysis | Data quality assessment, outlier detection, distribution analysis, time series analysis | `statistical_analysis.py` |
| Behavior Analysis | Behavioral economics perspective (Kahneman framework), FOMO effect, consumer psychology | `behavior_analysis.py` |
| Data Overview | Quick data summary, JSON output for key metrics | `data_overview.py` |
| Comprehensive Analysis | Full pipeline: data understanding → quality → outliers → distribution → time series → JSON output | `analyze_data.py` |
| Mother-Baby Consumption | Domain-specific analysis: consumption cycles, stock-up behavior, category preferences, seasonal patterns, consumer profiling | `母婴消费分析.py` |
| Skill Framework | Multi-expert analysis methodology, HTML/PPT design guidelines, report styling | `huashu-data-pro/SKILL.md` |
| Excel Reader | Parse Excel files, output markdown/csv/json summaries | `huashu-data-pro/scripts/read_excel.py` |
| PPTX Reader | Parse PowerPoint files, extract structure and content | `huashu-data-pro/scripts/read_pptx.py` |

## Data Flow

### Primary Analysis Path (Baby/Mother Products Data)

1. **Data Ingestion** — Load CSV from external path (`C:\Users\hello\Downloads\...`) (`analyze_data.py:15`, `behavior_analysis.py:15`)
2. **Data Quality Assessment** — Check missing values, duplicates, format consistency (`statistical_analysis.py:20-87`)
3. **Outlier Detection** — IQR method, extreme value thresholds (`statistical_analysis.py:90-158`)
4. **Distribution Analysis** — Power-law testing, user frequency, category HHI index (`statistical_analysis.py:161-244`)
5. **Time Series Analysis** — Monthly trends, trend significance, periodicity ANOVA (`statistical_analysis.py:247-345`)
6. **Output Generation** — Print to console + save JSON (`analyze_data.py:401-407`)

### Job Recruitment Data Flow

1. **Excel Input** — Read `石家庄市2026年事业单位公开招聘...xlsx` via script or pandas
2. **Matching/Processing** — Generate matched JSON/CSV files (`matched_final.json`, `final_matched.json`)
3. **HTML Report Output** — Generate guidance report (`石家庄事业单位招聘报考指导.html`)

### Multi-Expert Analysis Workflow (from SKILL.md)

```
Phase 1: Data Understanding     → Read data, output overview, identify fields and patterns
Phase 2: Expert Selection       → Choose 3-5 domain experts based on data characteristics
Phase 3: Parallel Analysis      → Each expert runs independent analysis (subagent architecture)
Phase 4: Unified Presentation   → Combine all insights into HTML report (no expert names visible)
```

## Key Abstractions

**Analysis Script Pattern:**
- Purpose: Each script encapsulates a complete analysis workflow
- Structure: Load data → Process → Print results → Save outputs
- Example files: `analyze_data.py`, `statistical_analysis.py`, `母婴消费分析.py`

**Multi-Expert Framework (huashu-data-pro):**
- Purpose: Domain-specific deep analysis with multiple perspectives
- Examples: McKinsey strategy analyst, Kahneman behavioral economist, Fathom statistical analyst
- Pattern: Defined in `huashu-data-pro/SKILL.md`, roles documented in `expert_roles.md`, `.planning/expert-roles-trade-history.md`

**Report Style System:**
- Purpose: Consistent visual design for HTML/PPT outputs
- Styles: Financial Times, McKinsey, Economist, Goldman Sachs, Swiss/NZZ + 6 design styles
- Reference: `huashu-data-pro/references/report-style-gallery.md`

## Entry Points

**Script Execution:**
- Location: Root directory `./*.py` files
- Triggers: Manual execution via `python <script_name>.py`
- Responsibilities: Complete end-to-end analysis for specific data source

**Skill Activation:**
- Location: `huashu-data-pro/SKILL.md`
- Triggers: User mentions keywords: "分析数据", "做报告", "做PPT", "Excel", "投放分析", "ROI"
- Responsibilities: Provides methodology, design guidelines, and utility scripts

**Jupyter Notebook:**
- Location: `01 Titanic/titanic.ipynb`
- Triggers: Open in Jupyter environment
- Responsibilities: Interactive ML analysis for Titanic dataset

## Architectural Constraints

- **Data Path Dependency**: Scripts reference hardcoded external paths (`C:\Users\hello\Downloads\...`) — requires modification for portability
- **No Package Management**: No `requirements.txt` or `pyproject.toml` — dependencies (pandas, numpy, scipy) assumed pre-installed
- **Single-threaded Execution**: Each script runs sequentially; no parallel processing within scripts
- **Output Path Variability**: JSON output path in `analyze_data.py` points to `J:\数据分析\` (different from project root)
- **Skill as Extracted Archive**: `huashu-data-pro-extracted/` is an extracted ZIP, includes macOS artifact folder (`__MACOSX/`)

## Anti-Patterns

### Hardcoded External Data Paths

**What happens:** All Python scripts load data from hardcoded Windows paths like `C:\Users\hello\Downloads\...`
**Why it's wrong:** Scripts fail on other machines; requires manual path editing
**Do this instead:** Use relative paths or command-line arguments: `python analyze_data.py --input data.csv`

### No Dependency Specification

**What happens:** No `requirements.txt` exists; scripts assume pandas, numpy, scipy, openpyxl are installed
**Why it's wrong:** New users cannot reproduce environment; dependency conflicts possible
**Do this instead:** Create `requirements.txt`:
```
pandas>=1.0
numpy>=1.18
scipy>=1.4
openpyxl>=3.0
python-pptx>=0.6
```

### Mixed Output Locations

**What happens:** `analyze_data.py` outputs JSON to `J:\数据分析\` while other outputs stay in project root
**Why it's wrong:** Results scattered across filesystem; hard to locate outputs
**Do this instead:** All outputs should go to `output/` subdirectory within project

## Error Handling

**Strategy:** Minimal error handling; warnings suppressed

**Patterns:**
- `warnings.filterwarnings('ignore')` in all analysis scripts — suppresses pandas/numpy warnings
- No try-except blocks for file operations — assumes files exist
- Direct `pd.read_csv()` without fallback — script exits on file error

## Cross-Cutting Concerns

**Logging:** Console print statements with formatted headers (`"=" * 60` separators)

**Validation:** Manual format checks (e.g., `df['day'].astype(str).str.match(r'^\d{8}$')`)

**Authentication:** None required — all data is local/static

**Internationalization:** Mixed Chinese/English — Chinese for reports/analysis, English for code/comments

---

*Architecture analysis: 2026-06-03*