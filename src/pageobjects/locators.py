"""
Locators - Contains all UI element locators for automation
"""

class Locators:
    """Single class containing all UI element locators for automation"""
    
    # SauceDemo Login Page Locators
    USERNAME_FIELD = "id=user-name"
    PASSWORD_FIELD = "id=password"
    LOGIN_BUTTON = "id=login-button"
    ERROR_MESSAGE = "data-test=error"
    
    # SauceDemo Inventory (post-login) Locators
    INVENTORY_CONTAINER = "id=inventory_container"
    APP_LOGO = "class=app_logo"
    BURGER_MENU_BUTTON = "id=react-burger-menu-btn"
    LOGOUT_LINK = "id=logout_sidebar_link"
    
    # SauceDemo Cart / Checkout Locators (minimal set for add-to-cart workflow)
    ADD_TO_CART_BACKPACK = "id=add-to-cart-sauce-labs-backpack"
    SHOPPING_CART_LINK = "class=shopping_cart_link"
    CART_BADGE = "class=shopping_cart_badge"
    CART_ITEM = "class=cart_item"
    
    # Common Locators (optional / kept for compatibility)
    LOADING_SPINNER = "css=.loading"
    
    # Additional locators for business functions
    FORGOT_PASSWORD_LINK = "id=forgot_password_link"
    SEARCH_BOX = "id=search_box"
    SEARCH_BUTTON = "id=search_button"
    HEADER_LOGO = "id=header_logo"
    FOOTER_TEXT = "id=footer_text"
    CONTACT_EMAIL = "id=contact_email"
