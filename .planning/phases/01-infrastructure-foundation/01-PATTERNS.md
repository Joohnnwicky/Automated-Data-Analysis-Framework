# Phase 1: Infrastructure Foundation - Pattern Map

**Mapped:** 2026-06-03
**Files analyzed:** 11 (5 create, 6 modify)
**Analogs found:** 6 / 11

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `requirements.txt` | config | file-I/O | None (greenfield) | no analog |
| `src/config/logging_config.py` | config | request-response | None (greenfield) | no analog |
| `.gitignore` (modify) | config | file-I/O | `.gitignore` (existing) | exact |
| `tests/test_infrastructure.py` | test | file-I/O | None (greenfield) | no analog |
| `tests/conftest.py` | config | file-I/O | None (greenfield) | no analog |
| `pytest.ini` | config | file-I/O | None (greenfield) | no analog |
| `src/analysis/analyze_data.py` | utility | file-I/O | `analyze_data.py` (existing) | exact |
| `src/analysis/behavior_analysis.py` | utility | file-I/O | `behavior_analysis.py` (existing) | exact |
| `src/analysis/statistical_analysis.py` | utility | file-I/O | `statistical_analysis.py` (existing) | exact |
| `src/scripts/read_excel.py` | utility | file-I/O | `huashu-data-pro/scripts/read_excel.py` | exact |
| `src/scripts/read_pptx.py` | utility | file-I/O | `huashu-data-pro/scripts/read_pptx.py` | exact |

## Pattern Assignments

### `requirements.txt` (config, file-I/O)

**Analog:** None - greenfield file

**Pattern from RESEARCH.md** (lines 51-54):
```bash
pip install pandas==3.0.1 numpy==2.4.3 scipy==1.17.1 openpyxl==3.1.5 python-pptx==1.0.2 Pillow==12.1.1
pip freeze > requirements.txt
```

**Generated from pip freeze** (executed 2026-06-03):
```text
pandas==3.0.1
numpy==2.4.3
scipy==1.17.1
openpyxl==3.1.5
python-pptx==1.0.2
Pillow==12.1.1
xlsxwriter==3.2.9
lxml==6.0.4
python-dateutil==2.9.0.post0
tzdata==2025.3
et-xmlfile==2.0.0
typing-extensions==4.15.0
six==1.17.0
```

**Action:** Run `pip freeze > requirements.txt` to capture locked versions with transitive dependencies.

---

### `src/config/logging_config.py` (config, request-response)

**Analog:** None - greenfield file

**Pattern from RESEARCH.md** (lines 185-199):
```python
# src/config/logging_config.py
import logging
import sys
from pathlib import Path

def setup_logging(level=logging.INFO, log_file=None):
    """Configure logging for the project."""
    handlers = [logging.StreamHandler(sys.stdout)]

    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=handlers,
        force=True
    )
```

**Usage pattern from RESEARCH.md** (lines 201-221):
```python
# In application modules:
import logging
from config.logging_config import setup_logging

logger = logging.getLogger(__name__)

def analyze(filepath):
    logger.info(f'Loading dataset from {filepath}')
    try:
        df = pd.read_csv(filepath)
        logger.debug(f'Dataset shape: {df.shape}')
        # ... analysis logic
        logger.info('Analysis complete')
    except Exception as e:
        logger.error(f'Failed to load {filepath}: {e}')
        raise

# Entry point:
if __name__ == '__main__':
    setup_logging(level=logging.INFO, log_file='output/analysis.log')
    analyze(Path('data/sample.csv'))
```

---

### `.gitignore` (modify) (config, file-I/O)

**Analog:** `.gitignore` (existing)

**Current pattern** (lines 1-32):
```gitignore
# Data files (keep analysis outputs, ignore raw data)
*.xlsx
*.csv
*.json
!data_info.json

# Python cache
__pycache__/
*.pyc
*.pyo

# Node.js
node_modules/

# IDE
.vscode/
.idea/

# OS
__MACOSX/
.DS_Store

# Temporary
*.tmp
*.log

# Extracted skill (will be integrated)
huashu-data-pro-extracted/
huashu-data-pro-*.zip

# Claude local settings (keep project settings)
.claude/settings.local.json
```

**Add pattern for Phase 1** (append to existing):
```gitignore
# GSD planning artifacts (Phase 1)
.planning/

# Test artifacts
.pytest_cache/
.coverage
htmlcov/
```

---

### `tests/test_infrastructure.py` (test, file-I/O)

**Analog:** None - greenfield file

**Pattern from RESEARCH.md** (lines 448-452):
```python
# tests/test_infrastructure.py
import pytest
from pathlib import Path

def test_requirements_locked():
    """INF-01: requirements.txt has locked versions"""
    req_file = Path(__file__).parent.parent / 'requirements.txt'
    assert req_file.exists()
    content = req_file.read_text()
    # All dependencies should have == locked versions, not >=
    assert '==' in content
    assert '>=' not in content

def test_paths_cross_platform():
    """INF-02: pathlib replaces hardcoded Windows paths"""
    # Check that analysis scripts use pathlib, not hardcoded C:\ paths
    analysis_dir = Path(__file__).parent.parent / 'src' / 'analysis'
    for py_file in analysis_dir.glob('*.py'):
        content = py_file.read_text()
        # Should not contain hardcoded Windows paths
        assert r'C:\Users' not in content
        assert r'C:\\Users' not in content
        # Should use pathlib
        assert 'from pathlib import Path' in content or 'Path(' in content

def test_logging_levels():
    """INF-03: logging replaces print statements"""
    analysis_dir = Path(__file__).parent.parent / 'src' / 'analysis'
    for py_file in analysis_dir.glob('*.py'):
        content = py_file.read_text()
        # Should import logging
        assert 'import logging' in content
        # Should have logger instance
        assert 'logger = logging.getLogger(__name__)' in content
        # Should not use print() (except in scripts/read_*.py CLI output)
        if 'scripts' not in str(py_file):
            print_count = content.count('print(')
            # Allow minimal print usage, but prefer logging
            assert print_count < 5, f"Too many print() in {py_file.name}"

def test_gitignore_patterns():
    """INF-04: .gitignore excludes planning artifacts"""
    gitignore = Path(__file__).parent.parent / '.gitignore'
    assert gitignore.exists()
    content = gitignore.read_text()
    assert '.planning' in content
    assert '__MACOSX' in content

def test_no_macosx_artifacts():
    """INF-05: __MACOSX directories cleaned up"""
    project_root = Path(__file__).parent.parent
    macosx_dirs = list(project_root.rglob('__MACOSX'))
    assert len(macosx_dirs) == 0, f"Found __MACOSX dirs: {macosx_dirs}"
```

---

### `tests/conftest.py` (config, file-I/O)

**Analog:** None - greenfield file

**Standard pytest fixture pattern**:
```python
# tests/conftest.py
import pytest
from pathlib import Path
import sys

# Add src to path for imports
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

@pytest.fixture
def project_root():
    """Provide project root directory"""
    return Path(__file__).parent.parent

@pytest.fixture
def data_dir(project_root):
    """Provide data directory"""
    data = project_root / 'data'
    data.mkdir(exist_ok=True)
    return data

@pytest.fixture
def output_dir(project_root):
    """Provide output directory"""
    output = project_root / 'output'
    output.mkdir(exist_ok=True)
    return output
```

---

### `pytest.ini` (config, file-I/O)

**Analog:** None - greenfield file

**Standard pytest configuration**:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

---

### `src/analysis/analyze_data.py` (utility, file-I/O)

**Analog:** `analyze_data.py` (existing at root)

**Anti-patterns to REMOVE** (lines 12, 15):
```python
# BEFORE (REMOVE):
import warnings
warnings.filterwarnings('ignore')  # Suppresses all warnings - BAD

df = pd.read_csv(r'C:\Users\hello\Downloads\(sample)sam_tianchi_mum_baby_trade_history.csv')  # Hardcoded path - BAD
```

**Imports pattern** (lines 1-11) - KEEP and ADD logging:
```python
# AFTER:
"""
天猫母婴交易历史数据 - 统计分析报告生成器
基于Fathom科研方法风格
"""

import pandas as pd
import numpy as np
from scipy import stats
from collections import Counter
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Cross-platform path construction
DATA_DIR = Path(__file__).parent.parent.parent / 'data'
OUTPUT_DIR = Path(__file__).parent.parent.parent / 'output'

# Read data
df = pd.read_csv(DATA_DIR / 'sam_tianchi_mum_baby_trade_history.csv')
logger.info(f'Loaded dataset: {len(df)} rows, {len(df.columns)} columns')
```

**Print replacement pattern** - replace all `print()` with `logger.info()`:
```python
# BEFORE (line 20-22):
print("=" * 60)
print("Phase 1: 数据理解")
print("=" * 60)

# AFTER:
logger.info("=" * 60)
logger.info("Phase 1: 数据理解")
logger.info("=" * 60)
```

**File output pattern** (lines 402-404):
```python
# BEFORE:
with open(r'J:\数据分析\analysis_result.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_result, f, ensure_ascii=False, indent=2)

# AFTER:
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
output_file = OUTPUT_DIR / 'analysis_result.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(analysis_result, f, ensure_ascii=False, indent=2)
logger.info(f'Saved analysis results to {output_file}')
```

**Entry point pattern** (add at end):
```python
if __name__ == '__main__':
    from config.logging_config import setup_logging
    setup_logging(level=logging.INFO)
    # ... main logic
```

---

### `src/analysis/behavior_analysis.py` (utility, file-I/O)

**Analog:** `behavior_analysis.py` (existing at root)

**Same anti-patterns to REMOVE** (lines 12, 15):
```python
# REMOVE:
import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv(r'C:\Users\hello\Downloads\(sample)sam_tianchi_mum_baby_trade_history.csv')
```

**Apply same refactoring pattern as analyze_data.py:**
- Add logging import and logger instance
- Replace hardcoded path with pathlib
- Replace all print() with logger.info()
- Add entry point with setup_logging() call

---

### `src/analysis/statistical_analysis.py` (utility, file-I/O)

**Analog:** `statistical_analysis.py` (existing at root)

**Anti-patterns to REMOVE** (lines 6, 9):
```python
# REMOVE:
import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv(r'C:\Users\hello\Downloads\(sample)sam_tianchi_mum_baby_trade_history.csv')
```

**Apply same refactoring pattern as analyze_data.py:**
- Add logging import and logger instance
- Replace hardcoded path with pathlib
- Replace all print() with logger.info()
- Add entry point with setup_logging() call

---

### `src/scripts/read_excel.py` (utility, file-I/O)

**Analog:** `huashu-data-pro/scripts/read_excel.py` (existing)

**Good patterns to KEEP** (lines 1-26, 45-48):
```python
#!/usr/bin/env python3
"""
read_excel.py — 读取 Excel 文件并输出结构化摘要

用法：
    python3 read_excel.py data.xlsx
    python3 read_excel.py data.xlsx --sheet "Sheet1"
    ...

依赖：
    pip install openpyxl pandas
"""

import sys
import json
import argparse
import logging

logger = logging.getLogger(__name__)

import pandas as pd
```

**Error handling pattern** (lines 56-58):
```python
# KEEP:
except Exception as e:
    print(f"读取失败: {e}", file=sys.stderr)
    sys.exit(1)

# CHANGE to logger:
except Exception as e:
    logger.error(f"读取失败: {e}")
    sys.exit(1)
```

**CLI output pattern** (lines 61-75):
```python
# KEEP print() for CLI output - this is acceptable
print(f"\n{'='*60}")
print(f"工作表: {name}")
# But add logger for debugging
logger.debug(f'Processing sheet: {name}')
```

---

### `src/scripts/read_pptx.py` (utility, file-I/O)

**Analog:** `huashu-data-pro/scripts/read_pptx.py` (existing)

**Good patterns to KEEP** (lines 1-26, 42-43):
```python
#!/usr/bin/env python3
"""
read_pptx.py — 读取 PPTX 文件并输出结构化内容
...

依赖：
    pip install python-pptx Pillow
"""

import sys
import json
import argparse
import os
import logging

logger = logging.getLogger(__name__)

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
```

**Error handling pattern** (lines 51-52):
```python
# KEEP:
except Exception as e:
    print(f"读取失败: {e}", file=sys.stderr)
    sys.exit(1)

# CHANGE to logger:
except Exception as e:
    logger.error(f'读取失败: {e}')
    sys.exit(1)
```

**CLI output pattern** (lines 58-74):
```python
# KEEP print() for CLI output
print(f"文件: {os.path.basename(filepath)}")
print(f"尺寸: {width_in:.1f}\" x {height_in:.1f}\" ({width_in/height_in:.2f}:1)")
# But add logger for debugging
logger.debug(f'Processing PPTX: {filepath}, {total_slides} slides')
```

---

## Shared Patterns

### Path Construction with pathlib

**Source:** RESEARCH.md Pattern 1 (lines 149-170)
**Apply to:** All analysis scripts (analyze_data.py, behavior_analysis.py, statistical_analysis.py, data_overview.py)

```python
from pathlib import Path

# Script-relative paths:
DATA_DIR = Path(__file__).parent.parent.parent / 'data'
OUTPUT_DIR = Path(__file__).parent.parent.parent / 'output'

# Environment variable pattern (alternative):
import os
DATA_DIR = Path(os.environ.get('DATA_DIR', Path.home() / 'Downloads'))

# Usage:
df = pd.read_csv(DATA_DIR / 'sample_data.csv')
output_file = OUTPUT_DIR / 'results.json'

# Key properties:
p = Path('data/output/results.json')
p.name      # 'results.json'
p.stem      # 'results'
p.suffix    # '.json'
p.parent    # Path('data/output')
p.resolve() # Full absolute path
```

### Logging Module Pattern

**Source:** RESEARCH.md Pattern 2 (lines 178-221)
**Apply to:** All Python modules replacing print statements

```python
# Module-level logger (every module):
import logging
logger = logging.getLogger(__name__)

# Usage patterns:
logger.info('Main progress messages')
logger.debug('Detailed debugging info')
logger.warning('Potential issues')
logger.error('Errors that don't stop execution')
logger.exception('Exceptions with stack trace')

# Entry point setup:
from config.logging_config import setup_logging

if __name__ == '__main__':
    setup_logging(level=logging.INFO, log_file='output/analysis.log')
    # ... main logic
```

### Anti-Patterns to Remove

**Source:** RESEARCH.md (lines 254-258)
**Apply to:** All existing Python files

| Anti-Pattern | Why Bad | Replace With |
|-------------|---------|--------------|
| `warnings.filterwarnings('ignore')` | Suppresses all warnings globally | Remove entirely or use targeted: `warnings.filterwarnings('ignore', category=SpecificWarning)` |
| `r'C:\Users\...'` hardcoded paths | Breaks on macOS/Linux | `Path.home()` or `Path(__file__).parent` |
| `print()` for output | No levels, no timestamps, no file persistence | `logger.info()`, `logger.warning()`, `logger.error()` |
| `os.path.join()` | Verbose compared to pathlib | `Path('dir') / 'file'` |

---

## No Analog Found

Files with no close match in the codebase (planner should use RESEARCH.md patterns instead):

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| `requirements.txt` | config | file-I/O | No existing requirements file |
| `src/config/logging_config.py` | config | request-response | No centralized logging module exists |
| `tests/test_infrastructure.py` | test | file-I/O | No test infrastructure exists yet |
| `tests/conftest.py` | config | file-I/O | No pytest fixtures exist yet |
| `pytest.ini` | config | file-I/O | No pytest configuration exists yet |

**Recommendation:** Use patterns from RESEARCH.md Code Examples section (lines 316-372) for these greenfield files.

---

## Metadata

**Analog search scope:**
- Root directory: `J:\dataanalyst\`
- Glob patterns: `**/*.py`, `.gitignore`, `requirements.txt`, `pytest.ini`, `**/config/**/*.py`, `**/test*.py`
- Directories: `huashu-data-pro-extracted/huashu-data-pro/scripts/`

**Files scanned:** 8 Python files, 1 .gitignore, 1 SKILL.md

**Key findings:**
- 5 files with hardcoded Windows paths: `analyze_data.py`, `behavior_analysis.py`, `statistical_analysis.py`, `data_overview.py`, `母婴消费分析.py`
- 200+ print() statements needing replacement with logging
- All files use `warnings.filterwarnings('ignore')` - anti-pattern
- No requirements.txt, tests, or config directory
- Good argparse patterns in `read_excel.py` and `read_pptx.py`
- Good json output pattern in `data_overview.py`

**Pattern extraction date:** 2026-06-03

---

## Execution Priority

When planner creates PLAN.md, follow this order:

1. **Wave 0** - Test infrastructure setup (before any refactoring)
   - Install pytest: `pip install pytest pytest-cov`
   - Create `pytest.ini`, `tests/conftest.py`, `tests/test_infrastructure.py`
   - Verify tests run (should fail initially - expected)

2. **Wave 1** - Dependency management
   - Create `requirements.txt` via `pip freeze > requirements.txt`
   - Update `.gitignore` to exclude `.planning/`, `.pytest_cache/`

3. **Wave 2** - Logging infrastructure
   - Create `src/config/logging_config.py`
   - Create `src/` directory structure (`src/analysis/`, `src/scripts/`, `src/config/`)

4. **Wave 3** - Path refactoring (move files + fix paths)
   - Move scripts from root to `src/analysis/` and `src/scripts/`
   - Replace all hardcoded paths with pathlib
   - Replace all `warnings.filterwarnings('ignore')` with removal

5. **Wave 4** - Logging integration
   - Replace all print() with logger.info() in analysis files
   - Add entry point setup_logging() calls
   - Keep print() in CLI scripts (read_excel.py, read_pptx.py) for stdout output

6. **Wave 5** - Cleanup and validation
   - Delete `__MACOSX` directories
   - Run `pytest tests/ -v` - all tests should pass
   - Normalize SKILL.md location if needed