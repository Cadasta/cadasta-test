import os
from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium_tests.pages import ProjectsPage


class AddGPXResource(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_add_gpx_resource(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        self.wd.find_element_by_link_text("Attach").click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        path = os.path.abspath("resources/Deramola.gpx")
        try :
            self.wd.find_element_by_xpath("//*[contains(text(), 'Select the file to upload')]")
        except :
            self.wd.find_element_by_link_text("Upload new").click()
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector("input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("deramola-gpx")
        self.wd.wait_for_xpath("//a[@class='file-link']")
        self.wd.find_element_by_name("submit").click()

        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        assert self.wd.find_element_by_xpath('//td/div/p/a/strong[contains(text(), "deramola-gpx")]')

        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="map"]/a').click()
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

    def tearDown(self):
        self.wd.quit()


class LoadGPXFileOnMap(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_load_gpx_file_on_map(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")

        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="map"]/a').click()
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

    def tearDown(self):
        self.wd.quit()
