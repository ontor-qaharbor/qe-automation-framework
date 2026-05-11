from src.runner.conftest import *  # noqa: F403

import pytest
from src.corecomponents.xls_reader import XlsReader
from src.corecomponents.constants import TEST_DATA_XLSX

# Import step definitions to register them
from src.tests.step_defs import test_saucedemo_steps  # noqa: F401


@pytest.fixture(scope="function")
def test_data(request):
    """Fixture providing test data from Excel."""
    reader = XlsReader()
    scenario_name = request.param if hasattr(request, 'param') else None
    if scenario_name:
        return reader.read_rows(TEST_DATA_XLSX, "login")
    return None

