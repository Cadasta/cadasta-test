import os
from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium_tests.pages import ProjectsPage


class AddResource(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_add_resource(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        self.wd.find_element_by_link_text("Attach").click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        path = os.path.abspath("resources/pdf_file.pdf")
        try :
            self.wd.find_element_by_xpath("//*[contains(text(), 'Select the file to upload')]")
        except :
            self.wd.find_element_by_link_text("Upload new").click()
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector("input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("resource-1")
        self.wd.wait_for_xpath("//a[@class='file-link']")
        self.wd.find_element_by_name("submit").click()

        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        assert self.wd.find_element_by_xpath('//td/div/p/a/strong[contains(text(), "resource-1")]')

    def tearDown(self):
        self.wd.quit()


class RemoveResource(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_detach_resource_from_project(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        self.wd.find_element_by_xpath("//button[@role='button']").click()
        assert self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")

    def test_delete_resource(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        self.wd.find_element_by_link_text("deramola-gpx").click()
        self.wd.find_element_by_xpath("//a[@title='Delete resource']").click()
        self.wd.switch_to_window(self.wd.window_handles[-1])
        self.wd.get("%s%s" % (self.wd.current_url, "archive"))
        assert self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")

    def tearDown(self):
        self.wd.quit()
