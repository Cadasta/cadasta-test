import os

from selenium.webdriver.common.action_chains import ActionChains

from ..base_test import SeleniumTestCase
from ..entities import Project
from ..pages import ProjectsPage, ResourcesPage


class AddGPXResource(SeleniumTestCase):

    def test_add_gpx_resource(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()
        resources_page = ResourcesPage(self.wd, self)
        resources_page.go_to()
        file_path = os.path.abspath("resources/Deramola.gpx")
        resources_page.upload_resource(file_path, "deramola-gpx")
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        assert self.wd.find_element_by_xpath(
            '//td/div/p/a/strong[contains(text(), "deramola-gpx")]')

        self.wd.find_element_by_xpath(
            '//div[@id="sidebar"]/ul/li[@class="map"]/a').click()
        self.wd.wait_for_xpath('//div[@id="project-map"]')
        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//div[@id="project-map"]')
        action.move_to_element(elem).perform()
        self.wd.find_element_by_xpath("//a[@title='Layers']").click()
        self.wd.wait_for_css(".leaflet-control-layers-expanded")

        assert self.wd.find_css(".leaflet-control-layers-selector")
        text = self.wd.find_css(".leaflet-control-layers-group-name").text
        assert text == "deramola-gpx"


class LoadGPXFileOnMap(SeleniumTestCase):

    def test_load_gpx_file_on_map(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text(Project.get_test_proj_name()).click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")

        self.wd.find_element_by_xpath(
            '//div[@id="sidebar"]/ul/li[@class="map"]/a').click()
        self.wd.wait_for_xpath('//div[@id="project-map"]')
        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//div[@id="project-map"]')
        action.move_to_element(elem).perform()
        self.wd.find_element_by_xpath("//a[@title='Layers']").click()
        self.wd.wait_for_css(".leaflet-control-layers-expanded")

        self.wd.find_element_by_xpath("//input[@type='checkbox']").click()
        assert self.wd.find_element_by_css_selector('img.leaflet-marker-icon')
