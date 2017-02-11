from selenium.common.exceptions import NoSuchElementException
from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium_tests.pages import RegistrationPage


class NewRegistration(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_new_registration(self):
        registration_page = RegistrationPage(self.wd, self)
        registration_page.go_to()

        self.wd.find_css('#id_username').send_keys("cadasta-test-user-1")
        self.wd.find_css('#id_email').send_keys("user1@abc.com")
        self.wd.find_css("#id_password1").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_password2").send_keys('XYZ#qwerty')
        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//button[@name="register"]')
        action.move_to_element(elem).click().perform()

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
        registration_page = RegistrationPage(self.wd, self)
        registration_page.go_to()

        self.wd.find_css('#id_username').send_keys("cadasta-test-user-1")
        self.wd.find_css('#id_email').send_keys("user@abc.com")
        self.wd.find_css("#id_password1").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_password2").send_keys('XYZ#qwerty')
        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//button[@name="register"]')
        action.move_to_element(elem).click().perform()
        self.wd.find_elements_by_xpath("//*[contains(text(), 'A user with that username already exists.')]")

    def tearDown(self):
        self.wd.quit()

class RegistrationAttemptEmailNotAvailable(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_registration_attempt_already_taken_email(self):
        registration_page = RegistrationPage(self.wd, self)
        registration_page.go_to()

        self.wd.find_css('#id_username').send_keys("cadasta-test-user")
        self.wd.find_css('#id_email').send_keys("user1@abc.com")
        self.wd.find_css("#id_password1").send_keys('XYZ#qwerty')
        self.wd.find_css("#id_password2").send_keys('XYZ#qwerty')
        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//button[@name="register"]')
        action.move_to_element(elem).click().perform()
        self.wd.find_elements_by_xpath("//*[contains(text(), 'Another user with this email already exists')]")

    def tearDown(self):
        self.wd.quit()

