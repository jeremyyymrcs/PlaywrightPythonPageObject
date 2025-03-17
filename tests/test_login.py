import pytest
from tests.base_test import BaseTest


class TestLogin(BaseTest):

    def test_successful_login(self):
        self.dashboard_page.assert_all_the_tabs_in_dashboard()

    @pytest.mark.skip_login
    def test_unsuccessful_login(self):
        self.login_page.failed_login_attempt_with_incorrect_password()
