import pytest
import traceback
from pages.base_page import BasePage
from utilities.custom_logging import get_custom_logger

logger = get_custom_logger(__name__)


class BaseTest:
    """Base test class to handle common setup and login for test cases."""

    # Explicitly declare instance attributes to avoid the warning
    base_page = None
    login_page = None
    dashboard_page = None
    demo_page = None

    @pytest.fixture(autouse=True)
    def setup(self, page, request):
        """Fixture to set up the page for each test and handle login functionality.
        This fixture runs before and after each test.
        """
        print("\n\n=== Starting New Test Case ===")
        try:
            self._initialize_pages(page)
            self._perform_login(request)
        except Exception as e:
            logger.error(f"Error during setup: {e}")
            logger.error("Traceback: " + traceback.format_exc())
            raise e  # Reraise exception to ensure test fails

        yield
        print("\n=== Test Case Completed ===\n")

    def _initialize_pages(self, page):
        """Initialize the necessary page objects for the test."""
        try:
            self.base_page = BasePage(page)
            self.base_page.open_page()

            # Initialize page objects
            self.login_page = self.base_page.get_login_page()
            self.dashboard_page = self.base_page.get_dashboard_page()
            self.demo_page = self.base_page.get_demo_page()

        except Exception as e:
            logger.error(f"Error initializing pages: {e}")
            logger.error("Traceback: " + traceback.format_exc())
            raise e  # Reraise exception to fail the test setup

    def _perform_login(self, request):
        """Perform login unless explicitly skipped by a test marker."""
        try:
            login_not_required = request.node.get_closest_marker("skip_login")

            if login_not_required:
                logger.info("Skipping login as requested by test marker.")
            else:
                logger.info("Performing successful login.")
                self.login_page.successful_login()
        except Exception as e:
            logger.error(f"Error during login: {e}")
            logger.error("Traceback: " + traceback.format_exc())
            raise e  # Reraise exception to fail the test
