"""pycui-utils"""

from pycui_utils.categories import Categories
from pycui_utils.filters import BasicCategories, SpecialCategories
from pycui_utils.models import Category, CategoryData
from pycui_utils.organizations import Organizations

__all__ = [
    # Models
    "Category",
    "CategoryData",
    # Main classes
    "Categories",
    "Organizations",
    # Convenience instances
    "categories",
    "organizations",
    "special_categories",
    "basic_categories",
]

categories = Categories()
organizations = Organizations(categories)
special_categories = SpecialCategories(categories)
basic_categories = BasicCategories(categories)
