import os
import unittest

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from .entities import Credentials
from .webdriver import CustomWebDriver


class SeleniumTestCase(unittest.TestCase):
    """
    A base test case for selenium, providing hepler methods for generating
    clients and logging in profiles.
    """
    def setUp(self):
        self.host_url = os.environ.get('CADASTA_HOST', 'http://localhost:8000')

        # Initialize webdriver
        webdriver_option = os.environ.get('CADASTA_TEST_WEBDRIVER', 'Chrome')
        if 'BrowserStack' in webdriver_option:
            url = 'http://{}:{}@hub.browserstack.com:80/wd/hub'.format(
                os.environ.get('BROWSERSTACK_USERNAME'),
                os.environ.get('BROWSERSTACK_ACCESS_KEY'))
            local_identifier = os.environ.get('BROWSERSTACK_LOCAL_IDENTIFIER')
            caps = {
                'os': 'Windows',
                'os_version': '10',
                'browser': 'Chrome',
                'browserstack.local': 'true',
                'browserstack.localIdentifier': local_identifier,
                'resolution': '1920x1080',
            }
            self.wd = CustomWebDriver(command_executor=url,
                                      desired_capabilities=caps)
        else:
            self.wd = CustomWebDriver()

    def tearDown(self):
        self.wd.quit()

    def open(self, path):
        self.wd.get(self.host_url + path)

    def user_login(self):
        self.open("/account/login/")
        self.wd.find_css('#id_login').send_keys(
            Credentials().get_test_username())
        self.wd.find_css("#id_password").send_keys(
            Credentials().get_test_password())
        self.wd.find_element_by_xpath('//button[@name="sign-in"]').click()

    def login_as(self, username, password):
        self.open("/account/login/")
        self.wd.find_css('#id_login').send_keys(username)
        self.wd.find_css("#id_password").send_keys(password)
        self.wd.find_element_by_xpath('//button[@name="sign-in"]').click()

    def restore_password(self, password, changedPassword):
        self.login_as("cadasta-test-user-1", changedPassword)
        self.wd.wait_for_css('.btn-user')
        self.open("/account/password/change/")
        self.wd.find_css('#id_oldpassword').send_keys(changedPassword)
        self.wd.find_css('#id_password').send_keys(password)
        self.wd.find_elements_by_xpath(
            "//button[contains(text(), 'Change password')]")[0].click()

    def restore_username(self, username):
        self.open("/account/profile/")
        self.wd.find_css('#id_username').clear()
        self.wd.find_css('#id_username').send_keys(username)
        self.wd.find_element_by_xpath('//button[@name="update"]').click()

    def restore_fullname(self, fullname):
        self.open("/account/profile/")
        self.wd.find_css('#id_full_name').clear()
        self.wd.find_css('#id_full_name').send_keys(fullname)
        self.wd.find_element_by_xpath('//button[@name="update"]').click()

    def restore_email(self, email):
        self.open("/account/profile/")
        self.wd.find_css('#id_email').clear()
        self.wd.find_css('#id_email').send_keys(email)
        self.wd.find_element_by_xpath('//button[@name="update"]').click()

    def register_new_user(self):
        self.open("/dashboard/")
        self.wd.find_element_by_xpath('//a[@href="/account/signup/"]').click()
        self.wd.wait_for_css("#signup_form")
        self.wd.find_css('#id_username').send_keys("cadasta-test-user-2")
        self.wd.find_css('#id_email').send_keys("user2@abc.com")
        self.wd.find_css("#id_password").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_full_name").send_keys('')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        try:
            self.wd.find_elements_by_xpath(
                "//*[contains(text(), "
                "'Confirmation email sent to user2@abc.com.')]")
            self.open("/account/logout/")
        except Exception:
            self.wd.find_elements_by_xpath(
                "//*[contains(text(), "
                "'A user with that username already exists.')]")
