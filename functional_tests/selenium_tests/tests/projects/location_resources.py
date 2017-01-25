from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

class AddLocationResource(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_attach_resource_to_new_location(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.wd.find_element_by_link_text("Projects").click()
        self.wd.wait_for_xpath("//h1[contains(text(), 'Projects')]")
        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_link_text("Add location").click()

        self.wd.wait_for_xpath("//h3[contains(text(), 'Draw location on map')]")
        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        self.wd.find_element_by_css_selector("a.leaflet-draw-draw-marker").click()

        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//div[@id="id_geometry_map"]')
        action.move_to_element(elem).move_by_offset(12, 12).click().perform()

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        Select(self.wd.find_element_by_id("id_type")).select_by_visible_text("Building")
        self.wd.find_element_by_xpath('//input[@value="Save"]').click()
        self.wd.wait_for_xpath("//span[contains(text(), 'Location')]")

        self.wd.find_element_by_xpath("//a[contains(text(),'Resources')]").click()
        self.wd.find_element_by_link_text("Attach").click()
        self.wd.find_element_by_xpath('//tr/td/label/strong[contains(text(), "resource-1")]').click()
        self.wd.find_element_by_name("submit").click()
        self.wd.wait_for_xpath('//a[@href="#resources"]')

    def test_attach_resource_to_existing_location(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.wd.find_element_by_link_text("Projects").click()
        self.wd.wait_for_xpath("//h1[contains(text(), 'Projects')]")
        self.wd.find_element_by_link_text("project-1").click()
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
        self.wd.find_element_by_xpath("//a[contains(text(),'Resources')]").click()
        self.wd.find_element_by_link_text("Attach").click()

        self.wd.find_element_by_xpath('//tr/td/label/strong[contains(text(), "resource-1")]').click()
        self.wd.find_element_by_name("submit").click()
        self.wd.wait_for_xpath('//a[@href="#resources"]')

    def tearDown(self):
        self.wd.quit()

