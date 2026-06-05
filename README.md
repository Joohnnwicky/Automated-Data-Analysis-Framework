# Automated Data Analysis Framework

[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-blue)](https://claude.ai/code)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)

> **Claude Code Skill for AI-powered data analysis** — From raw data to professional reports in minutes.

---

<<<<<<< HEAD
## 一键安装
=======
## 项目特色

传统数据分析流程繁琐：数据清洗 → 多工具切换 → 手动制图 → 报告排版，耗时数天。

**我们做到：数据上传 → 一键生成专业报告，仅需分钟级。**

| 传统方式 | 我们的方式 |
|---------|-----------|
| 多工具切换（Excel + Python + PowerPoint） | 单一平台完成全流程 |
| 人工分析，视角单一 | 6 种专家角色并行分析 |
| 报告设计耗时 | 11 种专业风格一键应用 |
| 数天完成 | 分钟级交付 |

---

## 核心能力

### 1. 智能数据理解

自动识别数据类型（表格/投放/时序），检测中文编码，输出完整数据画像：

- 数据维度、字段类型、统计分布
- 缺失值分析、异常值检测
- 初步趋势洞察

### 2. 多专家并行分析

独创的多专家架构，6 种专业角色同时分析同一数据：

- **量化分析师** — 统计分布、相关性、异常检测
- **估值专家** — 财务健康、现金流分析
- **投放优化师** — ROI 优化、渠道分析
- **用户增长专家** — 用户行为、漏斗分析
- **行业分析师** — 对标分析、竞争格局
- **财务分析师** — 财务比率、风险评估

每个专家独立分析，系统自动整合结论，检测冲突，输出综合洞察。

### 3. 专业报告生成

**11 种国际一流设计风格：**

Financial Times、McKinsey、Economist、Goldman Sachs、Wall Street Journal、Bloomberg、BCG、Bain、Reuters、Morningstar、Swiss Style

报告结构符合专业标准：
- 执行摘要 → 关键指标面板 → 主题深度分析 → 综合结论
- 中文输出，专业术语保留（ROI、CapEx、FCF）
- 图表自动匹配数据特征
- 支持 HTML（可导出 PDF）和 PPT 格式

### 4. 中文优先体验

专为中文用户设计：
- 自动检测 GB2312/GBK/UTF-8 编码
- 中文报告输出
- 中文自然语言交互
- 中文图表标注

---

## 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户交互层                                │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│   │  CLI 命令行  │    │ Claude Code │    │   Web API   │        │
│   └─────────────┘    └─────────────┘    └─────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                        工作流引擎                                │
│   意图检测 → 模式判断 → 流程编排 → 进度追踪 → 结果输出           │
└─────────────────────────────────────────────────────────────────┘
                              │
┌──────────────┬──────────────┬──────────────┬───────────────────┐
│   数据引擎    │   分析引擎    │   报告引擎    │   专家系统        │
│              │              │              │                   │
│ • 数据加载   │ • 类型识别   │ • 内容综合   │ • 角色定义        │
│ • 编码检测   │ • 专家选择   │ • 图表生成   │ • 并行执行        │
│ • 数据画像   │ • 冲突检测   │ • 模板渲染   │ • 结论整合        │
│ • 内存优化   │ • 统计强制   │ • 多格式输出 │                   │
└──────────────┴──────────────┴──────────────┴───────────────────┘
```

---

## 使用流程

### 快速模式（简单查询）

```
用户提问："这份数据有多少行？"
    ↓
意图检测 → 快速模式
    ↓
数据画像 → 直接返回结果
```

适用于：数据概览、单一指标查询、快速统计

### 完整模式（深度分析）

```
用户需求："分析这份广告数据，找出ROI下降原因"
    ↓
Phase 1: 业务澄清
    → 了解分析目标
    → 确认报告受众
    → 明确关注指标
    ↓
Phase 2: 数据理解
    → 加载与画像
    → 类型识别
    → 初步洞察
    ↓
Phase 3: 多专家分析
    → 选择相关专家
    → 并行独立分析
    → 检测结论冲突
    ↓
Phase 4: 报告生成
    → 综合专家结论
    → 应用设计风格
    → 输出 HTML/PPT
```

---

## 安装方式

### 一键安装

**macOS / Linux：**
```bash
curl -fsSL https://raw.githubusercontent.com/Joohnnwicky/Automated-Data-Analysis-Framework/main/install.sh | sh
```

**Windows：**
```powershell
iwr -useb https://raw.githubusercontent.com/Joohnnwicky/Automated-Data-Analysis-Framework/main/install.ps1 | iex
```

安装后可直接使用 `analyze` 命令。

### 手动安装
>>>>>>> 3045e07982863b4c1842a1963ec55be4c08fec2e

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

<<<<<<< HEAD
MIT
=======
MIT License

---

**让数据分析从「理解业务」开始，产出管理层可直接汇报的专业报告。**
>>>>>>> 3045e07982863b4c1842a1963ec55be4c08fec2e
