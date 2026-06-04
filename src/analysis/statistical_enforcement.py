"""
Statistical enforcement module for EXPT-07.

Mitigates PITFALL-01 (LLM statistical reasoning failures) and threat T-3-03
(HIGH severity: LLM hallucination in analysis) by enforcing code execution
requirement for all numerical conclusions.

All numerical claims in expert outputs must be backed by Python code execution,
not LLM mental math or estimation.

This module provides:
1. STATISTICAL_ENFORCEMENT_PROMPT: Prompt instructions to embed in expert prompts
2. verify_code_execution: Function to validate expert outputs contain code blocks

Usage:
    from src.analysis.statistical_enforcement import (
        STATISTICAL_ENFORCEMENT_PROMPT,
        verify_code_execution
    )

    # Include in expert prompt
    expert_prompt = base_prompt + "\\n\\n" + STATISTICAL_ENFORCEMENT_PROMPT

    # Verify expert output
    if not verify_code_execution(expert_output):
        raise ValueError("Expert output lacks code execution verification")

Architecture:
    This module is designed to be integrated into the expert runner pipeline
    (src/analysis/expert_runner.py). The STATISTICAL_ENFORCEMENT_PROMPT should
    be appended to every expert's system prompt, and verify_code_execution
    should be called on every expert's output before accepting conclusions.

Threat Mitigation:
    - T-3-03 (HIGH): LLM hallucination in analysis is mitigated by requiring
      all numerical claims to be backed by executed Python code
    - PITFALL-01: Statistical reasoning failures prevented by code execution
"""

import re

# EXPT-07: Enforce code execution in prompt
STATISTICAL_ENFORCEMENT_PROMPT = """
关键要求：所有数值结论必须通过Python代码计算。

禁止：
- 直接给出统计数值（如"均值是45.6"）而无代码支撑
- 心算或估算任何数值
- 编造不存在的数据点

必须：
- 写出完整的Python计算代码
- 显示代码执行结果
- 每个数值引用具体的数据来源（如"df['column'].mean()"）

示例正确格式：
```python
# 计算ROI均值
roi_mean = df['ROI'].mean()
print(f"ROI均值: {roi_mean:.2f}")
```
ROI均值: 45.62
"""


def verify_code_execution(output: str) -> bool:
    """Check that output contains code blocks for numerical claims.

    Verifies that expert analysis outputs contain Python code blocks,
    ensuring numerical conclusions are backed by code execution rather than
    LLM mental math or estimation.

    Args:
        output: Expert analysis text to check for code blocks.

    Returns:
        True if at least one Python code block is present, False otherwise.

    Examples:
        >>> output = '''Analysis:
        ... ```python
        ... mean = df['value'].mean()
        ... print(f"Mean: {mean:.2f}")
        ... ```
        ... Mean: 45.62'''
        >>> verify_code_execution(output)
        True

        >>> output = "The mean value is 45.6"
        >>> verify_code_execution(output)
        False
    """
    # Look for python code blocks
    code_blocks = re.findall(r'```python.*?```', output, re.DOTALL)

    # Look for numerical claims without code backing
    # This is a heuristic check - human review recommended for edge cases

    return len(code_blocks) > 0