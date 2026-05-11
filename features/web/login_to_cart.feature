Feature: SauceDemo login and add to cart

   @smoke
   Scenario Outline: Login with valid credentials
     Given I am on the SauceDemo login page
     When I login with test data "<TestCase>"
     Then I should be on the inventory page

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