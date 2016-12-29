from django.contrib.auth.models import User
from selenium.common.exceptions import NoSuchElementException

from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver

class NewRegistration(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_new_registration(self):
        self.open("/dashboard/")
        self.wd.find_element_by_xpath('//a[@href="/account/signup/"]').click()
        self.wd.wait_for_css("#signup_form")

        self.wd.find_css('#id_username').send_keys("cadasta-test-user1")
        self.wd.find_css('#id_email').send_keys("user1@abc.com")
        self.wd.find_css("#id_password1").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_password2").send_keys('XYZ#qwerty')
        self.wd.find_element_by_xpath('//button[@name="register"]').click()

        try:
            self.wd.find_elements_by_xpath("//*[contains(text(), 'Confirmation email sent to user1@abc.com.')]")

        except NoSuchElementException as e:
            # Debugging help.
            print ("Debug: " + e)
            self.wd.find_elements_by_xpath("//*[contains(text(), 'A user with that username already exists.')]")

    def tearDown(self):
        self.wd.quit()

class RegistrationAttemptUsernameNotAvailable(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_registration_attempt_already_taken_username(self):
        self.open("/dashboard/")
        self.wd.find_element_by_xpath('//a[@href="/account/signup/"]').click()
        self.wd.wait_for_css("#signup_form")

        self.wd.find_css('#id_username').send_keys("cadasta-test-user1")
        self.wd.find_css('#id_email').send_keys("user@abc.com")
        self.wd.find_css("#id_password1").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_password2").send_keys('XYZ#qwerty')
        self.wd.find_element_by_xpath('//button[@name="register"]').click()
        self.wd.find_elements_by_xpath("//*[contains(text(), 'A user with that username already exists.')]")

    def tearDown(self):
        self.wd.quit()

class RegistrationAttemptEmailNotAvailable(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_registration_attempt_already_taken_email(self):
        self.open("/dashboard/")
        self.wd.find_element_by_xpath('//a[@href="/account/signup/"]').click()
        self.wd.wait_for_css("#signup_form")

        self.wd.find_css('#id_username').send_keys("user")
        self.wd.find_css('#id_email').send_keys("user1@abc.com")
        self.wd.find_css("#id_password1").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_password2").send_keys('XYZ#qwerty')
        self.wd.find_element_by_xpath('//button[@name="register"]').click()
        self.wd.find_elements_by_xpath("//*[contains(text(), 'Another user with this email already exists')]")

def tearDown(self):
        self.wd.quit()

