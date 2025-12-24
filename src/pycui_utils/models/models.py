"""Data models for CUI categories."""

from typing import TypedDict


class CategoryData(TypedDict):
    """Type definition for category data from JSON."""

    name: str
    description: str
    is_specified: bool
    index_group: str
    marking_format: str


class Category:
    """Represents a CUI category."""

    __slots__ = ("code", "name", "description", "is_specified", "organization_code", "marking_format")

    def __init__(self, code: str, data: CategoryData):
        self.code = code
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.is_specified = data.get("is_specified", False)
        self.organization_code = data.get("index_group", "")
        self.marking_format = data.get("marking_format", "")

    def __repr__(self) -> str:
        return f"<Category: {self.code} - {self.name}>"

    def __eq__(self, other: object) -> bool:
        """Enable equality comparison."""
        if not isinstance(other, Category):
            return NotImplemented
        return self.code == other.code

    def __hash__(self) -> int:
        """Make Category hashable for use in sets/dicts."""
        return hash(self.code)
