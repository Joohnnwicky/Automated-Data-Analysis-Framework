# Roadmap — Data Analyst Pro

**Project:** AI-powered data analysis skill
**Mode:** Horizontal Layers
**Created:** 2026-06-03

## Overview

Data Analyst Pro is an enhanced data analysis skill that merges huashu-data-pro's report generation capabilities with data-analyst TUI's exploratory analysis strengths. The build follows a horizontal layers approach: complete technical layers built in sequence, then integrated at the end.

**Core Value:** 让数据分析从「理解业务问题」开始，产出管理层可直接汇报的专业报告

**Build Strategy:** Infrastructure → Data Processing → Analysis Engine → Report Generation → Integration Testing

## Phases

- [ ] **Phase 1: Infrastructure Foundation** - Establish Python toolchain, dependency management, cross-platform paths, logging, and version control
- [ ] **Phase 2: Data Processing Engine** - Build data loader, schema profiler, type detector, and insight generator with memory safety
- [ ] **Phase 3: Analysis Engine** - Implement multi-expert parallel analysis with subagent orchestration and statistical safeguards
- [ ] **Phase 4: Report Generation** - Create HTML/PPT generators with professional design system and synthesis engine
- [ ] **Phase 5: Integration & UX Polish** - End-to-end workflow integration, error handling, and user experience refinements

---

## Phase Details

### Phase 1: Infrastructure Foundation

**Goal:** Establish a clean, maintainable Python toolchain foundation that eliminates technical debt and enables cross-platform execution
**Depends on:** Nothing (first phase)
**Requirements:** INF-01, INF-02, INF-03, INF-04, INF-05
**Success Criteria** (what must be TRUE):

1. All Python dependencies are locked in requirements.txt with exact versions
2. All scripts run on Windows, macOS, and Linux without hardcoded path errors
3. All print statements replaced with structured logging (INFO/WARNING/ERROR levels)
4. Project initialized in Git with proper .gitignore for planning artifacts
5. Skill file structure follows Claude Code conventions with clean metadata

**Plans:** 6 plans in 5 waves
**Pitfalls Addressed:** PITFALL-03 (hardcoded paths), PITFALL-16 (warning suppression)

Plans:
**Wave 1**

- [ ] 01-01-PLAN.md — Wave 0: Test infrastructure scaffold (pytest, conftest, test stubs)
- [ ] 01-02-PLAN.md — Wave 1: Dependency management (requirements.txt, .gitignore)
- [ ] 01-03-PLAN.md — Wave 1: Logging infrastructure (logging_config.py, src/ structure)

**Wave 2** *(blocked on Wave 1 completion)*

- [ ] 01-04-PLAN.md — Wave 2: Path refactoring (move scripts, pathlib, remove warnings)

**Wave 3** *(blocked on Wave 2 completion)*

- [ ] 01-05-PLAN.md — Wave 3: Logging integration (replace print with logger)

**Wave 4** *(blocked on Wave 3 completion)*

- [ ] 01-06-PLAN.md — Wave 4: Cleanup & validation (__MACOSX, tests, obsolete files)

### Phase 2: Data Processing Engine

**Goal:** Users can load data files and receive accurate data profiles with automatic type detection and memory-safe processing
**Depends on:** Phase 1
**Requirements:** DATA-01, DATA-02, DATA-03, DATA-04, DATA-05, DATA-06, DATA-07, UX-04
**Success Criteria** (what must be TRUE):

1. User can load Excel (.xlsx), CSV, and JSON files with automatic encoding detection for Chinese data
2. User sees comprehensive data profile: dimensions, fields, types, missing rates, and statistical summaries
3. System automatically detects data type (table/advertising/time-series) and suggests analysis methods
4. User receives 1-2 initial insights (trends or anomalies) after data load
5. Large datasets (>100K rows) are processed without memory exhaustion via chunking/ sampling
6. User sees clear error messages for unsupported formats or corrupted files

**Plans:** 9 plans in 6 waves

Plans:
**Wave 0** *(test infrastructure - enables Nyquist validation)*

- [x] 02-01a-PLAN.md — Wave 0: Dependencies and test fixtures (charset-normalizer, sample data files)
- [ ] 02-01b-PLAN.md — Wave 0: Test scaffold files (pytest stubs for DATA-01 through DATA-07)

**Wave 1** *(blocked on Wave 0 completion)*

- [ ] 02-02a-PLAN.md — Wave 1: Package structure and encoding detection (DataLoadError, detect_encoding)
- [ ] 02-03a-PLAN.md — Wave 1: Profiling helper functions (profile_dimensions, profile_fields, profile_statistics)

**Wave 2** *(blocked on Wave 1 completion)*

- [ ] 02-02b-PLAN.md — Wave 2: Complete DataLoader (load_file, format loaders, security validation)
- [ ] 02-03b-PLAN.md — Wave 2: Complete DataProfiler (memory optimization, missing strategies, profile method)

**Wave 3** *(blocked on Wave 2 completion)*

- [ ] 02-04-PLAN.md — Wave 3: Type classifier (TypeClassifier, advertising/time-series/table detection)

**Wave 4** *(blocked on Wave 3 completion)*

- [ ] 02-05-PLAN.md — Wave 4: Insight generator (InsightGenerator, trend/anomaly detection)

**Wave 5** *(blocked on Wave 4 completion)*

- [ ] 02-06-PLAN.md — Wave 5: Memory utilities (chunked loading, sampling, memory estimation)
**Pitfalls Addressed:** PITFALL-05 (memory exhaustion), PITFALL-10 (missing value handling), PITFALL-04 (data hallucination)

### Phase 3: Analysis Engine

**Goal:** Users receive multi-perspective analysis from relevant expert roles with statistical rigor and coordination safety
**Depends on:** Phase 2
**Requirements:** EXPT-01, EXPT-02, EXPT-03, EXPT-04, EXPT-05, EXPT-06, EXPT-07, EXPT-08, CLAR-01, CLAR-02, CLAR-03, CLAR-04, CLAR-05
**Success Criteria** (what must be TRUE):

1. User can optionally answer 3 business intent questions (goal, audience, metrics) before analysis
2. System selects 3-5 relevant expert roles based on data type and business context
3. Each expert analyzes data in parallel as isolated subagent with no shared state
4. All numerical conclusions are backed by code execution (no LLM mental math)
5. User can review and adjust expert role definitions before analysis runs
6. User can skip business clarification for simple tasks and proceed directly
7. Conflicting expert conclusions are flagged for user attention

**Plans:** TBD
**Pitfalls Addressed:** PITFALL-01 (LLM statistical reasoning), PITFALL-02 (coordination risks), PITFALL-15 (subagent context leakage)

### Phase 4: Report Generation

**Goal:** Users receive professional HTML/PPT reports with synthesis from multiple expert perspectives in one cohesive narrative
**Depends on:** Phase 3
**Requirements:** REP-01, REP-02, REP-03, REP-04, REP-05, REP-06, REP-07, REP-08, REP-09, REP-10
**Success Criteria** (what must be TRUE):

1. User receives HTML report as default output with embedded visualizations
2. User can request PPT output when explicitly needed (HTML→PPTX conversion)
3. User can select from 11 professional design styles (FT, McKinsey, Economist, Goldman, Swiss, +6 others)
4. Report uses conclusion-style titles ("CapEx doubled, net cash turned negative" not "Capital Expenditure Analysis")
5. Report presents synthesis from manager-POV with no visible expert names, organized by theme
6. Report structure follows: Executive Summary → Key Metrics Panel → Thematic Analysis → Conclusions
7. Charts are automatically matched to data characteristics (no manual selection needed)
8. User sees PDF export hint (Ctrl/Cmd + P) for printing

**Plans:** TBD
**Pitfalls Addressed:** PITFALL-06 (insights buried), PITFALL-07 (chart type mismatch), PITFALL-08 (style drift), PITFALL-09 (output consistency)

### Phase 5: Integration & UX Polish

**Goal:** Users experience smooth end-to-end workflow with clear progress, helpful errors, and intuitive skill invocation
**Depends on:** Phase 4
**Requirements:** UX-01, UX-02, UX-03
**Success Criteria** (what must be TRUE):

1. User can invoke skill with natural keywords ("分析数据", "做报告", "做PPT", "Excel", "投放分析")
2. User receives quick responses for simple queries without full multi-expert workflow
3. User sees progress indicators at each phase transition (Clarify → Understand → Analyze → Report)
4. End-to-end workflow completes successfully from data load to report output
5. User receives helpful error messages for common failure scenarios (file not found, format unsupported, encoding issues)

**Plans:** TBD

---

## Coverage Check

### Requirement to Phase Mapping

| REQ-ID | Phase | Category | Status |
|--------|-------|----------|--------|
| INF-01 | Phase 1 | Infrastructure | Pending |
| INF-02 | Phase 1 | Infrastructure | Pending |
| INF-03 | Phase 1 | Infrastructure | Pending |
| INF-04 | Phase 1 | Infrastructure | Pending |
| INF-05 | Phase 1 | Infrastructure | Pending |
| DATA-01 | Phase 2 | Data Processing | Pending |
| DATA-02 | Phase 2 | Data Processing | Pending |
| DATA-03 | Phase 2 | Data Processing | Pending |
| DATA-04 | Phase 2 | Data Processing | Pending |
| DATA-05 | Phase 2 | Data Processing | Pending |
| DATA-06 | Phase 2 | Data Processing | Pending |
| DATA-07 | Phase 2 | Data Processing | Pending |
| CLAR-01 | Phase 3 | Analysis | Pending |
| CLAR-02 | Phase 3 | Analysis | Pending |
| CLAR-03 | Phase 3 | Analysis | Pending |
| CLAR-04 | Phase 3 | Analysis | Pending |
| CLAR-05 | Phase 3 | Analysis | Pending |
| EXPT-01 | Phase 3 | Analysis | Pending |
| EXPT-02 | Phase 3 | Analysis | Pending |
| EXPT-03 | Phase 3 | Analysis | Pending |
| EXPT-04 | Phase 3 | Analysis | Pending |
| EXPT-05 | Phase 3 | Analysis | Pending |
| EXPT-06 | Phase 3 | Analysis | Pending |
| EXPT-07 | Phase 3 | Analysis | Pending |
| EXPT-08 | Phase 3 | Analysis | Pending |
| REP-01 | Phase 4 | Report | Pending |
| REP-02 | Phase 4 | Report | Pending |
| REP-03 | Phase 4 | Report | Pending |
| REP-04 | Phase 4 | Report | Pending |
| REP-05 | Phase 4 | Report | Pending |
| REP-06 | Phase 4 | Report | Pending |
| REP-07 | Phase 4 | Report | Pending |
| REP-08 | Phase 4 | Report | Pending |
| REP-09 | Phase 4 | Report | Pending |
| REP-10 | Phase 4 | Report | Pending |
| UX-01 | Phase 5 | Integration | Pending |
| UX-02 | Phase 5 | Integration | Pending |
| UX-03 | Phase 5 | Integration | Pending |
| UX-04 | Phase 2 | Data Processing | Pending |

**Coverage:** 39/39 requirements mapped ✓
**Orphaned requirements:** None

### Pitfalls Coverage

| Pitfall ID | Phase | Mitigation |
|------------|-------|------------|
| PITFALL-01 | Phase 3 | Forced code execution, no mental math |
| PITFALL-02 | Phase 3 | Subagent context isolation, independent outputs |
| PITFALL-03 | Phase 1 | pathlib for all paths, cross-platform testing |
| PITFALL-04 | Phase 2 | All numbers backed by code, no hallucination |
| PITFALL-05 | Phase 2 | Chunking/ sampling for large datasets |
| PITFALL-06 | Phase 4 | Mandatory report structure, key insights first |
| PITFALL-07 | Phase 4 | Auto chart type matching |
| PITFALL-08 | Phase 4 | Single style source per report |
| PITFALL-09 | Phase 4 | Output consistency checks |
| PITFALL-10 | Phase 2 | Missing value reporting + strategy suggestions |
| PITFALL-15 | Phase 3 | Subagent context isolation enforcement |
| PITFALL-16 | Phase 1 | Remove global warning suppression |

---

## Progress Tracking

| Phase | Plans Complete | Status | Completed |
|-------|---------------|--------|-----------|
| 1. Infrastructure Foundation | 0/6 | Planning complete | - |
| 2. Data Processing Engine | 1/9 | In progress | 02-01a |
| 3. Analysis Engine | 0/1 | Not started | - |
| 4. Report Generation | 0/1 | Not started | - |
| 5. Integration & UX Polish | 0/1 | Not started | - |

---

*Last updated: 2026-06-03 after Plan 02-01a completion*
