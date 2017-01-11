from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver

class DuplicateOrganizationNameValidation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_organization_name_validation(self):
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
        self.wd.wait_for_css(".errorlist")
        elems = self.wd.find_elements_by_xpath("//*[contains(text(), 'Organization with this Name already exists.')]")
        assert len(elems) != 0

    def tearDown(self):
        self.wd.quit()


class EmptyOrganizationNameValidation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_empty_organization_name_validation(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/organizations/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/new/"]').click()
        self.wd.wait_for_css(".modal-title")
        self.wd.wait_for_css("#id_name")
        self.wd.find_css('#id_name').send_keys("")
        self.wd.find_css('#id_description').send_keys("Test organization-1 description.")
        self.wd.find_element_by_xpath('//button[@name="submit"]').click()
        self.wd.wait_for_css(".has-error")

        elems = self.wd.find_elements_by_xpath("//*[contains(text(), 'This field is required.')]")
        assert len(elems) != 0

    def tearDown(self):
        self.wd.quit()


class OrganizationURLValidation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_empty_organization_url_validation(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/organizations/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/new/"]').click()
        self.wd.wait_for_css(".modal-title")
        self.wd.wait_for_css("#id_name")
        self.wd.find_css('#id_name').send_keys("organization-x")
        self.wd.find_css('#id_urls').send_keys("http:localhost")
        self.wd.find_element_by_xpath('//button[@name="submit"]').click()
        self.wd.wait_for_css(".has-error")

        elems = self.wd.find_elements_by_xpath("//*[contains(text(), 'This value should be a valid url.')]")
        assert len(elems) != 0

    def tearDown(self):
            self.wd.quit()