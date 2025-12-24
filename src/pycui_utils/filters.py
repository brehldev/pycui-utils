from abc import ABC, abstractmethod

from pycui_utils.categories import Categories
from pycui_utils.models import Category


class CategoryFilter(ABC):
    """Abstract base class for filtered category collections."""

    def __init__(self, categories_obj: Categories):
        self._categories = categories_obj

    @abstractmethod
    def matches_criteria(self, category: Category) -> bool:
        """Determine if a category matches this filter's criteria."""
        pass

    def all(self) -> list[Category]:
        """Get all categories matching this filter's criteria."""
        return [cat for cat in self._categories.all() if self.matches_criteria(cat)]

    def by_organization(self, organization_code: str) -> list[Category]:
        """Get filtered categories by organization."""
        return [cat for cat in self.all() if cat.organization_code == organization_code]

    def get_by_marking(self, marking: str) -> Category | None:
        """Get filtered categories with a specific marking format."""

        value = [cat for cat in self.all() if cat.marking_format.lower() == marking.lower()]
        return value[0] if value else None


class BasicCategories(CategoryFilter):
    """Basic CUI categories (is_specified=False)."""

    def matches_criteria(self, category: Category) -> bool:
        return not category.is_specified


class SpecialCategories(CategoryFilter):
    """Special CUI categories (is_specified=True)."""

    def matches_criteria(self, category: Category) -> bool:
        return category.is_specified
