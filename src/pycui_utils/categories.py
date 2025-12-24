from collections.abc import Iterator

from pycui_utils.loader import load_database
from pycui_utils.models import Category

__all__ = ["Categories"]


class Categories:
    """Container for all CUI categories."""

    def __init__(self):
        self._categories: dict[str, Category] = {}
        self._marking_index: dict[str, Category] = {}
        self._org_index: dict[str, list[Category]] = {}

        self._build_indexes()

    def _build_indexes(self) -> None:
        """Build indexes for fast lookups."""
        for code, data in load_database().items():
            category = Category(code, data)

            self._categories[code] = category

            # Index by marking format
            self._marking_index[category.marking_format.lower()] = category

            # Index by organization code
            org_key = category.organization_code.lower()
            if org_key not in self._org_index:
                self._org_index[org_key] = []
            self._org_index[org_key].append(category)

    def get_by_marking(self, marking: str) -> Category | None:
        """Get a category by its marking format."""
        return self._marking_index.get(marking.lower())

    def get_by_organization(self, organization_code: str) -> list[Category]:
        """Get categories belonging to a specific organization."""
        return self._org_index.get(organization_code.lower(), [])

    def all(self) -> list[Category]:
        """Get all categories."""
        return list(self._categories.values())

    def __iter__(self) -> Iterator[Category]:
        return iter(self._categories.values())
