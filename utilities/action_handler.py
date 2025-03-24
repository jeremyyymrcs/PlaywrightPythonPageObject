import os, shutil
import time
from pathlib import Path

import allure
from playwright.sync_api import Page, expect
from utilities.custom_logging import get_custom_logger

logger = get_custom_logger(__name__)


class ActionHandler:
    # Define the class-level variable for tracking if the folder is cleared
    folder_cleared = False
    action_count = 0

    def __init__(self, page: Page):
        self.page = page
        self.default_window = page  # Store the default (original) page
        self.current_window = page  # Track the current window explicitly
        # self.screenshots_dir = "../reports/screenshots"
        self.screenshots_dir = os.path.join('..', 'reports', 'screenshots')
        self.allure_dir = os.path.join('..', 'reports', 'allure-results')
        self.action_count = 0  # This will keep track of the screenshot order
        self.folder_cleared = False
        self.clear_screenshot_folder()

    def clear_screenshot_folder(self):
        """Clears all files in the screenshot folder only once when initializing."""
        # Ensure the folder is cleared only once using the class-level flag
        if not ActionHandler.folder_cleared:
            # Ensure the parent directory exists
            parent_dir = os.path.dirname(self.screenshots_dir)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)  # Create the parent directory if it doesn't exist

            # Ensure the screenshots directory exists
            if not os.path.exists(self.screenshots_dir):
                os.makedirs(self.screenshots_dir)  # Create the folder if it doesn't exist

            try:
                for path in Path(self.allure_dir).glob("**/*"):
                    if path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        shutil.rmtree(path)
            except PermissionError:
                pass
            except FileNotFoundError:
                pass

            for screenshot_file_name in os.listdir(self.screenshots_dir):
                file_path = os.path.join(self.screenshots_dir, screenshot_file_name)
                if screenshot_file_name.endswith(".png"):
                    # if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        logger.debug(f"Deleted existing screenshot: {file_path}")
                    except PermissionError:
                        pass
                    except FileNotFoundError:
                        pass

            ActionHandler.folder_cleared = True  # Set the flag to True after clearing once

    def take_screenshot(self, action_name: str):
        """Takes a full-page screenshot after an action in a specific order."""
        # Increment the action count for each screenshot taken
        ActionHandler.action_count += 1  # Increment class-level action_count

        # Add action_count to the filename to maintain order
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(self.screenshots_dir,
                                       f"screenshot_{ActionHandler.action_count}_{action_name}_{timestamp}.png")

        try:
            self.page.screenshot(full_page=True, path=screenshot_path)
            logger.debug(
                f"Screenshot {ActionHandler.action_count} taken for action '{action_name}' and saved to '{screenshot_path}'")

        except Exception as e:
            logger.error(f"Failed to take screenshot for action '{action_name}': {e}")
            raise  # Re-raise the exception to make sure the error is handled properly

        # Attach the screenshot to Allure report
        with open(screenshot_path, "rb") as f:
            allure.attach(f.read(), name=f"screenshot_{ActionHandler.action_count}_{action_name}_{timestamp}.png",
                          attachment_type=allure.attachment_type.PNG)
            f"screenshot_{ActionHandler.action_count}_{action_name}_{timestamp}.png"

    def type(self, selector_value: str, value: str):
        """Fills an input field based on the locator type and its corresponding value."""
        # Increment action count before the action to ensure the correct order
        text_box = self.page.locator(selector_value)
        expect(text_box).to_be_visible(timeout=7000)
        text_box.fill(value)
        self.take_screenshot('type')

    def click(self, locator_type: str):
        """Clicks a button by its locator."""
        # Increment action count before the action to ensure the correct order
        button = self.page.locator(locator_type)
        expect(button).to_be_visible()
        self.take_screenshot('click')
        button.click()

    def click_and_open_new_page(self, action_text: str, page_class):
        """Clicks on an element to open a new page and returns the page instance."""
        self.take_screenshot('click_and_open_new_page')
        with self.page.context.expect_page() as new_page_info:
            self.click_by_text(action_text)

        # Capture the new page
        new_page = new_page_info.value
        # Wait for the new page to be fully loaded or for a specific element to be visible
        new_page.wait_for_load_state('load')

        # Optionally, you can check the URL or do any validation here
        logger.info(f"New page URL: {new_page.url}")
        # Return the page class instance (e.g., DemoPage or other page)
        return page_class(new_page)

    def click_by_text(self, button_text: str, timeout: int = 7000):
        """Clicks a button by its text."""
        # Increment action count before the action to ensure the correct order
        button = self.page.get_by_text(button_text)
        expect(button).to_be_visible(timeout=timeout)
        self.take_screenshot('click_by_text')
        button.click()

    def is_text_visible(self, text: str):
        """Checks if the text is visible on the page."""
        # Increment action count before the action to ensure the correct order
        self.take_screenshot('is_text_visible')
        expect(self.page.locator(f"text={text}")).to_be_visible()

    def hover_and_click(self, hover_locator: str, click_locator: str):
        """Hovers over an element using hover_locator and then clicks another element."""
        try:
            # Increment action count before the action to ensure the correct order
            self.take_screenshot('hover_and_click')
            hover_element = self.page.locator(hover_locator)
            expect(hover_element).to_be_visible()
            hover_element.hover()
            logger.debug(f"Hovered over the element with locator: '{hover_locator}'")

            click_element = self.page.locator(click_locator)
            expect(click_element).to_be_visible()
            click_element.click()
            logger.debug(f"Clicked on the element with locator: '{click_locator}'")

        except Exception as e:
            logger.error(
                f"Failed to hover and click with locators '{hover_locator}' and '{click_locator}'. Error: {str(e)}")
            raise

    def set_value(self, locator: str, value: str):
        """Sets a value on a slider by percentage using drag_to()."""
        # Increment action count before the action to ensure the correct order
        self.take_screenshot('set_value')
        slider = self.page.locator(locator)
        expect(slider).to_be_visible()

        if not slider.is_enabled():
            raise Exception(f"Slider with locator '{locator}' is not enabled.")

        bounding_box = slider.bounding_box()
        if not bounding_box:
            raise Exception(f"Could not get bounding box for the slider at '{locator}'")

        # Convert value to an integer
        try:
            percentage_value = int(value)
        except ValueError:
            raise ValueError(f"Invalid percentage value: {value}")

        if not (0 <= percentage_value <= 100):
            raise ValueError(f"Percentage value must be between 0 and 100: {value}")

        # Calculate the target X position based on percentage
        start_x = bounding_box["x"]
        target_x = start_x + (bounding_box["width"] * (percentage_value / 100))

        # Find an offset element for dragging
        target_offset_x = target_x - start_x

        # Drag the slider by the calculated offset
        slider.drag_to(slider, source_position={"x": 0, "y": 0}, target_position={"x": target_offset_x, "y": 0})

        logger.debug(f"Slider set to {value}%")

    def switch_to_default_window(self):
        """Switches back to the default window."""
        self.default_window.bring_to_front()
        self.page = self.default_window  # Reset the current page reference to the default

    def close_newest_window(self):
        """Closes the newest browser window/tab."""
        # Check if there's more than one window and if the current window is not the default one
        if len(self.page.context.pages) > 1 and self.current_window != self.default_window:
            self.current_window.close()
            logger.debug(f"Closed the current window with URL: {self.current_window.url}")
            # Reset to default window after closing the current one
            self.current_window = self.default_window
        else:
            logger.debug("No additional windows to close.")

    def switch_to_window(self, index: int):
        """Switch to a specific window by its index, with better handling for new popups."""
        # Wait for a new popup window if one is expected
        if len(self.page.context.pages) <= index:
            logger.debug(f"Waiting for a new window to open...")

            self.page.wait_for_event('popup', timeout=5000)  # Wait for the popup for up to 5 seconds

        pages = self.page.context.pages
        logger.debug(f"Currently, there are {len(pages)} open window(s).")

        if len(pages) > index:
            self.page = self.page.context.pages[index]  # Switching to the correct window
            self.current_window = self.page
            self.page.bring_to_front()
            time.sleep(1)
            logger.debug(f"Switched to window at index {index} with URL: {self.page.url}")
        else:
            logger.error(f"No window found at index {index}. There are only {len(pages)} window(s) open.")

    def close_a_window(self, index: int):
        """Close a window by its index."""
        pages = self.page.context.pages
        if index < len(pages):
            pages[index].close()
            logger.debug(f"Closed window at index {index} with URL: {pages[index].url}")
        else:
            logger.error(f"No window found at index {index}.")

    def assert_element(self, locator: str):
        """Asserts that an element is visible on the page."""
        try:
            expect(self.page.locator(locator)).to_be_visible()
            logger.debug(f"Element with locator '{locator}' is visible.")
        except AssertionError:
            logger.error(f"Element with locator '{locator}' is NOT visible.")
            raise  # Re-raise the exception to ensure the test fails

    def assert_text(self, text: str):
        """Asserts that a specific text is visible on the page."""
        try:
            expect(self.page.locator(f"text={text}")).to_be_visible()
            logger.debug(f"Text '{text}' is visible on the page.")
        except AssertionError:
            logger.error(f"Text '{text}' is NOT visible on the page.")
            raise  # Re-raise the exception to ensure the test fails
        self.take_screenshot('assert_text')
