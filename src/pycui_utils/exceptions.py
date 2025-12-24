__all__ = ["PyCUIError", "DatabaseLoadError", "CategoryNotFoundError"]


class PyCUIError(Exception):
    """Base exception for all pycui-utils errors."""


class DatabaseLoadError(PyCUIError):
    """Raised when database loading fails."""


class CategoryNotFoundError(PyCUIError):
    """Raised when a requested category is not found."""
