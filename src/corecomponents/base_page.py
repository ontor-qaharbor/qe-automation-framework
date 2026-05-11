"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              PLAYWRIGHT GENERIC BASE CLASS — CORE UTILITY LAYER             ║
║              Reusable · Extensible · POM-Ready · Exception-Safe             ║
╚══════════════════════════════════════════════════════════════════════════════╝

Author  : Automation Framework
Purpose : Generic base class wrapping Playwright interactions for all common
          HTML elements. Designed as the foundation layer for Page Object Model
          (POM) architectures.

Usage:
    class LoginPage(Generic):
        LOGIN_BTN  = "button[type='submit']"
        EMAIL_INPUT = "#email"

        def login(self, email: str, password: str) -> None:
            self.type_text(self.EMAIL_INPUT, email)
            self.click(self.LOGIN_BTN)
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Any, Callable, Literal, Optional, Union

from playwright.sync_api import (
    Dialog,
    ElementHandle,
    Error as PlaywrightError,
    FilePayload,
    Frame,
    FrameLocator,
    Locator,
    Page,
    TimeoutError as PlaywrightTimeoutError,
    expect,
)

# ─────────────────────────────── logger setup ────────────────────────────────

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)-8s]  %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ─────────────────────────────── type aliases ────────────────────────────────

Selector      = str                          # CSS / XPath / text= / role= …
Milliseconds  = int
DropdownBy    = Literal["value", "label", "index"]


# ══════════════════════════════════════════════════════════════════════════════
#  Generic
# ══════════════════════════════════════════════════════════════════════════════

class Generic:
    """
    Generic Playwright base class providing reusable wrappers for every
    common HTML-element interaction.

    Subclass this for individual Page Objects:

        class DashboardPage(Generic):
            HEADER = "h1.dashboard-title"

            def get_title(self) -> str:
                return self.get_text(self.HEADER)
    """

    # ------------------------------------------------------------------
    # Default timeouts (milliseconds)
    # ------------------------------------------------------------------
    DEFAULT_TIMEOUT:       Milliseconds = 30_000   # element waits
    SHORT_TIMEOUT:         Milliseconds = 5_000    # quick-existence checks
    LONG_TIMEOUT:          Milliseconds = 60_000   # slow page loads / uploads

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self, page: Page) -> None:
        """
        Parameters
        ----------
        page:
            An active Playwright ``Page`` instance injected by the test or
            fixture layer.
        """
        self.page = page
        self._dialog_handler: Optional[Callable[[Dialog], None]] = None
        logger.debug("Generic initialised with page: %s", page.url)

    # ══════════════════════════════════════════════════════════════════
    # §1  PRIVATE HELPERS
    # ══════════════════════════════════════════════════════════════════

    def _loc(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> Locator:
        """Return a Playwright ``Locator`` for *selector*."""
        return self.page.locator(selector)

    def _safe(self, action_name: str, fn: Callable[[], Any]) -> Any:
        """
        Execute *fn*, catch Playwright exceptions, log them, and re-raise
        as ``RuntimeError`` so callers see a clean, labelled error.
        """
        try:
            result = fn()
            logger.debug("✔ %s", action_name)
            return result
        except PlaywrightTimeoutError as exc:
            logger.error("✘ TIMEOUT  — %s | %s", action_name, exc)
            raise
        except PlaywrightError as exc:
            logger.error("✘ ERROR    — %s | %s", action_name, exc)
            raise
        except Exception as exc:
            logger.error("✘ UNKNOWN  — %s | %s", action_name, exc)
            raise

    # ══════════════════════════════════════════════════════════════════
    # §2  NAVIGATION & PAGE
    # ══════════════════════════════════════════════════════════════════

    def navigate(self, url: str, *, timeout: Milliseconds = LONG_TIMEOUT) -> None:
        """Navigate to *url* and wait for the page to reach 'load' state."""
        logger.info("navigate → %s", url)
        self._safe(
            f"navigate({url})",
            lambda: self.page.goto(url, wait_until="load", timeout=timeout),
        )

    def reload(self) -> None:
        """Reload the current page."""
        logger.info("reload")
        self._safe("reload", self.page.reload)

    def get_title(self) -> str:
        """Return the current page ``<title>``."""
        return self._safe("get_title", self.page.title)

    def get_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    # ══════════════════════════════════════════════════════════════════
    # §3  CLICK ACTIONS — buttons · links · icons · any element
    # ══════════════════════════════════════════════════════════════════

    def click(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
        force: bool = False,
    ) -> None:
        """Single left-click on *selector*."""
        logger.info("click(%s)", selector)
        self._safe(
            f"click({selector})",
            lambda: self._loc(selector).click(timeout=timeout, force=force),
        )

    def double_click(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Double-click on *selector*."""
        logger.info("double_click(%s)", selector)
        self._safe(
            f"double_click({selector})",
            lambda: self._loc(selector).dblclick(timeout=timeout),
        )

    def right_click(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Right-click (context-menu click) on *selector*."""
        logger.info("right_click(%s)", selector)
        self._safe(
            f"right_click({selector})",
            lambda: self._loc(selector).click(button="right", timeout=timeout),
        )

    def click_if_visible(self, selector: Selector) -> bool:
        """
        Click *selector* only when it is visible.

        Returns
        -------
        bool
            ``True`` if the element was visible and clicked, ``False`` otherwise.
        """
        if self.is_visible(selector):
            self.click(selector)
            return True
        logger.info("click_if_visible(%s) — element not visible, skip", selector)
        return False

    # ══════════════════════════════════════════════════════════════════
    # §4  TEXT INPUT — input · textarea · password
    # ══════════════════════════════════════════════════════════════════

    def type_text(
        self,
        selector: Selector,
        text: str,
        *,
        clear_first: bool = True,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
        delay: int = 0,
    ) -> None:
        """
        Fill *selector* with *text*.

        Parameters
        ----------
        clear_first:
            When ``True`` (default) the field is cleared before typing.
        delay:
            Milliseconds between keystrokes — useful to simulate human typing.
        """
        logger.info("type_text(%s, %r)", selector, text)
        loc = self._loc(selector)

        def _do() -> None:
            loc.wait_for(state="visible", timeout=timeout)
            if clear_first:
                loc.clear(timeout=timeout)
            if delay:
                loc.type(text, delay=delay)
            else:
                loc.fill(text, timeout=timeout)

        self._safe(f"type_text({selector})", _do)

    def clear_field(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Clear the value of an input or textarea."""
        logger.info("clear_field(%s)", selector)
        self._safe(
            f"clear_field({selector})",
            lambda: self._loc(selector).clear(timeout=timeout),
        )

    def append_text(self, selector: Selector, text: str) -> None:
        """Append *text* to the current value of *selector* without clearing."""
        logger.info("append_text(%s, %r)", selector, text)
        self._safe(
            f"append_text({selector})",
            lambda: self._loc(selector).type(text),
        )

    # ══════════════════════════════════════════════════════════════════
    # §5  CHECKBOXES
    # ══════════════════════════════════════════════════════════════════

    def check(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Ensure *selector* checkbox is checked."""
        logger.info("check(%s)", selector)
        self._safe(
            f"check({selector})",
            lambda: self._loc(selector).check(timeout=timeout),
        )

    def uncheck(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Ensure *selector* checkbox is unchecked."""
        logger.info("uncheck(%s)", selector)
        self._safe(
            f"uncheck({selector})",
            lambda: self._loc(selector).uncheck(timeout=timeout),
        )

    def is_checked(self, selector: Selector) -> bool:
        """Return ``True`` if *selector* checkbox / radio is currently checked."""
        result = self._safe(
            f"is_checked({selector})",
            lambda: self._loc(selector).is_checked(),
        )
        logger.info("is_checked(%s) → %s", selector, result)
        return result

    def toggle_checkbox(self, selector: Selector) -> None:
        """Toggle the checked state of *selector*."""
        if self.is_checked(selector):
            self.uncheck(selector)
        else:
            self.check(selector)

    # ══════════════════════════════════════════════════════════════════
    # §6  RADIO BUTTONS
    # ══════════════════════════════════════════════════════════════════

    def select_radio(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Select a radio button identified by *selector*."""
        logger.info("select_radio(%s)", selector)
        self._safe(
            f"select_radio({selector})",
            lambda: self._loc(selector).check(timeout=timeout),
        )

    def is_radio_selected(self, selector: Selector) -> bool:
        """Return ``True`` if the radio button *selector* is selected."""
        return self.is_checked(selector)

    def select_radio_by_value(
        self,
        group_name: str,
        value: str,
    ) -> None:
        """
        Select the radio input whose ``name`` attribute is *group_name* and
        ``value`` attribute equals *value*.
        """
        selector = f"input[type='radio'][name='{group_name}'][value='{value}']"
        self.select_radio(selector)

    # ══════════════════════════════════════════════════════════════════
    # §7  DROPDOWNS  — <select> elements
    # ══════════════════════════════════════════════════════════════════

    def select_dropdown(
        self,
        selector: Selector,
        option: Union[str, int],
        by: DropdownBy = "label",
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Select an option in a ``<select>`` element.

        Parameters
        ----------
        option:
            The option to choose — a string (value/label) or integer (index).
        by:
            ``"value"``  — match the ``value`` attribute.
            ``"label"``  — match visible text (default).
            ``"index"``  — match by zero-based index.
        """
        logger.info("select_dropdown(%s, %r, by=%s)", selector, option, by)
        loc = self._loc(selector)

        def _select() -> None:
            if by == "value":
                loc.select_option(value=str(option), timeout=timeout)
            elif by == "label":
                loc.select_option(label=str(option), timeout=timeout)
            elif by == "index":
                loc.select_option(index=int(option), timeout=timeout)
            else:
                raise ValueError(f"Unknown dropdown strategy: {by!r}")

        self._safe(f"select_dropdown({selector})", _select)

    def get_selected_option(self, selector: Selector) -> str:
        """Return the currently selected option's visible text for *selector*."""
        result = self._safe(
            f"get_selected_option({selector})",
            lambda: self._loc(selector).evaluate(
                "el => el.options[el.selectedIndex]?.text ?? ''"
            ),
        )
        logger.info("get_selected_option(%s) → %r", selector, result)
        return result

    def get_all_options(self, selector: Selector) -> list[str]:
        """Return a list of all option texts for a ``<select>`` element."""
        return self._safe(
            f"get_all_options({selector})",
            lambda: self._loc(selector).evaluate(
                "el => Array.from(el.options).map(o => o.text)"
            ),
        )

    # ══════════════════════════════════════════════════════════════════
    # §8  VISIBILITY & PRESENCE
    # ══════════════════════════════════════════════════════════════════

    def is_visible(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = SHORT_TIMEOUT,
    ) -> bool:
        """
        Return ``True`` if *selector* is visible in the viewport.
        Uses a short timeout — does **not** raise on not-found.
        """
        try:
            self._loc(selector).wait_for(state="visible", timeout=timeout)
            logger.info("is_visible(%s) → True", selector)
            return True
        except (PlaywrightTimeoutError, PlaywrightError):
            logger.info("is_visible(%s) → False", selector)
            return False

    def is_hidden(self, selector: Selector) -> bool:
        """Return ``True`` if *selector* is hidden (or absent)."""
        return not self.is_visible(selector)

    def is_present(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = SHORT_TIMEOUT,
    ) -> bool:
        """
        Return ``True`` if *selector* exists in the DOM regardless of visibility.
        """
        try:
            self._loc(selector).wait_for(state="attached", timeout=timeout)
            logger.info("is_present(%s) → True", selector)
            return True
        except (PlaywrightTimeoutError, PlaywrightError):
            logger.info("is_present(%s) → False", selector)
            return False

    # ══════════════════════════════════════════════════════════════════
    # §9  ENABLED / DISABLED STATE
    # ══════════════════════════════════════════════════════════════════

    def is_enabled(self, selector: Selector) -> bool:
        """Return ``True`` if *selector* is enabled (not disabled)."""
        result = self._safe(
            f"is_enabled({selector})",
            lambda: self._loc(selector).is_enabled(),
        )
        logger.info("is_enabled(%s) → %s", selector, result)
        return result

    def is_disabled(self, selector: Selector) -> bool:
        """Return ``True`` if *selector* is disabled."""
        return not self.is_enabled(selector)

    # ══════════════════════════════════════════════════════════════════
    # §10  HOVER
    # ══════════════════════════════════════════════════════════════════

    def hover(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Hover the mouse pointer over *selector*."""
        logger.info("hover(%s)", selector)
        self._safe(
            f"hover({selector})",
            lambda: self._loc(selector).hover(timeout=timeout),
        )

    # ══════════════════════════════════════════════════════════════════
    # §11  SCROLL
    # ══════════════════════════════════════════════════════════════════

    def scroll_into_view(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Scroll *selector* into the visible viewport."""
        logger.info("scroll_into_view(%s)", selector)
        self._safe(
            f"scroll_into_view({selector})",
            lambda: self._loc(selector).scroll_into_view_if_needed(timeout=timeout),
        )

    def scroll_to_bottom(self) -> None:
        """Scroll to the very bottom of the page."""
        logger.info("scroll_to_bottom")
        self._safe(
            "scroll_to_bottom",
            lambda: self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)"),
        )

    def scroll_to_top(self) -> None:
        """Scroll back to the top of the page."""
        logger.info("scroll_to_top")
        self._safe(
            "scroll_to_top",
            lambda: self.page.evaluate("window.scrollTo(0, 0)"),
        )

    def scroll_by(self, x: int = 0, y: int = 0) -> None:
        """Scroll the page by *(x, y)* pixels."""
        logger.info("scroll_by(%d, %d)", x, y)
        self._safe(
            f"scroll_by({x},{y})",
            lambda: self.page.evaluate(f"window.scrollBy({x}, {y})"),
        )

    # ══════════════════════════════════════════════════════════════════
    # §12  FILE UPLOAD
    # ══════════════════════════════════════════════════════════════════

    def upload_file(
        self,
        selector: Selector,
        file_path: Union[str, list[str], FilePayload, list[FilePayload]],
        *,
        timeout: Milliseconds = LONG_TIMEOUT,
    ) -> None:
        """
        Upload one or more files via an ``<input type="file">`` element.

        Parameters
        ----------
        file_path:
            Absolute path string, list of paths, or a ``FilePayload`` object.
        """
        logger.info("upload_file(%s, %s)", selector, file_path)
        self._safe(
            f"upload_file({selector})",
            lambda: self._loc(selector).set_input_files(file_path, timeout=timeout),
        )

    # ══════════════════════════════════════════════════════════════════
    # §13  KEYBOARD ACTIONS
    # ══════════════════════════════════════════════════════════════════

    def press_key(
        self,
        selector: Selector,
        key: str,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Press a keyboard *key* while *selector* has focus.

        Examples: ``"Enter"``, ``"Tab"``, ``"Escape"``, ``"Control+a"``.
        """
        logger.info("press_key(%s, %r)", selector, key)
        self._safe(
            f"press_key({selector}, {key})",
            lambda: self._loc(selector).press(key, timeout=timeout),
        )

    def press_global_key(self, key: str) -> None:
        """Press *key* on the page without targeting a specific element."""
        logger.info("press_global_key(%r)", key)
        self._safe(f"press_global_key({key})", lambda: self.page.keyboard.press(key))

    def type_with_keyboard(self, text: str, *, delay: int = 0) -> None:
        """
        Type *text* using the keyboard API (simulates actual key events).
        Useful for elements that do not respond to ``fill()``.
        """
        logger.info("type_with_keyboard(%r)", text)
        self._safe(
            f"type_with_keyboard({text!r})",
            lambda: self.page.keyboard.type(text, delay=delay),
        )

    def keyboard_shortcut(self, *keys: str) -> None:
        """
        Press a multi-key shortcut by holding keys in sequence.

        Example::

            self.keyboard_shortcut("Control", "Shift", "I")
        """
        logger.info("keyboard_shortcut(%s)", "+".join(keys))

        def _do() -> None:
            for k in keys[:-1]:
                self.page.keyboard.down(k)
            self.page.keyboard.press(keys[-1])
            for k in reversed(keys[:-1]):
                self.page.keyboard.up(k)

        self._safe("keyboard_shortcut", _do)

    # ══════════════════════════════════════════════════════════════════
    # §14  GET TEXT / GET ATTRIBUTE
    # ══════════════════════════════════════════════════════════════════

    def get_text(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> str:
        """Return the visible inner-text of *selector*."""
        result = self._safe(
            f"get_text({selector})",
            lambda: self._loc(selector).inner_text(timeout=timeout),
        )
        logger.info("get_text(%s) → %r", selector, result)
        return result.strip()

    def get_input_value(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> str:
        """Return the ``value`` property of an input / textarea / select."""
        result = self._safe(
            f"get_input_value({selector})",
            lambda: self._loc(selector).input_value(timeout=timeout),
        )
        logger.info("get_input_value(%s) → %r", selector, result)
        return result

    def get_attribute(
        self,
        selector: Selector,
        attribute: str,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> Optional[str]:
        """Return the value of *attribute* on *selector*, or ``None``."""
        result = self._safe(
            f"get_attribute({selector}, {attribute})",
            lambda: self._loc(selector).get_attribute(attribute, timeout=timeout),
        )
        logger.info("get_attribute(%s, %s) → %r", selector, attribute, result)
        return result

    def get_all_texts(self, selector: Selector) -> list[str]:
        """Return a list of inner-text values for every element matching *selector*."""
        return self._safe(
            f"get_all_texts({selector})",
            lambda: self._loc(selector).all_inner_texts(),
        )

    # ══════════════════════════════════════════════════════════════════
    # §15  EXPLICIT WAITS
    # ══════════════════════════════════════════════════════════════════

    def wait_for_visible(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Block until *selector* is visible, raising on timeout."""
        logger.info("wait_for_visible(%s, timeout=%d)", selector, timeout)
        self._safe(
            f"wait_for_visible({selector})",
            lambda: self._loc(selector).wait_for(state="visible", timeout=timeout),
        )

    def wait_for_hidden(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Block until *selector* disappears from view."""
        logger.info("wait_for_hidden(%s)", selector)
        self._safe(
            f"wait_for_hidden({selector})",
            lambda: self._loc(selector).wait_for(state="hidden", timeout=timeout),
        )

    def wait_for_text(
        self,
        selector: Selector,
        text: str,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Block until *selector*'s text contains *text*."""
        logger.info("wait_for_text(%s, %r)", selector, text)
        self._safe(
            f"wait_for_text({selector}, {text!r})",
            lambda: expect(self._loc(selector)).to_contain_text(text, timeout=timeout),
        )

    def wait_for_url(
        self,
        pattern: Union[str, re.Pattern],
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Block until the page URL matches *pattern* (string glob or regex)."""
        logger.info("wait_for_url(%r)", pattern)
        self._safe(
            f"wait_for_url({pattern!r})",
            lambda: self.page.wait_for_url(pattern, timeout=timeout),
        )

    def wait_for_load_state(
        self,
        state: Literal["load", "domcontentloaded", "networkidle"] = "load",
        *,
        timeout: Milliseconds = LONG_TIMEOUT,
    ) -> None:
        """Wait for the page to reach the specified load *state*."""
        logger.info("wait_for_load_state(%s)", state)
        self._safe(
            f"wait_for_load_state({state})",
            lambda: self.page.wait_for_load_state(state, timeout=timeout),
        )

    def wait_for_network_idle(self, *, timeout: Milliseconds = LONG_TIMEOUT) -> None:
        """Convenience wrapper — waits for ``networkidle``."""
        self.wait_for_load_state("networkidle", timeout=timeout)

    # ══════════════════════════════════════════════════════════════════
    # §16  DIALOGS / ALERTS
    # ══════════════════════════════════════════════════════════════════

    def accept_dialog(self, prompt_text: Optional[str] = None) -> None:
        """
        Register a one-time handler that **accepts** the next dialog.

        Parameters
        ----------
        prompt_text:
            For ``window.prompt()`` dialogs, fill in this text before accepting.
        """
        logger.info("accept_dialog (prompt_text=%r)", prompt_text)

        def _handler(dialog: Dialog) -> None:
            logger.info("dialog → type=%s, message=%r", dialog.type, dialog.message)
            dialog.accept(prompt_text) if prompt_text else dialog.accept()

        self.page.once("dialog", _handler)

    def dismiss_dialog(self) -> None:
        """Register a one-time handler that **dismisses** the next dialog."""
        logger.info("dismiss_dialog")
        self.page.once("dialog", lambda d: d.dismiss())

    def handle_dialog(self, accept: bool = True, text: Optional[str] = None) -> None:
        """
        Flexible dialog handler.

        Parameters
        ----------
        accept:
            ``True`` to accept, ``False`` to dismiss.
        text:
            Optional prompt text (only relevant when *accept* is ``True``).
        """
        if accept:
            self.accept_dialog(text)
        else:
            self.dismiss_dialog()

    # ══════════════════════════════════════════════════════════════════
    # §17  FRAMES / IFRAMES
    # ══════════════════════════════════════════════════════════════════

    def get_frame_by_name(self, name: str) -> Frame:
        """Return a ``Frame`` object by its *name* or ``id`` attribute."""
        frame = self.page.frame(name=name)
        if frame is None:
            raise ValueError(f"Frame not found: {name!r}")
        logger.info("get_frame_by_name(%r) → found", name)
        return frame

    def get_frame_by_url(self, url_pattern: Union[str, re.Pattern]) -> Frame:
        """Return the first ``Frame`` whose URL matches *url_pattern*."""
        frame = self.page.frame(url=url_pattern)
        if frame is None:
            raise ValueError(f"Frame not found for URL: {url_pattern!r}")
        logger.info("get_frame_by_url(%r) → found", url_pattern)
        return frame

    def get_frame_locator(self, iframe_selector: Selector) -> FrameLocator:
        """
        Return a ``FrameLocator`` for the iframe at *iframe_selector*.
        Use the returned locator's ``.locator()`` to interact with elements
        inside the frame::

            fl = self.get_frame_locator("#payment-iframe")
            fl.locator("#card-number").fill("4111111111111111")
        """
        logger.info("get_frame_locator(%s)", iframe_selector)
        return self.page.frame_locator(iframe_selector)

    def click_in_frame(
        self,
        iframe_selector: Selector,
        element_selector: Selector,
    ) -> None:
        """Convenience: click *element_selector* inside *iframe_selector*."""
        logger.info("click_in_frame(%s → %s)", iframe_selector, element_selector)
        self._safe(
            f"click_in_frame({iframe_selector} → {element_selector})",
            lambda: self.get_frame_locator(iframe_selector)
            .locator(element_selector)
            .click(),
        )

    def type_in_frame(
        self,
        iframe_selector: Selector,
        element_selector: Selector,
        text: str,
    ) -> None:
        """Convenience: fill text in *element_selector* inside *iframe_selector*."""
        logger.info("type_in_frame(%s → %s, %r)", iframe_selector, element_selector, text)
        self._safe(
            f"type_in_frame({iframe_selector} → {element_selector})",
            lambda: self.get_frame_locator(iframe_selector)
            .locator(element_selector)
            .fill(text),
        )

    # ══════════════════════════════════════════════════════════════════
    # §18  MULTIPLE ELEMENTS — lists · count · iteration
    # ══════════════════════════════════════════════════════════════════

    def get_elements(self, selector: Selector) -> list[ElementHandle]:
        """Return all ``ElementHandle`` objects matching *selector*."""
        return self._safe(
            f"get_elements({selector})",
            lambda: self._loc(selector).element_handles(),
        )

    def get_element_count(self, selector: Selector) -> int:
        """Return the number of DOM elements matching *selector*."""
        count = self._safe(
            f"get_element_count({selector})",
            lambda: self._loc(selector).count(),
        )
        logger.info("get_element_count(%s) → %d", selector, count)
        return count

    def get_nth_element(self, selector: Selector, index: int) -> Locator:
        """Return a ``Locator`` for the element at zero-based *index*."""
        return self._loc(selector).nth(index)

    def click_nth(self, selector: Selector, index: int) -> None:
        """Click the element at zero-based *index* among all *selector* matches."""
        logger.info("click_nth(%s, %d)", selector, index)
        self._safe(
            f"click_nth({selector}, {index})",
            lambda: self._loc(selector).nth(index).click(),
        )

    def get_texts_of_all(self, selector: Selector) -> list[str]:
        """Return stripped inner-text for every element matching *selector*."""
        texts = self.get_all_texts(selector)
        return [t.strip() for t in texts]

    def for_each_element(
        self,
        selector: Selector,
        action: Callable[[Locator, int], None],
    ) -> None:
        """
        Iterate over all elements matching *selector* and call *action* with
        ``(locator, index)`` for each.

        Example::

            self.for_each_element("ul.results li", lambda el, i: print(i, el.inner_text()))
        """
        count = self.get_element_count(selector)
        for i in range(count):
            action(self._loc(selector).nth(i), i)

    # ══════════════════════════════════════════════════════════════════
    # §19  SCREENSHOTS & DEBUGGING
    # ══════════════════════════════════════════════════════════════════

    def take_screenshot(
        self,
        path: str = "screenshot.png",
        *,
        full_page: bool = False,
    ) -> bytes:
        """
        Capture a screenshot.

        Parameters
        ----------
        path:
            File path to save the PNG.
        full_page:
            When ``True``, captures the entire scrollable page.
        """
        logger.info("take_screenshot → %s (full_page=%s)", path, full_page)
        return self._safe(
            "take_screenshot",
            lambda: self.page.screenshot(path=path, full_page=full_page),
        )

    def take_element_screenshot(
        self,
        selector: Selector,
        path: str = "element.png",
    ) -> bytes:
        """Capture a screenshot cropped to *selector*."""
        logger.info("take_element_screenshot(%s) → %s", selector, path)
        return self._safe(
            f"take_element_screenshot({selector})",
            lambda: self._loc(selector).screenshot(path=path),
        )

    # ══════════════════════════════════════════════════════════════════
    # §20  ASSERTIONS (Playwright expect wrappers)
    # ══════════════════════════════════════════════════════════════════

    def assert_visible(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Assert that *selector* is visible (raises ``AssertionError`` if not)."""
        logger.info("assert_visible(%s)", selector)
        expect(self._loc(selector)).to_be_visible(timeout=timeout)

    def assert_hidden(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Assert that *selector* is hidden."""
        logger.info("assert_hidden(%s)", selector)
        expect(self._loc(selector)).to_be_hidden(timeout=timeout)

    def assert_text(
        self,
        selector: Selector,
        expected: str,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Assert that *selector* contains *expected* text."""
        logger.info("assert_text(%s, %r)", selector, expected)
        expect(self._loc(selector)).to_contain_text(expected, timeout=timeout)

    def assert_value(
        self,
        selector: Selector,
        expected: str,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Assert that *selector* has the input value *expected*."""
        logger.info("assert_value(%s, %r)", selector, expected)
        expect(self._loc(selector)).to_have_value(expected, timeout=timeout)

    def assert_enabled(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Assert that *selector* is enabled."""
        expect(self._loc(selector)).to_be_enabled(timeout=timeout)

    def assert_disabled(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Assert that *selector* is disabled."""
        expect(self._loc(selector)).to_be_disabled(timeout=timeout)

    def assert_checked(
        self,
        selector: Selector,
        *,
        timeout: Milliseconds = DEFAULT_TIMEOUT,
    ) -> None:
        """Assert that *selector* checkbox/radio is checked."""
        expect(self._loc(selector)).to_be_checked(timeout=timeout)

    def assert_url_contains(self, fragment: str) -> None:
        """Assert that the current URL contains *fragment*."""
        assert fragment in self.get_url(), (
            f"URL {self.get_url()!r} does not contain {fragment!r}"
        )

    # ══════════════════════════════════════════════════════════════════
    # §21  JAVASCRIPT UTILITIES
    # ══════════════════════════════════════════════════════════════════

    def execute_script(self, script: str, *args: Any) -> Any:
        """
        Execute arbitrary JavaScript on the page.

        Parameters
        ----------
        script:
            JS expression or function body.
        *args:
            Arguments forwarded to the script as the ``arguments`` array.
        """
        logger.info("execute_script: %s", script[:80])
        return self._safe(
            "execute_script",
            lambda: self.page.evaluate(script, args[0] if len(args) == 1 else list(args)),
        )

    def execute_script_on_element(
        self,
        selector: Selector,
        script: str,
    ) -> Any:
        """
        Execute *script* with the element as ``el``::

            self.execute_script_on_element("#qty", "el => el.value = '5'")
        """
        logger.info("execute_script_on_element(%s)", selector)
        return self._safe(
            f"execute_script_on_element({selector})",
            lambda: self._loc(selector).evaluate(script),
        )

    def set_local_storage(self, key: str, value: str) -> None:
        """Set a ``localStorage`` item."""
        self.execute_script(f"localStorage.setItem('{key}', '{value}')")

    def get_local_storage(self, key: str) -> Optional[str]:
        """Get a ``localStorage`` item (returns ``None`` if not set)."""
        return self.execute_script(f"localStorage.getItem('{key}')")

    # ══════════════════════════════════════════════════════════════════
    # §21  PATTERN-SPECIFIC METHODS (for 4-layer framework)
    # ══════════════════════════════════════════════════════════════════

    def navigate_to(self, url: str) -> None:
        """Navigate to URL (alias for navigate)."""
        self.navigate(url)

    def fill(self, selector: Selector, value: str) -> None:
        """Fill input field (alias for type_text with clear_first=True)."""
        self.type_text(selector, value)

    def explicit_wait(self, selector: Selector, timeout: Milliseconds = DEFAULT_TIMEOUT) -> None:
        """Wait for element to be visible (alias for wait_for_visible)."""
        self.wait_for_visible(selector, timeout=timeout)

    def is_element_displayed(self, selector: Selector) -> bool:
        """Check if element is displayed (alias for is_visible)."""
        return self.is_visible(selector)

    def is_element_present(self, selector: Selector) -> bool:
        """Check if element is present in DOM (alias for is_present)."""
        return self.is_present(selector)

    def scroll_to_element(self, selector: Selector) -> None:
        """Scroll element into view (alias for scroll_into_view)."""
        self.scroll_into_view(selector)

    def report_pass(self, step_name: str, message: str) -> None:
        """Report a passed step."""
        logger.info(f"PASS: {step_name} - {message}")

    def report_fail(self, step_name: str, message: str) -> None:
        """Report a failed step."""
        logger.error(f"FAIL: {step_name} - {message}")

    def report_create_test(self, test_name: str) -> None:
        """Create a test entry in reports."""
        logger.info(f"TEST: {test_name}")

    def log_failed_step_with_screenshot(self, error_message: str) -> None:
        """Log failed step with screenshot."""
        logger.error(f"FAILED STEP: {error_message}")
        try:
            self.take_screenshot(f"failed_step_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")

    def log_info(self, message: str) -> None:
        """Log info message."""
        logger.info(message)

    def log_warning(self, message: str) -> None:
        """Log warning message."""
        logger.warning(message)

class _ExampleLoginPage(Generic):
    """
    Illustrative subclass — shows how to build a Page Object on top of Generic.
    """

    # Selectors declared as class-level constants → single place to update
    EMAIL_INPUT    = "#email"
    PASSWORD_INPUT = "#password"
    SUBMIT_BUTTON  = "button[type='submit']"
    ERROR_MESSAGE  = ".error-banner"
    REMEMBER_ME    = "#remember-me"

    def login(self, email: str, password: str, *, remember: bool = False) -> None:
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        if remember:
            self.check(self.REMEMBER_ME)
        self.click(self.SUBMIT_BUTTON)
        self.wait_for_load_state("networkidle")

    def get_error(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def is_login_error_visible(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)
