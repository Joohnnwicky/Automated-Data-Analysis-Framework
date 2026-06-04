"""
Statistical enforcement module for EXPT-07.

Mitigates PITFALL-01 (LLM statistical reasoning failures) and threat T-3-03
(HIGH severity: LLM hallucination in analysis) by enforcing code execution
requirement for all numerical conclusions.

All numerical claims in expert outputs must be backed by Python code execution,
not LLM mental math or estimation.
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