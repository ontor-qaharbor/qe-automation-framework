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
