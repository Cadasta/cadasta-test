import os

from ..base_test import SeleniumTestCase
from ..pages import ProjectsPage, ResourcesPage


class InvalidFileTypes(SeleniumTestCase):

    def attempt_upload_invalid_file(self, file_path, resource_name):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()
        resources_page = ResourcesPage(self.wd, self)
        resources_page.go_to()
        resources_page.upload_resource(file_path, resource_name)

    def test_attempt_add_python_file(self):
        path = os.path.abspath("resources/python_file.py")
        self.attempt_upload_invalid_file(path, "python-resource-1")
        assert self.wd.wait_for_css('.has-error')

    def test_attempt_add_file_with_no_ext(self):
        path = os.path.abspath("resources/no_ext_file")
        self.attempt_upload_invalid_file(path, "no-ext-resource-1")
        assert self.wd.wait_for_css('.has-error')
