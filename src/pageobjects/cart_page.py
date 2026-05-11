"""
Cart Page Object - Maps SauceDemo cart page actions.
"""

from __future__ import annotations

from src.corecomponents.base_page import Generic
from src.pageobjects.locators import Locators


class CartPage(Generic):
    """Cart page with all actions for SauceDemo cart workflow."""

    CART_ITEM = Locators.CART_ITEM
    SHOPPING_CART = Locators.SHOPPING_CART_LINK

    def is_cart_loaded(self) -> bool:
        """Check if cart page is loaded by verifying cart item is visible."""
        return self.is_visible(self.CART_ITEM)

    def is_item_in_cart(self) -> bool:
        """Check if item is present in the cart."""
        return self.is_present(self.CART_ITEM)

    def get_cart_item_count(self) -> int:
        """Get the number of items in cart."""
        return self.get_element_count(self.CART_ITEM)
