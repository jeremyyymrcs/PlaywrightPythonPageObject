import pytest
import traceback
from pages.base_page import BasePage
from utilities.custom_logging import get_custom_logger, handle_exceptions

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
        logger.info("====== STARTING NEW TEST CASE ======")
        self._initialize_pages(page)
        self._perform_login(request)

        yield
        logger.info("====== TEST CASE COMPLETED ======\n")

    @handle_exceptions
    def _initialize_pages(self, page):
        """Initialize the necessary page objects for the test."""

        self.base_page = BasePage(page)
        self.base_page.open_page()

        # Initialize page objects
        self.login_page = self.base_page.get_login_page()
        self.dashboard_page = self.base_page.get_dashboard_page()
        self.demo_page = self.base_page.get_demo_page()

    @handle_exceptions
    def _perform_login(self, request):
        """Perform login unless explicitly skipped by a test marker."""

        login_not_required = request.node.get_closest_marker("skip_login")

        if login_not_required:
            logger.info("Skipping login as requested by test marker.")
        else:
            logger.info("Performing successful login.")
            self.login_page.successful_login()