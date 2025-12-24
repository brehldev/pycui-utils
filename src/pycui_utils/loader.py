"""Lazy loading utilities for CUI data."""

import json
from functools import lru_cache
from pathlib import Path

__all__ = ["get_database_path", "load_database"]

from pycui_utils.exceptions import DatabaseLoadError
from pycui_utils.models import CategoryData


@lru_cache(maxsize=1)
def get_database_path() -> Path:
    """Get the path to the CUI database.

    Cached to avoid repeated filesystem operations.
    """
    return Path(__file__).parent / "database" / "cui.json"


@lru_cache(maxsize=1)
def load_database() -> dict[str, CategoryData]:
    """Load the CUI database from JSON.

    Returns:
        Dictionary mapping category codes to category data.

    Raises:
        DatabaseLoadError: If the database cannot be loaded.

    Note:
        Results are cached. For testing, clear cache with load_database.cache_clear()
    """

    try:
        with get_database_path().open(encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise DatabaseLoadError(f"Failed to load CUI database from {get_database_path()}: {e}") from e
