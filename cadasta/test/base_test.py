import os
import pytest

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
            if not isinstance(field_value, str):
                field_value = str(field_value)
            field.send_keys(field_value)

    def assert_form_field_has_error(self, field_name, error_msg):
        self.wd.wait_for_xpath((
            '//*[contains(@class, "form-group") and '
            '    contains(@class, "has-error") and '
            '    .//*[@name="{}"] and '
            '    .//*[normalize-space()="{}"]]'
        ).format(field_name, error_msg))

    def log_in(self, user, field='username'):
        """Logs in the test user."""
        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', user[field])
        self.update_form_field('password', user['password'])
        self.wd.BY_NAME('sign-in').click()
        label = user['full_name'] or user['username']
        self.wd.wait_for_xpath(USER_MENU_XPATH_FORMAT.format(label))
