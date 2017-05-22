from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from ..base_test import SeleniumTestCase


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


class EmptyUsernameValidation(SeleniumTestCase):

    def test_empty_username(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys("")
        self.wd.find_css('#id_email').send_keys("user2@abc.com")
        self.wd.find_css("#id_password").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_full_name").send_keys('')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        text = self.wd.wait_for_xpath(
            "//ul[contains(@class, 'parsley-errors-list')]").text
        assert text == "This field is required."


class EmptyEmailValidation(SeleniumTestCase):

    def test_empty_email(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys("cadasta-test-user2")
        self.wd.find_css('#id_email').send_keys("")
        self.wd.find_css("#id_password").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_full_name").send_keys('')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        text = self.wd.wait_for_xpath(
            "//ul[contains(@class, 'parsley-errors-list')]").text
        assert text == "This field is required."


class EmptyPasswordValidation(SeleniumTestCase):

    def test_empty_password(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys("cadasta-test-user2")
        self.wd.find_css('#id_email').send_keys("user2@abc.com")
        self.wd.find_css("#id_password").send_keys('')
        self.wd.find_css("#id_full_name").send_keys('')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        text = self.wd.wait_for_xpath(
            "//ul[contains(@class, 'parsley-errors-list')]").text
        assert text == "This field is required."


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
