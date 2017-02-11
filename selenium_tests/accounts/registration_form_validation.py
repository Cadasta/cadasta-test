from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium.webdriver.common.action_chains import ActionChains


class PasswordValidation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_invalid_password(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys("cadasta-test-user2")
        self.wd.find_css('#id_email').send_keys("user2@abc.com")
        self.wd.find_css("#id_password1").send_keys('password123')
        self.wd.find_css("#id_password2").send_keys('password123')
        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//button[@name="register"]')
        action.move_to_element(elem).click().perform()

        text = self.wd.find_element_by_xpath("//ul[contains(@class, 'parsley-errors-list')]").text
        assert text == "Your password must contain at least 3 of the following: lowercase characters, uppercase characters, special characters, and/or numerical characters."

    def tearDown(self):
        self.wd.quit()


class ConfirmPasswordValidation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_invalid_confirm_password(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys("cadasta-test-user2")
        self.wd.find_css('#id_email').send_keys("user2@abc.com")
        self.wd.find_css("#id_password1").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_password2").send_keys('password')
        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//button[@name="register"]')
        action.move_to_element(elem).click().perform()

        text = self.wd.find_element_by_xpath("//ul[contains(@class, 'parsley-errors-list')]").text
        assert text == "This value should be the same."

    def tearDown(self):
        self.wd.quit()


class EmptyUsernameValidation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_empty_username(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys("")
        self.wd.find_css('#id_email').send_keys("user2@abc.com")
        self.wd.find_css("#id_password1").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_password2").send_keys('XYZ#qwerty')
        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//button[@name="register"]')
        action.move_to_element(elem).click().perform()

        text = self.wd.find_element_by_xpath("//ul[contains(@class, 'parsley-errors-list')]").text
        assert text == "This field is required."

    def tearDown(self):
        self.wd.quit()


class EmptyEmailValidation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_empty_email(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys("cadasta-test-user2")
        self.wd.find_css('#id_email').send_keys("")
        self.wd.find_css("#id_password1").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_password2").send_keys('XYZ#qwerty')
        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//button[@name="register"]')
        action.move_to_element(elem).click().perform()

        text = self.wd.find_element_by_xpath("//ul[contains(@class, 'parsley-errors-list')]").text
        assert text == "This field is required."

    def tearDown(self):
        self.wd.quit()


class EmptyPasswordValidation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_empty_password(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys("cadasta-test-user2")
        self.wd.find_css('#id_email').send_keys("user2@abc.com")
        self.wd.find_css("#id_password1").send_keys('')
        self.wd.find_css("#id_password2").send_keys('XYZ#qwerty')
        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//button[@name="register"]')
        action.move_to_element(elem).click().perform()

        text = self.wd.find_element_by_xpath("//ul[contains(@class, 'parsley-errors-list')]").text
        assert text == "This field is required."

    def tearDown(self):
        self.wd.quit()


class EmptyConfirmPasswordValidation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_empty_confirm_password(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys("cadasta-test-user2")
        self.wd.find_css('#id_email').send_keys("user2@abc.com")
        self.wd.find_css("#id_password1").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_password2").send_keys('')
        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//button[@name="register"]')
        action.move_to_element(elem).click().perform()

        text = self.wd.find_element_by_xpath("//ul[contains(@class, 'parsley-errors-list')]").text
        assert text == "This field is required."

    def tearDown(self):
        self.wd.quit()