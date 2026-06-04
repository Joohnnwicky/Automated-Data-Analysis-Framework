"""Tests for UX-02 quick response mode requirements.

Tests for should_use_quick_mode and quick_response functions.
"""

import pytest
from pathlib import Path


class TestShouldUseQuickMode:
    """Tests for should_use_quick_mode function (UX-02)."""

    def test_returns_true_for_small_dataset(self):
        """UX-02: Verify quick mode triggered for small dataset (< 100 rows)."""
        pytest.skip("Implementation pending")

    def test_returns_false_for_large_dataset(self):
        """UX-02: Verify quick mode NOT triggered for large dataset (> 100 rows)."""
        pytest.skip("Implementation pending")

    def test_returns_true_for_quick_intent(self):
        """UX-02: Verify quick mode triggered by explicit quick intent."""
        pytest.skip("Implementation pending")

    def test_returns_false_for_complex_type(self):
        """UX-02: Verify quick mode NOT triggered for advertising/time_series data."""
        pytest.skip("Implementation pending")


class TestQuickResponse:
    """Tests for quick_response function (UX-02)."""

    def test_quick_response_returns_string(self):
        """UX-02: Verify quick_response returns formatted string."""
        pytest.skip("Implementation pending")

    def test_quick_response_includes_dimensions(self):
        """UX-02: Verify quick_response includes rows and columns."""
        pytest.skip("Implementation pending")

    def test_quick_response_includes_numeric_stats(self):
        """UX-02: Verify quick_response includes mean and range for numeric fields."""
        pytest.skip("Implementation pending")