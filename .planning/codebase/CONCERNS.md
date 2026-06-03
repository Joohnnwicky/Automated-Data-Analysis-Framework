---
last_mapped_commit: not a git repo
mapped_at: 2026-06-03
focus: concerns
---

# Technical Concerns

## Technical Debt

**Hardcoded Absolute Paths:**
- Issue: All 5 main analysis scripts contain hardcoded Windows paths pointing to a specific user's Downloads folder
- Files: `analyze_data.py`, `behavior_analysis.py`, `母婴消费分析.py`, `statistical_analysis.py`, `data_overview.py`
- Impact: Scripts will fail on any machine other than the original author's; cannot be shared or run in CI/CD
- Fix approach: Replace hardcoded paths with command-line arguments (`argparse`) or config file (`config.yaml`)

Example pattern found in all scripts:
```python
df = pd.read_csv(r'C:\Users\hello\Downloads\(sample)sam_tianchi_mum_baby_trade_history.csv')
```

Output path also hardcoded in `analyze_data.py`:
```python
with open(r'J:\数据分析\analysis_result.json', 'w', encoding='utf-8') as f:
```

**Duplicate Data Loading Code:**
- Issue: All 5 analysis scripts independently load the same CSV file with identical code
- Files: `analyze_data.py:15`, `behavior_analysis.py:15`, `母婴消费分析.py:8`, `statistical_analysis.py:9`, `data_overview.py:13`
- Impact: Code duplication increases maintenance burden; any change to data loading must be replicated 5 times
- Fix approach: Create shared utility module `src/data_loader.py` with reusable load function

**No Dependency Management:**
- Issue: No `requirements.txt`, `pyproject.toml`, or `setup.py` exists
- Files: Missing from project root
- Impact: New users cannot easily install dependencies; runtime errors due to missing packages
- Fix approach: Create `requirements.txt` with pinned versions:
```
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
openpyxl>=3.1.0
python-pptx>=0.6.21
```

**Global Warning Suppression:**
- Issue: All scripts suppress warnings globally at the top of files
- Files: `analyze_data.py:12`, `behavior_analysis.py:12`, `母婴消费分析.py:5`, `statistical_analysis.py:6`
- Impact: Hides potential issues from pandas/numpy (e.g., deprecated APIs, data quality warnings)
- Fix approach: Use targeted warning suppression only where necessary, or fix underlying issues

**No Modular Architecture:**
- Issue: Each script is a standalone file with no imports between project scripts
- Files: All `.py` files in root
- Impact: No shared utilities; cannot build reusable analysis pipeline
- Fix approach: Refactor into modules: `src/data/`, `src/analysis/`, `src/output/`

## Known Issues

**Missing Output Directory:**
- Issue: `analyze_data.py` writes to `J:\数据分析\` which may not exist
- Files: `analyze_data.py:402-403`
- Trigger: Running script on different machine or fresh environment
- Workaround: Manually create directory before running

**Silent Exception Handling:**
- Issue: `read_pptx.py` has `pass` statement inside exception handler that silently ignores errors
- Files: `huashu-data-pro-extracted\huashu-data-pro\scripts\read_pptx.py:124`
- Trigger: Image extraction failures are not reported to user
- Fix approach: Log the exception or inform user about skipped images

**Broad Exception Catching:**
- Issue: Scripts catch generic `Exception` without specific handling
- Files: `read_excel.py:56`, `read_pptx.py:50`
- Impact: All errors treated uniformly; no differentiation between file-not-found vs parse-error
- Fix approach: Use specific exception types (`FileNotFoundError`, `ValueError`, etc.)

## Security Considerations

**Data Sensitivity:**
- Risk: Analysis scripts process transaction data containing user_ids and auction_ids
- Files: All scripts reference external CSV with transaction records
- Current mitigation: Data file is external to repo (in Downloads folder)
- Recommendations: Document data handling policy; ensure input data files are not accidentally committed

**Job Matching Data Files:**
- Risk: `matched_final.csv`, `matched_positions.csv`, `matched_summary.csv` contain structured job matching data
- Files: `J:\dataanalyst\matched_final.csv`, `J:\dataanalyst\matched_positions.csv`, `J:\dataanalyst\matched_summary.csv`
- Current mitigation: Appears to be public job posting data (石家庄市事业单位公开招聘)
- Recommendations: Review if any personal information is included before sharing repo

**No Secrets Detected:**
- No `.env` files, credentials, API keys, or tokens found in codebase
- No passwords or authentication code present

## Performance Concerns

**Full Dataset Loading Without Chunking:**
- Problem: All scripts load entire CSV into memory without chunking options
- Files: All main analysis scripts
- Cause: `pd.read_csv()` used without `chunksize` parameter
- Impact: Memory pressure with large datasets (>100MB); may crash on constrained systems
- Improvement path: Add chunked reading option for large files; use `pd.read_csv(chunksize=10000)` for iterative processing

**Print-Based Output:**
- Problem: Scripts use extensive `print()` statements throughout for output (200+ print calls)
- Files: `behavior_analysis.py`, `analyze_data.py`, `母婴消费分析.py`, `statistical_analysis.py`
- Cause: No logging framework; output mixed with computation
- Impact: Cannot disable verbose output; slows execution for large datasets due to I/O overhead
- Improvement path: Replace `print()` with `logging` module; add verbosity levels

## Fragile Areas

**Single Point of Failure - Data Source:**
- Files: All 5 main analysis scripts depend on `C:\Users\hello\Downloads\(sample)sam_tianchi_mum_baby_trade_history.csv`
- Why fragile: One missing file breaks all scripts; path is user-specific
- Safe modification: Add argparse to accept file path as argument; validate file existence before processing
- Test coverage: None - scripts have no unit tests

**Exception Handling in Skill Scripts:**
- Files: `huashu-data-pro-extracted\huashu-data-pro\scripts\read_pptx.py:123-124`
- Why fragile: `except Exception: pass` silently swallows all errors during image extraction
- Safe modification: Replace with proper error logging
- Test coverage: No test files in extracted skill directory

**Date Parsing Without Validation:**
- Files: All analysis scripts convert `day` column to datetime without format error handling
- Why fragile: Malformed date strings will crash scripts
- Safe modification: Add `errors='coerce'` parameter to `pd.to_datetime()` and validate results

## Dependencies Risks

**Undeclared Dependencies:**
- pandas - Required for all analysis scripts, version not pinned
- numpy - Required for statistical calculations, version not pinned
- scipy - Required for `stats.linregress()`, `stats.kstest()`, `stats.f_oneway()`
- openpyxl - Required for `read_excel.py` Excel reading
- python-pptx - Required for `read_pptx.py` PowerPoint reading
- Pillow - Optional for thumbnail export in `read_pptx.py`

**Impact if missing:**
- Scripts fail immediately with ImportError
- No version constraints means future updates could break compatibility

**Migration plan:**
- Create `requirements.txt` with minimum versions
- Add dependency check in script entry points (pattern from skill scripts: `ensure_dependencies()`)

## Missing Critical Features

**No Unit Tests:**
- Problem: Zero test files exist in the codebase
- Files: No `test_*.py` or `*_test.py` found
- Blocks: Cannot verify analysis correctness; refactoring is risky

**No Configuration File:**
- Problem: All settings hardcoded in scripts
- Files: No `config.yaml`, `settings.py`, or similar
- Blocks: Cannot easily switch data sources, output paths, or analysis parameters

**No Version Control:**
- Problem: Directory is not a git repository
- Blocks: No history tracking; cannot collaborate; no rollback capability

## Test Coverage Gaps

**Untested Analysis Logic:**
- What's not tested: Statistical calculations, outlier detection, distribution analysis, time series processing
- Files: All analysis scripts - `analyze_data.py`, `statistical_analysis.py`, `behavior_analysis.py`, `母婴消费分析.py`
- Risk: Incorrect calculations go undetected; statistical conclusions may be wrong
- Priority: High - core business logic should have tests

**Untested Utility Scripts:**
- What's not tested: Excel reading, PPTX parsing, error handling paths
- Files: `huashu-data-pro-extracted\huashu-data-pro\scripts\read_excel.py`, `read_pptx.py`
- Risk: File format edge cases cause unexpected failures
- Priority: Medium - utility scripts used occasionally

---

*Concerns audit: 2026-06-03*