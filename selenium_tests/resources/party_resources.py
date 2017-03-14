import os
from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium_tests.pages import ProjectsPage


class PartyResource(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_add_new_resource_to_party(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()
        projects_page.open_parties_page()

        self.wd.find_element_by_link_text("party-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Party detail')]")
        self.wd.find_element_by_link_text("Resources").click()
        self.wd.wait_for_xpath("//*[@id=\"resources\"][contains(@class, 'active')]")
        self.wd.find_element_by_link_text("Attach").click()
        self.wd.switch_to_window(self.wd.window_handles[-1])
        try :
            self.wd.find_element_by_xpath("//*[contains(text(), 'Upload new resource')]")
        except :
            self.wd.find_element_by_link_text("Upload new").click()
        self.wd.wait_for_css("input.file-input")

        path = os.path.abspath("resources/pdf_file.pdf")
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector("input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("resource-2")
        self.wd.wait_for_xpath("//a[@class='file-link']")
        self.wd.find_element_by_name("submit").click()

        self.wd.wait_for_xpath("//h2[contains(text(), 'Party detail')]")
        assert self.wd.find_element_by_xpath('//td/div/p/a/strong[contains(text(), "resource-2")]')

    def test_attach_existing_resource_to_party(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()
        projects_page.open_parties_page()

        self.wd.find_element_by_link_text("party-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Party detail')]")
        self.wd.find_element_by_link_text("Resources").click()
        self.wd.wait_for_xpath("//*[@id=\"resources\"][contains(@class, 'active')]")
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
        self.wd.find_element_by_link_text("Resources").click()
        self.wd.wait_for_xpath("//*[@id=\"resources\"][contains(@class, 'active')]")
        self.wd.find_element_by_xpath("//button[@role='button']").click()
        assert self.wd.wait_for_xpath("//h2[contains(text(), 'Party detail')]")

    def tearDown(self):
        self.wd.quit()
