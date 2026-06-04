# src/config/logging_config.py
"""
Centralized logging configuration for Automated Data Analysis Framework.

Usage:
    from config.logging_config import setup_logging

    if __name__ == '__main__':
        setup_logging(level=logging.INFO, log_file='output/analysis.log')
"""

import logging
import sys
from pathlib import Path


def setup_logging(level=logging.INFO, log_file=None):
    """
    Configure logging for the project.

    Args:
        level: Logging level (default: logging.INFO)
        log_file: Optional path to log file. Parent directories created automatically.

    Creates:
        - StreamHandler(sys.stdout) for console output
        - FileHandler if log_file is provided

    Format:
        %(asctime)s - %(name)s - %(levelname)s - %(message)s
    """
    handlers = [logging.StreamHandler(sys.stdout)]

    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=handlers,
        force=True
    )