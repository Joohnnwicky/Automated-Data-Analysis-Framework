"""
Memory-safe processing utilities for large datasets.

Provides memory estimation, chunked loading, and sampling for datasets
that exceed memory thresholds (DATA-06 requirement).

Threat mitigations:
- T-2-04: 500MB file size limit prevents denial of service
- T-2-11: Memory exhaustion limited by chunked processing
"""

import logging
from pathlib import Path
from typing import Dict, Any, Union

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# DATA-06 thresholds
MEMORY_THRESHOLD_ROWS = 100000  # 100K rows
MEMORY_THRESHOLD_BYTES = 500 * 1024 * 1024  # 500MB


def estimate_memory(filepath: Path, sample_rows: int = 1000) -> int:
    """
    Estimate total memory usage by sampling rows.

    Loads a sample of rows, calculates memory usage per row,
    then estimates total memory based on file line count.

    Args:
        filepath: Path to the CSV file to estimate
        sample_rows: Number of rows to sample (default: 1000)

    Returns:
        Estimated total memory usage in bytes (int)

    Note:
        Uses memory_usage(deep=True) for accurate string memory estimation.
        Logs the estimation result at INFO level.
    """
    # Load sample rows
    df_sample = pd.read_csv(filepath, nrows=sample_rows)

    # Calculate memory usage per row
    sample_memory = df_sample.memory_usage(deep=True).sum()
    estimated_per_row = sample_memory / sample_rows

    # Count total lines (fast file iteration in binary mode)
    with open(filepath, 'rb') as f:
        total_lines = sum(1 for _ in f)

    # Estimate total memory
    estimated_memory = int(estimated_per_row * total_lines)

    logger.info(
        f'Estimated memory: {estimated_memory / 1024 / 1024:.1f}MB '
        f'for {total_lines} rows'
    )

    return estimated_memory


def load_with_chunking(
    filepath: Path,
    chunksize: int = 10000
) -> Union[pd.DataFrame, Dict[str, Any]]:
    """
    Load large file in chunks and aggregate statistics.

    For files under the memory threshold, loads directly.
    For larger files, processes in chunks and returns a profile
    dictionary instead of the full DataFrame.

    Args:
        filepath: Path to the CSV file to load
        chunksize: Number of rows per chunk (default: 10000)

    Returns:
        - pd.DataFrame for small files (estimated < 500MB)
        - Dict with profile statistics for large files

    Note:
        Profile dict contains:
        - total_rows: Total number of rows
        - columns: List of column names
        - column_profiles: Dict of column statistics
        - processing_mode: 'chunked'
        - chunk_size: Chunk size used

    Threat mitigation (T-2-11):
        unique_approx set limited to 100 items per column to prevent
        memory growth during chunked processing.
    """
    estimated_memory = estimate_memory(filepath)

    if estimated_memory < MEMORY_THRESHOLD_BYTES:
        # Small file: load directly
        logger.info(
            f'Loading directly (estimated {estimated_memory / 1024 / 1024:.1f}MB)'
        )
        return pd.read_csv(filepath)

    # Large file: chunked processing
    logger.info(
        f'Using chunked loading (estimated {estimated_memory / 1024 / 1024:.1f}MB)'
    )

    chunks = pd.read_csv(filepath, chunksize=chunksize)
    total_rows = 0
    column_stats: Dict[str, Dict[str, Any]] = {}

    for chunk in chunks:
        total_rows += len(chunk)

        for col in chunk.columns:
            if col not in column_stats:
                column_stats[col] = {
                    'dtype': str(chunk[col].dtype),
                    'null_count': 0,
                    'unique_approx': set()
                }

            column_stats[col]['null_count'] += chunk[col].isna().sum()

            # Limit unique_approx set size to prevent memory growth (T-2-11)
            if len(column_stats[col]['unique_approx']) < 100:
                column_stats[col]['unique_approx'].update(
                    chunk[col].dropna().head(50).unique()
                )

    # Build profile dict
    profile = {
        'total_rows': total_rows,
        'columns': list(column_stats.keys()),
        'column_profiles': column_stats,
        'processing_mode': 'chunked',
        'chunk_size': chunksize
    }

    logger.info(f'Chunked profile complete: {total_rows} rows')

    return profile


def sample_large_dataset(
    filepath: Path,
    sample_size: int = 50000
) -> pd.DataFrame:
    """
    Sample large dataset for analysis.

    For datasets under the sample size, loads directly.
    For larger datasets, uses random sampling via skiprows.

    Args:
        filepath: Path to the CSV file to sample
        sample_size: Target sample size (default: 50000)

    Returns:
        Sampled pandas DataFrame

    Note:
        Uses probabilistic skiprows for random sampling.
        Logs the sampling operation at INFO level.
    """
    # Count total lines (fast file iteration in binary mode)
    with open(filepath, 'rb') as f:
        total_lines = sum(1 for _ in f)

    if total_lines <= sample_size:
        # Small dataset: load directly
        logger.info(
            f'Small dataset ({total_lines} rows), loading directly'
        )
        return pd.read_csv(filepath)

    # Calculate skip probability
    skip_prob = (total_lines - sample_size) / total_lines

    # Random sampling using skiprows
    df = pd.read_csv(
        filepath,
        skiprows=lambda i: i > 0 and np.random.random() < skip_prob
    )

    logger.info(f'Sampled {len(df)} rows from {total_lines} total')

    return df