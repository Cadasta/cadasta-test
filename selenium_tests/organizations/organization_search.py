from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium_tests.pages import OrganizationsPage


class OrganizationSearch(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_search_organization(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.go_to()

        self.wd.find_element_by_xpath('//input[@type="search"]').send_keys("organization-1")
        elems = self.wd.find_elements_by_css_selector(".linked")
        assert len(elems) != 0

    def test_search_non_existing_organization(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.go_to()

        self.wd.find_element_by_xpath('//input[@type="search"]').send_keys("organization-x")
        text = self.wd.find_css(".dataTables_empty").text
        assert text == "No matching records found"

    def tearDown(self):
        self.wd.quit()