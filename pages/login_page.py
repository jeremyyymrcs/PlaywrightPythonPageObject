from utilities.action_handler import ActionHandler
from utilities.custom_logging import get_custom_logger, handle_exceptions
from utilities.read_config import Config
from locators.pages_locators import LoginPageLocators, HomePageLocators

logger = get_custom_logger(__name__)


class LoginPage(ActionHandler):

    def _enter_credentials(self, username, password):
        self.type(LoginPageLocators.USERNAME, username)
        self.type(LoginPageLocators.PASSWORD, password)
        self.click(LoginPageLocators.SIGN_IN_BUTTON)

    @handle_exceptions
    def successful_login(self):
        logger.info("Starting to login")
        self._enter_credentials(Config.USERNAME, Config.PASSWORD)
        self.is_text_visible(HomePageLocators.WELCOME_TEXT)

    @handle_exceptions
    def failed_login_attempt_with_incorrect_password(self):
        logger.info("Starting login with incorrect password.")
        self._enter_credentials(Config.USERNAME, Config.WRONG_PASSWORD)
        self.is_text_visible("Invalid Password")
        logger.info("Invalid password warning found, as expected.")
