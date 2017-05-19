import os
from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium_tests.pages import ProjectsPage
from selenium_tests.entities import Project


class AddLocationResource(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_attach_existing_resource_to_new_location(self):
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
        action.move_to_element(elem).move_by_offset(12, 12).click().perform()

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        Select(
            self.wd.find_element_by_id("id_type")
        ).select_by_visible_text("Building")
        self.wd.find_element_by_xpath('//input[@value="Save"]').click()
        self.wd.wait_for_xpath("//span[contains(text(), 'Location')]")

        self.wd.find_element_by_xpath(
            "//a[contains(text(),'Resources')]").click()
        self.wd.find_element_by_link_text("Attach").click()
        self.wd.find_element_by_xpath(
            '//tr/td/label/strong[contains(text(), "resource-1")]').click()
        self.wd.find_element_by_name("submit").click()
        self.wd.wait_for_xpath('//a[@href="#resources"]')
        assert self.wd.find_element_by_xpath(
            '//*[contains(text(), "resource-1")]')

    def test_attach_existing_resource_to_existing_location(self):
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
            "//a[contains(text(),'Resources')]").click()
        self.wd.find_element_by_link_text("Attach").click()

        self.wd.find_element_by_xpath(
            '//tr/td/label/strong[contains(text(), "resource-1")]').click()
        self.wd.find_element_by_name("submit").click()
        self.wd.wait_for_xpath('//a[@href="#resources"]')
        assert self.wd.find_element_by_xpath(
            '//*[contains(text(), "resource-1")]')

    def test_attach_new_resource_to_existing_location(self):
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
            "//a[contains(text(),'Resources')]").click()
        self.wd.find_element_by_link_text("Attach").click()
        self.wd.switch_to_window(self.wd.window_handles[-1])
        self.wd.find_element_by_link_text("Upload new").click()
        self.wd.wait_for_css("input.file-input")

        path = os.path.abspath("resources/pdf_file.pdf")
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector(
            "input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("resource-2")
        self.wd.wait_for_xpath("//a[@class='file-link']")
        self.wd.find_element_by_name("submit").click()
        self.wd.wait_for_xpath('//a[@href="#resources"]')
        assert self.wd.find_element_by_xpath(
            '//*[contains(text(), "resource-2")]')

    def tearDown(self):
        self.wd.quit()


class DetachLocationResource(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_detach_resource(self):
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
            "//a[contains(text(),'Resources')]").click()
        self.wd.find_element_by_xpath("//button[@type='submit']").click()

    def tearDown(self):
        self.wd.quit()
