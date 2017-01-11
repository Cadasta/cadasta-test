from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver

class OrganizationSearch(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_search_organization(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/organizations/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")
        self.wd.find_element_by_xpath('//input[@type="search"]').send_keys("organization-1")

        elems = self.wd.find_elements_by_css_selector(".linked")
        assert len(elems) != 0

    def test_search_non_existing_organization(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/organizations/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")
        self.wd.find_element_by_xpath('//input[@type="search"]').send_keys("organization-x")

        text = self.wd.find_css(".dataTables_empty").text
        assert text == "No matching records found"

    def tearDown(self):
        self.wd.quit()