"""
SauceDemo Business Functions - Contains all business logic for SauceDemo application
Uses base_page methods and locators only. No direct page interactions.
"""

from src.pageobjects.saucedemo_locators import SauceDemoLocators
from src.corecomponents.constants import BASE_URL


class SauceDemo:
    """Business functions class for SauceDemo application workflows."""

    def __init__(self, page, base_page):
        self.page = page
        self.base_page = base_page

    def navigate_to_login(self):
        """Navigate to SauceDemo login page."""
        try:
            self.base_page.navigate_to(BASE_URL)
            self.base_page.explicit_wait(SauceDemoLocators.USERNAME_FIELD)
            self.base_page.report_pass("Navigation", "Successfully navigated to login page")
        except Exception as e:
            self.base_page.report_fail("Navigation", "Failed to navigate. Error: " + str(e))

    def login_with_test_data(self, test_case):
        """Login with test data - routes to appropriate login method based on test case type."""
        try:
            from src.corecomponents.xls_reader import get_login_by_title
            from pathlib import Path
            TEST_DATA_XLSX = Path(__file__).resolve().parents[1] / ".." / "data" / "Test_Data.xlsx"

            row = get_login_by_title(TEST_DATA_XLSX, test_case, sheet_name="login")
            test_data = {"username": row.username, "password": row.password}

            if "valid" in test_case.lower():
                self.login_with_valid_credentials(test_data)
            else:
                self.login_with_invalid_credentials(test_data)
        except Exception as e:
            self.base_page.report_fail("Login", f"Login failed. Error: {str(e)}")

    def login_with_valid_credentials(self, test_data):
        """Login with valid credentials from test data."""
        try:
            self.base_page.fill(SauceDemoLocators.USERNAME_FIELD, test_data["username"])
            self.base_page.fill(SauceDemoLocators.PASSWORD_FIELD, test_data["password"])
            self.base_page.click(SauceDemoLocators.LOGIN_BUTTON)
            self.base_page.report_pass("Login", "Successfully logged in with valid credentials")
        except Exception as e:
            self.base_page.report_fail("Login", "Login failed. Error: " + str(e))

    def login_with_invalid_credentials(self, test_data):
        """Login with invalid credentials from test data."""
        try:
            self.base_page.fill(SauceDemoLocators.USERNAME_FIELD, test_data["username"])
            self.base_page.fill(SauceDemoLocators.PASSWORD_FIELD, test_data["password"])
            self.base_page.click(SauceDemoLocators.LOGIN_BUTTON)
            self.base_page.report_pass("Login", "Successfully attempted login with invalid credentials")
        except Exception as e:
            self.base_page.report_fail("Login", "Login attempt failed. Error: " + str(e))

    def verify_inventory_page_displayed(self):
        """Verify that inventory page is displayed after login."""
        try:
            self.base_page.wait_for_visible(SauceDemoLocators.INVENTORY_CONTAINER)
            self.base_page.report_pass("Inventory Page", "Inventory page is displayed correctly")
        except Exception as e:
            self.base_page.report_fail("Inventory Page", "Verification failed. Error: " + str(e))

    def verify_login_error_message(self):
        """Verify that login error message is displayed."""
        try:
            self.base_page.wait_for_visible(SauceDemoLocators.ERROR_MESSAGE)
            self.base_page.report_pass("Login Error", "Error message displayed correctly")
        except Exception as e:
            self.base_page.report_fail("Login Error", "Verification failed. Error: " + str(e))

    def add_item_to_cart(self):
        """Add backpack item to cart."""
        try:
            self.base_page.click(SauceDemoLocators.ADD_TO_CART_BACKPACK)
            self.base_page.report_pass("Add to Cart", "Item added to cart successfully")
        except Exception as e:
            self.base_page.report_fail("Add to Cart", "Failed to add item. Error: " + str(e))

    def verify_cart_count(self):
        """Verify cart badge shows correct count (implicitly 1 for single item)."""
        try:
            actual_count = self.base_page.get_text(SauceDemoLocators.CART_BADGE)
            if actual_count and actual_count == "1":
                self.base_page.report_pass("Cart Count", f"Cart count is correct: {actual_count}")
            else:
                self.base_page.report_fail("Cart Count", f"Cart count mismatch. Expected: 1, Actual: {actual_count}")
        except Exception as e:
            self.base_page.report_fail("Cart Count", "Verification failed. Error: " + str(e))