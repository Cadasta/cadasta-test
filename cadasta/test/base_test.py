import os
import pytest

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from urllib.parse import urlparse


HOST_URL = os.environ.get('CADASTA_HOST', 'http://localhost:8000')
USER_MENU_XPATH_FORMAT = '//header//*[normalize-space()="{}"]'


class SeleniumTestCase():
    """
    A base test case for Selenium, providing helper methods for generating
    clients and logging in profiles.
    """

    @pytest.fixture(autouse=True)
    def wrapper(self, webdriver):
        self.wd = webdriver
        self.open('/')
        yield
        self.open('/account/logout/')

    def open(self, path):
        self.wd.get(HOST_URL + path)

    def get_url_path(self):
        return urlparse(self.wd.current_url).path

    def get_url_query(self):
        return urlparse(self.wd.current_url).query

    def assert_url_path(self, path):
        assert self.get_url_path() == path

    def scroll_element_into_view(self, element):
        self.wd.execute_script('arguments[0].scrollIntoView()', element)

    def wait_for_alert(self, msg):
        self.wd.wait_for_xpath(
            '//*[@role="alert" and '
            'contains(normalize-space(), "{}")]'.format(msg))

    def update_form_field(self, field_name, field_value):
        field = self.wd.BY_NAME(field_name)
        if field.tag_name == 'select':
            Select(field).select_by_value(field_value)
        else:  # Assume tag_name is 'input' with type 'text' or 'password'
            field.clear()
            field.send_keys(field_value)

    def assert_form_field_has_error(self, field_name, error_msg):
        self.wd.wait_for_xpath((
            '//*[contains(@class, "form-group") and '
            '    contains(@class, "has-error") and '
            '    .//*[@name="{}"] and '
            '    .//*[normalize-space()="{}"]]'
        ).format(field_name, error_msg))

    def log_in(self, user):
        """Logs in the test user."""
        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', user['username'])
        self.update_form_field('password', user['password'])
        self.wd.BY_NAME('sign-in').click()
        label = user['full_name'] or user['username']
        self.wd.wait_for_xpath(USER_MENU_XPATH_FORMAT.format(label))

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
