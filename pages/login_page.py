from utilities.action_handler import ActionHandler
from utilities.custom_logging import get_custom_logger
from utilities.read_config import ReadConfig
from locators.pages_locators import LoginPageLocators, HomePageLocators

logger = get_custom_logger(__name__)


class LoginPage(ActionHandler):

    def _enter_credentials(self, username, password):
        self.type("id", LoginPageLocators.USERNAME, username)
        self.type("id", LoginPageLocators.PASSWORD, password)
        self.click(LoginPageLocators.SIGN_IN_BUTTON)

    def successful_login(self):
        try:
            logger.info("Starting to login")
            self._enter_credentials(ReadConfig.get_user_name(), ReadConfig.get_password())
            self.is_text_visible(HomePageLocators.WELCOME_TEXT)
        except Exception as e:
            logger.error(f"An error occurred during login: {e}")
            raise

    def failed_login_attempt_with_incorrect_password(self):

        try:
            logger.info("Starting login with incorrect password.")
            self._enter_credentials("demo_user", "wrong_password")
            self.is_text_visible("Invalid Password")
            logger.info("Invalid password warning found, as expected.")
        except Exception as e:
            logger.error(f"An error occurred during login: {e}")
            raise
