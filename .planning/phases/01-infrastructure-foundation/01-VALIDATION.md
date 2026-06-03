---
phase: 1
slug: infrastructure-foundation
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-03
---

# Phase 1 -- Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x (Wave 0 installs) |
| **Config file** | none -- Wave 0 installs |
| **Quick run command** | `pytest tests/ -q --tb=short` |
| **Full suite command** | `pytest tests/ -v --cov=src` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/ -q --tb=short`
- **After every plan wave:** Run `pytest tests/ -v --cov=src`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

> **Note:** Plan 01 (Wave 0) creates a consolidated `tests/test_infrastructure.py` covering all INF requirements. This single file replaces the per-requirement file approach for simpler test management.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 0 | INF-01 | - | N/A | unit | `pytest tests/test_infrastructure.py::test_requirements_locked -q` | Yes (Wave 0) | pending |
| 01-01-02 | 01 | 0 | INF-02 | - | N/A | unit | `pytest tests/test_infrastructure.py::test_paths_cross_platform -q` | Yes (Wave 0) | pending |
| 01-01-03 | 01 | 0 | INF-03 | - | N/A | unit | `pytest tests/test_infrastructure.py::test_logging_levels -q` | Yes (Wave 0) | pending |
| 01-01-04 | 01 | 0 | INF-04 | - | N/A | unit | `pytest tests/test_infrastructure.py::test_gitignore_patterns -q` | Yes (Wave 0) | pending |
| 01-01-05 | 01 | 0 | INF-05 | - | N/A | unit | `pytest tests/test_infrastructure.py::test_no_macosx_artifacts -q` | Yes (Wave 0) | pending |
| 01-02-01 | 02 | 1 | INF-01 | - | N/A | unit | `pytest tests/test_infrastructure.py::test_requirements_locked -q` | Yes (Wave 0) | pending |
| 01-03-01 | 03 | 1 | INF-02 | - | N/A | unit | `pytest tests/test_infrastructure.py::test_paths_cross_platform -q` | Yes (Wave 0) | pending |
| 01-04-01 | 04 | 2 | INF-04 | - | N/A | integration | `pytest tests/test_infrastructure.py::test_gitignore_patterns -q` | Yes (Wave 0) | pending |
| 01-05-01 | 05 | 2 | INF-05 | - | N/A | lint | `claude-code skill-validate` | N/A | pending |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

- [x] `tests/test_infrastructure.py` -- consolidated test file covering INF-01 through INF-05 (created by Plan 01)
- [x] `tests/conftest.py` -- shared fixtures (created by Plan 01)
- [x] `pytest.ini` -- pytest configuration (created by Plan 01)
- [ ] `pip install pytest pytest-cov` -- framework install (Plan 01 Task 1)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Cross-platform execution on macOS/Linux | INF-02 | No macOS/Linux environment available | 1. Push to GitHub 2. Run CI on multiple platforms 3. Verify no path errors |
| Skill metadata validation | INF-05 | Claude Code internal validation | Run `claude-code skill-validate` CLI command |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending