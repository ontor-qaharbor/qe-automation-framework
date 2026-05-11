from __future__ import annotations

from playwright.sync_api import sync_playwright

from src.projectconfig.project_config import ProjectConfig


class TestCaseDriver:
    """Playwright browser/context/page initialization."""

    def __init__(self, config: ProjectConfig | None = None):
        self.config = config or ProjectConfig()
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    def start(self):
        self._playwright = sync_playwright().start()
        browser_type = getattr(self._playwright, self.config.browser_name)
        self._browser = browser_type.launch(headless=self.config.headless)
        self._context = self._browser.new_context()
        self._page = self._context.new_page()
        return self._page

    def stop(self):
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

