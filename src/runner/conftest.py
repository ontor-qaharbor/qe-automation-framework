"""
Conftest - Root fixture configuration for Playwright + pytest-bdd automation framework.
Provides browser, page, and logging fixtures for all tests.
"""

from __future__ import annotations

import pytest
import logging
from pathlib import Path
from datetime import datetime

from playwright.sync_api import sync_playwright, Browser, Page
from src.businessfunctions.business_functions import BusinessFunctions


# ─────────────────────────────── LOGGING SETUP ────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)-8s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


# ─────────────────────────────── PYTEST HOOKS ────────────────────────────────


def pytest_addoption(parser):
    """Add custom command-line options."""
    parser.addoption(
        "--visible",
        action="store_true",
        default=False,
        help="Run browser in visible mode (default: headless)",
    )
    parser.addoption(
        "--browser-name",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser to use (default: chromium)",
    )


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "smoke: smoke test")
    config.addinivalue_line("markers", "regression: regression test")
    config.addinivalue_line("markers", "bdd: BDD test")
    config.addinivalue_line("markers", "negative: negative test case")


# ─────────────────────────────── SESSION FIXTURES ────────────────────────────────


@pytest.fixture(scope="session")
def playwright_instance():
    """
    Create and manage Playwright instance for entire test session.
    Yields the Playwright instance and closes it after all tests.
    """
    logger.info("Starting Playwright instance...")
    p = sync_playwright().start()
    yield p
    logger.info("Stopping Playwright instance...")
    p.stop()


# ─────────────────────────────── FUNCTION FIXTURES ────────────────────────────────


@pytest.fixture
def browser(playwright_instance, request) -> Browser:
    """
    Create a browser instance for each test function.
    Respects --visible and --browser options.
    
    Args:
        playwright_instance: Playwright session fixture
        request: pytest request object (for config access)
    
    Yields:
        Browser: Playwright browser instance
    """
    # Determine headless mode
    visible = request.config.getoption("--visible")
    headless = not visible
    
    # Get browser type
    browser_type_name = request.config.getoption("--browser-name")
    browser_type = getattr(playwright_instance, browser_type_name)
    
    logger.info(f"Launching {browser_type_name} browser (headless={headless})...")
    browser = browser_type.launch(headless=headless)
    
    yield browser
    
    logger.info("Closing browser...")
    browser.close()


@pytest.fixture
def page(browser):
    """Create a new page for each test."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture
def base_page(page):
    """Create base_page instance for each test."""
    from src.corecomponents.base_page import Generic
    return Generic(page)


@pytest.fixture
def page(browser: Browser) -> Page:
    """
    Create a new page (tab) for each test function.
    
    Args:
        browser: Browser fixture
    
    Yields:
        Page: Playwright page instance
    """
    logger.info("Creating new page context...")
    context = browser.new_context()
    page = context.new_page()
    
    yield page
    
    logger.info("Closing page context...")
    context.close()


# ─────────────────────────────── REPORTING FIXTURES ────────────────────────────────


@pytest.fixture(scope="function")
def test_report(request):
    """
    Fixture for test reporting (screenshots on failure, logging).
    """
    yield
    
    # Take screenshot on test failure
    if request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"reports/failure_{request.node.name}_{timestamp}.png"
        logger.error(f"Test failed. Screenshot saved to {screenshot_path}")

        business_functions.navigate("https://example.com/login")
        business_functions.complete_login_flow("user@example.com", "password123")
        business_functions.navigate("https://example.com/checkout")
        yield business_functions
    
    @pytest.fixture(scope="function")
    def home_page(self, business_functions):
        """Fixture for home page state"""
        business_functions.navigate("https://example.com")
        yield business_functions
    
    @pytest.fixture(scope="function")
    def search_page(self, business_functions):
        """Fixture for search page state"""
        business_functions.navigate("https://example.com")
        yield business_functions
    
    @pytest.fixture(scope="function")
    def profile_page(self, logged_in_user):
        """Fixture for user profile page"""
        logged_in_user.click_user_profile()
        yield logged_in_user


class FixtureMarkers:
    """Class for managing pytest markers"""
    
    @staticmethod
    def register_markers(config):
        """Register all custom pytest markers"""
        markers = [
            ("smoke", "mark test as smoke test"),
            ("regression", "mark test as regression test"),
            ("critical", "mark test as critical"),
            ("slow", "mark test as slow running"),
            ("positive", "mark test as positive scenario"),
            ("negative", "mark test as negative scenario"),
            ("integration", "mark test as integration test"),
            ("ui", "mark test as UI test"),
            ("api", "mark test as API test"),
            ("functional", "mark test as functional test"),
        ]
        
        for marker_name, marker_desc in markers:
            config.addinivalue_line("markers", f"{marker_name}: {marker_desc}")


# Standalone fixture functions for direct pytest use
@pytest.fixture(scope="session")
def pw_instance():
    """Create playwright instance for the test session"""
    p = sync_playwright().start()
    yield p
    p.stop()


@pytest.fixture(scope="function")
def pw_browser(pw_instance):
    """Create a browser instance for each test"""
    browser = pw_instance.chromium.launch()
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def pw_page(pw_browser):
    """Create a new page context for each test"""
    context = pw_browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def bf(pw_page):
    """Create BusinessFunctions instance for each test"""
    bf_instance = BusinessFunctions(pw_page)
    yield bf_instance


@pytest.fixture(scope="function")
def user_logged_in(bf):
    """Fixture for logged-in user state"""
    bf.navigate("https://example.com/login")
    bf.complete_login_flow("user@example.com", "password123")
    yield bf


@pytest.fixture(scope="function")
def checkout_state(bf):
    """Fixture for checkout page ready state"""
    bf.navigate("https://example.com/login")
    bf.complete_login_flow("user@example.com", "password123")
    bf.navigate("https://example.com/checkout")
    yield bf


@pytest.fixture(scope="function")
def home_state(bf):
    """Fixture for home page state"""
    bf.navigate("https://example.com")
    yield bf
