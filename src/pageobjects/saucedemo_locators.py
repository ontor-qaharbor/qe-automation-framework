"""
SauceDemo Locators - UI element locators for SauceDemo application
String constants ONLY. No methods, no logic, no Playwright imports.
"""

class SauceDemoLocators:
    """All locators for SauceDemo application organized by page/feature area."""

    # Login Page Locators
    USERNAME_FIELD = "#user-name"
    PASSWORD_FIELD = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    FORGOT_PASSWORD_LINK = "#forgot_password_link"

    # Inventory/Dashboard Page Locators
    INVENTORY_CONTAINER = "#inventory_container"
    APP_LOGO = ".app_logo"
    BURGER_MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    ADD_TO_CART_BACKPACK = "#add-to-cart-sauce-labs-backpack"

    # Cart Page Locators
    SHOPPING_CART_LINK = ".shopping_cart_link"
    CART_BADGE = ".shopping_cart_badge"
    CART_ITEM = ".cart_item"

    # Common Locators
    LOADING_SPINNER = ".loading"
    MODAL_POPUP = ".modal"  # Placeholder for modal elements