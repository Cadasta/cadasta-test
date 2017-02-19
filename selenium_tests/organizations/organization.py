import time
from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium_tests.pages import OrganizationsPage
from selenium_tests.entities import Organization


class CreateOrganization(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_new_organization(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.go_to()
        self.wd.find_element_by_xpath('//a[@href="/organizations/new/"]').click()
        self.wd.wait_for_css(".modal-title")
        self.wd.wait_for_css("#id_name")
        org_name_available = False
        index = 1

        while not org_name_available:
            test_org_name = "organization-" + `index`
            self.wd.find_css('#id_name').clear()
            self.wd.find_css('#id_name').send_keys(test_org_name)
            self.wd.find_css('#id_description').clear()
            self.wd.find_css('#id_description').send_keys("Test organization description.")
            self.wd.find_element_by_xpath('//button[@name="submit"]').click()

            time.sleep(1)
            elems = self.wd.find_elements_by_xpath(
                "//*[contains(text(), 'Organization with this Name already exists.')]")
            if len(elems) == 0:
                org_name_available = True
                Organization().set_test_org_name(test_org_name)
                self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
                text = self.wd.find_element_by_xpath("//h1[contains(@class, 'short')]").text
                assert text == "ORGANIZATION-" + `index`
            else:
                index = index + 1

    def tearDown(self):
        self.wd.quit()


class EditOrganization(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_edit_organization(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.go_to()

        self.wd.find_element_by_link_text(Organization.get_test_org_name()).click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        self.wd.find_element_by_xpath("(//button[@type='button'])[2]").click()
        self.wd.find_element_by_link_text("Edit organization").click()
        self.wd.switch_to_window(self.wd.window_handles[-1])
        self.wd.wait_for_css("#id_description")
        self.wd.find_element_by_id("id_description").clear()
        self.wd.find_element_by_id("id_description").send_keys("Test organization description edited.")
        self.wd.find_element_by_name("submit").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        text = self.wd.find_element_by_xpath("//div/section/p").text
        assert text == "Test organization description edited."

    def tearDown(self):
        self.wd.quit()


class OrganizationArchive(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_archive_organization(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.go_to()

        self.wd.find_element_by_link_text(Organization.get_test_org_name()).click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        self.open("/organizations/" + Organization.get_test_org_name() + "/archive/")
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        text = self.wd.find_element_by_xpath("//span[contains(@class, 'label-danger')]").text
        assert text == "ARCHIVED"

    def test_unarchive_organization(self):
        organizations_page = OrganizationsPage(self.wd, self)
        organizations_page.go_to()

        self.wd.find_css("#archive-filter").click()
        self.wd.find_element_by_xpath('//option[@value="archived-True"]').click()
        self.wd.find_element_by_link_text(Organization.get_test_org_name()).click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        self.open("/organizations/" + Organization.get_test_org_name() + "/unarchive/")
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")

        try:
            self.wd.find_element_by_xpath("//span[contains(@class, 'label-danger')]")
        except NoSuchElementException:
            assert True

    def tearDown(self):
        self.wd.quit()