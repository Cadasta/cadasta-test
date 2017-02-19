from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium_tests.pages import ProjectsPage
from selenium_tests.entities import Project


class ProjectSearch(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_search_project(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_xpath('//input[@type="search"]').send_keys(Project.get_test_proj_name())
        elems = self.wd.find_elements_by_css_selector(".linked")
        assert len(elems) != 0

    def test_search_non_existing_project(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_xpath('//input[@type="search"]').send_keys("project-x")
        text = self.wd.find_css(".dataTables_empty").text
        assert text == "No matching records found"

    def tearDown(self):
        self.wd.quit()