import pytest

from ..base_test import SeleniumTestCase
from ..entities import Project, Organization

pytestmark = pytest.mark.skip


class AnonymousUserOrganizationView(SeleniumTestCase):

    def test_anonymous_user_project_view(self):
        self.open("")
        self.wd.wait_for_css(".organizations")
        self.wd.find_element_by_link_text("Organizations").click()
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")
        self.wd.find_element_by_link_text(
            Organization.get_test_org_name()).click()
        self.wd.wait_for_xpath(
            "//h2[contains(text(), 'Organization Overview')]")
        assert self.wd.find_element_by_xpath("//div/section/p")


class AnonymousUserProjectView(SeleniumTestCase):

    def test_anonymous_user_project_view(self):
        self.open("")
        self.wd.wait_for_css(".projects")
        self.wd.find_element_by_link_text("Projects").click()
        self.wd.wait_for_xpath("//h1[contains(text(), 'Projects')]")
        self.wd.find_element_by_link_text(Project.get_test_proj_name()).click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        assert self.wd.wait_for_xpath("//*[contains(text(), 'Sign in')]")
