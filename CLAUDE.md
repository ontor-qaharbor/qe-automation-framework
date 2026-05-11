Here is the CLAUDE.md file:

---

```markdown
# CLAUDE.md

## Project Overview

QE Playwright Python test automation framework
following a strict 4-layer BDD pattern using
Python, Playwright, Pytest, and pytest-bdd.

---

## Project Structure

```
dev-1/
├── features/
│   ├── web/
│   │   └── login_to_cart.feature
│   └── api/
├── src/
│   ├── businessfunctions/
│   │   ├── __init__.py
│   │   └── saucedemo.py
│   ├── corecomponents/
│   │   ├── __init__.py
│   │   ├── base_page.py
│   │   ├── constants.py
│   │   ├── xls_reader.py
│   │   └── xml_reader.py
│   ├── pageobjects/
│   │   ├── __init__.py
│   │   └── saucedemo_locators.py
│   ├── projectconfig/
│   │   └── project_config.py
│   ├── runner/
│   │   ├── __init__.py
│   │   └── conftest.py
│   ├── testcasedriver/
│   │   ├── __init__.py
│   │   └── test_case_driver.py
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── step_defs/
│       │   ├── __init__.py
│       │   └── test_saucedemo_steps.py
│       └── test_bdd_login_to_cart.py
├── data/
│   └── Test_Data.xlsx
├── reports/
├── tools/
│   └── create_test_data_xlsx.py
├── requirements.txt
└── pytest.ini
```

---

## Tech Stack

| Tool        | Purpose               |
|-------------|-----------------------|
| Python      | Primary language      |
| Playwright  | Browser automation    |
| Pytest      | Test execution engine |
| pytest-bdd  | BDD Gherkin support   |
| openpyxl    | Excel data reading    |
| pytest-html | HTML reports          |
| Allure      | Test reporting        |
| Azure DevOps| CI/CD pipeline        |

---

## The 4-Layer Pattern

Every single test must follow this exact chain.
Never break this pattern.

```
LAYER 1 — features/web/*.feature
         ↓ each step maps to
LAYER 2 — src/tests/step_defs/test_*_steps.py
         ↓ only calls
LAYER 3 — src/businessfunctions/*.py
         ↓ uses actions from      ↓ uses locators from
    src/corecomponents/       src/pageobjects/
       base_page.py            *_locators.py
```

---

## Layer 1 — Feature File

**Location:** `features/web/` or `features/api/`

**Rules:**
- Plain English Gherkin only
- No code, no imports, no logic
- One file per feature area
- Web UI tests go in `features/web/`
- API tests go in `features/api/`
- Use Scenario Outline for data driven tests
- Parameter name in Examples table must exactly
  match parsers.parse() parameter in step def

**Example:**
```gherkin
Feature: SauceDemo Login and Cart

  @smoke
  Scenario Outline: Login with valid credentials
    Given I navigate to saucedemo login page
    When I login with test data "<TestCase>"
    Then I should be on the inventory page
    And I add item to cart
    Then I verify cart count is correct

    Examples:
      | TestCase                  |
      | valid_login_standard_user |

  @negative
  Scenario Outline: Login with invalid credentials
    When I login with test data "<TestCase>"
    Then I should see a login error message

    Examples:
      | TestCase                     |
      | invalid_login_wrong_password |
```

---

## Layer 2 — Step Definition

**Location:** `src/tests/step_defs/test_saucedemo_steps.py`

**Rules:**
- Only 4 things allowed per step method:
  1. log_info() the step name
  2. report_create_test() the test name
  3. Create business function class instance
  4. Call ONE business function method
- Catch exception, log warning, screenshot
- Zero business logic
- Zero assertions
- Zero locators
- Use parsers.parse() for Scenario Outline steps

**Example:**
```python
from pytest_bdd import given, when, then, parsers
from src.businessfunctions.saucedemo import SauceDemo

@given("I navigate to saucedemo login page")
def navigate_to_login(base_page, page):
    try:
        base_page.log_info("Navigate to login page")
        base_page.report_create_test("Navigate to login")
        saucedemo = SauceDemo(page, base_page)
        saucedemo.navigate_to_login()
    except Exception as e:
        base_page.log_warning(str(e))
        base_page.log_failed_step_with_screenshot(str(e))

@when(parsers.parse('I login with test data "{TestCase}"'))
def login_with_test_data(base_page, page, TestCase):
    try:
        base_page.log_info(f"Login with: {TestCase}")
        base_page.report_create_test("Login with test data")
        saucedemo = SauceDemo(page, base_page)
        saucedemo.login_with_test_data(TestCase)
    except Exception as e:
        base_page.log_warning(str(e))
        base_page.log_failed_step_with_screenshot(str(e))

@then("I should be on the inventory page")
def verify_inventory_page(base_page, page):
    try:
        base_page.log_info("Verify inventory page")
        base_page.report_create_test("Verify inventory page")
        saucedemo = SauceDemo(page, base_page)
        saucedemo.verify_inventory_page_displayed()
    except Exception as e:
        base_page.log_warning(str(e))
        base_page.log_failed_step_with_screenshot(str(e))

@then("I add item to cart")
def add_item_to_cart(base_page, page):
    try:
        base_page.log_info("Add item to cart")
        base_page.report_create_test("Add item to cart")
        saucedemo = SauceDemo(page, base_page)
        saucedemo.add_item_to_cart()
    except Exception as e:
        base_page.log_warning(str(e))
        base_page.log_failed_step_with_screenshot(str(e))

@then("I verify cart count is correct")
def verify_cart_count(base_page, page):
    try:
        base_page.log_info("Verify cart count")
        base_page.report_create_test("Verify cart count")
        saucedemo = SauceDemo(page, base_page)
        saucedemo.verify_cart_count()
    except Exception as e:
        base_page.log_warning(str(e))
        base_page.log_failed_step_with_screenshot(str(e))

@then("I should see a login error message")
def verify_login_error(base_page, page):
    try:
        base_page.log_info("Verify login error message")
        base_page.report_create_test("Verify login error")
        saucedemo = SauceDemo(page, base_page)
        saucedemo.verify_login_error_message()
    except Exception as e:
        base_page.log_warning(str(e))
        base_page.log_failed_step_with_screenshot(str(e))
```

---

## Layer 3 — Business Function

**Location:** `src/businessfunctions/saucedemo.py`

**Rules:**
- Contains ALL real logic
- Uses ONLY base_page methods for actions
- Uses ONLY locator constants from Layer 4
- Never touches self.page directly for actions
- Has own try/except per method
- Reports pass or fail at end of every method
- One class per feature area
- One method per business action

**Example:**
```python
from src.pageobjects.saucedemo_locators import SauceDemoLocators

class SauceDemo:
    def __init__(self, page, base_page):
        self.page = page
        self.base_page = base_page

    def navigate_to_login(self):
        try:
            self.base_page.navigate_to(
                self.base_page.constants.BASE_URL)
            self.base_page.explicit_wait(
                SauceDemoLocators.USERNAME_FIELD)
            self.base_page.report_pass(
                "Navigation",
                "Navigated to login page successfully")
        except Exception as e:
            self.base_page.report_fail(
                "Navigation",
                "Failed to navigate. Error: " + str(e))

    def login_with_test_data(self, test_case):
        try:
            data = self.base_page.get_test_data(test_case)
            self.base_page.fill(
                SauceDemoLocators.USERNAME_FIELD,
                data["username"])
            self.base_page.fill(
                SauceDemoLocators.PASSWORD_FIELD,
                data["password"])
            self.base_page.click(
                SauceDemoLocators.LOGIN_BUTTON)
            self.base_page.report_pass(
                "Login",
                "Login successful: " + test_case)
        except Exception as e:
            self.base_page.report_fail(
                "Login",
                "Login failed. Error: " + str(e))

    def verify_inventory_page_displayed(self):
        try:
            if self.base_page.is_element_displayed(
                SauceDemoLocators.INVENTORY_CONTAINER):
                self.base_page.report_pass(
                    "Inventory Page",
                    "Inventory page displayed correctly")
            else:
                self.base_page.report_fail(
                    "Inventory Page",
                    "Inventory page not displayed")
        except Exception as e:
            self.base_page.report_fail(
                "Inventory Page",
                "Verification failed. Error: " + str(e))

    def add_item_to_cart(self):
        try:
            self.base_page.click(
                SauceDemoLocators.ADD_TO_CART_BUTTON)
            self.base_page.report_pass(
                "Add to Cart",
                "Item added to cart successfully")
        except Exception as e:
            self.base_page.report_fail(
                "Add to Cart",
                "Failed to add item. Error: " + str(e))

    def verify_cart_count(self):
        try:
            count = self.base_page.get_text(
                SauceDemoLocators.CART_BADGE)
            if count:
                self.base_page.report_pass(
                    "Cart Count",
                    "Cart count verified: " + str(count))
            else:
                self.base_page.report_fail(
                    "Cart Count",
                    "Cart count not found")
        except Exception as e:
            self.base_page.report_fail(
                "Cart Count",
                "Verification failed. Error: " + str(e))

    def verify_login_error_message(self):
        try:
            if self.base_page.is_element_displayed(
                SauceDemoLocators.ERROR_MESSAGE):
                self.base_page.report_pass(
                    "Login Error",
                    "Error message displayed correctly")
            else:
                self.base_page.report_fail(
                    "Login Error",
                    "Error message not displayed")
        except Exception as e:
            self.base_page.report_fail(
                "Login Error",
                "Verification failed. Error: " + str(e))
```

---

## Layer 4 — Locators

**Location:** `src/pageobjects/saucedemo_locators.py`

**Rules:**
- String constants ONLY
- No methods, no logic, no imports
- One class per page or feature area
- Organized by section with comments
- All names in UPPER_SNAKE_CASE
- XPath locators start with //
- CSS locators do not start with //

**Example:**
```python
class SauceDemoLocators:

    # Login Page
    USERNAME_FIELD = "#user-name"
    PASSWORD_FIELD = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    # Inventory Page
    INVENTORY_CONTAINER = "#inventory_container"
    INVENTORY_ITEM = ".inventory_item"
    ADD_TO_CART_BUTTON = "//button[text()='Add to cart']"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"

    # Cart
    CART_BADGE = ".shopping_cart_badge"
    CART_ICON = ".shopping_cart_link"
    CART_ITEM = ".cart_item"
    REMOVE_BUTTON = "//button[text()='Remove']"
    CHECKOUT_BUTTON = "#checkout"

    # Header
    PAGE_TITLE = ".title"
    MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
```

---

## Naming Conventions

| Item              | Convention          | Example                     |
|-------------------|---------------------|-----------------------------|
| Feature files     | snake_case.feature  | login_to_cart.feature       |
| Business function | snake_case.py       | saucedemo.py                |
| Locator files     | snake_case_locators | saucedemo_locators.py       |
| Locator constants | UPPER_SNAKE_CASE    | LOGIN_BUTTON                |
| Step def files    | test_*_steps.py     | test_saucedemo_steps.py     |
| Business classes  | PascalCase          | SauceDemo                   |
| Business methods  | snake_case          | login_with_test_data()      |
| Step def methods  | snake_case          | login_with_test_data()      |
| Fixtures          | snake_case          | base_page, test_data        |

---

## Step Mapping Rules

**Regular step:**
```python
@given("I navigate to saucedemo login page")
def method_name(base_page, page):
```

**Scenario Outline step with parameter:**
```python
@when(parsers.parse('I login with test data "{TestCase}"'))
def method_name(base_page, page, TestCase):
```

**Parameter name in parsers.parse() must exactly
match the column name in the Examples table.**

---

## Test Data — Excel Structure

**Location:** `data/Test_Data.xlsx`

```
| TestCase                    | username       | password     |
|-----------------------------|----------------|--------------|
| valid_login_standard_user   | standard_user  | secret_sauce |
| invalid_login_wrong_password| standard_user  | wrong_pass   |
```

---

## pytest.ini

```ini
[pytest]
bdd_features_base_dir = features/
addopts = --html=reports/report.html
          --self-contained-html
          -v
markers =
    smoke: smoke test suite
    regression: regression test suite
    negative: negative test scenarios
    api: API test scenarios
```

---

## How To Run Tests

```bash
# Run all tests
pytest

# Run only web tests
pytest features/web/

# Run only API tests
pytest features/api/

# Run smoke tests only
pytest -m smoke

# Run regression tests only
pytest -m regression

# Run specific feature file
pytest features/web/login_to_cart.feature

# Run with html report
pytest --html=reports/report.html
```

---

## How To Add A New Feature

```
1. Create feature file in features/web/ or features/api/
2. Create locator file in src/pageobjects/
3. Create business function file in src/businessfunctions/
4. Add step definitions in src/tests/step_defs/
5. Add test data rows in data/Test_Data.xlsx
6. Run pytest to verify
```

---

## What NOT To Do

```
NEVER put logic inside step def functions
NEVER put locators inside business function files
NEVER put business logic inside base_page.py
NEVER hardcode locator strings in business functions
NEVER hardcode URLs or credentials in test files
NEVER rename base_page.py
NEVER change existing locator constant names
NEVER skip try/except in business functions
NEVER put assertions directly in step defs
NEVER store feature files inside src/ folder
NEVER delete requirements.txt or pytest.ini
