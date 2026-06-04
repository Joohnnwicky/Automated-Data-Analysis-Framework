# tests/test_statistical_enforcement.py
"""
Test scaffolds for EXPT-07 requirement.
Initially skipped - will pass after src/analysis/statistical_enforcement.py implementation.
"""

import pytest
import pandas as pd
from pathlib import Path


class TestStatisticalEnforcement:
    """Tests for statistical code execution enforcement."""

    def test_verify_code_execution_detects_code_blocks(self):
        """EXPT-07: Verify verify_code_execution returns True when output contains python blocks."""
        from src.analysis.statistical_enforcement import verify_code_execution

        # Output with python code blocks
        output_with_code = """
## Analysis Results

Based on the statistical analysis:

```python
import pandas as pd
import numpy as np

# Calculate mean and standard deviation
mean = df['value'].mean()
std = df['value'].std()

print(f"Mean: {mean:.2f}, Std: {std:.2f}")
```

The results show significant variation.
"""

        result = verify_code_execution(output_with_code)

        # Should return True when python code blocks are present
        assert result is True

    def test_verify_code_execution_fails_without_code(self):
        """EXPT-07: Verify verify_code_execution returns False when output has numerical claims without code."""
        from src.analysis.statistical_enforcement import verify_code_execution

        # Output with numerical claims but no code blocks
        output_without_code = """
## Analysis Results

Based on the statistical analysis:
- The mean value is 45.67
- The standard deviation is 12.34
- The correlation coefficient is 0.89

These results show significant patterns in the data.
"""

        result = verify_code_execution(output_without_code)

        # Should return False when numerical claims exist without code
        assert result is False

    def test_statistical_enforcement_prompt_contains_rules(self):
        """EXPT-07: Verify STATISTICAL_ENFORCEMENT_PROMPT contains rules."""
        from src.analysis.statistical_enforcement import STATISTICAL_ENFORCEMENT_PROMPT

        # Verify prompt is defined
        assert STATISTICAL_ENFORCEMENT_PROMPT is not None
        assert isinstance(STATISTICAL_ENFORCEMENT_PROMPT, str)

        # Verify prompt contains Chinese enforcement rules
        # Should mention "禁止" (prohibited) and "必须" (required)
        assert '禁止' in STATISTICAL_ENFORCEMENT_PROMPT
        assert '必须' in STATISTICAL_ENFORCEMENT_PROMPT

        # Should mention code execution requirement
        assert '代码' in STATISTICAL_ENFORCEMENT_PROMPT or 'python' in STATISTICAL_ENFORCEMENT_PROMPT.lower()

        # Should mention statistical claims
        assert '统计' in STATISTICAL_ENFORCEMENT_PROMPT or '数值' in STATISTICAL_ENFORCEMENT_PROMPT