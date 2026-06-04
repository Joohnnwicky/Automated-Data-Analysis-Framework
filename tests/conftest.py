# tests/conftest.py
"""
Shared pytest fixtures and path setup for Data Analyst Pro tests.
"""

import pytest
from pathlib import Path
import sys

# Add src to path for imports
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))


@pytest.fixture
def project_root():
    """Provide project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def data_dir(project_root):
    """Provide data directory."""
    data = project_root / 'data'
    data.mkdir(exist_ok=True)
    return data


@pytest.fixture
def output_dir(project_root):
    """Provide output directory."""
    output = project_root / 'output'
    output.mkdir(exist_ok=True)
    return output