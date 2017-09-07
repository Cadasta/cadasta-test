import pytest

from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from ..base_test import SeleniumTestCase
from ..entities import Project
from ..pages import ProjectsPage

pytestmark = pytest.mark.skip


class AddLocationRelationship(SeleniumTestCase):

    def test_attach_relationship_to_new_location(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text(Project.get_test_proj_name()).click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_link_text("Add location").click()

        self.wd.wait_for_xpath(
            "//h3[contains(text(), 'Draw location on map')]")
        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        self.wd.find_element_by_css_selector(
            "a.leaflet-draw-draw-marker").click()

        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//div[@id="id_geometry_map"]')
        action.move_to_element(elem).move_by_offset(15, 15).click().perform()

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        Select(
            self.wd.find_element_by_id("id_type")
        ).select_by_visible_text("Building")
        self.wd.find_element_by_xpath('//input[@value="Save"]').click()
        self.wd.wait_for_xpath("//span[contains(text(), 'Location')]")

        self.wd.find_element_by_link_text("Relationships").click()
        self.wd.find_element_by_link_text("Add relationship").click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        self.wd.wait_for_xpath("//h3[@class='modal-title']")
        try:
            self.wd.find_element_by_id("id_name").send_keys("party-1")
        except ElementNotVisibleException:
            self.wd.find_element_by_id("add-party").click()
            self.wd.find_element_by_id("id_name").send_keys("party-1")
        Select(
            self.wd.find_element_by_id("id_party_type")
        ).select_by_visible_text("Individual")
        Select(
            self.wd.find_element_by_id("id_tenure_type")
        ).select_by_visible_text("Freehold")
        self.wd.find_element_by_name("submit").click()
        self.wd.wait_for_xpath('//a[@href="#relationships"]')

    def test_attach_relationship_to_existing_location(self):
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

        self.wd.find_element_by_link_text("Relationships").click()
        self.wd.find_element_by_link_text("Add relationship").click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        self.wd.wait_for_xpath("//h3[@class='modal-title']")
        try:
            self.wd.find_element_by_id("id_name").send_keys("party-1")
        except ElementNotVisibleException:
            self.wd.find_element_by_id("add-party").click()
            self.wd.find_element_by_id("id_name").send_keys("party-1")
        Select(
            self.wd.find_element_by_id("id_party_type")
        ).select_by_visible_text("Individual")
        Select(
            self.wd.find_element_by_id("id_tenure_type")
        ).select_by_visible_text("Freehold")
        self.wd.find_element_by_name("submit").click()
        self.wd.wait_for_xpath('//a[@href="#relationships"]')


class ViewRelationshipDetails(SeleniumTestCase):

    def xtest_view_relationship_details(self):
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
        assert self.wd.wait_for_xpath(
            '//*[contains(text(), "Relationship Detail")]')


class EditRelationshipDetails(SeleniumTestCase):

    def xtest_edit_relationship_details(self):
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
        self.wd.wait_for_xpath('//a[@title="Edit relationship"]').click()
        self.wd.wait_for_xpath('//*[contains(text(), "Edit Relationship")]')
        Select(
            self.wd.find_element_by_id("id_tenure_type")
        ).select_by_visible_text("Leasehold")
        self.wd.find_element_by_xpath('//button[@type="submit"]').click()
        self.wd.wait_for_xpath('//*[contains(text(), "Relationship Detail")]')
        assert self.wd.wait_for_xpath('//*[contains(text(), "Leasehold")]')
