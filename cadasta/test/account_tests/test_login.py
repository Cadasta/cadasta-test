import pytest

from ..base_test import SeleniumTestCase

pytestmark = pytest.mark.skip


class Login(SeleniumTestCase):

    def test_login(self):
        self.open("/account/login/")
        self.wd.find_css('#id_login').send_keys("cadasta-test-user-1")
        self.wd.find_css("#id_password").send_keys('XYZ#qwerty')
        self.wd.find_element_by_xpath('//button[@name="sign-in"]').click()
        self.wd.find_elements_by_xpath(
            "//span[contains(text(), 'cadasta-test-user-1')]")


class LoginFailure(SeleniumTestCase):

    def test_login_failure(self):
        self.open("/account/login/")
        self.wd.BY_NAME('login').send_keys('admin')
        self.wd.BY_NAME('password').send_keys('admin')
        self.wd.BY_NAME('sign-in').click()
        self.wd.BY_XPATH(
            '//*[@role="alert" and contains(normalize-space(),'
            '"The login and/or password you specified are not correct.")]')
