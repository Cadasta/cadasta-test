import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from ..base_test import SeleniumTestCase
from ..entities import Credentials
from ..pages import RegistrationPage


class NewRegistration(SeleniumTestCase):

    def test_new_registration(self):
        registration_page = RegistrationPage(self.wd, self)
        registration_page.go_to()
        username_available = False
        index = 1

        while not username_available:
            test_username = "cadasta-test-user-" + repr(index)
            test_password = "XYZ#qwerty"
            self.wd.find_css('#id_username').clear()
            self.wd.find_css('#id_username').send_keys(test_username)
            self.wd.find_css('#id_email').clear()
            self.wd.find_css('#id_email').send_keys(
                test_username + "@example.com")
            self.wd.find_css("#id_password").clear()
            self.wd.find_css("#id_password").send_keys(test_password)
            self.wd.find_css("#id_full_name").send_keys('')
            action = ActionChains(self.wd)
            action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

            time.sleep(1)
            elems = self.wd.find_elements_by_xpath(
                "//*[contains(text(), "
                "'A user with that username already exists')]")
            elems.extend(self.wd.find_elements_by_xpath(
                "//*[contains(text(), "
                "'Another user with this email already exists')]"))
            if len(elems) == 0:
                username_available = True
                # Credentials().set_test_username(test_username)
                # Credentials().set_test_password(test_password)
                # Credentials().set_test_email(test_username + "@example.com")
                assert self.wd.wait_for_css('.btn-user')
            else:
                index = index + 1


class RegistrationAttemptUsernameNotAvailable(SeleniumTestCase):

    def test_registration_attempt_already_taken_username(self):
        registration_page = RegistrationPage(self.wd, self)
        registration_page.go_to()

        self.wd.find_css('#id_username').send_keys(
            Credentials().get_test_username())
        self.wd.find_css('#id_email').send_keys("user@abc.com")
        self.wd.find_css("#id_password").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_full_name").send_keys('')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        assert self.wd.wait_for_xpath(
            "//*[contains(text(), "
            "'A user with that username already exists')]")


class RegistrationAttemptEmailNotAvailable(SeleniumTestCase):

    def test_registration_attempt_already_taken_email(self):
        registration_page = RegistrationPage(self.wd, self)
        registration_page.go_to()

        self.wd.find_css('#id_username').send_keys("cadasta-test-user")
        self.wd.find_css('#id_email').send_keys(Credentials().get_test_email())
        self.wd.find_css("#id_password").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_full_name").send_keys('')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        assert self.wd.wait_for_xpath(
            "//*[contains(text(), "
            "'Another user with this email already exists')]")
