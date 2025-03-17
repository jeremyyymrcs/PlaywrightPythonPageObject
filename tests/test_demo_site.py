from tests.base_test import BaseTest


class TestDemoSite(BaseTest):

    def test_demo_page(self):
        self.dashboard_page.navigate_to_demo_page().demo_site_practice()
        self.dashboard_page.close_a_window(1)
        self.dashboard_page.switch_to_window(0)
        self.dashboard_page.log_out()
