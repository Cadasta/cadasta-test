from ..base_test import SeleniumTestCase
from ..entities import Organization
from ..pages import OrganizationsPage


class DuplicateOrganizationNameValidation(SeleniumTestCase):

    def test_organization_name_validation(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.create_new_org_form()

        self.wd.find_css('#id_name').send_keys(
            Organization.get_test_org_name())
        self.wd.find_css('#id_description').send_keys(
            "Test organization description.")
        self.wd.find_element_by_xpath('//button[@name="submit"]').click()
        self.wd.wait_for_css(".errorlist")
        elems = self.wd.find_elements_by_xpath(
            "//*[contains(text(), "
            "'Organization with this Name already exists.')]")
        assert len(elems) != 0


class EmptyOrganizationNameValidation(SeleniumTestCase):

    def test_empty_organization_name_validation(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.create_new_org_form()

        self.wd.find_css('#id_name').send_keys("")
        self.wd.find_css('#id_description').send_keys(
            "Test organization description.")
        self.wd.find_element_by_xpath('//button[@name="submit"]').click()
        self.wd.wait_for_css(".has-error")

        elems = self.wd.find_elements_by_xpath(
            "//*[contains(text(), 'This field is required.')]")
        assert len(elems) != 0


class OrganizationURLValidation(SeleniumTestCase):

    def test_empty_organization_url_validation(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.create_new_org_form()

        self.wd.find_css('#id_name').send_keys("organization-x")
        self.wd.find_css('#id_urls').send_keys("http:localhost")
        self.wd.find_element_by_xpath('//button[@name="submit"]').click()
        self.wd.wait_for_css(".has-error")

        elems = self.wd.find_elements_by_xpath(
            "//*[contains(text(), 'This value should be a valid url.')]")
        assert len(elems) != 0
