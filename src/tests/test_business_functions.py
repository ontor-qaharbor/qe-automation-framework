"""
Test Cases - Comprehensive test suite using BusinessFunctions and Locators
"""

import pytest
from src.corecomponents.xls_reader import load_login_rows


class TestApplicationFunctionality:
    """All application test cases in single class"""

    @pytest.mark.parametrize(
        "row",
        load_login_rows(r"d:\Drive Code\Student\Task2.2\dev-1\data\Test_Data.xlsx", sheet_name="login"),
        ids=lambda r: r.title,
    )
    def test_login_with_valid_credentials(self, bf, row):
        """SauceDemo: login using credentials from Excel"""
        bf.navigate("https://www.saucedemo.com/")
        assert bf.complete_login_flow(row.username, row.password), "Login flow failed"
        assert bf.verify_dashboard_loaded(), "Inventory page not loaded after login"

    @pytest.mark.parametrize(
        "row",
        load_login_rows(r"d:\Drive Code\Student\Task2.2\dev-1\data\Test_Data.xlsx", sheet_name="login"),
        ids=lambda r: r.title,
    )
    def test_login_to_add_to_cart_workflow(self, bf, row):
        """
        SauceDemo best workflow example:
        login -> add to cart -> open cart -> verify item present.
        """
        bf.navigate("https://www.saucedemo.com/")
        assert bf.complete_login_flow(row.username, row.password), "Login flow failed"

        assert bf.complete_add_to_cart_flow(), "Cart badge not visible after add-to-cart"
        bf.open_cart()
        assert bf.is_visible(bf.locators.CART_ITEM), "Cart item not visible in cart page"


# ─────────────────────────────────────────────────────────────────
# PYTEST CONFIGURATION
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
