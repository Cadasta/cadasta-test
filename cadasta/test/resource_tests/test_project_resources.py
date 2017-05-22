import os

from ..base_test import SeleniumTestCase
from ..pages import ProjectsPage, ResourcesPage


class AddResource(SeleniumTestCase):

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


class RemoveResource(SeleniumTestCase):

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
