class HomePageLocators:
    WELCOME_LABEL = "//h1[contains(text(),'Welcome!')]"
    WELCOME_TEXT = "Welcome!"


class LoginPageLocators:
    TESTING_PAGE_LABEL = "//h4[contains(.,'MFA Login Testing Page')]"
    USERNAME = "username"
    PASSWORD = "password"
    SIGN_IN_BUTTON = "#log-in"
    INVALID_PASSWORD_WARNING = "//h6[contains(.,'Invalid Password!')]"


class DemoPageLocators:
    DEMO_PAGE_TAB = "//a[contains(.,'Demo Page')]"
    DEMO_PAGE_LABEL = "//h1[contains(text(),'Demo Page')]"
    TEXT_INPUT_FIELD = "myTextInput"
    TEXT_AREA = "textarea.area1"
    PRE_FILLED_TEXT_FIELD = '[name="preText2"]'
    MY_DROP_DOWN = "#myDropdown"
    DROP_DOWN_OPTION_TWO = "#dropOption2"
    LINK_TWO_SELECTED_TEXT = "Link Two Selected"
    PLACE_HOLDER_TEXT_FIELD = "Placeholder Text Field"
    THIS_TEXT_IS_GREEN = "This Text is Green"
    CLICK_ME = "Click Me"
    THIS_TEXT_IS_PURPLE = "This Text is Purple"
    INPUT_SLIDER_CONTOL = "#mySlider"
    PROGRESS_BAR = "Progress Bar: {}"
