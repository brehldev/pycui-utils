"""Comprehensive test suite for Categories class.

This suite acts as the definitive source of truth for the Categories class,
encoding the exact problems it solves and the behavior it guarantees.
"""

from unittest.mock import patch

import pytest

from pycui_utils.loader import load_database
from pycui_utils.models import Category


@pytest.fixture
def mock_database():
    """Mock database with known test data."""
    return {
        "TEST-001": {
            "name": "Test Category One",
            "description": "First test category",
            "is_specified": True,
            "index_group": "TEST_ORG",
            "marking_format": "TEST-001",
        },
        "TEST-002": {
            "name": "Test Category Two",
            "description": "Second test category",
            "is_specified": False,
            "index_group": "TEST_ORG",
            "marking_format": "TEST-002",
        },
        "OTHER-001": {
            "name": "Other Category",
            "description": "Category from different org",
            "is_specified": True,
            "index_group": "OTHER_ORG",
            "marking_format": "OTHER-001",
        },
    }


@pytest.fixture
def mock_empty_database():
    """Mock empty database for boundary testing."""
    return {}


@pytest.fixture
def mock_single_entry_database():
    """Mock database with single entry for boundary testing."""
    return {
        "SINGLE-001": {
            "name": "Single Entry",
            "description": "Only one entry",
            "is_specified": True,
            "index_group": "SINGLE_ORG",
            "marking_format": "SINGLE-001",
        }
    }


@pytest.fixture
def mock_case_sensitive_database():
    """Mock database with various case combinations."""
    return {
        "UPPER-001": {
            "name": "Upper Case",
            "description": "Test upper case",
            "is_specified": True,
            "index_group": "UPPER_ORG",
            "marking_format": "UPPER-001",
        },
        "lower-001": {
            "name": "Lower Case",
            "description": "Test lower case",
            "is_specified": True,
            "index_group": "lower_org",
            "marking_format": "lower-001",
        },
        "MiXeD-001": {
            "name": "Mixed Case",
            "description": "Test mixed case",
            "is_specified": True,
            "index_group": "MiXeD_OrG",
            "marking_format": "MiXeD-001",
        },
    }


@pytest.fixture
def mock_large_database():
    """Mock database with many entries for performance testing."""
    return {
        f"CODE-{i:04d}": {
            "name": f"Category {i}",
            "description": f"Description {i}",
            "is_specified": i % 2 == 0,
            "index_group": f"ORG_{i % 10}",
            "marking_format": f"CODE-{i:04d}",
        }
        for i in range(1000)
    }


def test_should_initialize_and_build_indexes_on_construction(mock_database):
    """Test that Categories builds all indexes during initialization."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        assert len(categories._categories) == 3
        assert len(categories._marking_index) == 3
        assert len(categories._org_index) == 2


def test_should_store_categories_by_code(mock_database):
    """Test that categories are stored and retrievable by their code."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        assert "TEST-001" in categories._categories
        assert categories._categories["TEST-001"].code == "TEST-001"
        assert categories._categories["TEST-001"].name == "Test Category One"


def test_should_get_category_by_marking_format(mock_database):
    """Test retrieval of category by its marking format."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.get_by_marking("TEST-001")

        assert result is not None
        assert result.code == "TEST-001"
        assert result.marking_format == "TEST-001"


def test_should_get_categories_by_organization_code(mock_database):
    """Test retrieval of all categories belonging to an organization."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.get_by_organization("TEST_ORG")

        assert len(result) == 2
        assert all(cat.organization_code == "TEST_ORG" for cat in result)


def test_should_return_all_categories_as_list(mock_database):
    """Test that all() returns complete list of all categories."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.all()

        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(cat, Category) for cat in result)


def test_should_be_iterable_over_categories(mock_database):
    """Test that Categories supports iteration protocol."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = list(categories)

        assert len(result) == 3
        assert all(isinstance(cat, Category) for cat in result)


def test_should_group_multiple_categories_under_same_organization(mock_database):
    """Test that multiple categories from same org are grouped correctly."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        test_org_categories = categories.get_by_organization("TEST_ORG")
        other_org_categories = categories.get_by_organization("OTHER_ORG")

        assert len(test_org_categories) == 2
        assert len(other_org_categories) == 1


def test_should_handle_empty_database_gracefully(mock_empty_database):
    """Test that Categories handles empty database without errors."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_empty_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        assert len(categories._categories) == 0
        assert len(categories._marking_index) == 0
        assert len(categories._org_index) == 0


def test_should_return_empty_list_when_all_called_on_empty_database(mock_empty_database):
    """Test that all() returns empty list for empty database."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_empty_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.all()

        assert result == []
        assert isinstance(result, list)


def test_should_return_none_for_nonexistent_marking(mock_database):
    """Test that get_by_marking returns None for non-existent marking."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.get_by_marking("NONEXISTENT-999")

        assert result is None


def test_should_return_empty_list_for_nonexistent_organization(mock_database):
    """Test that get_by_organization returns empty list for non-existent org."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.get_by_organization("NONEXISTENT_ORG")

        assert result == []
        assert isinstance(result, list)


def test_should_handle_single_category_database(mock_single_entry_database):
    """Test that Categories works correctly with only one entry."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_single_entry_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        assert len(categories.all()) == 1
        assert categories.get_by_marking("SINGLE-001") is not None
        assert len(categories.get_by_organization("SINGLE_ORG")) == 1


def test_should_handle_large_database_efficiently(mock_large_database):
    """Test that Categories handles large datasets without errors."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_large_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        assert len(categories.all()) == 1000
        assert len(categories._marking_index) == 1000
        assert len(categories._org_index) == 10


def test_should_iterate_over_empty_categories_without_error(mock_empty_database):
    """Test that iteration works on empty Categories instance."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_empty_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = list(categories)

        assert result == []


def test_should_handle_marking_lookup_with_empty_string(mock_database):
    """Test that empty string marking lookup returns None gracefully."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.get_by_marking("")

        assert result is None


def test_should_handle_organization_lookup_with_empty_string(mock_database):
    """Test that empty string organization lookup returns empty list."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.get_by_organization("")

        assert result == []


def test_should_handle_marking_lookup_with_whitespace(mock_database):
    """Test that whitespace-only marking lookup returns None."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.get_by_marking("   ")

        assert result is None


def test_should_handle_organization_lookup_with_whitespace(mock_database):
    """Test that whitespace-only organization lookup returns empty list."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.get_by_organization("   ")

        assert result == []


def test_should_not_mutate_categories_dict_when_returning_all():
    """Test that all() returns a copy, not a reference to internal dict."""
    mock_db = {
        "CAT-001": {
            "name": "Category",
            "description": "Test",
            "is_specified": True,
            "index_group": "ORG",
            "marking_format": "CAT-001",
        }
    }
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_db):
        from pycui_utils.categories import Categories

        categories = Categories()

        result1 = categories.all()
        result2 = categories.all()

        assert result1 is not result2
        assert result1 == result2


def test_should_return_organization_list_from_index():
    """Test that get_by_organization returns the list from internal index."""
    mock_db = {
        "CAT-001": {
            "name": "Category",
            "description": "Test",
            "is_specified": True,
            "index_group": "ORG",
            "marking_format": "CAT-001",
        }
    }
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_db):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.get_by_organization("ORG")

        assert isinstance(result, list)
        assert len(result) == 1


def test_should_perform_case_insensitive_marking_lookup(mock_case_sensitive_database):
    """Test that marking lookup is case-insensitive."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_case_sensitive_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        upper_result = categories.get_by_marking("UPPER-001")
        lower_result = categories.get_by_marking("upper-001")
        mixed_result = categories.get_by_marking("UpPeR-001")

        assert upper_result is not None
        assert upper_result == lower_result
        assert upper_result == mixed_result


def test_should_perform_case_insensitive_organization_lookup(mock_case_sensitive_database):
    """Test that organization lookup is case-insensitive."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_case_sensitive_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        upper_result = categories.get_by_organization("UPPER_ORG")
        lower_result = categories.get_by_organization("upper_org")
        mixed_result = categories.get_by_organization("UpPeR_oRg")

        assert len(upper_result) == 1
        assert upper_result[0] == lower_result[0]
        assert upper_result[0] == mixed_result[0]


def test_should_index_by_lowercase_marking_format(mock_case_sensitive_database):
    """Test that marking index stores keys in lowercase."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_case_sensitive_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        assert "upper-001" in categories._marking_index
        assert "lower-001" in categories._marking_index
        assert "mixed-001" in categories._marking_index


def test_should_index_by_lowercase_organization_code(mock_case_sensitive_database):
    """Test that organization index stores keys in lowercase."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_case_sensitive_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        assert "upper_org" in categories._org_index
        assert "lower_org" in categories._org_index
        assert "mixed_org" in categories._org_index


def test_should_handle_special_characters_in_marking_format():
    """Test that special characters in marking format are handled correctly."""
    mock_db = {
        "SP-CRITAN": {
            "name": "Special",
            "description": "Has special chars",
            "is_specified": True,
            "index_group": "SPECIAL",
            "marking_format": "SP-CRITAN",
        }
    }
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_db):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.get_by_marking("SP-CRITAN")

        assert result is not None
        assert result.marking_format == "SP-CRITAN"


def test_should_handle_special_characters_in_organization_code():
    """Test that special characters in organization code are handled."""
    mock_db = {
        "TEST-001": {
            "name": "Test",
            "description": "Test",
            "is_specified": True,
            "index_group": "ORG_WITH_UNDERSCORE",
            "marking_format": "TEST-001",
        }
    }
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_db):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.get_by_organization("ORG_WITH_UNDERSCORE")

        assert len(result) == 1
        assert result[0].organization_code == "ORG_WITH_UNDERSCORE"


def test_should_preserve_category_order_within_organization():
    """Test that categories maintain insertion order within organization groups."""
    mock_db = {
        "A-001": {
            "name": "First",
            "description": "First",
            "is_specified": True,
            "index_group": "ORG",
            "marking_format": "A-001",
        },
        "B-002": {
            "name": "Second",
            "description": "Second",
            "is_specified": True,
            "index_group": "ORG",
            "marking_format": "B-002",
        },
        "C-003": {
            "name": "Third",
            "description": "Third",
            "is_specified": True,
            "index_group": "ORG",
            "marking_format": "C-003",
        },
    }
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_db):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.get_by_organization("ORG")

        assert len(result) == 3
        assert [cat.code for cat in result] == ["A-001", "B-002", "C-003"]


def test_should_load_database_only_once_during_initialization():
    """Test that load_database is called exactly once during initialization."""
    mock_db = {
        "TEST-001": {
            "name": "Test",
            "description": "Test",
            "is_specified": True,
            "index_group": "ORG",
            "marking_format": "TEST-001",
        }
    }

    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_db) as mock_load:
        from pycui_utils.categories import Categories

        categories = Categories()

        # Trigger multiple operations
        categories.all()
        categories.get_by_marking("TEST-001")
        categories.get_by_organization("ORG")

        # Verify database was loaded only during initialization
        assert mock_load.call_count == 1


def test_should_handle_unicode_characters_in_marking():
    """Test that Unicode characters in marking formats are handled correctly."""
    mock_db = {
        "TEST-001": {
            "name": "Tëst Çätégöry",
            "description": "Unicode test",
            "is_specified": True,
            "index_group": "ORG",
            "marking_format": "TEST-001",
        }
    }
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_db):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.get_by_marking("TEST-001")

        assert result is not None
        assert result.name == "Tëst Çätégöry"


def test_should_return_same_category_instance_for_duplicate_marking_lookups(mock_database):
    """Test that repeated lookups return the same Category instance."""
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_database):
        from pycui_utils.categories import Categories

        categories = Categories()

        result1 = categories.get_by_marking("TEST-001")
        result2 = categories.get_by_marking("TEST-001")

        assert result1 is result2


def test_should_handle_numeric_strings_in_marking_format():
    """Test that numeric strings in marking formats work correctly."""
    mock_db = {
        "123-456": {
            "name": "Numeric",
            "description": "Numeric code",
            "is_specified": True,
            "index_group": "ORG",
            "marking_format": "123-456",
        }
    }
    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_db):
        from pycui_utils.categories import Categories

        categories = Categories()

        result = categories.get_by_marking("123-456")

        assert result is not None
        assert result.marking_format == "123-456"


def test_should_build_indexes_immediately_in_constructor():
    """Test that _build_indexes is called during __init__ not lazily."""
    mock_db = {
        "TEST-001": {
            "name": "Test",
            "description": "Test",
            "is_specified": True,
            "index_group": "ORG",
            "marking_format": "TEST-001",
        }
    }

    load_database.cache_clear()
    with patch("pycui_utils.categories.load_database", return_value=mock_db):
        from pycui_utils.categories import Categories

        categories = Categories()

        # Indexes should already be built
        assert len(categories._categories) == 1
        assert len(categories._marking_index) == 1
        assert len(categories._org_index) == 1
