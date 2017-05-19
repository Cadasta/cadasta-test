import os
from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium_tests.pages import ProjectsPage
from selenium_tests.pages import ResourcesPage


class AddResource(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_add_resource(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()
        resources_page = ResourcesPage(self.wd, self)
        resources_page.go_to()
        file_path = os.path.abspath("resources/pdf_file.pdf")
        resources_page.upload_resource(file_path, "resource-1")
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        assert self.wd.find_element_by_xpath(
            '//td/div/p/a/strong[contains(text(), "resource-1")]')

    def tearDown(self):
        self.wd.quit()


class RemoveResource(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_detach_resource_from_project(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()
        resources_page = ResourcesPage(self.wd, self)
        resources_page.go_to()
        self.wd.find_element_by_xpath("//button[@role='button']").click()
        assert self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")

    def test_delete_resource(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()
        resources_page = ResourcesPage(self.wd, self)
        resources_page.go_to()
        self.wd.find_element_by_link_text("deramola-gpx").click()
        self.wd.find_element_by_xpath("//a[@title='Delete resource']").click()
        self.wd.switch_to_window(self.wd.window_handles[-1])
        self.wd.get("%s%s" % (self.wd.current_url, "archive"))
        assert self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")

    def tearDown(self):
        self.wd.quit()
