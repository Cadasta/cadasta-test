from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver

class NewOrganization(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_new_organization(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/organizations/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/new/"]').click()
        self.wd.wait_for_css(".modal-title")
        self.wd.wait_for_css("#id_name")
        self.wd.find_css('#id_name').send_keys("organization-1")
        self.wd.find_css('#id_description').send_keys("Test organization-1 description.")
        self.wd.find_element_by_xpath('//button[@name="submit"]').click()

        try:
            self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
            text = self.wd.find_element_by_xpath("//h1[contains(@class, 'short')]").text
            assert text == "ORGANIZATION-1"

        except Exception:
            self.wd.wait_for_css(".error-block")

    def tearDown(self):
        self.wd.quit()