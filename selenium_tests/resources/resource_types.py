import os
from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium_tests.pages import ProjectsPage
from selenium_tests.pages import ResourcesPage


class AcceptedResourceTypes(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def upload_valid_resource(self, file_path, resource_name):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()
        resources_page = ResourcesPage(self.wd, self)
        resources_page.go_to()
        resources_page.upload_resource(file_path, resource_name)
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")

    def test_add_csv_resource(self):
        path = os.path.abspath("resources/csv_file.csv")
        self.upload_valid_resource(path, "csv-resource-1")
        assert self.wd.wait_for_xpath('//td/div/p/a/strong[contains(text(), "csv-resource-1")]')

    def test_add_doc_resource(self):
        path = os.path.abspath("resources/doc_file.doc")
        self.upload_valid_resource(path, "doc-resource-1")
        assert self.wd.wait_for_xpath('//td/div/p/a/strong[contains(text(), "doc-resource-1")]')

    def test_add_docx_resource(self):
        path = os.path.abspath("resources/docx_file.docx")
        self.upload_valid_resource(path, "docx-resource-1")
        assert self.wd.wait_for_xpath('//td/div/p/a/strong[contains(text(), "docx-resource-1")]')

    def test_add_jpg_resource(self):
        path = os.path.abspath("resources/jpg_file.jpg")
        self.upload_valid_resource(path, "jpg-resource-1")
        assert self.wd.wait_for_xpath('//td/div/p/a/strong[contains(text(), "jpg-resource-1")]')

    def test_add_mp3_resource(self):
        path = os.path.abspath("resources/mp3_file.mp3")
        self.upload_valid_resource(path, "mp3-resource-1")
        assert self.wd.wait_for_xpath('//td/div/p/a/strong[contains(text(), "mp3-resource-1")]')

    def test_add_mp4_resource(self):
        path = os.path.abspath("resources/mp4_file.mp4")
        self.upload_valid_resource(path, "mp4-resource-1")
        assert self.wd.wait_for_xpath('//td/div/p/a/strong[contains(text(), "mp4-resource-1")]')

    def test_add_png_resource(self):
        path = os.path.abspath("resources/png_file.png")
        self.upload_valid_resource(path, "png-resource-1")
        assert self.wd.wait_for_xpath('//td/div/p/a/strong[contains(text(), "png-resource-1")]')

    def tearDown(self):
        self.wd.quit()

