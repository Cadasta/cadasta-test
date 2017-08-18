import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Determine the WebDriver module; default to Chrome
web_driver_module = getattr(
    webdriver, os.environ.get('CADASTA_TEST_WEBDRIVER', 'Chrome'))


class CustomWebDriver(web_driver_module):
    """Our own WebDriver with some helpers added"""

    def __init__(self):
        super().__init__()
        self.set_window_size(1920, 1080)

        # Helper find-element methods to reduce line lengths
        self.BY_CLASS = self.find_element_by_class_name
        self.BY_CSS = self.find_element_by_css_selector
        self.BYS_CSS = self.find_elements_by_css_selector
        self.BY_ID = self.find_element_by_id
        self.BY_NAME = self.find_element_by_name
        self.BY_TAG = self.find_element_by_tag_name
        self.BYS_TAG = self.find_elements_by_tag_name
        self.BY_XPATH = self.find_element_by_xpath

    def find_css(self, css_selector):
        """Shortcut to find elements by CSS. Returns either a list or
        singleton"""
        elems = self.BYS_CSS(css_selector)
        found = len(elems)
        if found == 1:
            return elems[0]
        elif not elems:
            raise NoSuchElementException(css_selector)
        return elems

    def wait_for_css(self, css_selector, timeout=10):
        """ Shortcut for WebDriverWait"""
        wait = WebDriverWait(self, timeout)
        return wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, css_selector)))

    def wait_for_xpath(self, xpath, timeout=10):
        """ Shortcut for WebDriverWait"""
        wait = WebDriverWait(self, timeout)
        return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def switch_to_modal_dialog(self):
        modal_dialog_window_handle = None
        main_window_handle = self.current_window_handle
        print(main_window_handle)
        for handle in self.window_handles:
            print(handle)
            if handle != main_window_handle:
                modal_dialog_window_handle = handle
                break
        self.switch_to.window(modal_dialog_window_handle)
