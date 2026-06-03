# Technology Stack — Data Analyst Pro

**Project:** AI-powered data analysis skill (merged huashu-data-pro + data-analyst TUI)
**Researched:** 2026-06-03
**Mode:** Ecosystem research for greenfield project

---

## Executive Summary

This stack recommendation balances **proven stability** with **2025/2026 modern best practices**. The core data analysis layer uses mature, well-maintained libraries (pandas 3.0, numpy 2.4) while the AI integration layer leverages Claude API's structured output capabilities. Key decision: **Do NOT chase bleeding-edge alternatives** — pandas remains the industry standard with 3.0's Apache Arrow backend addressing historical performance concerns.

**Confidence:** HIGH for core stack (versions verified from PyPI), MEDIUM for AI integration patterns (based on Claude API docs + ecosystem patterns).

---

## AI/LLM Integration Stack

### Claude API Integration

| Component | Version/Method | Purpose | Rationale | Confidence |
|-----------|----------------|---------|-----------|------------|
| **Claude API** | Latest (claude-sonnet-4-6 or claude-opus-4-8) | Core LLM for analysis | Best-in-class for structured reasoning, tool use, Chinese language | HIGH |
| **Tool Use** | Native Anthropic API | Structured function calling | Guarantees schema conformance with `strict: true` | HIGH |
| **JSON Mode** | Tool-based (not native) | Enforce structured output | Use tool with JSON schema + `tool_choice: {"type": "tool", "name": "..."}` | HIGH |
| **Pydantic** | 2.13.4 | Schema validation | Type-safe schemas for Claude API calls, input validation | HIGH |

### Prompt Design Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| **Chain of Thought** | Complex analysis tasks | "Let's think step by step about this data..." |
| **Role Prompting** | Multi-expert analysis | "As a quantitative analyst, analyze ROI trends..." |
| **Structured Output** | Report generation | Tool with JSON schema → guaranteed structure |
| **Context Injection** | Business intent clarification | Pre-populate system prompt with clarified context |

### Subagent Architecture

```
Main Agent (Orchestrator)
├── Business Intent Clarifier (Phase 0)
├── Data Understanding Agent (Phase 1)
├── Expert Analysis Agents (Phase 2, parallel):
│   ├── Quantitative Analyst
│   ├── Valuation Expert
│   ├── Growth Expert
│   └── Industry Analyst
└── Report Generator (Phase 3)
```

**Key Pattern:** Each subagent operates with **isolated context** to prevent cross-contamination of analysis perspectives.

### Anti-Patterns (AI Integration)

| Anti-Pattern | Why Bad | Instead |
|--------------|---------|---------|
| **Unstructured prompts for structured output** | Parsing fragility | Use tool use with JSON schema |
| **Single monolithic prompt** | Context explosion, loss of focus | Multi-agent decomposition |
| **No validation layer** | API changes break downstream | Pydantic models for all inputs/outputs |
| **Hardcoded model names** | Model deprecation breaks code | Config-driven model selection |

---

## Data Processing Stack

### Core DataFrame Layer

| Library | Version | Purpose | Rationale | Confidence |
|---------|---------|---------|-----------|------------|
| **pandas** | 3.0.3 | Primary DataFrame library | Industry standard, 3.0+ has Apache Arrow backend, massive ecosystem | HIGH |
| **numpy** | 2.4.6 | Numerical computing | Foundation layer, 2.x has breaking changes but better performance | HIGH |
| **polars** | 1.41.2 (optional) | High-performance alternative | **Use only for:** >1M row datasets, performance-critical pipelines | MEDIUM |

**Decision: pandas as default, polars as opt-in**

**Why pandas 3.0:**
- Apache Arrow backend addresses historical memory concerns
- Zero-copy interoperability with DuckDB, polars
- Massive ecosystem (plotting, I/O, ML integration)
- Python 3.11+ requirement aligns with modern stack

**When to use polars:**
- Dataset >1M rows and performance is critical
- Lazy evaluation needed for complex pipelines
- Memory-constrained environments

**When NOT to use polars:**
- Small-to-medium datasets (<100K rows) — pandas simpler
- Heavy matplotlib/seaborn integration — pandas more natural
- Team unfamiliar with Rust ecosystem debugging

### Statistical Analysis

| Library | Version | Purpose | Rationale |
|---------|---------|---------|-----------|
| **scipy** | 1.17.1 | Statistical tests, optimization | Standard library for scientific computing |
| **statsmodels** | 0.14.4 (latest) | Time series, regression | More advanced statistical modeling than scipy alone |

### Data Validation & I/O

| Library | Version | Purpose | Rationale |
|---------|---------|---------|-----------|
| **pydantic** | 2.13.4 | Data validation | Type-safe schemas for all structured data |
| **openpyxl** | 3.1.5 | Excel I/O | Production-stable, supports xlsx/xlsm/xltx/xltm |
| **python-pptx** | 1.0.2 | PowerPoint generation | Industry standard, mature API |

### Chinese NLP

| Library | Version | Purpose | Rationale |
|---------|---------|---------|-----------|
| **jieba** | 0.42.1 | Chinese text segmentation | Most popular, stable, supports custom dictionaries |

**Note:** jieba hasn't been updated since 2020. Consider **pkuseg** or **lac** for active maintenance, but jieba remains sufficient for basic segmentation.

---

## Visualization & Reporting Stack

### Chart Generation (HTML Reports)

| Library | Version | Purpose | Rationale | Confidence |
|---------|---------|---------|-----------|------------|
| **matplotlib** | 3.10.9 | Static charts, publication-quality | Foundation library, full control | HIGH |
| **seaborn** | 0.13.2 | Statistical visualization | High-level API over matplotlib | HIGH |
| **plotly** | 6.7.0 | Interactive charts | Best for HTML reports, hover/zoom | HIGH |

**Recommendation:** Use **plotly** for HTML reports (interactive), **matplotlib/seaborn** for static images in PPTX.

### HTML Report Generation

| Component | Purpose | Rationale |
|-----------|---------|-----------|
| **Jinja2** | HTML templating | Standard Python templating, easy to maintain |
| **Chart.js** (via CDN) | Lightweight interactive charts | CDN delivery, no build step |
| **Custom CSS** | Design system implementation | 11 design styles from huashu-data-pro |

**Anti-Patterns (HTML Reports):**
| Anti-Pattern | Why Bad | Instead |
|--------------|---------|---------|
| **Embedding large datasets in HTML** | Page load time, memory | Lazy load, pagination |
| **No responsive design** | Mobile unusable | CSS grid/flexbox |
| **Inline CSS everywhere** | Maintainability nightmare | CSS variables, design tokens |

### PPTX Generation

| Approach | Purpose | Rationale |
|----------|---------|-----------|
| **python-pptx** (Python) | Direct PPTX creation | Full control, template support |
| **pptxgenjs** (Node.js) | HTML→PPTX conversion | Existing skill uses this |

**Recommendation:** Keep **both** paths:
1. **Python path:** Direct data → PPTX (no HTML intermediate)
2. **Node.js path:** HTML → PPTX (for design-rich slides)

### Design System

| Component | Purpose | Implementation |
|-----------|---------|----------------|
| **11 Design Styles** | Professional report aesthetics | CSS templates from huashu-data-pro |
| **Design Tokens** | Consistent colors/typography | CSS variables per style |
| **Chart Templates** | Style-matched visualizations | Plotly themes mapped to design styles |

---

## Infrastructure Stack

### Dependency Management

| Tool | Purpose | Rationale |
|------|---------|-----------|
| **uv** | Python package management | 10-100x faster than pip, modern resolver |
| **requirements.txt** | Dependency declaration | Simple, universal |
| **.python-version** | Python version pinning | Ensures 3.11+ |

**Anti-Patterns:**
| Anti-Pattern | Why Bad | Instead |
|--------------|---------|---------|
| **No requirements.txt** | Dependency hell | Pin all versions |
| **Global pip install** | Environment conflicts | Virtual environments |
| **`pip install -U *`** | Breaks reproducibility | Pin versions, test upgrades explicitly |

### Logging

| Library | Version | Purpose | Rationale |
|---------|---------|---------|-----------|
| **structlog** | Latest (24.4.0+) | Structured logging | JSON output, context binding, better than stdlib logging |
| **rich** | 13.9.4+ | Console formatting | Beautiful CLI output for skill execution |

**Pattern:**
```python
import structlog

log = structlog.get_logger()
log.info("analysis_started", dataset=filename, rows=len(df))
```

### Configuration

| Library | Purpose | Rationale |
|---------|---------|-----------|
| **pydantic-settings** | Settings management | Type-safe config, env var support |

---

## Skill Development Stack

### Claude Code Skill Architecture

| Component | Purpose | Best Practice |
|-----------|---------|---------------|
| **SKILL.md** | Skill definition | Clear intent, trigger conditions, capabilities |
| **prompts/** | LLM prompts | Modular, parameterized, version-controlled |
| **scripts/** | Utility scripts | Python for data, Node.js for PPTX |
| **references/** | Knowledge base | Domain-specific knowledge files |

### Skill Design Patterns

| Pattern | Purpose | Example |
|---------|---------|---------|
| **Phase-based workflow** | Structured analysis | Phase 0: Intent → Phase 1: Data → Phase 2: Analysis → Phase 3: Report |
| **Subagent isolation** | Parallel expert analysis | Each expert gets fresh context, no cross-talk |
| **Context injection** | Business intent propagation | `.planning/context.md` injected into all phases |
| **Output contracts** | Guaranteed structure | Tool schemas for each phase output |

### Anti-Patterns (Skill Development)

| Anti-Pattern | Why Bad | Instead |
|--------------|---------|---------|
| **Monolithic skill** | Hard to debug, extend | Modular phases, clear boundaries |
| **No error handling** | Silent failures | Explicit error types, user-visible messages |
| **Hardcoded paths** | Portability | Relative paths, config-driven |
| **No versioning** | Breaking changes | Semantic versioning in SKILL.md |

---

## Recommended Stack Summary

### Tier 1: Must Have (Core)

```txt
# requirements.txt
pandas==3.0.3
numpy==2.4.6
scipy==1.17.1
openpyxl==3.1.5
python-pptx==1.0.2
pydantic==2.13.4
pydantic-settings==2.8.3
structlog==24.4.0
plotly==6.7.0
matplotlib==3.10.9
seaborn==0.13.2
jieba==0.42.1
jinja2==3.1.4
```

### Tier 2: Recommended (Quality of Life)

```txt
rich==13.9.4          # Beautiful CLI output
duckdb==1.5.3         # SQL on DataFrames, large datasets
polars==1.41.2        # High-performance alternative (opt-in)
statsmodels==0.14.4   # Advanced statistics
```

### Tier 3: Node.js (PPTX Path)

```json
{
  "dependencies": {
    "pptxgenjs": "3.12.0",
    "playwright": "1.60.0",
    "sharp": "0.33.5"
  }
}
```

---

## Version Compatibility Matrix

| Library | Python 3.11 | Python 3.12 | Python 3.13 | Python 3.14 |
|---------|-------------|-------------|-------------|-------------|
| pandas 3.0.3 | ✓ | ✓ | ✓ | ✓ |
| numpy 2.4.6 | ✓ | ✓ | ✓ | ✓ |
| scipy 1.17.1 | ✓ | ✓ | ✓ | ✓ |
| polars 1.41.2 | ✓ | ✓ | ✓ | ✓ |
| duckdb 1.5.3 | ✓ | ✓ | ✓ | ✓ |

**Recommendation:** Target **Python 3.12** for best library compatibility.

---

## Migration Path from Current Stack

| Current | Target | Migration Effort | Notes |
|---------|--------|------------------|-------|
| Python 3.14.3 | Python 3.12 | Low | 3.14 is bleeding edge, 3.12 is stable |
| Hardcoded paths | Config-driven | Medium | Refactor to use pydantic-settings |
| print statements | structlog | Medium | Replace 200+ print statements |
| No requirements.txt | requirements.txt | Low | Create from pip freeze, pin versions |
| No git | Git repo | Low | `git init`, add .gitignore |

---

## Sources & Confidence Levels

| Source | URL | Confidence | Topic |
|--------|-----|------------|-------|
| PyPI | https://pypi.org/project/pandas/ | HIGH | pandas version |
| PyPI | https://pypi.org/project/numpy/ | HIGH | numpy version |
| PyPI | https://pypi.org/project/polars/ | HIGH | polars version |
| PyPI | https://pypi.org/project/python-pptx/ | HIGH | python-pptx version |
| PyPI | https://pypi.org/project/openpyxl/ | HIGH | openpyxl version |
| PyPI | https://pypi.org/project/scipy/ | HIGH | scipy version |
| PyPI | https://pypi.org/project/matplotlib/ | HIGH | matplotlib version |
| PyPI | https://pypi.org/project/seaborn/ | HIGH | seaborn version |
| PyPI | https://pypi.org/project/plotly/ | HIGH | plotly version |
| PyPI | https://pypi.org/project/pydantic/ | HIGH | pydantic version |
| PyPI | https://pypi.org/project/playwright/ | HIGH | playwright version |
| PyPI | https://pypi.org/project/duckdb/ | HIGH | duckdb version |
| Claude API Docs | https://platform.claude.com/docs/en/docs/build-with-claude/tool-use | HIGH | Tool use patterns |
| WebSearch | pandas alternatives 2025 | MEDIUM | Polars vs pandas trends |
| WebSearch | python-pptx best practices | MEDIUM | PPTX generation patterns |
| WebSearch | LLM data analysis agent architecture | MEDIUM | Multi-agent patterns |

---

## Open Questions (Needs Phase-Specific Research)

1. **Chinese report generation quality:** How well does Claude handle Chinese technical writing? (Need to test with actual prompts)
2. **Subagent parallel execution:** Claude API limits? Context isolation patterns? (Need architecture validation)
3. **HTML→PPTX fidelity:** Current Node.js path quality? Should we prioritize Python-only path?
4. **Design system scaling:** 11 styles maintainable? Need design token system?

---

*Stack research completed: 2026-06-03*