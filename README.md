# Automated Data Analysis Framework

[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-blue)](https://claude.ai/code)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)

> **Claude Code Skill for AI-powered data analysis** — From raw data to professional reports in minutes.

---

## 一键安装

```bash
npx skills add Joohnnwicky/Automated-Data-Analysis-Framework
```

或手动安装到对应目录：

| Runtime | Skills 目录 |
|---------|------------|
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| Continue | `~/.continue/skills/` |

---

## 使用示例

安装后，在 Claude Code 中直接用自然语言：

```
> 分析这份销售数据，找出增长趋势

> 用 McKinsey 风格生成 PPT 报告

> 这份广告数据的 ROI 为什么下降？
```

Claude 会自动调用此 Skill 完成分析。

---

## 核心能力

| 能力 | 说明 |
|------|------|
| **智能理解** | 自动识别数据类型、编码，输出完整画像 |
| **多专家分析** | 6 种专业角色并行分析，多视角洞察 |
| **专业报告** | 11 种设计风格（FT、McKinsey 等），HTML/PPT 输出 |
| **中文优先** | 中文报告，自动检测中文编码 |

---

## 工作原理

```
数据输入 → 业务澄清 → 数据理解 → 多专家分析 → 报告生成
              ↓           ↓           ↓           ↓
         了解目标      画像数据    6专家并行    风格输出
```

---

## 目录结构

```
automated-data-analysis/
├── SKILL.md                 # Skill 定义文件
├── src/
│   ├── data/                # 数据处理
│   ├── analysis/            # 多专家分析引擎
│   ├── report/              # 报告生成
│   └── workflow/            # 工作流协调
└── requirements.txt
```

---

## 专家角色

| 角色 | 领域 | 专长 |
|------|------|------|
| 量化分析师 | 统计 | 分布、相关性、异常 |
| 估值专家 | 财务 | FCF、估值指标 |
| 投放优化师 | 广告 | ROI、CTR、渠道 |
| 用户增长专家 | 增长 | 用户行为、漏斗 |
| 行业分析师 | 战略 | 对标、竞争格局 |
| 财务分析师 | 财务 | 财务比率、风险 |

---

## 设计风格

`ft` | `mckinsey` | `economist` | `goldman` | `swiss` | `wsj` | `bloomberg` | `reuters` | `morningstar` | `bcg` | `bain`

---

## 要求

- Python 3.10+
- 支持：Excel (.xlsx)、CSV、JSON

---

## 许可证

MIT