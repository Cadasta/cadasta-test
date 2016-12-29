from django.contrib.auth.models import User
from selenium.common.exceptions import NoSuchElementException

from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver

class NewRegistration(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def tearDown(self):
        self.wd.quit()

    def test_new_registration(self):
        self.open("/dashboard/")
        self.wd.find_element_by_xpath('//a[@href="/account/signup/"]').click()
        self.wd.wait_for_css("#signup_form")

        self.wd.find_css('#id_username').send_keys("user1")
        self.wd.find_css('#id_email').send_keys("user1@abc.com")
        self.wd.find_css("#id_password1").send_keys('user1#qwerty')
        self.wd.find_css("#id_password2").send_keys('user1#qwerty')
        self.wd.find_element_by_xpath('//button[@name="register"]').click()

        msgs = self.wd.find_element_by_xpath("//div[@id='messages']")
        try:
            msgs.find_element_by_xpath(
                ("div[contains(@class,'{}') and contains(.,'{}')]").
                format('alert', "signed in")
            )
        except NoSuchElementException as e:
            # Debugging help.
            print("Messages: " + msgs.text)
            # raise e

