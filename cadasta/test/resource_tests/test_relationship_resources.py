import os
import pytest

from selenium.webdriver.common.action_chains import ActionChains

from ..base_test import SeleniumTestCase
from ..entities import Project
from ..pages import ProjectsPage

pytestmark = pytest.mark.skip


class AddRelationshipResource(SeleniumTestCase):

    def xtest_attach_existing_resource_to_relationship(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text(Project.get_test_proj_name()).click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//div[@id="project-map"]')
        action.move_to_element(elem).perform()
        self.wd.find_element_by_css_selector('img.leaflet-marker-icon').click()
        self.wd.find_element_by_link_text("Open location").click()
        self.wd.wait_for_xpath("//span[contains(text(), 'Location')]")
        self.wd.find_element_by_xpath(
            "//a[contains(text(),'Relationships')]").click()
        self.wd.find_element_by_xpath("//tr/td/a").click()
        self.wd.wait_for_xpath('//*[contains(text(), "Relationship Detail")]')
        self.wd.find_element_by_link_text("Attach").click()

        self.wd.find_element_by_xpath(
            '//tr/td/label/strong[contains(text(), "resource-1")]').click()
        self.wd.find_element_by_name("submit").click()
        self.wd.wait_for_xpath('//h4[contains(text(), "Resources")]')
        assert self.wd.find_element_by_xpath(
            '//*[contains(text(), "resource-1")]')

    def xtest_attach_new_resource_to_relationship(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text(Project.get_test_proj_name()).click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//div[@id="project-map"]')
        action.move_to_element(elem).perform()
        self.wd.find_element_by_css_selector('img.leaflet-marker-icon').click()
        self.wd.find_element_by_link_text("Open location").click()
        self.wd.wait_for_xpath("//span[contains(text(), 'Location')]")
        self.wd.find_element_by_xpath(
            "//a[contains(text(),'Relationships')]").click()
        self.wd.find_element_by_xpath("//tr/td/a").click()
        self.wd.wait_for_xpath('//*[contains(text(), "Relationship Detail")]')
        self.wd.find_element_by_link_text("Attach").click()
        self.wd.switch_to_window(self.wd.window_handles[-1])
        self.wd.find_element_by_link_text("Upload new").click()
        self.wd.wait_for_css("input.file-input")

        path = os.path.abspath("resources/resource-1.pdf")
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector(
            "input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("resource-2")
        self.wd.wait_for_xpath("//a[@class='file-link']")
        self.wd.find_element_by_name("submit").click()
        self.wd.wait_for_xpath('//h4[contains(text(), "Resources")]')
        assert self.wd.find_element_by_xpath(
            '//*[contains(text(), "resource-2")]')


class DetachRelationshipResource(SeleniumTestCase):

    def xtest_detach_resource(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text(Project.get_test_proj_name()).click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//div[@id="project-map"]')
        action.move_to_element(elem).perform()
        self.wd.find_element_by_css_selector('img.leaflet-marker-icon').click()
        self.wd.find_element_by_link_text("Open location").click()
        self.wd.wait_for_xpath("//span[contains(text(), 'Location')]")
        self.wd.find_element_by_xpath(
            "//a[contains(text(),'Relationships')]").click()
        self.wd.find_element_by_xpath("//tr/td/a").click()
        self.wd.wait_for_xpath('//*[contains(text(), "Relationship Detail")]')
        self.wd.find_element_by_xpath("//button[@type='submit']").click()
