"""
Root Conftest - Global fixtures for Playwright + pytest-bdd automation framework.
"""

from __future__ import annotations
import pytest
import logging
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, Browser, Page

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

@pytest.fixture(scope="session")
def playwright_instance():
    p = sync_playwright().start()
    yield p
    p.stop()

@pytest.fixture
def browser(playwright_instance, request) -> Browser:
    visible = request.config.getoption("--visible")
    browser_type_name = request.config.getoption("--browser-name")
    browser_type = getattr(playwright_instance, browser_type_name)
    browser = browser_type.launch(headless=not visible)
    yield browser
    browser.close()

@pytest.fixture
def page(browser: Browser) -> Page:
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def base_page(page):
    from src.corecomponents.base_page import Generic
    return Generic(page)
