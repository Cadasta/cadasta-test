from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from functional_tests.selenium_tests.pages import ProjectsPage


class AddLocation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_add_location(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_link_text("Add location").click()
        self.wd.wait_for_xpath("//h3[contains(text(), 'Draw location on map')]")

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')
        print page_state

        self.wd.find_element_by_xpath('//a[@class="leaflet-draw-draw-marker"]').click()
        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//div[@id="id_geometry_map"]')
        action.move_to_element(elem).move_by_offset(10, 10).click().perform()

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')

        Select(self.wd.find_element_by_id("id_type")).select_by_visible_text("Parcel")
        self.wd.find_element_by_xpath('//input[@value="Save"]').click()

        self.wd.wait_for_xpath("//span[contains(text(), 'Location')]")
        text = self.wd.find_element_by_xpath("//h2/span").text
        assert text == "LOCATION"

    def tearDown(self):
        self.wd.quit()


class EditLocation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_edit_location_details(self):
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
        self.wd.find_element_by_xpath("//a[@title='Edit location']").click()
        self.wd.wait_for_xpath("//h3[contains(text(), 'Draw location on map')]")
        Select(self.wd.find_element_by_id("id_type")).select_by_visible_text("Apartment")
        self.wd.find_element_by_xpath('//input[@value="Save"]').click()

        self.wd.wait_for_xpath("//span[contains(text(), 'Location')]")
        assert self.wd.find_element_by_xpath("//*[contains(text(), 'Apartment')]")

    def tearDown(self):
        self.wd.quit()


class DeleteLocation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_delete_location(self):
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
        self.wd.find_element_by_xpath("//a[@title='Delete location']").click()
        self.wd.switch_to_window(self.wd.window_handles[-1])
        self.wd.wait_for_xpath("//button[@value='Confirm']").click()

    def tearDown(self):
        self.wd.quit()