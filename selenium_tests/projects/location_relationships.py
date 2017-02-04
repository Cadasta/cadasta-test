from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotVisibleException
from functional_tests.selenium_tests.pages import ProjectsPage


class AddLocationRelationship(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_attach_relationship_to_new_location(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

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
        action.move_to_element(elem).move_by_offset(15, 15).click().perform()

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        Select(self.wd.find_element_by_id("id_type")).select_by_visible_text("Building")
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
        Select(self.wd.find_element_by_id("id_party_type")).select_by_visible_text("Individual")
        Select(self.wd.find_element_by_id("id_tenure_type")).select_by_visible_text("Freehold")
        self.wd.find_element_by_name("submit").click()
        self.wd.wait_for_xpath('//a[@href="#relationships"]')

    def test_attach_relationship_to_existing_location(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

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

        self.wd.find_element_by_link_text("Relationships").click()
        self.wd.find_element_by_link_text("Add relationship").click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        self.wd.wait_for_xpath("//h3[@class='modal-title']")
        try:
            self.wd.find_element_by_id("id_name").send_keys("party-1")
        except ElementNotVisibleException:
            self.wd.find_element_by_id("add-party").click()
            self.wd.find_element_by_id("id_name").send_keys("party-1")
        Select(self.wd.find_element_by_id("id_party_type")).select_by_visible_text("Individual")
        Select(self.wd.find_element_by_id("id_tenure_type")).select_by_visible_text("Freehold")
        self.wd.find_element_by_name("submit").click()
        self.wd.wait_for_xpath('//a[@href="#relationships"]')

    def tearDown(self):
        self.wd.quit()

