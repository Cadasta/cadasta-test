import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from ..base_test import SeleniumTestCase
from ..entities import Organization
from ..pages import ProjectsPage


class AddProjectWithExtent(SeleniumTestCase):

    def test_new_project_with_extent(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()
        proj_name_available = False
        index = 1

        self.wd.find_element_by_xpath('//a[@href="/projects/new/"]').click()
        self.wd.wait_for_css(".wizard")

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        self.wd.find_element_by_xpath(
            '//a[@class="leaflet-draw-draw-polygon"]').click()
        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath(
            '//div[@id="id_extents_extent_map"]')
        action.move_to_element(elem).move_by_offset(10, 10).click().perform()
        action.move_to_element(elem).move_by_offset(15, 10).click().perform()
        action.move_to_element(elem).move_by_offset(15, 15).click().perform()
        action.move_to_element(elem).move_by_offset(10, 15).click().perform()
        action.move_to_element(elem).move_by_offset(10, 10).click().perform()

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        self.wd.find_element_by_xpath('//button[@type="submit"]').click()
        self.wd.wait_for_xpath(
            "//h3[contains(text(), '1. General Information')]")

        while not proj_name_available:
            test_proj_name = "project-with-extent-" + repr(index)
            Select(
                self.wd.find_element_by_name("details-organization")
            ).select_by_visible_text(Organization.get_test_org_name())
            self.wd.find_element_by_xpath(
                '//input[@id="id_details-name"]').clear()
            self.wd.find_element_by_xpath(
                '//input[@id="id_details-name"]').send_keys(test_proj_name)
            self.wd.find_element_by_xpath(
                '//textarea[@id="id_details-description"]').clear()
            self.wd.find_element_by_xpath(
                '//textarea[@id="id_details-description"]').send_keys(
                "Project-with-extent description")
            elem = self.wd.find_element_by_xpath('//button[@type="submit"]')
            try:
                elem.click()
            except WebDriverException:  # Fix : element not clickable in Chrome
                action = ActionChains(self.wd)
                action.move_to_element(elem).send_keys(
                    Keys.TAB * 11).send_keys(Keys.RETURN).perform()

            time.sleep(1)
            elems = self.wd.find_elements_by_xpath(
                "//*[contains(text(), "
                "'Project with this name already exists in this "
                "organization.')]")
            if len(elems) == 0:
                proj_name_available = True
                self.wd.wait_for_xpath(
                    "//h3[contains(text(), 'Assign permissions to members')]")
                self.wd.find_element_by_xpath(
                    '//button[@type="submit"]').click()
                self.wd.wait_for_xpath(
                    "//h2[contains(text(), 'Project Overview')]")
                text = self.wd.find_element_by_xpath(
                    "//h1[contains(@class, 'short')]").text
                assert text.endswith("PROJECT-WITH-EXTENT-" + repr(index))
            else:
                index = index + 1
