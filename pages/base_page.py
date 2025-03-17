import re
import logging
from playwright.sync_api import Page, expect
from utilities.read_config import ReadConfig
from utilities.action_handler import ActionHandler

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.action_handler = ActionHandler(self.page)

    def setup(self):
        """Set up the pages, initializing all required pages."""
        logger.info("Setting up BasePage components.")
        self.open_page()

    def open_page(self):
        """Navigate to the login page and perform validation checks."""
        logger.info("Navigating to the login page.")
        self.page.goto(ReadConfig.get_simple_login_url())
        try:
            expect(self.page).to_have_title(re.compile("Login / Simple App"))
            logger.info("Successfully reached the login page.")
        except Exception as e:
            logger.error(f"Failed to load login page: {str(e)}")
            raise

    def get_login_page(self):
        from pages.login_page import LoginPage
        return LoginPage(self.page)

    def get_dashboard_page(self):
        from pages.dashboard_page import DashboardPage
        return DashboardPage(self.page)

    def get_demo_page(self):
        from pages.demo_page import DemoPage
        return DemoPage(self.page)
