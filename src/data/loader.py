"""
Data loading module for Data Analyst Pro.

Provides data loading, encoding detection, and user-friendly error handling.
"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class DataLoadError(Exception):
    """
    Custom exception with user-friendly error messages.

    Attributes:
        user_message: User-friendly error message (Chinese for UX-04)
        technical_detail: Optional technical detail (English)
    """

    def __init__(self, message: str, technical_detail: Optional[str] = None):
        """
        Initialize DataLoadError with message and optional technical detail.

        Args:
            message: User-friendly error message
            technical_detail: Optional technical detail for debugging
        """
        self.user_message = message
        self.technical_detail = technical_detail
        super().__init__(message)