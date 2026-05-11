"""
Business Functions - Contains all business logic using Generic and Locators
"""

from src.corecomponents.base_page import Generic
from src.pageobjects.saucedemo_locators import SauceDemoLocators


class BusinessFunctions(Generic):
    """Single class containing all business functions and workflows"""
    
    def __init__(self, page):
        """Initialize BusinessFunctions with page and locators"""
        super().__init__(page)
        self.locators = SauceDemoLocators
    
    # ─────────────────────────────────────────────────────────────────
    # LOGIN WORKFLOWS
    # ─────────────────────────────────────────────────────────────────
    
    def login_with_credentials(self, username: str, password: str) -> None:
        """
        Login workflow - Enter username, password and click login button
        
        Args:
            username (str): Username to enter
            password (str): Password to enter
        """
        self.type_text(self.locators.USERNAME_FIELD, username)
        self.type_text(self.locators.PASSWORD_FIELD, password)
        self.click(self.locators.LOGIN_BUTTON)
    
    def verify_login_error(self) -> str:
        """
        Verify login error message is displayed
        
        Returns:
            str: Error message text
        """
        error_text = self.get_text(self.locators.ERROR_MESSAGE)
        return error_text
    
    def click_forgot_password(self) -> None:
        """Click on forgot password link"""
        self.click(self.locators.FORGOT_PASSWORD_LINK)
    
    def is_login_page_loaded(self) -> bool:
        """Check if login page elements are loaded"""
        return (self.is_visible(self.locators.USERNAME_FIELD) and 
                self.is_visible(self.locators.LOGIN_BUTTON))
    
    # ─────────────────────────────────────────────────────────────────
    # DASHBOARD WORKFLOWS
    # ─────────────────────────────────────────────────────────────────
    
    def verify_dashboard_loaded(self) -> bool:
        """SauceDashboard: verify dashboard page is loaded successfully"""
        try:
            self.wait_for_visible(self.locators.APP_LOGO)
            return True
        except Exception:
            return False
    
    def logout_user(self) -> None:
        """SauceDemo: open burger menu and logout"""
        self.click(self.locators.BURGER_MENU_BUTTON)
        self.click(self.locators.LOGOUT_LINK)
    
    # ─────────────────────────────────────────────────────────────────
    # CHECKOUT WORKFLOWS
    # ─────────────────────────────────────────────────────────────────
    
    def add_to_cart(self) -> None:
        """SauceDemo: add a product (Backpack) to the cart"""
        self.click(self.locators.ADD_TO_CART_BACKPACK)

    def open_cart(self) -> None:
        """SauceDemo: open the cart page"""
        self.click(self.locators.SHOPPING_CART_LINK)
    
    # ─────────────────────────────────────────────────────────────────
    # HEADER & FOOTER WORKFLOWS
    # ─────────────────────────────────────────────────────────────────
    
    def click_header_logo(self) -> None:
        """Click header logo to navigate to home"""
        self.click(self.locators.HEADER_LOGO)
    
    def search_product(self, search_term: str) -> None:
        """
        Search for product using search box
        
        Args:
            search_term (str): Product name to search
        """
        self.type_text(self.locators.SEARCH_BOX, search_term)
        self.click(self.locators.SEARCH_BUTTON)
    
    def get_footer_text(self) -> str:
        """Get footer text"""
        return self.get_text(self.locators.FOOTER_TEXT)
    
    def get_contact_email(self) -> str:
        """Get contact email from footer"""
        return self.get_text(self.locators.CONTACT_EMAIL)
    
    # ─────────────────────────────────────────────────────────────────
    # ADDITIONAL BUSINESS FUNCTIONS
    # ─────────────────────────────────────────────────────────────────
    
    def complete_login_flow(self, username: str, password: str) -> bool:
        """Complete login flow: enter credentials and verify dashboard"""
        self.login_with_credentials(username, password)
        return self.verify_dashboard_loaded()
    
    def verify_success_message(self) -> bool:
        """Verify success message (cart badge visible after add to cart)"""
        return self.is_visible(self.locators.CART_BADGE)
    
    def wait_for_loading_complete(self) -> None:
        """Wait for loading spinner to disappear"""
        self.wait_for_hidden(self.locators.LOADING_SPINNER)
    
    # ─────────────────────────────────────────────────────────────────
    # COMMON WORKFLOWS
    # ─────────────────────────────────────────────────────────────────
    
    def get_page_title(self) -> str:
        """Get page title"""
        return self.get_title()
    
    def is_loading_spinner_visible(self) -> bool:
        """Check if loading spinner is visible"""
        return self.is_visible(self.locators.LOADING_SPINNER)
    
    def wait_for_loading_complete(self) -> None:
        """Wait for loading spinner to disappear"""
        while self.is_loading_spinner_visible():
            self.page.wait_for_timeout(500)
    
    def is_modal_displayed(self) -> bool:
        """Check if modal popup is displayed"""
        return self.is_visible(self.locators.MODAL_POPUP)
    
    def close_modal(self) -> None:
        """Close modal popup"""
        self.click(self.locators.CLOSE_BUTTON)
    
    def verify_success_message(self) -> bool:
        """SauceDemo: verify cart badge appears (item added)"""
        return self.is_visible(self.locators.CART_BADGE)
    
    # ─────────────────────────────────────────────────────────────────
    # COMPLETE USER WORKFLOWS (END-TO-END)
    # ─────────────────────────────────────────────────────────────────
    
    def complete_login_flow(self, username: str, password: str) -> bool:
        """
        Complete login flow - Login and verify dashboard
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            bool: True if login successful
        """
        self.login_with_credentials(username, password)
        self.wait_for_loading_complete()
        return self.verify_dashboard_loaded()

    def complete_add_to_cart_flow(self) -> bool:
        """SauceDemo: add one item to cart and verify badge shows"""
        self.add_to_cart()
        self.wait_for_loading_complete()
        return self.verify_success_message()
