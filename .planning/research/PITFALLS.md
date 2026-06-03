# Domain Pitfalls: AI-Powered Data Analysis

**Domain:** AI data analysis skill/framework
**Researched:** 2026-06-03
**Confidence:** MEDIUM (derived from multiple sources; some domain-specific extrapolation)

---

## Executive Summary

AI-powered data analysis projects fail in predictable ways across three dimensions: analysis quality (hallucination, statistical errors), technical implementation (performance, file handling), and user experience (workflow friction, unclear outputs). This project's multi-expert approach introduces additional coordination risks around parallel execution and conclusion synthesis.

**Most critical pitfalls for this project:**
1. LLM statistical reasoning failures (correlation vs. causation, wrong tests)
2. Multi-expert coordination (race conditions, inconsistent conclusions)
3. Report quality variance (buried insights, inconsistent styling)
4. Large dataset memory exhaustion (already present in existing code)
5. Hardcoded paths breaking portability (critical in existing codebase)

---

## Critical Pitfalls

Mistakes that cause rewrites or major issues.

### PITFALL-01: LLM Statistical Reasoning Failures

**What goes wrong:**
LLMs frequently misinterpret statistical results, conflate correlation with causation, apply incorrect statistical tests, and present findings with unwarranted confidence. Research shows LLMs perform poorly on causal inference tasks compared to simple statistical association tasks.

**Why it happens:**
- LLMs pattern-match rather than reason causally
- Training data contains correlation-causation fallacies that get reproduced
- No ground truth for causality encoded in statistical associations alone

**Consequences:**
- Wrong business recommendations (e.g., "increase X to improve Y" when no causal link exists)
- Misleading reports presented to executives with high confidence
- Decisions based on spurious correlations

**Prevention:**
1. **Always use code execution** for statistical calculations—never rely on LLM mental math
2. **Require explicit methodology** before analysis (which test, why, assumptions)
3. **Mandate assumption checks** (normality, independence, sample size requirements)
4. **Include domain expert review** for causal claims
5. **Add explicit disclaimers** when results are correlational

**Detection:**
- Confidence language without numerical support ("clearly," "obviously")
- Causal language ("leads to," "causes") for observational data
- Missing assumption verification (p-value without checking test conditions)
- Conclusions that don't follow from analysis shown

**Phase mapping:** Phase 2 (Multi-expert Analysis Layer) must include methodology validation and assumption checks.

---

### PITFALL-02: Multi-Expert Coordination Failures

**What goes wrong:**
Parallel expert agents can produce contradictory conclusions, access shared resources incorrectly (race conditions), or develop inconsistent understandings of the same data. Synthesis becomes impossible or produces incoherent reports.

**Why it happens:**
- No locking mechanism for shared file access
- Agents don't share context about what others discovered
- Different experts interpret the same data differently
- Synthesis layer forced to reconcile irreconcilable conclusions

**Consequences:**
- Report contradicts itself across sections
- Experts reach opposite recommendations
- File corruption from concurrent writes
- User confusion from inconsistent analysis

**Prevention:**
1. **Implement context isolation**: Each expert writes to separate file, no shared mutable state
2. **Add synthesis layer validation**: Check for contradictions before integrating
3. **Use structured output format**: Enforce consistent schema for expert outputs
4. **Document expert perspectives**: Explicitly state viewpoint assumptions
5. **Sequential synthesis**: Read all expert outputs, then synthesize (don't let experts see each other's work in parallel mode)

**Detection:**
- Two experts recommend opposite actions
- Same metric reported with different values
- File write errors or corrupted outputs
- Synthesis layer unable to reconcile viewpoints

**Phase mapping:** Phase 2 (Multi-expert Analysis Layer) requires explicit coordination architecture; Phase 3 (Report Generation) needs contradiction detection.

---

### PITFALL-03: Hardcoded Paths Breaking Portability

**What goes wrong:**
Scripts contain absolute file paths specific to original developer's machine. Code fails immediately on any other system.

**Why it happens:**
- Quick prototyping without refactoring
- No configuration file pattern established
- Developer assumes single-user environment

**Consequences:**
- **CRITICAL: Already present in codebase**—all 5 analysis scripts hardcode `C:\Users\hello\Downloads\...`
- Cannot share code with team members
- CI/CD impossible
- Any user other than original author gets immediate crash

**Prevention:**
1. **Use command-line arguments**: `argparse` for input/output paths
2. **Create config file**: `config.yaml` for project-level settings
3. **Use pathlib**: Cross-platform path handling
4. **Validate paths early**: Check existence before processing

**Detection:**
- Absolute paths with user-specific directories
- Scripts that work only on one machine
- No `argparse` or config file usage

**Phase mapping:** Phase 0 (Infrastructure) must address this before any feature development.

---

### PITFALL-04: LLM Hallucination of Data Points

**What goes wrong:**
LLMs generate plausible-sounding but completely fabricated data points, statistics, or trends. Numbers look reasonable but have no basis in the actual data.

**Why it happens:**
- LLMs predict next token, not verify accuracy
- Pattern completion creates "reasonable" numbers
- No grounding in actual data when generating text

**Consequences:**
- Reports contain invented statistics
- Business decisions made on fake data
- Loss of trust when errors discovered

**Prevention:**
1. **Ground all claims in actual data**: Every numerical claim must trace to data file
2. **Require code execution**: LLM writes Python to calculate, not mental math
3. **Show work**: Include the calculation/code that produced each number
4. **Validate aggregations**: Cross-check sums, averages, counts
5. **Audit trail**: Track which data rows contributed to which conclusions

**Detection:**
- Numbers that don't match data when spot-checked
- Statistics that "sound right" but can't be reproduced
- Claims without supporting code or data references
- Overly round numbers (suspicious precision)

**Phase mapping:** Phase 1 (Data Understanding Layer) must establish grounding; Phase 2 (Analysis) requires code-based calculations.

---

### PITFALL-05: Large Dataset Memory Exhaustion

**What goes wrong:**
Scripts load entire datasets into memory without chunking, causing crashes on large files (>100MB) or memory-constrained systems.

**Why it happens:**
- Default `pd.read_csv()` loads full file
- No memory profiling during development
- Developer tested only on small sample files

**Consequences:**
- **CRITICAL: Already present in codebase**—all analysis scripts use unchunked reads
- Out-of-memory crashes
- System slowdown affecting other processes
- Cannot analyze production-sized datasets

**Prevention:**
1. **Add chunking support**: `pd.read_csv(chunksize=10000)`
2. **Profile memory usage**: Test with large files during development
3. **Use efficient dtypes**: `category` for low-cardinality, downcast numerics
4. **Lazy loading**: Load only needed columns with `usecols`
5. **Document limits**: Specify max dataset size in requirements

**Detection:**
- Memory usage grows linearly with file size
- No `chunksize` parameter in file reading
- Testing only with small sample files

**Phase mapping:** Phase 1 (Data Understanding Layer) must include memory-efficient patterns.

---

## Moderate Pitfalls

### PITFALL-06: Buried Insights in Reports

**What goes wrong:**
Key findings are hidden in lengthy reports without clear executive summary or visual hierarchy. Decision-makers miss the most important information.

**Why it happens:**
- No structured report format enforced
- Linear narrative without prioritization
- Analysts include everything, bury the critical

**Prevention:**
1. **Lead with conclusions**: Executive summary at top with 3-5 key findings
2. **Use conclusion-style headers**: "Revenue increased 23% due to new channel"
3. **Visual hierarchy**: Bold key numbers, use callout boxes
4. **Invert pyramid**: Most important first, supporting details later
5. **Limit section length**: Force prioritization through space constraints

**Phase mapping:** Phase 3 (Report Generation Layer) must enforce report structure.

---

### PITFALL-07: Incorrect Chart Selection

**What goes wrong:**
LLM or analysis code selects inappropriate visualization types (pie chart for time series, 3D charts that distort perception, wrong axis scales).

**Why it happens:**
- No domain knowledge encoded in chart selection logic
- Default chart choices without data type consideration
- Aesthetic preferences over communication effectiveness

**Consequences:**
- Misleading visualizations
- Audience misinterpretation
- Loss of credibility when errors noticed

**Prevention:**
1. **Chart type mapping**: Encode rules (time series → line chart, comparison → bar, distribution → histogram)
2. **Avoid problematic chart types**: Ban 3D charts, truncated axes, dual-axis (unless justified)
3. **Human review for complex visualizations**: Flag non-standard charts for review
4. **Axis validation**: Check that zero-baseline is used where appropriate

**Phase mapping:** Phase 3 (Report Generation) needs chart type validation.

---

### PITFALL-08: Numerical Precision Errors

**What goes wrong:**
LLMs perform mental arithmetic incorrectly, or floating-point precision issues create wrong results in calculations.

**Why it happens:**
- LLMs cannot reliably do arithmetic
- Floating-point precision in aggregations
- Rounding errors compound across calculations

**Prevention:**
1. **Never trust LLM calculations**: All math via Python code execution
2. **Use appropriate precision**: Round only at final display, not intermediate steps
3. **Validate totals**: Sum of parts should equal whole
4. **Decimal for financial data**: Use `decimal.Decimal` for currency

**Phase mapping:** Phase 1 (Data Understanding) and Phase 2 (Analysis) must use code-based calculations.

---

### PITFALL-09: Inconsistent Report Styling

**What goes wrong:**
Reports generated from templates show inconsistent formatting, font sizes, color schemes, or layout across runs or sections.

**Why it happens:**
- Multiple template sources
- Dynamic content breaking layout
- No style enforcement validation

**Prevention:**
1. **Single source of truth for styles**: One CSS/template file
2. **Template validation**: Check output against style guide
3. **Automated visual diff**: Compare generated reports to reference
4. **Lock styling elements**: Prevent dynamic modification of key styles

**Phase mapping:** Phase 3 (Report Generation) must have single style source.

---

### PITFALL-10: Missing Value Handling Errors

**What goes wrong:**
Analysis produces wrong results because `NaN` values are mishandled—ignored, incorrectly imputed, or contaminating calculations.

**Why it happens:**
- `NaN != NaN` returns True (comparison fails)
- Aggregations silently skip NaN without warning
- Mean imputation distorts distributions

**Prevention:**
1. **Explicit missing value policy**: Document how each analysis handles missing data
2. **Check missingness first**: `df.isna().sum()` before any analysis
3. **Use `pd.isna()` not `== NaN`**: Correct comparison method
4. **Consider impact**: Document how imputation affects conclusions
5. **Warn about high missingness**: Flag columns with >10% missing

**Phase mapping:** Phase 1 (Data Understanding) must surface missingness patterns.

---

### PITFALL-11: Tool Format Mismatches

**What goes wrong:**
LLM generates tool calls in wrong format, with incorrect parameters, or with hallucinated capabilities.

**Why it happens:**
- Tool documentation unclear or incomplete
- LLM forgets available tools
- Complex schemas confuse the model

**Prevention:**
1. **Clear tool documentation**: Include examples, edge cases, input format requirements
2. **Validate inputs before execution**: Check types, ranges, required fields
3. **Simple tool interfaces**: Avoid complex nested schemas
4. **Explicit tool boundaries**: Clearly separate what each tool does

**Phase mapping:** All phases need validated tool interfaces.

---

### PITFALL-12: Context Window Overflow

**What goes wrong:**
Long analyses or large datasets exceed context window limits, causing the model to "forget" earlier parts of the analysis.

**Why it happens:**
- Accumulating conversation history
- Large dataset samples in context
- No summarization strategy

**Prevention:**
1. **Chunk large datasets**: Process in segments, summarize intermediate results
2. **Summarize progress**: Periodically consolidate findings
3. **Prioritize context**: Only include essential information
4. **Use file-based state**: Write important findings to files, reference them

**Phase mapping:** Phase 2 (Multi-expert Analysis) must manage context per expert.

---

## Minor Pitfalls

### PITFALL-13: Print-Based Output Instead of Logging

**What goes wrong:**
Extensive `print()` statements create I/O overhead and cannot be disabled or redirected.

**Why it happens:**
- Quick debugging during development
- No logging framework introduced
- **Already present: 200+ print statements in codebase**

**Prevention:**
1. **Replace with logging module**: `logging.info()`, `logging.debug()`
2. **Add verbosity levels**: Control output detail
3. **Log to file**: Persistent record for debugging
4. **Remove debug prints**: Clean up before production

---

### PITFALL-14: Silent Exception Handling

**What goes wrong:**
`except Exception: pass` swallows all errors, hiding real problems from users.

**Why it happens:**
- Developer didn't know how to handle specific error
- Quick fix during prototyping
- **Already present: Image extraction in read_pptx.py**

**Prevention:**
1. **Log exceptions**: Never silently ignore
2. **Handle specific exceptions**: `except FileNotFoundError`, not bare `Exception`
3. **Inform user**: Explain what failed and why

---

### PITFALL-15: No Dependency Version Pinning

**What goes wrong:**
Code works with one library version but breaks when dependencies update.

**Why it happens:**
- No `requirements.txt` with version constraints
- Testing only with one environment
- **Already present: No requirements.txt in codebase**

**Prevention:**
1. **Pin versions**: `pandas==2.0.0` not `pandas`
2. **Document minimum versions**: Specify tested configurations
3. **Freeze dependencies**: `pip freeze > requirements.txt`

---

### PITFALL-16: Cross-Platform Path Issues

**What goes wrong:**
Paths work on Windows but fail on Linux/macOS due to different separators (`\` vs `/`).

**Why it happens:**
- Hardcoded backslashes
- String concatenation instead of `pathlib`

**Prevention:**
1. **Use pathlib**: `Path('dir') / 'file'` works everywhere
2. **Avoid string concatenation**: No `dir + '\\' + file`
3. **Test on multiple platforms**: CI across OS variants

---

### PITFALL-17: Global Warning Suppression

**What goes wrong:**
`warnings.filterwarnings('ignore')` hides important warnings about deprecated APIs, data quality issues, or configuration problems.

**Why it happens:**
- Developer didn't want to see warnings
- Library produced noisy warnings
- **Already present: All main scripts suppress warnings globally**

**Prevention:**
1. **Suppress specific warnings**: Only target known issues
2. **Fix underlying issues**: Address root cause
3. **Log warnings for review**: Don't hide silently

---

## Phase-Specific Prevention

| Phase | Critical Pitfalls | Prevention Measures |
|-------|-------------------|---------------------|
| **Phase 0: Infrastructure** | PITFALL-03 (Hardcoded paths), PITFALL-15 (Dependencies), PITFALL-16 (Cross-platform) | Implement argparse/config system, create requirements.txt, use pathlib |
| **Phase 1: Data Understanding** | PITFALL-05 (Memory exhaustion), PITFALL-10 (Missing values), PITFALL-04 (Hallucination) | Add chunking, validate missingness, ground all observations in actual data |
| **Phase 2: Multi-expert Analysis** | PITFALL-01 (Statistical errors), PITFALL-02 (Coordination), PITFALL-12 (Context overflow) | Enforce code-based calculations, isolate expert contexts, require methodology validation |
| **Phase 3: Report Generation** | PITFALL-06 (Buried insights), PITFALL-07 (Bad charts), PITFALL-09 (Inconsistent styling) | Enforce report structure, validate chart types, single style source |
| **All Phases** | PITFALL-08 (Precision), PITFALL-11 (Tool format), PITFALL-13 (Logging), PITFALL-14 (Silent errors) | Code-based math, input validation, logging module, exception logging |

---

## Detection Checklist

Use during development and review:

### Before Moving to Next Phase

- [ ] All file paths use argparse or config (not hardcoded)
- [ ] Memory profiling completed with realistic dataset size
- [ ] Missing value analysis documented
- [ ] All numerical claims traceable to source data
- [ ] No `print()` statements in production code
- [ ] No bare `except:` or silent exception handlers
- [ ] Dependencies pinned in requirements.txt

### During Analysis

- [ ] Statistical test assumptions verified before running
- [ ] Causal language only when causally validated
- [ ] Each expert output written to separate file
- [ ] No concurrent writes to same file
- [ ] Context window not approaching limit

### During Report Generation

- [ ] Executive summary lists top 3-5 findings first
- [ ] Chart types appropriate for data types
- [ ] Style consistency verified against template
- [ ] All numbers verified against calculation code
- [ ] No claims without supporting data/code reference

---

## Sources

- **LLM Statistical Reasoning:** Multiple academic studies on causal reasoning in LLMs (2023-2024), showing poor performance on causal inference vs. statistical association tasks
- **Hallucination in Data Analysis:** Industry reports on LLM data analysis failures, pattern completion vs. verification
- **Multi-Agent Coordination:** "A Survey of Multi-Agent Large Language Models" (ArXiv 2024), coordination challenges in parallel execution
- **Pandas Memory Management:** Official pandas documentation on scaling, chunking, and efficient data types
- **Tool Calling Errors:** Anthropic research on building effective agents (anthropic.com/research)
- **Data Visualization Mistakes:** Industry guides on common chart selection errors, misleading visualizations
- **Prompt Engineering for Analysis:** Best practices for LLM data analysis tasks, chain-of-thought prompting
- **Codebase Analysis:** Existing technical debt documented in CONCERNS.md (hardcoded paths, print statements, warning suppression)

**Confidence Levels:**
- LLM limitations (hallucination, statistical errors): HIGH (well-documented in research)
- Multi-agent coordination: MEDIUM (emerging research, some extrapolation)
- Report quality issues: MEDIUM (industry knowledge, project-specific extrapolation)
- Technical implementation pitfalls: HIGH (existing codebase evidence + common patterns)