from ..base_test import SeleniumTestCase
from ..entities import Organization
from ..pages import OrganizationsPage


class OrganizationSearch(SeleniumTestCase):

    def test_search_organization(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.go_to()

        self.wd.find_element_by_xpath('//input[@type="search"]').send_keys(
            Organization.get_test_org_name())
        elems = self.wd.find_elements_by_css_selector(".linked")
        assert len(elems) != 0

    def test_search_non_existing_organization(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.go_to()

        self.wd.find_element_by_xpath('//input[@type="search"]').send_keys(
            "organization-x")
        text = self.wd.find_css(".dataTables_empty").text
        assert text == "No matching records found"
