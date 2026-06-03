# Architecture Patterns: AI-Powered Data Analysis Skill

**Domain:** AI-powered data analysis skill/framework
**Researched:** 2026-06-03
**Confidence:** HIGH (based on existing codebase patterns + multi-agent framework research)

---

## High-Level Architecture Pattern

**Recommended Pattern: Orchestrator-Workers with Phase-Gated Workflow**

The AI-powered data analysis skill follows a **phase-gated orchestrator-workers pattern**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR (Claude Code Skill)                      │
│                                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐                 │
│  │ Phase 0  │ → │ Phase 1  │ → │ Phase 2  │ → │ Phase 3  │                 │
│  │ Clarify  │   │ Understand│   │ Analyze  │   │ Report   │                 │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘                 │
│       │              │              │              │                        │
│       ▼              ▼              ▼              ▼                        │
│  [User Input]   [Data Files]  [Subagents]    [Templates]                   │
└─────────────────────────────────────────────────────────────────────────────┘
         │              │              │              │
         └──────────────┴──────────────┴──────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        │                 STATE LAYER               │
        │  .planning/context.md (Phase 0 output)   │
        │  Data cache, analysis results, config    │
        └───────────────────────────────────────────┘
```

**Why this pattern:**

| Aspect | Pattern Choice | Rationale |
|--------|---------------|-----------|
| **Orchestration** | Central skill orchestrator | Claude Code skill provides natural coordination point for phases |
| **Parallelism** | Worker subagents in Phase 2 | Multiple expert analyses benefit from parallel execution with context isolation |
| **Gating** | Phase boundaries with explicit state | Each phase produces artifacts that become inputs for next phase |
| **Flexibility** | Optional Phase 0 | Simple tasks can skip clarification and go directly to data understanding |

**Alternative patterns considered:**

| Pattern | Why Not Used |
|---------|--------------|
| **Monolithic Pipeline** | No parallel execution; difficult to isolate expert contexts |
| **Event-Driven Architecture** | Over-engineered for batch analysis use case; adds complexity without benefit |
| **Microservices** | Deployment overhead; skill runs in single Claude Code environment |

---

## Component Breakdown

### Phase 0: Business Intent Clarification Layer

**Purpose:** Optional interactive clarification to align analysis with business goals.

```
┌─────────────────────────────────────────────────────┐
│                  Phase 0 Component                   │
├─────────────────────────────────────────────────────┤
│  Input:  User's initial request + data file(s)      │
│  Output: .planning/context.md                      │
│                                                     │
│  ┌─────────────┐   ┌─────────────┐                │
│  │ Clarification│   │  Decision   │                │
│  │   Questions  │ → │   Router    │                │
│  │   Engine    │   │             │                │
│  └─────────────┘   └─────────────┘                │
│         │                  │                        │
│         ▼                  ▼                        │
│    [3 Core Questions]  [Skip/Proceed]              │
│    1. Analysis goal?                                │
│    2. Report audience?                              │
│    3. Key metrics?                                  │
└─────────────────────────────────────────────────────┘
```

**Components:**

| Component | Responsibility | Implementation |
|-----------|---------------|----------------|
| **Clarification Engine** | Generate context-appropriate questions | LLM prompt with business context awareness |
| **Decision Router** | Determine if clarification needed or skip to Phase 1 | Heuristic: explicit goals + audience = skip |
| **Context Writer** | Persist clarification results | Write to `.planning/context.md` |

**State:**
- Input: Raw user request
- Output: Structured context file with analysis goals, audience, metrics

---

### Phase 1: Data Understanding Layer

**Purpose:** Automatic data profiling and initial insight generation.

```
┌─────────────────────────────────────────────────────┐
│                  Phase 1 Component                   │
├─────────────────────────────────────────────────────┤
│  Input:  Data file(s) + .planning/context.md       │
│  Output: Data profile + Initial insights            │
│                                                     │
│  ┌─────────────┐   ┌─────────────┐   ┌──────────┐ │
│  │   Data      │   │   Type      │   │ Insight  │ │
│  │   Loader    │ → │  Detector   │ → │ Generator│ │
│  └─────────────┘   └─────────────┘   └──────────┘ │
│         │                  │                  │     │
│         ▼                  ▼                  ▼     │
│    [pandas/openpyxl] [Table/Ad/Time Series]  [LLM] │
└─────────────────────────────────────────────────────┘
```

**Components:**

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| **Data Loader** | Read Excel/CSV/JSON files | `pandas`, `openpyxl` |
| **Schema Profiler** | Extract dimensions, fields, types, missing rates | `pandas.describe()`, custom profiling |
| **Type Detector** | Classify data type (table/ad-spend/time-series) | Rule-based heuristics + LLM classification |
| **Statistics Generator** | Compute summary statistics | `numpy`, `scipy` |
| **Insight Generator** | Surface 1-2 initial trends/anomalies | LLM with statistical context |

**Data Type Detection Logic:**

```
IF has_date_column AND has_metrics AND has_dimensions:
    IF has_ad_spend OR has_impressions OR has_ctr:
        type = "ad_spend_analysis"
    ELIF has_recurring_user_ids:
        type = "user_behavior_analysis"
    ELSE:
        type = "time_series_analysis"
ELIF has_transactions OR has_financial_metrics:
    type = "financial_analysis"
ELSE:
    type = "general_table_analysis"
```

**Output Artifacts:**
- Data profile JSON (schema, statistics, quality issues)
- Initial insights markdown (1-2 trends or anomalies)
- Data type classification

---

### Phase 2: Multi-Expert Analysis Layer

**Purpose:** Parallel deep analysis from multiple domain perspectives.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Phase 2 Component                             │
├─────────────────────────────────────────────────────────────────────┤
│  Input:  Data + context.md + data type + initial insights            │
│  Output: Expert analysis files (one per subagent)                   │
│                                                                      │
│  ┌──────────────┐                                                   │
│  │    Expert    │                                                   │
│  │   Selector   │                                                   │
│  └──────┬───────┘                                                   │
│         │                                                            │
│         ▼                                                            │
│  ┌──────────────────────────────────────────────┐                   │
│  │         Expert Role Definitions              │                   │
│  │  (Write to expert-roles.md for user review) │                   │
│  └──────────────────────────────────────────────┘                   │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │  Subagent 1 │  │  Subagent 2 │  │  Subagent 3 │  ... (parallel)  │
│  │ (Quant)     │  │ (Growth)    │  │ (Risk)      │                 │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                 │
│         │                │                │                         │
│         ▼                ▼                ▼                         │
│  [analysis_1.md]  [analysis_2.md]  [analysis_3.md]                 │
└─────────────────────────────────────────────────────────────────────┘
```

**Components:**

| Component | Responsibility | Implementation |
|-----------|---------------|----------------|
| **Expert Selector** | Choose 3-5 domain experts based on data type | LLM with expert role library |
| **Role Definition Writer** | Write expert personas for user confirmation | Markdown file generation |
| **Subagent Orchestrator** | Launch parallel subagents with isolated context | Task tool with `run_in_background=true` |
| **Analysis Aggregator** | Collect subagent outputs | File read + synthesis |

**Expert Role Selection Matrix:**

| Data Type | Expert Roles (pick 3-5) |
|-----------|------------------------|
| **Financial/Stock** | Quantitative Analyst, Valuation Expert, Industry Analyst, Macro Economist, Behavioral Finance Expert |
| **Ad Spend/Marketing** | Ad Optimization Specialist, User Growth Expert, ROI Analyst, Brand Strategist, Finance Analyst |
| **User Behavior** | User Researcher, Product Manager, Data Scientist, Behavioral Psychologist, Growth Hacker |
| **Operations** | Operations Expert, Process Optimizer, Quality Manager, Cost Analyst, Industry Consultant |
| **Market Research** | Industry Analyst, Competitive Strategy Expert, Consumer Insights Expert, Trend Researcher, Pricing Specialist |

**Subagent Prompt Structure:**

```markdown
## Role Definition
你是 [专家角色]，[一句话专业背景]。

## Task
分析以下数据文件：
- [文件路径]

## Data Overview
[粘贴Phase 1的数据概览摘要]

## Analysis Direction
[该角色在Phase 2中陈述的分析方向]

## Specific Tasks
1. [任务1：具体分析任务]
2. [任务2：具体分析任务]
3. [任务3：具体分析任务]

## Output Requirements
将分析结果写入：[指定输出路径]
结构：
1. 核心发现（3-5条，带具体数字）
2. 详细分析（每个任务一节）
3. 关键数据表
4. 图表建议
```

**Context Isolation Pattern:**

Each subagent receives:
- Role definition (unique perspective)
- Data file paths (shared)
- Data overview (shared context)
- Analysis tasks (role-specific)
- Output path (isolated file)

No subagent sees other subagents' outputs during analysis phase.

---

### Phase 3: Report Generation Layer

**Purpose:** Synthesize expert analyses into unified, audience-appropriate report.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Phase 3 Component                            │
├─────────────────────────────────────────────────────────────────┤
│  Input:  Expert analysis files + context.md + style preference  │
│  Output: HTML report (default) or PPTX (on request)            │
│                                                                 │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐          │
│  │   Theme     │   │  Synthesis  │   │   Report    │          │
│  │   Organizer │ → │   Engine    │ → │  Generator  │          │
│  └─────────────┘   └─────────────┘   └─────────────┘          │
│         │                  │                  │                 │
│         ▼                  ▼                  ▼                 │
│    [Cross-validate] [Manager POV]    [HTML/PPTX]              │
│    [Identify gaps]  [融合叙事]        [11 styles]              │
└─────────────────────────────────────────────────────────────────┘
```

**Components:**

| Component | Responsibility | Implementation |
|-----------|---------------|----------------|
| **Theme Organizer** | Group findings by theme, not by expert | LLM clustering of insights |
| **Cross-Validator** | Identify contradictions between experts | Pattern matching on conclusions |
| **Synthesis Engine** | Merge analyses into coherent narrative | LLM with manager perspective prompt |
| **Style Selector** | Choose from 11 design styles | LLM choice or user specification |
| **HTML Generator** | Generate styled HTML report | Template engine + inline SVG/JS charts |
| **PPTX Converter** | Convert HTML to PowerPoint (optional) | `pptxgenjs`, `playwright` |

**Report Structure:**

```html
1. 标题（结论式中文）
2. 核心摘要（5条核心发现）
3. 关键指标面板（4-6个大数字）
4. 分主题深度分析（融合多专家视角）
5. 综合结论与建议
6. 页脚（中文）
```

**Critical Rule:** No expert names appear in final report. All insights presented from unified "senior analyst" perspective.

**Style System:**

| Category | Styles | Use Case |
|----------|--------|----------|
| **Classic Financial** | Financial Times, McKinsey, Economist, Goldman Sachs, Swiss/NZZ | Professional reports, board presentations |
| **Design-focused** | Stamen, Fathom, Sagmeister & Walsh, Takram, Irma Boom, Build | Creative reports, brand presentations |

---

## Data Flow Diagram

```
┌──────────────┐
│   User       │
│   Request    │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│                     PHASE 0: CLARIFY                          │
│  ┌────────────────┐         ┌─────────────────┐              │
│  │ User Intent    │────────▶│ .planning/      │              │
│  │ Analysis       │         │ context.md      │              │
│  └────────────────┘         └─────────────────┘              │
│                                     │                         │
└─────────────────────────────────────┼─────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────┐
│                     PHASE 1: UNDERSTAND                       │
│  ┌────────────────┐   ┌─────────────┐   ┌───────────────┐   │
│  │ Data Files     │──▶│ Profile     │──▶│ Data Profile   │   │
│  │ (Excel/CSV)    │   │ Engine      │   │ JSON          │   │
│  └────────────────┘   └─────────────┘   └───────────────┘   │
│                              │                               │
│                              ▼                               │
│                       ┌─────────────┐                       │
│                       │ Initial     │                       │
│                       │ Insights    │                       │
│                       └─────────────┘                       │
└──────────────────────────────────────┬───────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────┐
│                     PHASE 2: ANALYZE                          │
│  ┌────────────────┐   ┌─────────────────┐                    │
│  │ Expert Roles   │──▶│ expert-roles.md │                    │
│  │ Definition     │   │ (user confirms) │                    │
│  └────────────────┘   └─────────────────┘                    │
│          │                                                    │
│          ▼                                                    │
│  ┌────────────────────────────────────────────┐              │
│  │         PARALLEL SUBAGENTS                  │              │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐      │              │
│  │  │Expert 1 │ │Expert 2 │ │Expert 3 │      │              │
│  │  │Analysis │ │Analysis │ │Analysis │      │              │
│  │  └────┬────┘ └────┬────┘ └────┬────┘      │              │
│  └───────┼───────────┼───────────┼───────────┘              │
│          │           │           │                           │
│          ▼           ▼           ▼                           │
│    ┌──────────┐ ┌──────────┐ ┌──────────┐                   │
│    │analysis_1│ │analysis_2│ │analysis_3│                   │
│    │   .md    │ │   .md    │ │   .md    │                   │
│    └──────────┘ └──────────┘ └──────────┘                   │
└──────────────────────────────────────┬───────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────┐
│                     PHASE 3: REPORT                           │
│  ┌────────────────┐   ┌─────────────┐   ┌───────────────┐   │
│  │ Aggregate      │──▶│ Synthesize  │──▶│ HTML Report   │   │
│  │ Analyses       │   │ (Manager    │   │ (styled)      │   │
│  │                │   │  POV)       │   │               │   │
│  └────────────────┘   └─────────────┘   └───────────────┘   │
│                                             │                │
│                                             ▼                │
│                                      ┌─────────────┐        │
│                                      │ PPTX (opt)  │        │
│                                      └─────────────┘        │
└──────────────────────────────────────────────────────────────┘
```

---

## Integration Points

### Claude Code Skill Integration

```
┌─────────────────────────────────────────────────────────┐
│                  Claude Code Environment                 │
│                                                         │
│  ┌──────────────┐    ┌──────────────┐                  │
│  │   SKILL.md   │◀──▶│   Claude     │                  │
│  │  (Triggers)  │    │   Sonnet     │                  │
│  └──────────────┘    └──────┬───────┘                  │
│                             │                            │
│                             ▼                            │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Task Tool (Subagents)               │   │
│  │  - subagent_type: "general-purpose"              │   │
│  │  - run_in_background: true (parallel)            │   │
│  │  - prompt: [role + context + tasks]              │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Trigger Keywords:** "分析数据", "做报告", "做PPT", "Excel", "投放分析", "ROI", "复盘", "周报", "月报"

**Skill Activation Flow:**
1. User mentions trigger keyword
2. SKILL.md loads with methodology
3. Phase determination (skip Phase 0 if goals explicit)
4. Sequential phase execution with state persistence

### Python Tool Integration

```
┌─────────────────────────────────────────────────────────┐
│                   Python Runtime                         │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   pandas     │  │   numpy      │  │   scipy      │   │
│  │  (data I/O)  │  │ (computing)  │  │ (statistics) │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  openpyxl    │  │  matplotlib  │  │   seaborn    │   │
│  │  (Excel)     │  │  (charts)    │  │  (viz)       │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Analysis Scripts                     │   │
│  │  - data_overview.py (Phase 1 profiling)          │   │
│  │  - statistical_analysis.py (Phase 2 analysis)    │   │
│  │  - behavior_analysis.py (Phase 2 expert)         │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### HTML/PPT Generation Pipeline

```
┌─────────────────────────────────────────────────────────┐
│                Report Generation                         │
│                                                         │
│  ┌──────────────┐                                       │
│  │  Analysis    │                                       │
│  │  Results     │                                       │
│  │  (Markdown)  │                                       │
│  └──────┬───────┘                                       │
│         │                                               │
│         ▼                                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │              HTML Generator                        │   │
│  │  - Template selection (11 styles)                 │   │
│  │  - Chart generation (SVG/ECharts/D3.js)          │   │
│  │  - Layout rendering (responsive grid)            │   │
│  └──────────────────────────┬───────────────────────┘   │
│                             │                            │
│                   ┌────────┴────────┐                   │
│                   ▼                 ▼                    │
│           ┌─────────────┐    ┌─────────────┐            │
│           │ HTML Report │    │ PPTX (opt)  │            │
│           │  (default)  │    │ Node.js     │            │
│           └─────────────┘    │ pptxgenjs   │            │
│                             │ playwright   │            │
│                             └─────────────┘            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Multi-Agent Subagent Architecture

### Pattern: Parallel Worker Subagents with Context Isolation

```
┌─────────────────────────────────────────────────────────────────┐
│                     Orchestrator Agent                          │
│  (Main Claude Sonnet Instance - SKILL.md context)              │
│                                                                 │
│  Responsibilities:                                              │
│  - Phase sequencing                                            │
│  - Expert role selection                                       │
│  - Subagent coordination                                       │
│  - Result synthesis                                            │
│  - Report generation                                           │
└─────────────────────────────────────────────────────────────────┘
           │                    │                    │
           │ Task Tool          │ Task Tool          │ Task Tool
           │ (background)       │ (background)       │ (background)
           ▼                    ▼                    ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │ Subagent 1  │      │ Subagent 2  │      │ Subagent 3  │
    │             │      │             │      │             │
    │ Context:    │      │ Context:    │      │ Context:    │
    │ - Role def  │      │ - Role def  │      │ - Role def  │
    │ - Data path │      │ - Data path │      │ - Data path │
    │ - Tasks    │      │ - Tasks     │      │ - Tasks     │
    │            │      │             │      │             │
    │ ISOLATED:  │      │ ISOLATED:   │      │ ISOLATED:   │
    │ No cross-  │      │ No cross-   │      │ No cross-   │
    │ talk       │      │ talk        │      │ talk        │
    └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
           │                    │                    │
           ▼                    ▼                    ▼
    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │analysis_1.md│      │analysis_2.md│      │analysis_3.md│
    └─────────────┘      └─────────────┘      └─────────────┘
           │                    │                    │
           └────────────────────┴────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │ Aggregation Point   │
                    │ (Back to            │
                    │  Orchestrator)      │
                    └─────────────────────┘
```

**Why Context Isolation:**

| Benefit | Description |
|---------|-------------|
| **Perspective Purity** | Each expert analyzes from their domain without contamination from other perspectives |
| **Parallel Efficiency** | 3-5 analyses run simultaneously vs. sequentially |
| **Quality Assurance** | Each subagent receives complete context in prompt - no shared state corruption |
| **Debuggability** | Each analysis is a separate file - easy to inspect individual expert reasoning |

**Subagent Communication Pattern:**

```
Orchestrator → Subagent: Full context in prompt (one-way)
Subagent → Orchestrator: Analysis file (one-way)
Subagent ↔ Subagent: NO COMMUNICATION
```

**Wait Strategy:**

```python
# Pseudocode for orchestrator
subagents = [
    launch_subagent(role="quant_analyst", data=profile),
    launch_subagent(role="growth_expert", data=profile),
    launch_subagent(role="risk_analyst", data=profile)
]

# All launch with run_in_background=true
# Orchestrator waits for all to complete
results = wait_for_all(subagents)

# Then synthesizes
synthesis = aggregate_and_synthesize(results)
```

---

## Build Order Suggestions

### Recommended Phase Sequence

```
Phase 0 (Clarify) ──────▶ Phase 1 (Understand) ─────▶ Phase 2 (Analyze) ─────▶ Phase 3 (Report)
     │                         │                         │                         │
     │                         │                         │                         │
     ▼                         ▼                         ▼                         ▼
[Optional]              [Required]               [Required]               [Required]
     │                         │                         │                         │
     ▼                         ▼                         ▼                         ▼
context.md              data_profile.json        analysis_*.md            report.html
                        initial_insights.md      (multiple)               report.pptx
```

### Dependency Graph

```
Phase 0 ──────┐
              │
              ▼
Phase 1 ◀─────┘───┐
                   │
                   ▼
Phase 2 ◀──────────┘───┐
                       │
                       ▼
Phase 3 ◀──────────────┘
```

### Component Build Order

| Order | Component | Dependencies | Est. Complexity |
|-------|-----------|--------------|-----------------|
| 1 | Data Loader (Phase 1) | None | Low |
| 2 | Schema Profiler (Phase 1) | Data Loader | Low |
| 3 | Type Detector (Phase 1) | Schema Profiler | Medium |
| 4 | Statistics Generator (Phase 1) | Data Loader | Low |
| 5 | Insight Generator (Phase 1) | Statistics + Type | Medium |
| 6 | Expert Selector (Phase 2) | Type Detector | Medium |
| 7 | Subagent Orchestrator (Phase 2) | Expert Selector | High |
| 8 | Analysis Aggregator (Phase 2) | Subagent outputs | Medium |
| 9 | Theme Organizer (Phase 3) | Analysis files | Medium |
| 10 | Synthesis Engine (Phase 3) | Theme groups | High |
| 11 | Style Selector (Phase 3) | None | Low |
| 12 | HTML Generator (Phase 3) | Synthesis + Style | Medium |
| 13 | PPTX Converter (Phase 3) | HTML Generator | Medium |
| 14 | Clarification Engine (Phase 0) | None | Medium |

**Parallel Development Opportunities:**

- Components 1-5 (Phase 1) can be built independently
- Components 14 (Phase 0) can be built in parallel with Phase 1
- Components 9-12 (Phase 3) can start while Phase 2 subagents are running

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Shared Mutable State Between Subagents

**What goes wrong:** Subagents read from shared state object, leading to race conditions and inconsistent analysis.

**Why it happens:** Developers used to traditional multi-threading patterns.

**Consequences:** Expert perspectives bleed into each other; analyses become redundant or contradictory.

**Prevention:** Each subagent receives complete context in prompt; writes to isolated file; no shared state.

**Detection:** Check that no subagent output references another subagent's findings during Phase 2.

---

### Anti-Pattern 2: Sequential Expert Analysis

**What goes wrong:** Running experts one-by-one instead of in parallel.

**Why it happens:** Simpler implementation; familiar pattern.

**Consequences:** 3-5x slower execution; orchestrator context accumulates across analyses, biasing later experts.

**Prevention:** Use `run_in_background=true` for all subagents; wait for all before synthesis.

**Detection:** Measure Phase 2 execution time; should be ~constant regardless of expert count (within limits).

---

### Anti-Pattern 3: Expert Names in Final Report

**What goes wrong:** Final report attributes insights to specific experts (e.g., "The quant analyst found...").

**Why it happens:** Natural tendency to credit sources; easier to write.

**Consequences:** Undermines unified manager perspective; feels fragmented; not board-ready.

**Prevention:** Synthesis step explicitly removes expert attribution; rewrites as unified findings.

**Detection:** Grep final report for expert role names; should return 0 matches.

---

### Anti-Pattern 4: Skip Phase 1 for "Simple" Data

**What goes wrong:** Jumping directly to Phase 2 without data profiling.

**Why it happens:** Assumption that "simple" data doesn't need understanding.

**Consequences:** Experts analyze wrong columns; miss data quality issues; produce irrelevant insights.

**Prevention:** Phase 1 is always required; Phase 0 is optional.

**Detection:** Check that Phase 2 subagent prompts include data profile summary.

---

### Anti-Pattern 5: Monolithic Analysis Script

**What goes wrong:** Single Python script does all analysis instead of using subagent architecture.

**Why it happens:** Familiarity with traditional data analysis scripts.

**Consequences:** Single perspective; no parallel execution; difficult to extend with new expert types.

**Prevention:** Follow Phase 2 subagent pattern; use Task tool for orchestration.

**Detection:** Check Phase 2 implementation; should use Task tool with background subagents.

---

## Scalability Considerations

| Concern | At 1 User | At 100 Users | At Enterprise |
|---------|-----------|--------------|---------------|
| **Subagent Parallelism** | 3-5 concurrent | Queue-based execution | Distributed worker pool |
| **Context Window** | Fits in Sonnet 200K | May need compression | Implement checkpointing |
| **File Storage** | Local filesystem | Shared volume | S3/object storage |
| **Style Customization** | 11 built-in styles | + User preferences | + Enterprise branding |

---

## Sources

**HIGH Confidence:**
- Existing codebase: `huashu-data-pro/SKILL.md` - Multi-expert methodology
- Existing codebase: `workflows.md` - Subagent orchestration pattern
- LangChain docs: Multi-agent patterns, orchestrator-workers
- CrewAI docs: Agent coordination, sequential/hierarchical processes

**MEDIUM Confidence:**
- Web search: Phase-based workflow patterns (general AI/ML patterns, not specific to analysis skills)
- Web search: Report generation pipeline best practices (general software patterns)

**Verified Against:**
- LangChain documentation: https://docs.langchain.com/oss/python/langchain/overview
- CrewAI documentation: https://docs.crewai.com/core-concepts/agents
- Existing SKILL.md methodology