from pycui_utils.categories import Categories
from pycui_utils.models import Category


class Organizations:
    """Container for organization codes extracted from categories."""

    def __init__(self, categories_obj: Categories):
        self._categories = categories_obj
        self._organization_codes = self._extract_organization_codes()

    def _extract_organization_codes(self) -> list[str]:
        """Extract unique organization codes from categories."""
        org_codes = {cat.organization_code for cat in self._categories.all()}
        return sorted(org_codes)

    def all(self) -> list[str]:
        """Get all organization codes."""
        return self._organization_codes

    def categories(self, organization_code: str) -> list[Category]:
        """Get all categories for a specific organization."""
        return self._categories.get_by_organization(organization_code)
