import os
from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium_tests.pages import ProjectsPage
from selenium_tests.pages import ResourcesPage


class InvalidFileTypes(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

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

    def tearDown(self):
        self.wd.quit()

