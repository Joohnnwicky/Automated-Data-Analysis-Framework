# tests/test_infrastructure.py
"""
Test scaffolds for INF requirements.
Initially failing - will pass after implementation waves complete.
"""

import pytest
from pathlib import Path


def test_requirements_locked():
    """INF-01: requirements.txt has locked versions."""
    req_file = Path(__file__).parent.parent / 'requirements.txt'
    assert req_file.exists(), "requirements.txt not found at project root"
    content = req_file.read_text(encoding='utf-8')
    # All dependencies should have == locked versions, not >=
    assert '==' in content, "No locked versions found (expected == format)"
    assert '>=' not in content, "Found >= constraints - use == locked versions only"


def test_paths_cross_platform():
    """INF-02: pathlib replaces hardcoded Windows paths."""
    analysis_dir = Path(__file__).parent.parent / 'src' / 'analysis'
    if not analysis_dir.exists():
        # Skip if src/analysis not created yet
        pytest.skip("src/analysis directory not created yet")

    # Files exempt from pathlib requirement (pure data/class definitions)
    exempt_from_pathlib = {
        '__init__.py',      # Package marker
        'expert_roles.py',  # Pure dataclass definitions
        'statistical_enforcement.py',  # Pure prompt string + utility function
    }

    for py_file in analysis_dir.glob('*.py'):
        if py_file.name in exempt_from_pathlib:
            continue
        content = py_file.read_text(encoding='utf-8')
        # Should not contain hardcoded Windows paths
        assert r'C:\Users' not in content, f"Hardcoded C:\\Users path in {py_file.name}"
        assert 'C:\\\\Users' not in content, f"Hardcoded escaped path in {py_file.name}"
        # Should use pathlib
        assert 'from pathlib import Path' in content or 'Path(' in content, \
            f"No pathlib import in {py_file.name}"


def test_logging_levels():
    """INF-03: logging replaces print statements."""
    analysis_dir = Path(__file__).parent.parent / 'src' / 'analysis'
    if not analysis_dir.exists():
        pytest.skip("src/analysis directory not created yet")

    # Files exempt from logging requirement (pure data/class definitions)
    exempt_from_logging = {
        '__init__.py',      # Package marker
        'expert_roles.py',  # Pure dataclass definitions - no runtime operations
        'statistical_enforcement.py',  # Pure utility function - returns bool, no logging needed
    }

    for py_file in analysis_dir.glob('*.py'):
        if py_file.name in exempt_from_logging:
            continue
        content = py_file.read_text(encoding='utf-8')
        # Should import logging
        assert 'import logging' in content, f"No logging import in {py_file.name}"
        # Should have logger instance
        assert 'logger = logging.getLogger(__name__)' in content, \
            f"No logger instance in {py_file.name}"
        # Should not use excessive print() (allow minimal for user output)
        print_count = content.count('print(')
        assert print_count < 5, f"Too many print() in {py_file.name}: {print_count}"


def test_gitignore_patterns():
    """INF-04: .gitignore excludes planning artifacts."""
    gitignore = Path(__file__).parent.parent / '.gitignore'
    assert gitignore.exists(), ".gitignore not found at project root"
    content = gitignore.read_text(encoding='utf-8')
    assert '.planning' in content, ".planning not in .gitignore"
    assert '__MACOSX' in content, "__MACOSX not in .gitignore"


def test_no_macosx_artifacts():
    """INF-05: __MACOSX directories cleaned up."""
    project_root = Path(__file__).parent.parent
    macosx_dirs = list(project_root.rglob('__MACOSX'))
    assert len(macosx_dirs) == 0, f"Found __MACOSX dirs: {macosx_dirs}"