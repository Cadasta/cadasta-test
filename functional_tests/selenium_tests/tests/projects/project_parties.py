import os
from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver
from selenium.webdriver.support.ui import Select
from functional_tests.selenium_tests.pages import ProjectsPage


class ViewParty(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_view_party(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="parties"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Parties')]")
        self.wd.find_element_by_link_text("party-1").click()

        text = self.wd.find_element_by_xpath("//div[@class='page-title']/h2").text
        assert text == "PARTY DETAIL"

    def tearDown(self):
        self.wd.quit()


class PartyResource(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_attach_resource_to_party(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="parties"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Parties')]")
        self.wd.find_element_by_link_text("party-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Party detail')]")
        self.wd.find_element_by_link_text("Attach").click()
        self.wd.switch_to_window(self.wd.window_handles[-1])
        self.wd.find_element_by_xpath('//tr/td/label/strong[contains(text(), "resource-1")]').click()
        self.wd.find_element_by_name("submit").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Party detail')]")
        assert self.wd.find_element_by_xpath('//td/div/p/a/strong[contains(text(), "resource-1")]')

    def test_detach_resource_from_party(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="parties"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Parties')]")
        self.wd.find_element_by_link_text("party-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Party detail')]")
        self.wd.find_element_by_link_text("Detach").click()
        assert not self.wd.find_element_by_xpath('//td/div/p/a/strong[contains(text(), "resource-1")]')

    def tearDown(self):
        self.wd.quit()


class EditParty(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_edit_party(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="parties"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Parties')]")
        self.wd.find_element_by_link_text("party-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Party detail')]")
        self.wd.find_element_by_xpath("//a[@title='Edit party']").click()
        self.wd.switch_to_window(self.wd.window_handles[-1])
        Select(self.wd.find_element_by_id("id_type")).select_by_visible_text("Group")
        self.wd.find_element_by_name("submit").click()
        text = self.wd.find_element_by_xpath("//table/tbody/tr[2]/td[2]").text
        assert text == "Group"

    def tearDown(self):
        self.wd.quit()


class DeleteParty(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_delete_party(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="parties"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Parties')]")
        self.wd.find_element_by_link_text("party-1").click()
        self.wd.find_element_by_xpath("//a[@title='Delete party']").click()
        self.wd.switch_to_window(self.wd.window_handles[-1])
        self.wd.wait_for_xpath("//button[@value='Confirm']").click()

    def tearDown(self):
        self.wd.quit()

