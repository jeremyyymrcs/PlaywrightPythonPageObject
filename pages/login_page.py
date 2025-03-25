import allure

from utilities.action_handler import ActionHandler
from utilities.custom_logging import get_custom_logger, handle_exceptions_class
from utilities.read_config import Config
from locators.pages_locators import LoginPageLocators, HomePageLocators

logger = get_custom_logger(__name__)


@handle_exceptions_class
class LoginPage(ActionHandler):

    def _enter_credentials(self, username, password):
        self.type(LoginPageLocators.USERNAME, username)
        self.type(LoginPageLocators.PASSWORD, password)
        self.click(LoginPageLocators.SIGN_IN_BUTTON)

    @allure.step("Enter valid credentials and verify successful login")
    def successful_login(self):
        logger.info("Starting to login")
        self._enter_credentials(Config.USERNAME, Config.PASSWORD)

    @allure.step("Enter invalid credentials and verify login failure")
    def failed_login_attempt_with_incorrect_password(self):
        logger.info("Starting login with incorrect password.")
        self._enter_credentials(Config.USERNAME, Config.WRONG_PASSWORD)
        self.is_text_visible("Invalid Password")
        logger.info("Invalid password warning found, as expected.")
