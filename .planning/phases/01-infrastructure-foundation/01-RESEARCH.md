# Phase 1: Infrastructure Foundation - Research

**Researched:** 2026-06-03
**Domain:** Python toolchain foundation (dependency management, cross-platform paths, logging, version control)
**Confidence:** HIGH

## Summary

Phase 1 establishes the foundation for a data analysis skill project that currently has significant technical debt: hardcoded Windows paths in 5+ Python files, 200+ print statements needing replacement with structured logging, no requirements.txt, and __MACOSX metadata artifacts from extracted archives. The project uses pandas, numpy, scipy, openpyxl, and python-pptx for data processing and report generation.

**Primary recommendation:** Create a requirements.txt with locked versions using `pip freeze`, replace all hardcoded paths with pathlib's `/` operator pattern, implement a centralized logging configuration module, and clean up __MACOSX directories while normalizing skill file structure.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Path construction | Application Code | - | All scripts use pathlib for file I/O |
| Dependency management | Build System | - | requirements.txt at project root |
| Logging output | Application Code | stdout/file | Structured logging for all modules |
| Git ignore rules | Version Control | - | .gitignore at project root |
| Skill metadata | Configuration | - | SKILL.md YAML frontmatter |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pandas | 3.0.1 | Data manipulation and analysis | Industry-standard for tabular data |
| numpy | 2.4.3 | Numerical computations | Foundation for pandas, scipy |
| scipy | 1.17.1 | Statistical functions | IQR, ANOVA, regression tests |
| openpyxl | 3.1.5 | Excel (.xlsx) reading/writing | Required for data input |
| python-pptx | 1.0.2 | PPTX generation | HTML-to-PPTX conversion workflow |
| Pillow | 12.1.1 | Image processing | Thumbnail extraction from PPTX |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pathlib | stdlib | Cross-platform path handling | All file I/O operations |
| logging | stdlib | Structured output | Replace all print statements |
| json | stdlib | Data serialization | Analysis result output |
| argparse | stdlib | CLI argument parsing | Script entry points |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| pathlib | os.path | Legacy API, no `/` operator, more verbose |
| logging | print | No levels, no timestamps, no file output |
| requirements.txt | Pipenv/Poetry | Added complexity for single-developer project |

**Installation:**
```bash
pip install pandas==3.0.1 numpy==2.4.3 scipy==1.17.1 openpyxl==3.1.5 python-pptx==1.0.2 Pillow==12.1.1
pip freeze > requirements.txt
```

**Version verification:**
```bash
pip show pandas numpy scipy openpyxl python-pptx Pillow | grep "Version:"
# Verified: 2026-06-03 on Python 3.14.3
```

## Package Legitimacy Audit

> **Required** whenever this phase installs external packages. Run the Package Legitimacy Gate protocol before completing this section.

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| pandas | PyPI | ~17 yrs | ~50M/wk | github.com/pandas-dev/pandas | [OK] | Approved |
| numpy | PyPI | ~23 yrs | ~50M/wk | github.com/numpy/numpy | [OK] | Approved |
| scipy | PyPI | ~22 yrs | ~30M/wk | github.com/scipy/scipy | [OK] | Approved |
| openpyxl | PyPI | ~15 yrs | ~8M/wk | openpyxl.readthedocs.io | [OK] | Approved |
| python-pptx | PyPI | ~13 yrs | ~500K/wk | github.com/scanny/python-pptx | [OK] | Approved |
| Pillow | PyPI | ~15 yrs | ~15M/wk | github.com/python-pillow/Pillow | [OK] | Approved |

**Packages removed due to slopcheck [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** none

**slopcheck output:**
```
[OK] scipy (pypi)
[OK] python-pptx (pypi) - Name starts with 'python-' -- classic LLM naming pattern but package is established
[OK] Pillow (pypi)
[OK] openpyxl (pypi)
[OK] numpy (pypi)
[OK] pandas (pypi)
scanned 6 packages, 6 OK
```

## Architecture Patterns

### System Architecture Diagram

```
+-------------------------------------------------------------------+
|                    Project Root (J:\dataanalyst)                   |
+-------------------------------------------------------------------+
|  requirements.txt ---------> Python Environment                    |
|  (locked versions)           (pip install -r)                      |
|                                                                   |
|  .gitignore ---------------> Git Repository                        |
|  (exclude patterns)          (tracked files)                      |
|                                                                   |
|  src/config/ --------------> Logging Configuration                 |
|  logging_config.py           (centralized setup)                   |
|         |                                                         |
|         v                                                         |
|  +-------------------------------------------------------+        |
|  |  Application Modules (using pathlib + logging)        |        |
|  |  |-- analyze_data.py                                  |        |
|  |  |-- behavior_analysis.py                             |        |
|  |  |-- statistical_analysis.py                          |        |
|  |  +-- scripts/read_excel.py                            |        |
|  |     +-- scripts/read_pptx.py                          |        |
|  +-------------------------------------------------------+        |
|         |                                                         |
|         v                                                         |
|  Path.resolve() ------------> Cross-platform file I/O            |
|  logger.info() --------------> Structured output (stdout/file)    |
+-------------------------------------------------------------------+
```

### Recommended Project Structure
```
J:\dataanalyst\
+-- requirements.txt           # Locked dependencies (Phase 1)
+-- .gitignore                 # Git exclude patterns (Phase 1)
+-- src/
|   +-- config/
|   |   +-- logging_config.py  # Centralized logging setup (Phase 1)
|   +-- analysis/
|   |   +-- analyze_data.py    # Refactored with pathlib + logging
|   |   +-- behavior_analysis.py
|   |   +-- statistical_analysis.py
|   +-- scripts/
|       +-- read_excel.py      # huashu-data-pro utility
|       +-- read_pptx.py       # huashu-data-pro utility
+-- data/                      # Sample data files (gitignored)
+-- output/                    # Analysis outputs (gitignored)
+-- .planning/                 # GSD planning artifacts
```

### Pattern 1: pathlib Cross-Platform Path Construction

**What:** Use Path's `/` operator for joining paths, never string concatenation or os.path.join
**When to use:** All file I/O operations in Python scripts

**Example:**
```python
# Source: https://docs.python.org/3/library/pathlib.html
from pathlib import Path

# BEFORE (hardcoded Windows path - BAD):
df = pd.read_csv(r'C:\Users\hello\Downloads\(sample)sam_tianchi_mum_baby_trade_history.csv')

# AFTER (cross-platform - GOOD):
DATA_DIR = Path(__file__).parent.parent / 'data'
df = pd.read_csv(DATA_DIR / 'sample_data.csv')

# Or with environment variable:
DATA_DIR = Path(os.environ.get('DATA_DIR', Path.home() / 'Downloads'))
df = pd.read_csv(DATA_DIR / 'sample_data.csv')

# Key properties:
p = Path('data/output/results.json')
p.name      # 'results.json' - filename
p.stem      # 'results' - name without extension
p.suffix    # '.json' - extension
p.parent    # Path('data/output')
p.resolve() # Full absolute path
```

### Pattern 2: Structured Logging Configuration

**What:** Centralized logging setup with module-level loggers using `getLogger(__name__)`
**When to use:** All Python modules replacing print statements

**Example:**
```python
# Source: https://docs.python.org/3/library/logging.html
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

# src/analysis/analyze_data.py
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

### Pattern 3: requirements.txt with Locked Versions

**What:** Use `pip freeze` to capture exact installed versions, enabling repeatable installs
**When to use:** Project initialization, dependency updates

**Example:**
```bash
# Generate locked requirements:
pip freeze > requirements.txt

# Example output:
pandas==3.0.1
numpy==2.4.3
scipy==1.17.1
openpyxl==3.1.5
python-pptx==1.0.2
Pillow==12.1.1
XlsxWriter==3.2.9
lxml==6.0.4
python-dateutil==2.9.0.post0
tzdata==2025.3
et-xmlfile==2.0.0
typing-extensions==4.15.0
six==1.17.0

# Install exact versions:
pip install -r requirements.txt
```

### Anti-Patterns to Avoid

- **`warnings.filterwarnings('ignore')`**: Suppresses all warnings globally - prevents detecting real issues. Remove entirely. Use targeted suppression: `warnings.filterwarnings('ignore', category=SpecificWarning)`
- **`r'C:\Users\...'` hardcoded paths**: Breaks on macOS/Linux. Use `Path.home()` or environment variables.
- **`print()` for output**: No log levels, no timestamps, no file persistence. Use `logger.info()`, `logger.warning()`, `logger.error()`.
- **`os.path.join()`**: Verbose compared to pathlib's `/` operator. Use `Path('dir') / 'file'`.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Path joining | String concatenation `dir + '/' + file` | pathlib `/` operator | Handles platform separators automatically |
| Logging | print() statements | logging module | Levels, timestamps, file output, filtering |
| Dependency locking | Manual version listing | pip freeze > requirements.txt | Captures actual installed versions with transitive deps |
| Cross-platform home dir | `'/Users/' + username` | Path.home() | Works on Windows/macOS/Linux |
| Git ignore patterns | Manual file exclusion | .gitignore patterns | Standard convention, automatically respected |

**Key insight:** All these infrastructure problems have standard library or ecosystem solutions. Custom implementations introduce maintenance burden and platform-specific bugs.

## Runtime State Inventory

> Include this section for rename/refactor/migration phases only. Omit entirely for greenfield phases.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | None - no databases or persistent stores yet | None |
| Live service config | None - project is local scripts only | None |
| OS-registered state | None - no scheduled tasks or services | None |
| Secrets/env vars | None - hardcoded paths reference local user directories | Will need DATA_DIR env var design |
| Build artifacts | `huashu-data-pro-extracted/__MACOSX/` - macOS archive metadata (20+ files) | Delete entire `__MACOSX` directory tree |

**Nothing found in category:** Verified explicitly for stored data, live service config, OS-registered state, and secrets.

## Common Pitfalls

### Pitfall 1: Case Sensitivity in Paths
**What goes wrong:** `Path('data/file.csv')` works on Windows but fails on Linux if actual filename is `File.csv`
**Why it happens:** Windows is case-insensitive, POSIX is case-sensitive
**How to avoid:** Use exact filenames from source, or `Path.resolve().name` to get canonical name
**Warning signs:** FileNotFoundError on Linux/macOS for files that work on Windows

### Pitfall 2: Logger Propagation Duplicate Output
**What goes wrong:** Same log message appears multiple times in output
**Why it happens:** Multiple handlers attached to different levels of logger hierarchy
**How to avoid:** Configure only root logger, let child loggers propagate (`propagate=True` default)
**Warning signs:** Duplicate lines in logs with same timestamp

### Pitfall 3: requirements.txt Version Drift
**What goes wrong:** Package versions change between environments, causing subtle bugs
**Why it happens:** Using `>=` constraints instead of `==` locked versions
**How to avoid:** Always use `pip freeze > requirements.txt`, never edit manually
**Warning signs:** Different pandas behavior on different machines

### Pitfall 4: Absolute vs Relative Path Confusion
**What goes wrong:** `Path('data/file.csv')` resolves differently depending on working directory
**Why it happens:** Relative paths depend on cwd, which changes with script location
**How to avoid:** Use `Path(__file__).parent / 'data'` for script-relative paths, or `Path.cwd() / 'data'` for cwd-relative
**Warning signs:** FileNotFoundError when running script from different directory

## Code Examples

Verified patterns from official sources:

### Cross-Platform Path Construction
```python
# Source: https://docs.python.org/3/library/pathlib.html
from pathlib import Path

# Construct paths with / operator
config_dir = Path.home() / '.config' / 'myapp'
data_file = Path('data') / 'output' / 'results.json'

# Resolve to absolute path
full_path = data_file.resolve()

# Check existence before reading
if data_file.exists():
    with open(data_file, 'r') as f:
        data = json.load(f)

# Convert to string for legacy APIs
str(data_file)  # 'data/output/results.json' (native format)
```

### Structured Logging
```python
# Source: https://docs.python.org/3/library/logging.html
import logging

# Module-level logger
logger = logging.getLogger(__name__)

def process_data(filepath):
    logger.info(f'Processing {filepath}')
    try:
        # ... processing
        logger.debug(f'Records processed: {count}')
    except ValueError as e:
        logger.warning(f'Invalid data format: {e}')
    except Exception as e:
        logger.error(f'Processing failed: {e}')
        raise

# Entry point configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
```

### Requirements.txt Generation
```bash
# Source: https://pip.pypa.io/en/stable/user_guide/#requirements-files
# Generate locked requirements
python -m pip freeze > requirements.txt

# Reinstall exact versions
python -m pip install -r requirements.txt
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| os.path.join() | pathlib Path with `/` operator | Python 3.4+ | More readable, cross-platform by default |
| print() debugging | logging module with levels | Python 2.3+ | Structured output, filtering, file persistence |
| Loose version constraints | pip freeze locked versions | pip 1.3+ | Repeatable installs, no drift |
| Manual .gitignore | Standard patterns per ecosystem | Git standard | Excludes caches, artifacts, secrets automatically |

**Deprecated/outdated:**
- `os.path` module: Still works but pathlib is recommended for new code
- `warnings.filterwarnings('ignore')` globally: Prevents legitimate warning detection - use targeted suppression only
- String path concatenation: `dir + '/' + file` - use pathlib instead

## Assumptions Log

> List all claims tagged `[ASSUMED]` in this research. The planner and discuss-phase use this section to identify decisions that need user confirmation before execution.

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Python 3.14.3 is the target runtime version | Environment | Compatibility issues if older version used |
| A2 | Project will use centralized logging config (not per-module config) | Architecture | May need per-module flexibility |
| A3 | DATA_DIR will be configurable via environment variable | Architecture | May need command-line argument instead |

**All other claims:** Verified via pip show, slopcheck, official documentation, or direct codebase inspection.

## Open Questions (RESOLVED)

1. **Should scripts be moved to src/scripts/ or kept at project root?** - RESOLVED
   - What we know: Current scripts are at root level (analyze_data.py, etc.) plus huashu-data-pro/scripts/
   - What was unclear: Preferred organization for single-developer analysis project
   - **Resolution:** Scripts organized into `src/scripts/` (utility scripts like read_excel.py, read_pptx.py) and `src/analysis/` (analysis scripts like analyze_data.py, behavior_analysis.py, statistical_analysis.py). Per Recommended Project Structure (lines 96-114).

2. **Should logging go to file or only stdout?** - RESOLVED
   - What we know: Current code uses print() for all output
   - What was unclear: Whether file logging is needed for debugging/audit
   - **Resolution:** Default to stdout via `StreamHandler(sys.stdout)`. Optional file logging via `log_file` parameter in `setup_logging()`. Per Pattern 2: Structured Logging Configuration (lines 146-196).

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | Runtime | Yes | 3.14.3 | - |
| pip | Package management | Yes | 26.1.1 | - |
| Git | Version control | Yes | 2.54.0.windows.1 | - |
| pandas | Data analysis | Yes | 3.0.1 | - |
| numpy | Numerical ops | Yes | 2.4.3 | - |
| scipy | Statistical tests | Yes | 1.17.1 | - |
| openpyxl | Excel reading | Yes | 3.1.5 | - |
| python-pptx | PPTX generation | Yes | 1.0.2 | - |
| Pillow | Image processing | Yes | 12.1.1 | - |
| pytest | Testing framework | No | - | Will install in Wave 0 |

**Missing dependencies with no fallback:**
- pytest: Required for nyquist_validation - Wave 0 will install

**Missing dependencies with fallback:**
- None - all core dependencies verified available

## Validation Architecture

> nyquist_validation enabled in .planning/config.json

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (not yet installed) |
| Config file | None - see Wave 0 |
| Quick run command | `pytest tests/ -x -v` |
| Full suite command | `pytest tests/ -v --tb=short` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| INF-01 | requirements.txt with locked versions | unit | `pytest tests/test_infrastructure.py::test_requirements_locked -x` | No - Wave 0 |
| INF-02 | pathlib replaces hardcoded paths | unit | `pytest tests/test_infrastructure.py::test_paths_cross_platform -x` | No - Wave 0 |
| INF-03 | logging replaces print statements | unit | `pytest tests/test_infrastructure.py::test_logging_levels -x` | No - Wave 0 |
| INF-04 | Git initialized with proper .gitignore | unit | `pytest tests/test_infrastructure.py::test_gitignore_patterns -x` | No - Wave 0 |
| INF-05 | __MACOSX cleanup, skill structure normalized | unit | `pytest tests/test_infrastructure.py::test_no_macosx_artifacts -x` | No - Wave 0 |

### Sampling Rate
- **Per task commit:** `pytest tests/ -x -v`
- **Per wave merge:** `pytest tests/ -v --tb=short`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_infrastructure.py` - covers INF-01 through INF-05
- [ ] `tests/conftest.py` - shared fixtures (test data paths, logging setup)
- [ ] pytest install: `pip install pytest pytest-cov`
- [ ] pytest.ini: Basic configuration for test discovery

*(No existing test infrastructure - all Phase 1 tests require Wave 0 setup)*

## Security Domain

> security_enforcement not explicitly set - default enabled

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | No user auth in this phase |
| V3 Session Management | no | No sessions in this phase |
| V4 Access Control | no | No access control in this phase |
| V5 Input Validation | no | No user input validation (file paths from code, not user) |
| V6 Cryptography | no | No crypto operations |

**Note:** Phase 1 is infrastructure-only - no security-sensitive operations. Future phases handling user-provided data files will require V5 (Input Validation) for filepath sanitization.

### Known Threat Patterns for Python Data Analysis

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Path traversal (user-provided paths) | Tampering | pathlib.resolve() validation, reject absolute paths from user input |
| CSV injection (formula injection) | Tampering | sanitize cell values, use openpyxl's security features |
| Pickle deserialization | Elevation of Privilege | Never load untrusted pickle files, use JSON/safe formats |

**Phase 1 security scope:** No user-provided input paths yet - all paths are hardcoded and being converted to pathlib. Security considerations apply in Phase 2+.

## Sources

### Primary (HIGH confidence)
- https://docs.python.org/3/library/pathlib.html - pathlib Path construction, `/` operator, cross-platform handling
- https://docs.python.org/3/library/logging.html - logging module, getLogger(__name__), basicConfig, levels
- https://pip.pypa.io/en/stable/user_guide/#requirements-files - pip freeze, locked versions, repeatable installs

### Secondary (MEDIUM confidence)
- pip show output (verified installed versions on local environment)
- slopcheck package legitimacy scan (verified all packages [OK])

### Tertiary (LOW confidence)
- None - all claims verified via primary/secondary sources

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All packages verified via pip show and slopcheck, versions confirmed on registry
- Architecture: HIGH - pathlib and logging patterns from official Python documentation
- Pitfalls: HIGH - Known issues documented in official docs and community knowledge

**Research date:** 2026-06-03
**Valid until:** 30 days (stable Python stdlib APIs, package versions current)

---

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| INF-01 | Create requirements.txt with locked Python dependency versions | Pattern 3: requirements.txt with locked versions, pip freeze workflow |
| INF-02 | Replace all hardcoded Windows paths with pathlib for cross-platform compatibility | Pattern 1: pathlib Cross-Platform Path Construction, 5+ hardcoded paths found in codebase |
| INF-03 | Introduce logging module to replace 200+ print statements with log level support | Pattern 2: Structured Logging Configuration, getLogger(__name__) pattern |
| INF-04 | Git version control initialization, proper .gitignore for planning artifacts | Git already initialized, .gitignore exists but may need refinement for .planning/ |
| INF-05 | Clean up __MACOSX metadata directories, normalize skill file structure | Runtime State Inventory: 20+ __MACOSX files found, SKILL.md exists in huashu-data-pro |