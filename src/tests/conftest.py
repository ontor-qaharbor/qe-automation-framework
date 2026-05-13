"""
Conftest for step definitions - Registers all step definitions for pytest-bdd
"""
import pytest
from src.corecomponents.xls_reader import XlsReader
from src.corecomponents.constants import TEST_DATA_XLSX

# Register step definitions as plugins for global discovery
pytest_plugins = [
    "steps.test_saucedemo_steps"
]

@pytest.fixture(scope="function")

def test_data(request):
    """Fixture providing test data from Excel."""
    reader = XlsReader()
    scenario_name = request.param if hasattr(request, 'param') else None
    if scenario_name:
        return reader.read_rows(TEST_DATA_XLSX, "login")
    return None
