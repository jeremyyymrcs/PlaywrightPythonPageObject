import allure
import pytest
from tests.base_test import BaseTest


@allure.feature('Login Functionality')  # Class-level feature label
@allure.suite('Login Tests Suite')  # Class-level suite label
@allure.description(
    "This class contains tests related to the login functionality, ""including both successful and unsuccessful login scenarios, " "and edge cases such as incorrect password input.")
class TestLogin(BaseTest):

    @allure.story('Login with valid credentials should be successful')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test verifies that a user can successfully log in using valid credentials.")
    @pytest.mark.skip_login  # Marking this test to be skipped
    def test_successful_login(self):
        """
        Test Case: Verify successful login with valid credentials.
        Steps:
        1. Navigate to the login page.
        2. Enter valid username and password.
        3. Verify that the user is successfully redirected to the dashboard.
        """
        self.login_page.successful_login()
        self.dashboard_page.verify_welcome_message()
        allure.attach("Login Status", "Success", attachment_type=allure.attachment_type.TEXT)

    @allure.story('Login with invalid credentials due to incorrect password should fail')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test ensures that login fails when an incorrect password is provided.")
    @pytest.mark.skip_login  # Marking this test to be skipped
    def test_unsuccessful_login(self):
        """
        Test Case: Verify failed login attempt with an incorrect password.
        Steps:
        1. Navigate to the login page.
        2. Enter a valid username with an incorrect password.
        3. Verify that the login attempt fails and an error message is displayed.
        """
        self.login_page.failed_login_attempt_with_incorrect_password()
