---
last_mapped_commit: not a git repo
mapped_at: 2026-06-03
focus: quality
---

# Coding Conventions

## Code Style

**Python:**
- Scripts use procedural style, not object-oriented
- Standard library imports first, then third-party packages
- No formal style enforcement (no pylint, black, or flake8 configuration found)
- Consistent use of `warnings.filterwarnings('ignore')` to suppress warnings
- UTF-8 encoding declared in headers: `# -*- coding: utf-8 -*-`

**JavaScript:**
- CommonJS module format (`require`, `module.exports`)
- Async/await pattern throughout
- Detailed JSDoc-style header comments with usage documentation
- No ESLint or formatting configuration found

## Naming Patterns

**Files:**
- Python: lowercase with underscores, Chinese characters acceptable (e.g., `母婴消费分析.py`)
- JavaScript: lowercase with underscores (e.g., `html2pptx.js`, `build_pptx.js`)

**Functions:**
- Python: snake_case (e.g., `ensure_dependencies`, `read_excel`, `classify_user`)
- JavaScript: camelCase (e.g., `checkDependencies`, `parseArgs`, `getBodyDimensions`)

**Variables:**
- Python: snake_case for local variables, Chinese characters used for domain-specific names (e.g., `df`, `buy_dist`, `extreme_users`)
- JavaScript: camelCase (e.g., `missing`, `config`, `slideResults`)

**Constants:**
- UPPERCASE with underscores (e.g., `PT_PER_PX`, `PX_PER_IN`, `EMU_PER_IN`, `CHART_COLORS`)

## Documentation

**File Headers:**
- Python: Triple-quoted docstrings after encoding declaration
  - Example from `behavior_analysis.py`: `"""母婴消费行为心理学分析 基于Kahneman行为经济学框架"""`
  - Example from `read_excel.py`: Detailed usage block with usage examples, parameters, and dependencies
- JavaScript: Block comments with USAGE, FEATURES, VALIDATION, RETURNS sections
  - Example from `html2pptx.js`: 25-line header explaining usage, features, validation rules, and return values

**Inline Comments:**
- Section markers using `# ====...====` pattern for dividing code into logical sections
- Chinese comments for domain-specific explanations
- Minimal inline comments - code is generally self-documenting

**No README or formal documentation structure** - Scripts are self-contained with embedded usage instructions

## Error Handling

**Python:**
- Basic `try/except` blocks around file operations and external calls
- `sys.exit(1)` for failure cases
- Print error messages to stderr: `print(..., file=sys.stderr)`
- No custom exception classes
- `warnings.filterwarnings('ignore')` suppresses all warnings at startup

**JavaScript:**
- `try/catch` with async operations
- `console.error()` for error output
- `process.exit(1)` for failures
- Detailed error messages with helpful context (e.g., missing dependencies include install command)
- Validation errors collected and thrown together with descriptive messages

**Pattern for dependency missing:**
```python
# From read_excel.py
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

## Code Organization

**Python Scripts:**
- Imports at top (standard library, then third-party)
- Functions defined before main execution block
- `if __name__ == '__main__':` pattern for entry point
- Section markers using `print("=" * 60)` for output organization
- No classes - all procedural with functions

**JavaScript Scripts:**
- Dependency checking function at top
- Helper functions defined before main logic
- Command-line argument parsing function
- Main async function at bottom with `.catch()` for error handling
- `module.exports` for reusable modules

**Typical Python script structure:**
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Docstring"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Data loading
df = pd.read_csv(...)

# Section 1 - print("=" * 60) separator
# Analysis logic

# Section 2
# More analysis

print("分析完成!")
```

## Patterns & Idioms

**Output Formatting:**
- `print("=" * 60)` creates visual section separators
- `print("\n" + "=" * 60)` for new section with spacing
- JSON dumps for structured output: `json.dumps(stats, ensure_ascii=False, indent=2)`
- Pandas `to_markdown()`, `to_string()` for table output

**Data Analysis Patterns:**
- Load data immediately at script start: `df = pd.read_csv(...)`
- Date conversion pattern: `pd.to_datetime(df['day'], format='%Y%m%d')`
- Groupby aggregation with named columns:
  ```python
  cat_analysis = df.groupby('cat1').agg({
      'buy_mount': ['sum', 'count', 'mean'],
      'user_id': lambda x: x.nunique()
  }).reset_index()
  cat_analysis.columns = ['cat1', 'total_buy', 'order_count', 'avg_buy', 'user_count']
  ```
- Statistical tests using `scipy.stats`: `stats.linregress`, `stats.f_oneway`, `stats.kstest`

**Command-line Argument Pattern (JavaScript):**
```javascript
function parseArgs() {
  const args = process.argv.slice(2);
  const config = { slides: [], output: 'output.pptx', charts: [] };
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--slides':
        while (i + 1 < args.length && !args[i + 1].startsWith('--')) {
          config.slides.push(args[++i]);
        }
        break;
      // ... more cases
    }
  }
  return config;
}
```

**Validation Pattern (JavaScript):**
- Collect multiple errors into array
- Throw combined error message if any exist:
  ```javascript
  if (validationErrors.length > 0) {
    const errorMessage = validationErrors.length === 1
      ? validationErrors[0]
      : `Multiple validation errors found:\n${validationErrors.map((e, i) => `  ${i + 1}. ${e}`).join('\n')}`;
    throw new Error(errorMessage);
  }
  ```

## Language Rules

**Chinese vs English:**
- File names and comments primarily in Chinese for domain-specific analysis scripts
- Function/variable names in English for utility scripts (skill scripts)
- Report output in Chinese with English preserved for: abbreviations (FCF, ROI), company names (Meta, Apple), and standard terms (IPO, AI)
- Technical scripts (skill scripts) use English throughout

**Import Organization:**
- Standard library first
- Third-party packages second (pandas, numpy, scipy, etc.)
- No explicit grouping comments