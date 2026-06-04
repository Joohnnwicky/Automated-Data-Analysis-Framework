---
phase: 02-data-processing-engine
plan: 06
subsystem: data-processing
tags: [memory, chunking, sampling, security, data-loading]
dependency_graph:
  requires: [02-02b, 02-01a]
  provides: [memory-safe-processing]
  affects: [loader.py]
tech_stack:
  added: [numpy-random-sampling, pandas-chunksize]
  patterns: [memory-estimation, chunked-aggregation, probabilistic-sampling]
key_files:
  created: [src/data/memory.py]
  modified: [src/data/loader.py, tests/test_memory.py]
decisions:
  - 500MB memory threshold for chunked processing
  - 50MB threshold for chunking suggestion warning
  - 100 items limit for unique_approx sets (T-2-11 mitigation)
  - 1000 default sample rows for memory estimation
  - 10000 default chunk size for chunked loading
  - 50000 default sample size for large dataset sampling
metrics:
  duration: 4 min
  tasks: 4
  commits: 3
  tests: 11
  completed_date: 2026-06-04
---

# Phase 2 Plan 06: Memory Utilities Summary

## One-Liner

Memory-safe processing utilities with memory estimation, chunked loading, and probabilistic sampling for datasets exceeding memory thresholds (DATA-06 requirement, T-2-04/T-2-11 mitigations).

## Tasks Completed

| Task | Name | Status | Commit |
|------|------|--------|--------|
| 1 | Implement estimate_memory helper function | Complete | 9a5659c |
| 2 | Implement load_with_chunking helper function | Complete | 9a5659c |
| 3 | Implement sample_large_dataset helper function | Complete | 9a5659c |
| 4 | Integrate chunking check into DataLoader | Complete | 9823064 |

## Implementation Details

### Task 1-3: Memory Utilities (src/data/memory.py)

Created `src/data/memory.py` with three core functions:

1. **estimate_memory(filepath, sample_rows=1000)**
   - Loads sample rows via `pd.read_csv(nrows=sample_rows)`
   - Calculates memory usage via `df.memory_usage(deep=True).sum()`
   - Counts total lines via fast binary file iteration
   - Returns estimated total memory in bytes (int)

2. **load_with_chunking(filepath, chunksize=10000)**
   - Checks estimated memory against `MEMORY_THRESHOLD_BYTES` (500MB)
   - Small files (<500MB): loads directly as DataFrame
   - Large files: processes in chunks, aggregates statistics
   - Returns profile dict with: total_rows, columns, column_profiles, processing_mode
   - Threat mitigation (T-2-11): unique_approx sets limited to 100 items

3. **sample_large_dataset(filepath, sample_size=50000)**
   - Counts total lines via binary file iteration
   - Small datasets (<=sample_size): loads directly
   - Large datasets: probabilistic sampling via `skiprows` lambda
   - Returns sampled DataFrame for analysis

**Constants:**
- `MEMORY_THRESHOLD_ROWS = 100000` (DATA-06 threshold)
- `MEMORY_THRESHOLD_BYTES = 500 * 1024 * 1024` (500MB)

### Task 4: DataLoader Integration (src/data/loader.py)

Updated `load_file` function to integrate memory utilities:

- Import `estimate_memory` and `MEMORY_THRESHOLD_BYTES` from memory module
- Added memory estimation check for CSV files
- If estimated_memory > 50MB: log warning suggesting chunked processing
- Existing 500MB hard limit remains enforced (T-2-04 security mitigation)

## Verification Results

```bash
# Module structure verified
ls src/data/memory.py  # EXISTS

# Imports verified
python -c "from src.data.memory import estimate_memory, load_with_chunking, sample_large_dataset"
# OK

# Constants verified
grep "MEMORY_THRESHOLD_ROWS = 100000" src/data/memory.py  # FOUND
grep "MEMORY_THRESHOLD_BYTES = 500" src/data/memory.py    # FOUND

# Tests passed
pytest tests/test_memory.py -v
# 11 passed, 2 skipped

# Integration verified
grep "from src.data.memory import" src/data/loader.py  # FOUND
```

## Deviations from Plan

### Auto-fixed Issues

None - plan executed exactly as written. TDD workflow followed:
1. RED commit: test(02-06) - failing tests added
2. GREEN commit: feat(02-06) - implementation passes all tests
3. Integration commit: feat(02-06) - loader.py integration

## Threat Mitigation Coverage

| Threat ID | Category | Mitigation | Status |
|-----------|----------|------------|--------|
| T-2-04 | Denial of Service | 500MB file size limit in loader.py | ✓ Enforced |
| T-2-11 | Denial of Service | unique_approx set size <100 | ✓ Implemented |
| T-2-12 | Information Disclosure | Profile aggregation only | ✓ Accept |

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| 1000 sample rows for estimation | Balance between accuracy and speed |
| 10000 chunk size | Typical pandas chunking recommendation |
| 50MB warning threshold | Alert before memory becomes critical |
| 100 items unique_approx limit | Prevent unbounded memory growth during chunking |

## Test Coverage

| Test Class | Tests | Purpose |
|------------|-------|---------|
| TestEstimateMemory | 3 | Memory estimation behavior |
| TestLoadWithChunking | 3 | Chunked loading and profile dict |
| TestSampleLargeDataset | 3 | Sampling behavior |
| TestConstants | 2 | Threshold constants verification |

## Self-Check: PASSED

- [x] src/data/memory.py exists
- [x] src/data/loader.py modified
- [x] tests/test_memory.py updated (11 tests)
- [x] Commits: 60a0ba0 (test), 9a5659c (feat), 9823064 (integration)
- [x] DATA-06 requirement complete

---

*Completed: 2026-06-04T01:06:36Z - 2026-06-04T01:10:36Z (4 min)*