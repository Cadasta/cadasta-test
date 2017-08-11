import pytest

from ..base_test import SeleniumTestCase
from ..entities import Project
from ..pages import ProjectsPage

pytestmark = pytest.mark.skip


class ProjectSearch(SeleniumTestCase):

    def test_search_project(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_xpath(
            '//input[@type="search"]').send_keys(Project.get_test_proj_name())
        elems = self.wd.find_elements_by_css_selector(".linked")
        assert len(elems) != 0

    def test_search_non_existing_project(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_xpath(
            '//input[@type="search"]').send_keys("project-x")
        text = self.wd.find_css(".dataTables_empty").text
        assert text == "No matching records found"
