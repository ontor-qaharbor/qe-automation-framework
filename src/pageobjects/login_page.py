"""
Login Page Object - Maps SauceDemo login page actions using Generic base class.
"""

from __future__ import annotations

from src.corecomponents.base_page import Generic
from src.pageobjects.locators import Locators


class LoginPage(Generic):
    """Login page with all actions for SauceDemo login workflow."""

    USERNAME_INPUT = Locators.USERNAME_FIELD
    PASSWORD_INPUT = Locators.PASSWORD_FIELD
    LOGIN_BTN = Locators.LOGIN_BUTTON
    ERROR_MSG = Locators.ERROR_MESSAGE

    def open(self) -> None:
        """Navigate to SauceDemo login page."""
        self.navigate("https://www.saucedemo.com/")

    def login(self, username: str, password: str) -> None:
        """
        Perform login action with given credentials.
        
        Args:
            username: Username to enter
            password: Password to enter
        """
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BTN)

    def is_error_visible(self) -> bool:
        """Check if error message is visible after failed login."""
        return self.is_visible(self.ERROR_MSG)

    def get_error_message(self) -> str:
        """Get the error message text."""
        return self.get_text(self.ERROR_MSG)

    def is_login_button_visible(self) -> bool:
        """Check if login button is visible."""
        return self.is_visible(self.LOGIN_BTN)
