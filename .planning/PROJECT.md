---
last_updated: 2026-06-04
after: phase-03-analysis-engine
---

# Data Analyst Pro — 融合增强版数据分析 Skill

## What This Is

增强版数据分析 skill，融合 huashu-data-pro 的报告生成能力与 data-analyst TUI 的探索性分析优势。提供「业务意图澄清 → 数据理解 → 多专家深度分析 → 正式报告生成」的端到端工作流，服务于业务分析师、数据分析师、运营团队和管理层。

核心能力：表格数据/投放数据/时序数据分析、中文报告生成、HTML/PPT 输出、11 种专业设计风格。

## Core Value

**让数据分析从「理解业务问题」开始，产出管理层可直接汇报的专业报告。**

关键差异：Phase 0 业务意图澄清前置，确保分析方向正确；多专家并行分析提供多视角洞察；专业设计系统输出可直接汇报的报告。

## Requirements

### Validated

**Phase 03: Analysis Engine** (2026-06-04)
- [x] **EXPT-01**: Expert selection algorithm with data type filtering and business context refinement
- [x] **EXPT-02**: ExpertRole dataclass with 6 predefined roles covering all data types
- [x] **EXPT-03**: ExpertRunner orchestration class for parallel subagent execution
- [x] **EXPT-04**: Context isolation in expert prompts (no cross-expert references)
- [x] **EXPT-05**: Statistical enforcement prompt with Chinese rules to prevent LLM hallucination
- [x] **EXPT-06**: Unique output file per expert in output/experts/ directory
- [x] **EXPT-07**: verify_code_execution function validates code block presence
- [x] **EXPT-08**: Conflict detection for numerical (>10% diff) and recommendation (opposite directions) conflicts
- [x] **CLAR-01**: BusinessClarifier with skip option for optional intent clarification
- [x] **CLAR-02**: 3 core questions: goal, audience, metrics
- [x] **CLAR-03**: Business context written to output/experts/business_context.md
- [x] **CLAR-04**: skip=True parameter to bypass clarification flow
- [x] **CLAR-05**: Complexity threshold trigger (score > 2)

### Active

**Phase 1: Data Understanding Layer**
- [ ] **DATA-01**: Auto-load Excel/CSV/JSON data files
- [ ] **DATA-02**: Output data overview (dimensions, fields, statistical summary, missing rate)
- [ ] **DATA-03**: Integrate data-analyst TUI Python toolchain (pandas/numpy/matplotlib)
- [ ] **DATA-04**: Identify data type (table/advertising/time_series) and match analysis methods
- [ ] **DATA-05**: Output preliminary insights (1-2 trends or anomalies)

**Phase 2: Data Processing Engine**
- [ ] **PROC-01**: Data validation and quality checks
- [ ] **PROC-02**: Data transformation pipeline
- [ ] **PROC-03**: Feature extraction for analysis

**Phase 4: Report Generation Layer**
- [ ] **REP-01**: HTML report generation (default output)
- [ ] **REP-02**: PPT generation (HTML→PPTX conversion, on explicit request)
- [ ] **REP-03**: 11 design style choices (FT/McKinsey/Economist/Goldman/Swiss + 6 styles)
- [ ] **REP-04**: Chinese-first output, conclusion-style titles
- [ ] **REP-05**: Integration from management analyst perspective (no expert names)
- [ ] **REP-06**: Key metrics panel + themed deep analysis + comprehensive conclusions

**基础设施**
- [ ] **INF-01**: Python 依赖管理（requirements.txt）
- [ ] **INF-02**: 跨平台路径处理（消除硬编码 Windows 路径）
- [ ] **INF-03**: 日志框架替代 print 语句
- [ ] **INF-04**: Git 版本控制初始化

### Out of Scope

- **实时数据接入** — 仅处理静态文件（Excel/CSV/JSON），不接入数据库或 API 实时流
- **英文报告生成** — v1 保持中文优先，英文支持放入 v2
- **自定义设计风格** — v1 使用现有 11 种风格，自定义参数放入 v2
- **数据清洗工具** — 假设用户已准备好数据，不做清洗预处理
- **自动化部署** — 作为 Claude Code skill 使用，不独立部署

## Context

**现有代码库状态：**
- `huashu-data-pro-extracted/` 包含完整的 skill 源码（SKILL.md + scripts + references）
- 现有 Python 分析脚本：analyze_data.py、behavior_analysis.py、data_overview.py 等
- 现有 JSON 数据文件：data_info.json、matched_final.json、final_matched.json
- 无测试覆盖、无依赖管理、无版本控制

**技术债务（从 CONCERNS.md）：**
- 5 个脚本硬编码 Windows 路径
- 200+ print 语句替代日志框架
- 零测试覆盖
- 全局 warning suppression

**参考资源：**
- huashu-data-pro SKILL.md（核心方法论）
- data-analyst TUI prompts.ts（精简 prompt 设计）
- html-templates.md（可视化组件库）
- report-style-gallery.md（设计风格库）

## Constraints

- **Tech Stack**: Python 3.10+（数据分析）、Node.js 18+（PPT 生成）、Claude Code skill 运行环境
- **Dependencies**: pandas、numpy、matplotlib、seaborn、openpyxl、python-pptx、pptxgenjs、playwright
- **Runtime**: Claude Code CLI 环境调用，subagent 并行执行
- **Language**: 中文输出优先，保留专业术语英文（ROI、CapEx、FCF 等）

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 增强现有 skill | huashu-data-pro 已有完整架构，增量开发更高效 | ✓ Good |
| Phase 0 可选交互 | 简单任务可跳过，避免过度流程化 | — Pending |
| 自动理解模式 | 用户直接提供数据，skill 自动识别类型和方法 | — Pending |
| 正式报告优先 | 目标用户是业务/管理层，汇报场景为主 | ✓ Good |
| 中文优先输出 | 目标用户中文环境，保留专业术语英文 | ✓ Good |
| 保持 11 种风格库 | 已验证的设计系统，无需重新设计 | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-06-04 after Phase 03 analysis-engine completion*