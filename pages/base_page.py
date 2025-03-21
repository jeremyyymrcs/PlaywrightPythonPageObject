import re
from playwright.sync_api import Page, expect
from utilities.read_config import Config
from utilities.action_handler import ActionHandler
from utilities.custom_logging import get_custom_logger, handle_exceptions
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.demo_page import DemoPage

logger = get_custom_logger(__name__)


class BasePage:

    def __init__(self, page: Page):
        self.page = page
        self.action_handler = ActionHandler(self.page)

    @handle_exceptions
    def open_page(self):
        """Navigate to the login page and perform validation checks."""
        logger.info("Navigating to the login page.")
        self.page.goto(Config.LOGIN_URL)
        expect(self.page).to_have_title(re.compile("Login / Simple App"))
        logger.info("Successfully reached the login page.")

    def get_login_page(self):
        return LoginPage(self.page)

    def get_dashboard_page(self):
        return DashboardPage(self.page)

    def get_demo_page(self):
        return DemoPage(self.page)
