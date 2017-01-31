from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver
from functional_tests.selenium_tests.pages import OrganizationsPage


class DuplicateOrganizationNameValidation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_organization_name_validation(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.create_new_org_form()

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
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.create_new_org_form()

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
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.create_new_org_form()

        self.wd.find_css('#id_name').send_keys("organization-x")
        self.wd.find_css('#id_urls').send_keys("http:localhost")
        self.wd.find_element_by_xpath('//button[@name="submit"]').click()
        self.wd.wait_for_css(".has-error")

        elems = self.wd.find_elements_by_xpath("//*[contains(text(), 'This value should be a valid url.')]")
        assert len(elems) != 0

    def tearDown(self):
            self.wd.quit()