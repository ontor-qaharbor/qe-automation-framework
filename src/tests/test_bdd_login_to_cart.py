"""
BDD Test Driver - Feature file scenarios converted to pytest-bdd tests
Step definitions are inline to ensure pytest-bdd can find them.
"""

from __future__ import annotations

from pathlib import Path
from pytest_bdd import given, when, then, parsers, scenarios
from src.businessfunctions.saucedemo import SauceDemo
from src.corecomponents.xls_reader import get_login_by_title

# Excel test data path
TEST_DATA_XLSX = Path(__file__).resolve().parents[2] / "data" / "Test_Data.xlsx"


@given("I am on the SauceDemo login page")
def navigate_to_login_page(base_page, page):
    """Navigate to SauceDemo login page."""
    try:
        base_page.log_info("Navigate to SauceDemo login page")
        base_page.report_create_test("Navigate to login page")
        saucedemo = SauceDemo(page, base_page)
        saucedemo.navigate_to_login()
    except Exception as e:
        base_page.log_warning(str(e))
        base_page.log_failed_step_with_screenshot(str(e))


@when(parsers.parse('I login with test data "{TestCase}"'))
def login_with_test_data(base_page, page, TestCase: str):
    """Login using credentials from Excel test data."""
    try:
        base_page.log_info(f"Login with test data: {TestCase}")
        base_page.report_create_test(f"Login with {TestCase}")
        saucedemo = SauceDemo(page, base_page)

        # Get test data from Excel
        row = get_login_by_title(TEST_DATA_XLSX, TestCase, sheet_name="login")
        test_data = {"username": row.username, "password": row.password}

        # Determine if valid or invalid based on test case name
        if "valid" in TestCase.lower():
            saucedemo.login_with_valid_credentials(test_data)
        else:
            saucedemo.login_with_invalid_credentials(test_data)

    except Exception as e:
        base_page.log_warning(str(e))
        base_page.log_failed_step_with_screenshot(str(e))


@then("I should be on the inventory page")
def verify_inventory_page(base_page, page):
    """Verify that inventory page is displayed."""
    try:
        base_page.log_info("Verify inventory page is displayed")
        base_page.report_create_test("Verify inventory page")
        saucedemo = SauceDemo(page, base_page)
        saucedemo.verify_inventory_page_displayed()
    except Exception as e:
        base_page.log_warning(str(e))
        base_page.log_failed_step_with_screenshot(str(e))


@then("I should see a login error message")
def verify_login_error(base_page, page):
    """Verify that login error message is displayed."""
    try:
        base_page.log_info("Verify login error message")
        base_page.report_create_test("Verify login error")
        saucedemo = SauceDemo(page, base_page)
        saucedemo.verify_login_error_message()
    except Exception as e:
        base_page.log_warning(str(e))
        base_page.log_failed_step_with_screenshot(str(e))


# Load feature file scenarios
FEATURE_FILE = Path(__file__).resolve().parents[2] / "features" / "web" / "login_to_cart.feature"

# Load all scenarios from feature file
scenarios(str(FEATURE_FILE))
