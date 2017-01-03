from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver

class PasswordReset(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_password_reset(self):
        self.user_login()
        self.open("/account/password/reset/")
        self.wd.find_css('#id_email').send_keys("user1@abc.com")
        self.wd.find_element_by_xpath('//input[@value="Reset password"]').click()
        text = self.wd.find_element_by_xpath("//h1").text
        assert text == "Reset your password"

    def tearDown(self):
        self.wd.quit()