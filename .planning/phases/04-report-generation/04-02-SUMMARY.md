---
phase: 04-report-generation
plan: 02
subsystem: styles
tags: [tdd, design-system, css-variables, REP-03, REP-08]
requires: [04-01]
provides: [DesignStyle, DESIGN_STYLES, get_design_style]
affects: [html_report.py, ppt_report.py, templates/base.html]
tech_stack:
  added: []
  patterns: [dataclass, css-custom-properties, single-source-truth]
key_files:
  created: [src/report/styles.py]
  modified: [tests/test_styles.py]
decisions:
  - Use Noto Sans SC for all Chinese fonts (T-4-04 mitigation, SIL open-source license)
  - 7 fields per DesignStyle: id, name, primary_color, secondary_color, font_family, font_family_en, chart_colors
  - CSS variables use '--' prefix with semantic names (--primary-color, --secondary-color)
  - get_design_style raises ValueError for unknown style (explicit error handling)
metrics:
  duration_minutes: 8.5
  completed_date: 2026-06-04
  tdd_commits: 7
  tests_passed: 4
  files_modified: 2
  lines_added: 195
---

# Phase 04 Plan 02: Design Style System Summary

**One-liner:** Implemented DesignStyle dataclass with 11 professional design styles and single-source CSS variable architecture for report generation.

## Completed Tasks

| Task | Name | Commit | Status |
|------|------|--------|--------|
| 1 | Define DesignStyle dataclass | cd594b4 | DONE |
| 2 | Define 11 design styles | c7cef20 | DONE |
| 3 | Implement get_design_style | 9c8362a | DONE |
| 4 | Validate single source CSS | eb8b9c2 | DONE |

## Implementation Details

### DesignStyle Dataclass (REP-03)

Created `src/report/styles.py` with:
- **DesignStyle dataclass** with 7 fields:
  - `id`: Unique identifier (snake_case: 'ft', 'mckinsey', etc.)
  - `name`: Display name ('Financial Times', 'McKinsey', etc.)
  - `primary_color`: Primary color hex code
  - `secondary_color`: Secondary/accent color hex code
  - `font_family`: Chinese font family (Noto Sans SC)
  - `font_family_en`: English font family
  - `chart_colors`: List of 3 chart color hex codes

- **to_css_vars() method** returning CSS custom properties dict:
  - `--primary-color`, `--secondary-color`
  - `--font-family`, `--font-family-en`
  - `--chart-color-1`, `--chart-color-2`, `--chart-color-3`

### 11 Predefined Styles

| ID | Name | Primary | Secondary | Chinese Font | English Font |
|----|------|---------|-----------|--------------|--------------|
| ft | Financial Times | #33302E | #E3120B | Noto Sans SC, serif | Georgia, serif |
| mckinsey | McKinsey | #051C2C | #2DFF99 | Noto Sans SC, sans-serif | Helvetica Neue |
| economist | The Economist | #1D1D1B | #E3120B | Noto Sans SC, serif | Georgia, serif |
| goldman | Goldman Sachs | #0033A0 | #B9B9B9 | Noto Sans SC, sans-serif | Arial, sans-serif |
| swiss | Swiss Design | #000000 | #FF0000 | Noto Sans SC, sans-serif | Helvetica, sans-serif |
| wsj | Wall Street Journal | #333333 | #0066CC | Noto Sans SC, serif | Georgia, serif |
| bloomberg | Bloomberg | #FF6600 | #000000 | Noto Sans SC, sans-serif | Helvetica Neue |
| reuters | Reuters | #FF8000 | #333333 | Noto Sans SC, sans-serif | Arial, sans-serif |
| morningstar | Morningstar | #FFD700 | #333333 | Noto Sans SC, sans-serif | Georgia, serif |
| bcg | BCG | #0033A0 | #2DFF99 | Noto Sans SC, sans-serif | Helvetica Neue |
| bain | Bain & Company | #003366 | #CC0000 | Noto Sans SC, sans-serif | Georgia, serif |

### get_design_style Helper

- Function signature: `get_design_style(style_id: str) -> DesignStyle`
- Searches DESIGN_STYLES by id
- Raises `ValueError(f"Unknown style: {style_id}")` for invalid id
- Used by HTML/PPT report generators to select style

## TDD Gate Compliance

| Gate | Commit | Status |
|------|--------|--------|
| RED (Task 1) | 063572f | test(04-02): add failing test for DesignStyle dataclass |
| GREEN (Task 1) | cd594b4 | feat(04-02): implement DesignStyle dataclass |
| RED (Task 2) | 011dbf0 | test(04-02): add failing test for 11 design styles |
| GREEN (Task 2) | c7cef20 | feat(04-02): add 11 predefined design styles |
| RED (Task 3) | 36f283d | test(04-02): add failing test for get_design_style |
| GREEN (Task 3) | 9c8362a | feat(04-02): implement get_design_style helper |
| GREEN (Task 4) | eb8b9c2 | test(04-02): unskip single source CSS validation test |

**Compliance:** PASS - All RED/GREEN gates present with proper commit sequence.

## Threat Model Mitigations

| Threat | Category | Mitigation | Status |
|--------|----------|------------|--------|
| T-4-04 | Legal | Noto Sans SC for all Chinese fonts (SIL license) | MITIGATED |
| T-4-08 | Tampering | Single source via to_css_vars(), no inline styles | MITIGATED |

## Deviations from Plan

None - plan executed exactly as written.

## Tests Verification

```bash
python -m pytest tests/test_styles.py -xvs
```

**Results:**
- 4 tests passed
- 0 tests skipped
- All REP-03 and REP-08 requirements validated

## Self-Check

| Item | Status |
|------|--------|
| src/report/styles.py exists | PASSED |
| tests/test_styles.py has 4 tests | PASSED |
| All commits present in git log | PASSED |
| 195 lines in styles.py (>= 120) | PASSED |

## Next Steps

- Plan 04-03: Synthesis engine (REP-05, REP-06)
- Plan 04-04: Chart type auto-matching (REP-09)
- Integration: Use DesignStyle in html_report.py templates

---

*Completed: 2026-06-04*
*Duration: 8.5 minutes*