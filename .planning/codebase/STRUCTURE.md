---
last_mapped_commit: not a git repo
mapped_at: 2026-06-03
focus: arch
---

# Directory Structure

## Layout Overview

```
J:\dataanalyst/
├── .claude/                     # Claude local settings
├── .planning/                   # Planning and analysis artifacts
│   ├── codebase/                # Codebase mapping documents (this folder)
│   └── expert-roles-trade-history.md  # Expert role selection for analysis
├── 01 Titanic/                  # Titanic ML project (Kaggle-style)
│   ├── input/                   # Source datasets (train.csv, test.csv)
│   ├── output/                  # Output directory (empty or unused)
│   ├── titanic.ipynb            # Jupyter notebook analysis
│   └── submission.csv           # Kaggle submission file
├── huashu-data-pro-extracted/   # Extracted skill archive
│   ├── huashu-data-pro/         # Main skill folder
│   │   ├── SKILL.md             # Skill definition and methodology
│   │   ├── scripts/             # Utility scripts
│   │   └── references/          # Design and workflow references
│   └── __MACOSX/                # macOS archive artifact (ignore)
├── *.py                         # Analysis scripts (5 files)
├── *.html                       # Generated reports (4 files)
├── *.json                       # Data files (3 files)
├── *.csv                        # Intermediate/export data (5 files)
├── *.xlsx                       # Source Excel data (1 file)
├── *.zip                        # Skill archive (1 file)
└── expert_roles.md              # Expert selection documentation
```

## Key Locations

**Entry Points:**
- `analyze_data.py`: Full statistical analysis pipeline for baby/mother products data
- `behavior_analysis.py`: Behavioral economics analysis (Kahneman framework)
- `母婴消费分析.py`: Domain-specific mother-baby consumption analysis
- `01 Titanic/titanic.ipynb`: Interactive ML notebook

**Configuration:**
- `.claude/settings.local.json`: Claude local configuration
- `huashu-data-pro/SKILL.md`: Skill methodology and design guidelines

**Core Logic:**
- `statistical_analysis.py`: Data quality, outliers, distributions, time series
- `data_overview.py`: Quick JSON-based data summary

**Data Files:**
- `data_info.json`: Metadata about Excel source (shape, columns)
- `matched_final.json`: Job recruitment matched results (first version)
- `final_matched.json`: Job recruitment matched results (final version)
- `*.csv`: Exported matched data, preview data
- `石家庄市2026年事业单位公开招聘...xlsx`: Source Excel for job recruitment

**Generated Reports:**
- `statistical_report.html`: Statistical analysis HTML report
- `天猫母婴交易分析报告.html`: Baby/mother products analysis report
- `母婴消费行为心理学分析报告.html`: Behavioral psychology analysis report
- `石家庄事业单位招聘报考指导.html`: Job recruitment guidance report

**Skill Resources:**
- `huashu-data-pro/references/report-style-gallery.md`: 11 report style definitions
- `huashu-data-pro/references/visual-design-system.md`: PPT visual design parameters
- `huashu-data-pro/references/workflows.md`: Detailed workflow specifications
- `huashu-data-pro/references/ad-analytics.md`: Advertising analytics domain knowledge
- `huashu-data-pro/references/html-templates.md`: HTML visualization components

**Utility Scripts (in skill):**
- `huashu-data-pro/scripts/read_excel.py`: Excel file parser
- `huashu-data-pro/scripts/read_pptx.py`: PowerPoint file parser
- `huashu-data-pro/scripts/html2pptx.js`: HTML to PPTX converter
- `huashu-data-pro/scripts/build_pptx.js`: Multi-page HTML to single PPTX

## Naming Conventions

**Files:**
- Python scripts: Snake case (`analyze_data.py`, `behavior_analysis.py`)
- Chinese scripts: Mixed Chinese/English (`母婴消费分析.py`)
- JSON/CSV: Descriptive names (`matched_final.json`, `data_preview.csv`)
- Excel: Long descriptive Chinese names with date stamps (`石家庄市2026年事业单位公开招聘...xlsx`)
- HTML reports: Chinese descriptive (`天猫母婴交易分析报告.html`, `母婴消费行为心理学分析报告.html`)
- Skill archive: Hashed filename (`huashu-data-pro-392180986bf0238616fd1839e6781e05.zip`)

**Directories:**
- Numbered projects: `01 Titanic/` (Kaggle-style naming)
- Extracted archives: `<name>-extracted/` pattern
- Skill folder: Lowercase with hyphen (`huashu-data-pro/`)
- Hidden folders: `.claude/`, `.planning/` (dot prefix)

**Functions/Variables (in code):**
- Snake case for functions and variables (Python convention)
- Chinese variable names in some scripts (e.g., `buy_dist`, `monthly_sales`)
- JSON keys: Chinese (`"总记录数"`, `"缺失比例"`)

## File Categories

**Analysis Scripts (`*.py`):**
- Location: Root directory
- Purpose: Data processing, statistical analysis, report generation
- Dependencies: pandas, numpy, scipy, json, warnings

**Generated Reports (`*.html`):**
- Location: Root directory
- Purpose: Human-readable analysis outputs
- Style: Based on huashu-data-pro report style gallery

**Data Outputs (`*.json`, `*.csv`):**
- Location: Root directory
- Purpose: Machine-readable results, intermediate data
- Format: JSON with Chinese keys, CSV with UTF-8 encoding

**Source Data (`*.xlsx`, `*.csv` in input/):**
- Location: Root (`*.xlsx`) or `01 Titanic/input/` (`*.csv`)
- Purpose: Raw analysis inputs

**Skill Resources (`huashu-data-pro/`):**
- Location: `huashu-data-pro-extracted/huashu-data-pro/`
- Purpose: Methodology, design guidelines, utility scripts

## Where to Add New Code

**New Analysis Script:**
- Primary location: Root directory (`J:\dataanalyst\`)
- Naming: `<purpose>_analysis.py` or Chinese `XX分析.py`
- Template: Follow `analyze_data.py` structure (load → process → output)

**New Project Folder:**
- Location: Root directory
- Naming: Numbered sequence (`02 <project_name>/`)
- Structure: `input/`, `output/`, `<project>.ipynb` or `*.py`

**New Utility Script:**
- For data analysis: Add to root directory
- For skill integration: Add to `huashu-data-pro/scripts/`

**New Data File:**
- Source data: Root directory or `<project>/input/`
- Output data: Root directory (current pattern) or `<project>/output/` (better organization)

**New Report:**
- HTML output: Root directory (current pattern)
- Consider: Creating `reports/` subdirectory for better organization

**Expert Role Definitions:**
- Location: `.planning/` directory
- Naming: `expert-roles-<topic>.md`

## Special Directories

**`.planning/`:**
- Purpose: Planning artifacts, expert role definitions, codebase maps
- Generated: Yes (by GSD workflows)
- Committed: Should be committed for project continuity
- Contains: `expert-roles-trade-history.md`, `codebase/`

**`huashu-data-pro-extracted/__MACOSX/`:**
- Purpose: macOS archive metadata (artifact from ZIP extraction)
- Generated: Yes (ZIP extraction on macOS)
- Committed: Should NOT be committed (add to `.gitignore`)
- Action: Can be deleted safely

**`01 Titanic/output/`:**
- Purpose: Intended for Titanic analysis outputs
- Generated: Yes
- Committed: Empty or unused
- Action: Use for organizing Titanic-specific outputs

## Organization Patterns

**Analysis Project Pattern:**
- Each analysis project is self-contained
- Scripts are standalone, not modules
- Data flows through scripts: Input (external) → Process → Output (local)

**Skill Integration Pattern:**
- Skill extracted to `*-extracted/` folder
- SKILL.md provides methodology, not executable code
- Scripts in skill are utilities, not core analysis logic

**Output Organization (Current):**
- All outputs in root directory (flat structure)
- HTML, JSON, CSV mixed with source files
- Consider: Organizing by type (`reports/`, `data/`, `scripts/`)

---

*Structure analysis: 2026-06-03*