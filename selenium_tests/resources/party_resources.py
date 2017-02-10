from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium_tests.pages import ProjectsPage


class PartyResource(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_attach_resource_to_party(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()
        projects_page.open_parties_page()

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
        projects_page.open_parties_page()

        self.wd.find_element_by_link_text("party-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Party detail')]")
        self.wd.find_element_by_link_text("Detach").click()
        assert not self.wd.find_element_by_xpath('//td/div/p/a/strong[contains(text(), "resource-1")]')

    def tearDown(self):
        self.wd.quit()
