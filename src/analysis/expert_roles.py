"""Expert role definitions for multi-expert analysis.

This module defines the ExpertRole dataclass and the EXPERT_ROLES library
for the multi-expert analysis system. Each role represents a specialized
analytical perspective with specific domain expertise, framework, and tasks.

Threat Model:
- T-3-01: Role definitions are constants (immutable), no user input in EXPERT_ROLES
- T-3-05: Each role definition is self-contained, no cross-role references
"""

from dataclasses import dataclass
from typing import List


@dataclass
class ExpertRole:
    """Definition of an expert role for analysis.

    Attributes:
        id: Unique identifier for the role (snake_case)
        name: Display name (Chinese + English)
        domain: Expertise domain description
        framework: Analysis framework summary
        tasks: List of specific analysis tasks (3 items, Chinese)
        data_types: Compatible data types ['table', 'time_series', 'advertising']
    """
    id: str
    name: str
    domain: str
    framework: str
    tasks: List[str]
    data_types: List[str]


# Expert Role Library (EXPT-02)
# Each role defines a specialized analytical perspective
EXPERT_ROLES: List[ExpertRole] = [
    ExpertRole(
        id="quant_analyst",
        name="量化分析师 (Quantitative Analyst)",
        domain="数量分析与统计建模",
        framework="专注于数据分布、相关性、统计检验",
        tasks=["分布分析", "相关性矩阵", "异常值检测"],
        data_types=["table", "time_series", "advertising"]
    ),
    ExpertRole(
        id="valuation_expert",
        name="估值专家 (Damodaran School)",
        domain="财务估值与现金流分析",
        framework="DCF建模、FCF分析、估值框架",
        tasks=["FCF计算", "估值指标", "风险评估"],
        data_types=["table", "time_series"]
    ),
    ExpertRole(
        id="growth_optimizer",
        name="投放优化师 (Advertising Expert)",
        domain="广告投放ROI优化",
        framework="CTR/CVR分析、渠道优化、预算分配",
        tasks=["ROI分析", "CTR趋势", "渠道对比"],
        data_types=["advertising"]
    ),
    ExpertRole(
        id="user_growth",
        name="用户增长专家 (Growth Hacker)",
        domain="用户行为与增长分析",
        framework="漏斗分析、留存分析、A/B测试",
        tasks=["漏斗转化", "留存曲线", "行为聚类"],
        data_types=["table", "advertising"]
    ),
    ExpertRole(
        id="industry_analyst",
        name="行业分析师 (McKinsey Style)",
        domain="行业对标与战略分析",
        framework="对标分析、市场定位、竞争格局",
        tasks=["行业对比", "市场定位", "竞争分析"],
        data_types=["table", "time_series"]
    ),
    ExpertRole(
        id="financial_analyst",
        name="财务分析师 (CFA Perspective)",
        domain="财务健康度与风险评估",
        framework="财务比率、现金流、风险指标",
        tasks=["财务比率", "现金流分析", "风险评估"],
        data_types=["table", "time_series"]
    ),
]