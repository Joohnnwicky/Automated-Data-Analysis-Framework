---
last_mapped_commit: not a git repo
mapped_at: 2026-06-03
focus: tech
---

# External Integrations

## APIs & Services

### CDN Libraries (Browser-side)

| Service | Usage | Files |
|---------|-------|-------|
| jsDelivr CDN | Chart.js, pandas-js loading | `statistical_report.html` and other HTML reports |
| Chart.js CDN | Interactive charts | All HTML reports |

**CDN URLs used:**
- `https://cdn.jsdelivr.net/npm/chart.js`
- `https://cdn.jsdelivr.net/npm/pandas-js@0.2.4/dist/pandas.min.js`

### Browser Automation

| Service | Purpose | Files |
|---------|---------|-------|
| Chromium (via Playwright) | HTML-to-PPTX rendering | `scripts/html2pptx.js` |
| Chrome (macOS channel) | Alternative browser | `scripts/html2pptx.js` (platform detection) |

**No external API calls** - All processing is local.

## Data Sources

### Input Data Files

| Type | Files | Purpose |
|------|-------|---------|
| CSV | `(sample)sam_tianchi_mum_baby_trade_history.csv` | Tmall mother-infant transaction history (external download) |
| CSV | `data_preview.csv`, `matched_positions.csv`, `matched_summary.csv`, `matched_final.csv`, `final_matched.csv` | Civil service recruitment analysis |
| Excel | `1.石家庄市2026年事业单位公开招聘...xlsx` | Civil service job position data |
| JSON | `data_info.json`, `matched_final.json`, `final_matched.json` | Structured analysis results |
| CSV (Kaggle) | `01 Titanic/input/train.csv`, `test.csv`, `gender_submission.csv` | Titanic ML dataset |

### Data File Schemas

**Transaction data (Tmall):**
- `user_id` (int64) - User identifier
- `auction_id` (int64) - Product identifier
- `buy_mount` (int64) - Purchase quantity
- `day` (YYYYMMDD format) - Transaction date
- `cat_id` (int64) - Secondary category
- `cat1` (int64) - Primary category

**Recruitment data (JSON structure from `matched_final.json`):**
```json
{
  "主管部门": "string",
  "单位名称": "string",
  "招聘岗位": "string",
  "学历条件": "string",
  "所学专业条件": "string",
  "其他条件": "string",
  "招聘人数": "integer"
}
```

### External Data Downloads

Scripts reference external paths (not included in repo):
- `C:\Users\hello\Downloads\(sample)sam_tianchi_mum_baby_trade_history.csv`

## Authentication

**No authentication system** - All scripts run locally without auth.

- No OAuth/API keys
- No database credentials
- No session management

## Webhooks & Events

**No webhook integrations** - Standalone local processing.

## Output Destinations

### Generated Reports

| Format | Files | Purpose |
|--------|-------|---------|
| HTML | `statistical_report.html`, `天猫母婴交易分析报告.html`, `母婴消费行为心理学分析报告.html`, `石家庄事业单位招聘报考指导.html` | Visual analysis reports with charts |
| JSON | `analysis_result.json` (external path `J:\数据分析\`) | Structured analysis output |
| PPTX | Generated via `build_pptx.js` | PowerPoint presentations from HTML slides |

### Output Paths

**Internal (repo):**
- HTML reports: Project root
- JSON data: Project root

**External (hardcoded):**
- `J:\数据分析\analysis_result.json` (from `analyze_data.py`)

### HTML Report Features

Reports include:
- Embedded Chart.js visualizations
- Responsive grid layouts (3-column metric grids)
- Styled tables with zebra striping
- Financial Times-inspired design (salmon pink #C85A50 accent)

## File Format Capabilities

### Read Support

| Format | Tool | Script |
|--------|------|--------|
| Excel (.xlsx/.xls) | pandas + openpyxl | `scripts/read_excel.py` |
| PowerPoint (.pptx) | python-pptx | `scripts/read_pptx.py` |
| CSV | pandas | All analysis scripts |
| JSON | json (stdlib) | All scripts |

### Write Support

| Format | Tool | Script |
|--------|------|--------|
| PowerPoint (.pptx) | pptxgenjs | `scripts/build_pptx.js`, `scripts/html2pptx.js` |
| HTML | Direct generation | Analysis scripts (via print/output) |
| JSON | json.dump() | `analyze_data.py`, `data_overview.py` |
| CSV | pandas.to_csv() | Analysis scripts |

## Skill Integration

### huashu-data-pro Skill

Extracted skill provides:
- Multi-expert analysis workflow (Phase 1-4)
- 11 report style presets (Financial Times, McKinsey, Fathom, etc.)
- PPT conversion with placeholder support
- Reference documentation in `references/`:
  - `report-style-gallery.md` - 11 style presets with color palettes
  - `visual-design-system.md` - PPT design system
  - `html-templates.md` - HTML component library
  - `workflows.md` - Detailed execution workflows
  - `ad-analytics.md` - Advertising analysis domain knowledge

---

*Integration audit: 2026-06-03*