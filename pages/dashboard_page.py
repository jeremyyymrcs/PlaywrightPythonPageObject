from pages.demo_page import DemoPage
from utilities.action_handler import ActionHandler
from utilities.custom_logging import get_custom_logger

logger = get_custom_logger(__name__)


class DashboardPage(ActionHandler):

    def navigate_to_demo_page(self):
        """Navigates to the demo page and returns the DemoPage instance for further interaction."""
        try:
            logger.info("Navigating to the demo page.")

            # Click on "Demo Page" to open the new tab
            with self.page.context.expect_page() as new_page_info:
                self.click_by_text("Demo Page")

            # Capture the new page that was opened
            new_page = new_page_info.value

            # Optional: Check the URL of the new page to confirm it's correct
            logger.info(f"New page URL: {new_page.url}")

            # Return the DemoPage instance, passing the new page to it for further interaction
            return DemoPage(new_page)

        except Exception as e:
            logger.error(f"An error occurred while navigating to the demo page: {e}")
            raise

    def assert_all_the_tabs_in_dashboard(self):
        try:
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

        except Exception as e:
            logger.error(f"An error occurred while asserting the tabs on the dashboard: {e}")
            raise

    def log_out(self):
        try:
            logger.info("Logging out of the dashboard.")

            # Click the "Sign out" button
            self.click_by_text("Sign out")

            # Verify that the "Simple Login Testing Page" is visible after logout
            self.is_text_visible("Simple Login Testing Page")

            logger.info("Successfully logged out and redirected to the Simple Login Testing Page.")

        except Exception as e:
            logger.error(f"An error occurred while logging out of the dashboard: {e}")
            raise
