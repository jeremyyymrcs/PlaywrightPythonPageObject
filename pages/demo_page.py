from utilities.action_handler import ActionHandler
from utilities.custom_logging import get_custom_logger
from locators.pages_locators import DemoPageLocators

logger = get_custom_logger(__name__)


class DemoPage(ActionHandler):

    def demo_site_practice(self):

        try:
            logger.info("Starting demo site interaction.")
            # Type text into various text fields and then assert
            self.type(DemoPageLocators.TEXT_INPUT_FIELD, "This is Automated")
            self.type(DemoPageLocators.TEXT_AREA, "Testing Time!\n")
            self.type(DemoPageLocators.PRE_FILLED_TEXT_FIELD, "Typing Text!")
            self.type(DemoPageLocators.PLACE_HOLDER_TEXT_FIELD, "This is Automated")
            self.hover_and_click(DemoPageLocators.MY_DROP_DOWN, DemoPageLocators.DROP_DOWN_OPTION_TWO)
            self.assert_text(DemoPageLocators.LINK_TWO_SELECTED_TEXT)
            self.assert_text(DemoPageLocators.THIS_TEXT_IS_GREEN)
            self.click_by_text(DemoPageLocators.CLICK_ME)
            self.assert_text(DemoPageLocators.THIS_TEXT_IS_PURPLE)
            progress_bar_value = "70"
            self.set_value(DemoPageLocators.INPUT_SLIDER_CONTOL, progress_bar_value)
            self.assert_text(f"Progress Bar: ({progress_bar_value}%)")
            logger.info("Demo site interaction completed successfully.")

        except Exception as e:
            logger.error(f"An error occurred while interacting with the demo site: {e}")
            raise
