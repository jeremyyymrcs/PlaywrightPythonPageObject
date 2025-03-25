import allure

from pages.demo_page import DemoPage
from utilities.action_handler import ActionHandler
from utilities.custom_logging import get_custom_logger, handle_exceptions, handle_exceptions_class

logger = get_custom_logger(__name__)


@handle_exceptions_class
class DashboardPage(ActionHandler):

    def navigate_to_demo_page(self):
        """Navigates to the demo page and returns the DemoPage instance for further interaction."""

        logger.info("Navigating to the demo page.")
        return self.click_and_open_new_page("Demo Page", DemoPage)

    @allure.step("Verify Welcome Message in Dashboard")
    def verify_welcome_message(self):
        logger.info("Verifying Welcome Message.")
        self.is_text_visible("Welcome!")
        logger.info("Welcome Message visible on the dashboard.")

    def assert_all_the_tabs_in_dashboard(self):
        logger.info("Asserting all the tabs in the dashboard.")

        # Assert visibility of all the expected tabs
        self.is_text_visible("This Page")
        self.is_text_visible("Demo Page")
        self.is_text_visible("SeleniumBase Docs")
        self.is_text_visible("The API")
        self.is_text_visible("GitHub Page")
        self.is_text_visible("Syntax Formats")
        self.is_text_visible("HTML Playground")
        self.is_text_visible("Sign out")

        logger.info("All tabs are visible on the dashboard.")

    def log_out(self):
        logger.info("Logging out of the dashboard.")

        # Click the "Sign out" button
        self.click_by_text("Sign out")

        # Verify that the "Simple Login Testing Page" is visible after logout
        self.is_text_visible("Simple Login Testing Page")

        logger.info("Successfully logged out and redirected to the Simple Login Testing Page.")
