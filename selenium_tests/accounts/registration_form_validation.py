from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class PasswordValidation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_invalid_password(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys("cadasta-test-user2")
        self.wd.find_css('#id_email').send_keys("user2@abc.com")
        self.wd.find_css("#id_password1").send_keys('password123')
        self.wd.find_css("#id_password2").send_keys('password123')
        self.wd.find_css("#id_full_name").send_keys('')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        text = self.wd.wait_for_xpath("//ul[contains(@class, 'parsley-errors-list')]").text
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
        self.wd.find_css("#id_full_name").send_keys('')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        text = self.wd.wait_for_xpath("//ul[contains(@class, 'parsley-errors-list')]").text
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
        self.wd.find_css("#id_full_name").send_keys('')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        text = self.wd.wait_for_xpath("//ul[contains(@class, 'parsley-errors-list')]").text
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
        self.wd.find_css("#id_full_name").send_keys('')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        text = self.wd.wait_for_xpath("//ul[contains(@class, 'parsley-errors-list')]").text
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
        self.wd.find_css("#id_full_name").send_keys('')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        text = self.wd.wait_for_xpath("//ul[contains(@class, 'parsley-errors-list')]").text
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
        self.wd.find_css("#id_full_name").send_keys('')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        text = self.wd.wait_for_xpath("//ul[contains(@class, 'parsley-errors-list')]").text
        assert text == "This field is required."

    def tearDown(self):
        self.wd.quit()

class EmptyUsernameInPasswordValidation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_empty_username_in_password(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys('')
        self.wd.find_css('#id_email').send_keys("user2@abc.com")
        self.wd.find_css("#id_password1").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_password2").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_full_name").send_keys('user2-name')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        text = self.wd.find_elements_by_xpath("//ul[contains(@class, 'parsley-errors-list')]")
        assert len(text) == 1

    def tearDown(self):
        self.wd.quit()

class EmptyEmailInPasswordValidation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_empty_email_in_password(self):
        self.open("/account/signup/")

        self.wd.find_css('#id_username').send_keys("cadasta-test-user2")
        self.wd.find_css('#id_email').send_keys("")
        self.wd.find_css("#id_password1").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_password2").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_full_name").send_keys('user2-name')
        action = ActionChains(self.wd)
        action.send_keys(Keys.TAB).send_keys(Keys.RETURN).perform()

        text = self.wd.find_elements_by_xpath("//ul[contains(@class, 'parsley-errors-list')]")
        assert len(text) == 1

    def tearDown(self):
        self.wd.quit()