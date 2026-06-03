# Research Summary — Data Analyst Pro

**Project:** AI-powered data analysis skill (huashu-data-pro + data-analyst TUI 融合)
**Researched:** 2026-06-03
**Mode:** Greenfield ecosystem research

---

## Executive Summary

本项目定位明确：**增强版数据分析 skill**，在现有 huashu-data-pro 基础上新增业务意图澄清层，融合 data-analyst TUI 的 Python 工具链优势。研究确认这是可行的且有差异化的方向。

**核心差异化组合（竞争对手未同时提供）：**
1. Phase 0 业务意图澄清前置
2. 多专家并行分析架构
3. 11 种专业报告设计风格
4. 中文优先输出

---

## Stack Summary

### 核心技术栈

| Layer | 选择 | 版本 | Confidence |
|-------|------|------|------------|
| **LLM** | Claude API (Sonnet/Opus) | Latest | HIGH |
| **数据处理** | pandas + numpy | 3.0 / 2.4 | HIGH |
| **可视化** | matplotlib + seaborn | 3.10 / 0.13 | HIGH |
| **Excel 处理** | openpyxl | 3.1 | HIGH |
| **PPT 生成** | pptxgenjs + python-pptx | Latest | MEDIUM |
| **HTML 截图** | Playwright | Latest | HIGH |

### Claude Code Skill 开发模式

```
SKILL.md (skill 定义)
├── scripts/ (Python/Node 工具)
├── references/ (设计参考)
└── workflow: 4 阶段 (Clarify → Understand → Analyze → Report)
```

### Anti-Patterns (不要使用)

- ❌ LangChain/CrewAI — 过度抽象，Claude Code skill 更直接
- ❌ 原生 JS 数据处理 — Python 数据栈更成熟
- ❌ 实时数据库连接 — 保持静态文件分析定位

---

## Features Summary

### Table Stakes (必须实现)

| Feature | Complexity | Dependencies |
|---------|------------|--------------|
| 自然语言查询 | LOW | Python 数据栈 |
| 数据概览 | LOW | pandas |
| 自动可视化 | MEDIUM | matplotlib |
| 基础分析 | LOW | scipy |
| 代码透明 | LOW | Claude tool use |
| 导出能力 | MEDIUM | openpyxl, pptxgenjs |

### Differentiators (差异化特性)

| Feature | Complexity | Dependencies |
|---------|------------|--------------|
| Phase 0 业务意图澄清 | MEDIUM | AskUserQuestion |
| 多专家并行分析 | HIGH | Subagent 架构 |
| 专业报告生成 | HIGH | 设计系统 + synthesis |
| 中文优先 | LOW | Prompt 设计 |

### Anti-Features (明确不做)

- ❌ 实时数据流接入
- ❌ 自定义 Dashboard builder
- ❌ 自动 ML 训练
- ❌ SQL 数据库连接
- ❌ 英文报告生成 (v1)

---

## Architecture Summary

### 核心模式：Orchestrator-Workers

```
┌─────────────────────────────────────────────────────────┐
│              Claude Code Skill (Orchestrator)           │
├─────────────────────────────────────────────────────────┤
│  Phase 0: Business Intent Clarifier                     │
│  → AskUserQuestion (目标/受众/指标)                      │
│  → 写入 .planning/context.md                            │
├─────────────────────────────────────────────────────────┤
│  Phase 1: Data Understanding                            │
│  → Python: Data Loader, Schema Profiler                 │
│  → 输出: 数据概览 + 初步洞察                             │
├─────────────────────────────────────────────────────────┤
│  Phase 2: Multi-Expert Analysis (并行)                  │
│  → Expert Selector (基于 Phase 0/1 结果)                │
│  → 3-5 个 Subagent 并行执行                             │
│  → 每个写入独立 md 文件                                  │
├─────────────────────────────────────────────────────────┤
│  Phase 3: Report Generation                             │
│  → Synthesis Engine (融合多专家结论)                     │
│  → Style Selector (11 种风格)                           │
│  → HTML/PPT Generator                                   │
└─────────────────────────────────────────────────────────┘
```

### 关键设计决策

1. **Subagent 上下文隔离** — 每个专家只看到自己的角色定义和任务
2. **Manager-POV Synthesis** — 最终报告不出现专家名字，按主题整合
3. **Phase-Gated Workflow** — 每阶段产出明确 artifact，作为下一阶段输入

### Build Order

```
Phase 0 (Infrastructure): Python 工具链 — 无依赖，最优先
Phase 1 (Data Understanding): Type Detector, Insight Generator — 依赖 Phase 0
Phase 2 (Multi-Expert): Subagent Orchestrator — 依赖 Phase 1 输出
Phase 3 (Report): Synthesis, Style, HTML/PPT — 依赖 Phase 2 输出
```

---

## Pitfalls Summary

### Critical Pitfalls (必须处理)

| ID | Pitfall | Phase | Prevention |
|----|---------|-------|------------|
| PITFALL-01 | LLM 统计推理不可靠 | Phase 2 | 强制代码计算，禁用 mental math |
| PITFALL-02 | 多专家协调风险 | Phase 2 | 上下文隔离 + 独立输出文件 |
| PITFALL-03 | 硬编码路径 | Phase 0 | 使用 pathlib，配置化路径 |
| PITFALL-04 | 数据幻觉 | Phase 1 | 所有数字必须有代码支撑 |
| PITFALL-05 | 内存耗尽 | Phase 1 | 大数据集 chunking |

### Moderate Pitfalls

| ID | Pitfall | Phase | Prevention |
|----|---------|-------|------------|
| PITFALL-06 | 洞察被埋没 | Phase 3 | 强制报告结构，核心结论前置 |
| PITFALL-07 | 图表类型错配 | Phase 3 | 类型检测 + 图表建议逻辑 |
| PITFALL-10 | 缺失值处理不当 | Phase 1 | 缺失率报告 + 处理策略询问 |

### 现有代码库问题

- ⚠️ 5 个脚本硬编码 Windows 路径 — Phase 0 必须修复
- ⚠️ 无 requirements.txt — Phase 0 添加依赖管理
- ⚠️ 200+ print 语句 — Phase 0 引入 logging
- ⚠️ 零测试覆盖 — 后续添加

---

## Roadmap Implications

### Phase Structure Recommendation

| Phase | Name | Goal | Key Requirements | Risk Level |
|-------|------|------|------------------|------------|
| 1 | Infrastructure | 建立工具链基础 | INF-01~04, PITFALL-03,15,16 | LOW |
| 2 | Business Intent + Data Understanding | Phase 0 + Phase 1 | CLAR-01~04, DATA-01~05 | MEDIUM |
| 3 | Multi-Expert Analysis | Phase 2 核心架构 | EXPT-01~05, PITFALL-01,02 | HIGH |
| 4 | Report Generation | Phase 3 输出层 | REP-01~06, PITFALL-06,07 | HIGH |

### Critical Dependencies

- Phase 2 必须等待 Phase 1 数据概览完成
- Phase 3 必须等待 Phase 2 所有专家分析完成
- Phase 0 (Clarify) 可与 Phase 1 并行开发

### Open Questions (需在规划阶段解决)

1. **大数据集处理** — 100K+ 行数据是否需要 Phase 1 sampling？
2. **专家矛盾处理** — 专家分析矛盾时如何呈现给用户？
3. **错误恢复策略** — Subagent 失败时的处理方式？
4. **PPT 转换可靠性** — HTML→PPTX 转换工具选型？

---

## Files Created

| File | Lines | Content |
|------|-------|---------|
| STACK.md | ~200 | 技术栈推荐 + 版本 + rationale |
| FEATURES.md | ~150 | Table stakes/Differentiators/Anti-features |
| ARCHITECTURE.md | ~180 | Orchestrator-Workers 模式 + 组件定义 |
| PITFALLS.md | ~180 | 17 个陷阱 + 防护策略 + Phase 映射 |

---

## Confidence Assessment

| Area | Level | Notes |
|------|-------|-------|
| Stack Recommendations | HIGH | 版本已验证，成熟组合 |
| Feature Categories | MEDIUM | 竞品分析基于 WebSearch，需实测验证 |
| Architecture Pattern | HIGH | 与现有 skill 方法论一致 |
| Pitfall Identification | MEDIUM | 通用陷阱，需场景化验证 |
| Build Order | HIGH | 依赖关系清晰 |

---

*Synthesized: 2026-06-03*