import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Determine the WebDriver module; default to local ChromeDriver
webdriver_option = os.environ.get('CADASTA_TEST_WEBDRIVER', 'Chrome')
if 'BrowserStack' in webdriver_option:
    webdriver_module = webdriver.Remote
elif webdriver_option == 'Firefox':
    webdriver_module = webdriver.Firefox
else:
    webdriver_module = webdriver.Chrome


class CustomWebDriver(webdriver_module):
    """Our own WebDriver with some helpers added"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_window_size(1200, 800)

        # Method aliases to reduce line lengths.
        # Naming convention: "BY_*" returns the first element found while
        #   "BYS_*" returns a list of all elements found. These correspond to
        #   the "find_element_by_*" and "find_elements_by_*" WebDriver methods.
        self.BY_CLASS = self.find_element_by_class_name
        self.BY_CSS = self.find_element_by_css_selector
        self.BYS_CSS = self.find_elements_by_css_selector
        self.BY_ID = self.find_element_by_id
        self.BY_NAME = self.find_element_by_name
        self.BY_LINK = self.find_element_by_link_text
        self.BY_TAG = self.find_element_by_tag_name
        self.BYS_TAG = self.find_elements_by_tag_name
        self.BY_XPATH = self.find_element_by_xpath
        self.BYS_XPATH = self.find_elements_by_xpath

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

    def wait_until_clickable(self, selector, timeout=10):
        """ Shortcut for WebDriverWait"""
        wait = WebDriverWait(self, timeout)
        return wait.until(EC.element_to_be_clickable(selector))

    def wait_until_gone(self, selector, timeout=10):
        wait = WebDriverWait(self, timeout)
        return wait.until(EC.invisibility_of_element_located(selector))

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
