---
last_mapped_commit: not a git repo
mapped_at: 2026-06-03
focus: tech
---

# Technology Stack

## Languages & Runtime

**Primary:**
- Python 3.14.3 - Data analysis scripts, Excel/PPTX reading utilities
- JavaScript (Node.js v25.6.1) - HTML-to-PPTX conversion engine

**Secondary:**
- HTML/CSS - Report output format with embedded JavaScript charts
- JSON - Data interchange format for analysis results and matched records

## Frameworks & Libraries

### Python Data Science Stack

| Library | Purpose | Files Using It |
|---------|---------|---------------|
| pandas | DataFrame operations, CSV/Excel I/O | `analyze_data.py`, `behavior_analysis.py`, `data_overview.py`, `statistical_analysis.py`, `母婴消费分析.py`, `scripts/read_excel.py`, `scripts/read_pptx.py` |
| numpy | Numerical computations, array operations | `analyze_data.py`, `behavior_analysis.py`, `statistical_analysis.py`, `母婴消费分析.py` |
| scipy.stats | Statistical tests (ANOVA, linregress, KS test) | `analyze_data.py`, `statistical_analysis.py` |
| openpyxl | Excel file reading | `scripts/read_excel.py` |
| python-pptx | PowerPoint file structure reading | `scripts/read_pptx.py` |
| json (stdlib) | JSON serialization | `analyze_data.py`, `data_overview.py` |
| warnings (stdlib) | Suppress warnings | All analysis scripts |

### JavaScript/Node.js Stack

| Library | Purpose | Files Using It |
|---------|---------|---------------|
| pptxgenjs | PowerPoint generation | `scripts/html2pptx.js`, `scripts/build_pptx.js` |
| playwright (Chromium) | HTML rendering for PPTX conversion | `scripts/html2pptx.js` |
| sharp | Image processing | `scripts/html2pptx.js` |

### HTML Report Libraries (CDN)

| Library | Purpose |
|---------|---------|
| Chart.js | Interactive charts in HTML reports |
| pandas-js | Client-side DataFrame operations (experimental) |

## Dependencies

### Package Managers

- **Python**: pip (no requirements.txt present - dependencies installed ad-hoc)
- **Node.js**: npm (no package.json present - dependencies installed ad-hoc)

### Dependency Installation Patterns

Scripts check dependencies at runtime and prompt for installation:

```python
# Pattern from scripts/read_excel.py and scripts/read_pptx.py
def ensure_dependencies():
    missing = []
    try:
        import pandas
    except ImportError:
        missing.append('pandas')
    if missing:
        print(f"缺少依赖: {', '.join(missing)}", file=sys.stderr)
        print(f"请运行: pip install {' '.join(missing)}", file=sys.stderr)
        sys.exit(1)
```

```javascript
// Pattern from scripts/build_pptx.js
function checkDependencies() {
  const missing = [];
  for (const dep of ['pptxgenjs', 'playwright', 'sharp']) {
    try {
      require.resolve(dep);
    } catch {
      missing.push(dep);
    }
  }
  if (missing.length > 0) {
    console.error(`缺少依赖: ${missing.join(', ')}`);
    console.error(`请运行: npm install ${missing.join(' ')}`);
    process.exit(1);
  }
}
```

## Configuration

### Environment Configuration

- **No `.env` files** - All paths are hardcoded in scripts
- **No `.nvmrc` or `.python-version`** - Uses system defaults
- **Windows-specific paths** - Scripts use Windows absolute paths (e.g., `C:\Users\hello\Downloads\...`, `J:\数据分析\...`)

### Data Input Paths

Hardcoded in analysis scripts:
- `analyze_data.py`: `C:\Users\hello\Downloads\(sample)sam_tianchi_mum_baby_trade_history.csv`
- Output: `J:\数据分析\analysis_result.json`

### HTML Report Design Contract

All HTML reports must follow base layout (from `huashu-data-pro` skill):

```css
html { background: [与body背景色一致]; }
body {
  max-width: 1200px;
  margin: 0 auto;        /* 水平居中 */
  padding: 40px 48px;    /* 内容呼吸空间 */
}
```

### PPTX Slide Dimensions

HTML slides for PPTX conversion must use:
- `width: 720pt; height: 405pt` (16:9 ratio)
- Match `pptx.layout = 'LAYOUT_16x9'`

## Build & Tooling

### Script Execution

**Python analysis scripts:**
```bash
python analyze_data.py          # Statistical analysis with JSON output
python behavior_analysis.py     # Consumer psychology analysis
python data_overview.py         # Quick data summary
python statistical_analysis.py  # Full statistical report
python 母婴消费分析.py          # Mother-infant consumption analysis
```

**Skill utility scripts:**
```bash
python scripts/read_excel.py data.xlsx --summary    # Excel overview
python scripts/read_excel.py data.xlsx --format csv # CSV output
python scripts/read_pptx.py presentation.pptx       # PPTX structure
python scripts/read_pptx.py presentation.pptx --inventory
```

**PPTX generation:**
```bash
node scripts/build_pptx.js --slides slide1.html slide2.html --output report.pptx
node scripts/build_pptx.js --dir ./slides/ --output report.pptx
node scripts/build_pptx.js --slides slide1.html --output report.pptx --chart 0:bar:data.json
```

### HTML Report Generation

Reports are generated directly by Python scripts with embedded Chart.js:
- `statistical_report.html` - Generated from `statistical_analysis.py` output
- `天猫母婴交易分析报告.html` - Tmall mother-infant transaction analysis
- `母婴消费行为心理学分析报告.html` - Consumer psychology analysis
- `石家庄事业单位招聘报考指导.html` - Civil service recruitment guide

### Jupyter Notebook

- `01 Titanic/titanic.ipynb` - Kaggle Titanic dataset exploration
- Uses sklearn for ML models (pandas, numpy, matplotlib, seaborn)

---

*Stack analysis: 2026-06-03*