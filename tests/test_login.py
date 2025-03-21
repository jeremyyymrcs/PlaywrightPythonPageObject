import allure
import pytest
from tests.base_test import BaseTest


class TestLogin(BaseTest):
    @allure.story('Successful login')
    def test_successful_login(self):
        self.dashboard_page.verify_welcome_message()

    @allure.story('Unsuccessful login due to incorrect password')
    @pytest.mark.skip_login
    def test_unsuccessful_login(self):
        self.login_page.failed_login_attempt_with_incorrect_password()
