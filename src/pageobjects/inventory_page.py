"""
Inventory Page Object - Maps SauceDemo inventory/dashboard page actions.
"""

from __future__ import annotations

from src.corecomponents.base_page import Generic
from src.pageobjects.locators import Locators


class InventoryPage(Generic):
    """Inventory page with all actions for SauceDemo post-login workflow."""

    INVENTORY_CONTAINER = Locators.INVENTORY_CONTAINER
    APP_LOGO = Locators.APP_LOGO
    BURGER_MENU = Locators.BURGER_MENU_BUTTON
    LOGOUT_LINK = Locators.LOGOUT_LINK
    SHOPPING_CART = Locators.SHOPPING_CART_LINK
    ADD_TO_CART_BACKPACK = Locators.ADD_TO_CART_BACKPACK
    CART_BADGE = Locators.CART_BADGE

    def is_dashboard_loaded(self) -> bool:
        """Check if inventory container is visible (dashboard loaded successfully)."""
        return self.is_visible(self.INVENTORY_CONTAINER)

    def is_logo_visible(self) -> bool:
        """Check if app logo is visible."""
        return self.is_visible(self.APP_LOGO)

    def add_backpack_to_cart(self) -> None:
        """Click 'Add to Cart' button for backpack item."""
        self.click(self.ADD_TO_CART_BACKPACK)

    def is_cart_badge_visible(self) -> bool:
        """Check if cart badge (item count) is visible."""
        return self.is_visible(self.CART_BADGE)

    def get_cart_badge_count(self) -> str:
        """Get the number shown on cart badge."""
        return self.get_text(self.CART_BADGE)

    def open_cart(self) -> None:
        """Click on shopping cart link to open cart page."""
        self.click(self.SHOPPING_CART)

    def open_menu(self) -> None:
        """Click on burger menu button."""
        self.click(self.BURGER_MENU)

    def logout(self) -> None:
        """Perform logout action (open menu and click logout)."""
        self.open_menu()
        self.click(self.LOGOUT_LINK)
