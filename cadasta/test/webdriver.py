from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


# Determine the WebDriver module; default to Firefox
web_driver_module = webdriver.Firefox


class CustomWebDriver(web_driver_module):
    """Our own WebDriver with some helpers added"""

    def __init__(self):
        super().__init__()
        self.set_window_size(1920, 1080)

    def find_css(self, css_selector):
        """Shortcut to find elements by CSS. Returns either a list or
        singleton"""
        elems = self.find_elements_by_css_selector(css_selector)
        found = len(elems)
        if found == 1:
            return elems[0]
        elif not elems:
            raise NoSuchElementException(css_selector)
        return elems

    def wait_for_css(self, css_selector, timeout=10):
        """ Shortcut for WebDriverWait"""
        try:
            return WebDriverWait(self, timeout).until(
                lambda driver: driver.find_css(css_selector))
        except:
            self.quit()

    def wait_for_xpath(self, xpath, timeout=10):
        """ Shortcut for WebDriverWait"""
        try:
            return WebDriverWait(self, timeout).until(
                lambda driver: driver.find_element_by_xpath(xpath))
        except:
            self.quit()

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
