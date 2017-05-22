from ..base_test import SeleniumTestCase


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
        self.wd.find_css('#id_login').send_keys("admin")
        self.wd.find_css("#id_password").send_keys('admin')
        self.wd.find_element_by_xpath('//button[@name="sign-in"]').click()
        elem = self.wd.find_element_by_xpath("//div[contains(@role, 'alert')]")
        assert elem != []
