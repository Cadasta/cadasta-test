import pytest

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from ..base_test import SeleniumTestCase
from ..util import random_string


@pytest.mark.skip
class PasswordValidation(SeleniumTestCase):

    def test_invalid_password(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys("cadasta-test-user2")
        self.wd.find_css('#id_email').send_keys("user2@abc.com")
        self.wd.find_css("#id_password").send_keys('password123')
        self.wd.find_css("#id_full_name").send_keys('')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        text = self.wd.wait_for_xpath(
            "//ul[contains(@class, 'parsley-errors-list')]").text
        assert text == ("Your password must contain at least 3 of the "
                        "following: lowercase characters, uppercase "
                        "characters, special characters, and/or numerical "
                        "characters.")


class RegistrationTest(SeleniumTestCase):

    def setUp(self):
        super().setUp()
        self.username = random_string()
        self.email = random_string() + '@example.com'
        self.password = 'XYZ#qwerty'
        self.full_name = 'John Lennon'

    def test_username_is_required(self):
        """Verifies User Accounts test case #R6."""

        self.open("/")
        self.wd.BY_XPATH('//header//a[normalize-space()="Register"]').click()
        self.wd.BY_NAME('email').send_keys(self.email)
        self.wd.BY_NAME('password').send_keys(self.password)
        self.wd.BY_NAME('full_name').send_keys(self.full_name)
        button = self.wd.BY_NAME('register')
        self.wd.scroll_element_into_view(button)
        button.click()

        self.wd.wait_for_xpath(
            '//*[contains(@class, "form-group") and '
            '    contains(@class, "has-error") and '
            '    //*[@name="username"] and '
            '    //*[normalize-space()="This field is required."]]'
        )

    def test_email_address_is_required(self):
        """Verifies User Accounts test case #R9."""

        self.open("/")
        self.wd.BY_XPATH('//header//a[normalize-space()="Register"]').click()
        self.wd.BY_NAME('username').send_keys(self.username)
        self.wd.BY_NAME('password').send_keys(self.password)
        self.wd.BY_NAME('full_name').send_keys(self.full_name)
        button = self.wd.BY_NAME('register')
        self.wd.scroll_element_into_view(button)
        button.click()

        self.wd.wait_for_xpath(
            '//*[contains(@class, "form-group") and '
            '    contains(@class, "has-error") and '
            '    //*[@name="email"] and '
            '    //*[normalize-space()="This field is required."]]'
        )

    def test_password_is_required(self):
        """Verifies User Accounts test case #R12."""

        self.open("/")
        self.wd.BY_XPATH('//header//a[normalize-space()="Register"]').click()
        self.wd.BY_NAME('username').send_keys(self.username)
        self.wd.BY_NAME('email').send_keys(self.email)
        self.wd.BY_NAME('full_name').send_keys(self.full_name)
        button = self.wd.BY_NAME('register')
        self.wd.scroll_element_into_view(button)
        button.click()

        self.wd.wait_for_xpath(
            '//*[contains(@class, "form-group") and '
            '    contains(@class, "has-error") and '
            '    //*[@name="password"] and '
            '    //*[normalize-space()="This field is required."]]'
        )


@pytest.mark.skip
class EmptyUsernameInPasswordValidation(SeleniumTestCase):

    def test_empty_username_in_password(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys('')
        self.wd.find_css('#id_email').send_keys("user2@abc.com")
        self.wd.find_css("#id_password").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_full_name").send_keys('user2-name')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        text = self.wd.find_elements_by_xpath(
            "//ul[contains(@class, 'parsley-errors-list')]")
        assert len(text) == 1


@pytest.mark.skip
class EmptyEmailInPasswordValidation(SeleniumTestCase):

    def test_empty_email_in_password(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys("cadasta-test-user2")
        self.wd.find_css('#id_email').send_keys("")
        self.wd.find_css("#id_password").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_full_name").send_keys('user2-name')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        text = self.wd.find_elements_by_xpath(
            "//ul[contains(@class, 'parsley-errors-list')]")
        assert len(text) == 1
