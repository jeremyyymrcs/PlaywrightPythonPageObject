import allure

from tests.base_test import BaseTest


@allure.feature('Demo Website Functionality')  # Class-level feature label
@allure.suite('Demo Website Tests Suite')  # Class-level suite label
class TestDemoSite(BaseTest):
    @allure.story('Test the Demo Site Practice')
    @allure.description("This test ensures the different test scenarios in demo website")
    @allure.step("Enter different valid actions among practice website")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label('category', 'Smoke')  # Categorizing this test as 'Smoke'
    def test_demo_page(self):
        self.dashboard_page.navigate_to_demo_page().demo_site_practice()
        self.dashboard_page.close_a_window(1)
        self.dashboard_page.switch_to_window(0)
        self.dashboard_page.log_out()
