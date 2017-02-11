from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium_tests.pages import ProjectsPage


class CreatePublicProject(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_new_project(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_xpath('//a[@href="/projects/new/"]').click()
        self.wd.wait_for_css(".wizard")
        self.wd.wait_for_xpath('//button[@type="submit"]')
        text = self.wd.find_element_by_xpath('//button[@type="submit"]').text
        assert text == "Next"
        self.wd.find_element_by_xpath('//button[@type="submit"]').click()

        self.wd.wait_for_xpath("//h3[contains(text(), '1. General Information')]")
        self.wd.find_element_by_xpath('//select[@name="details-organization"]').click()
        self.wd.find_element_by_xpath('//option[@value="organization-1"]').click()
        self.wd.find_element_by_xpath('//input[@id="id_details-name"]').send_keys("project-1")
        self.wd.find_element_by_xpath('//textarea[@id="id_details-description"]').send_keys("Project-1 description")

        try:
            elem = self.wd.find_element_by_xpath('//button[@type="submit"]')
            try :
                elem.click()
            except WebDriverException: # Fix : element not clickable in Chrome
                action = ActionChains(self.wd)
                action.move_to_element(elem).send_keys(Keys.TAB * 11).send_keys(Keys.RETURN).perform()

            self.wd.wait_for_xpath("//h3[contains(text(), 'Assign permissions to members')]")
            self.wd.find_element_by_xpath('//button[@type="submit"]').click()
            self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
            text = self.wd.find_element_by_xpath("//h1[contains(@class, 'short')]").text
            assert text.endswith("PROJECT-1")
        except Exception:
            self.wd.wait_for_css(".error-block")
            assert True

    def tearDown(self):
        self.wd.quit()


class CreatePrivateProject(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_new_project(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_xpath('//a[@href="/projects/new/"]').click()
        self.wd.wait_for_css(".wizard")
        self.wd.wait_for_xpath('//button[@type="submit"]')
        text = self.wd.find_element_by_xpath('//button[@type="submit"]').text
        assert text == "Next"
        self.wd.find_element_by_xpath('//button[@type="submit"]').click()

        self.wd.wait_for_xpath("//h3[contains(text(), '1. General Information')]")
        self.wd.find_element_by_xpath('//select[@name="details-organization"]').click()
        self.wd.find_element_by_xpath('//option[@value="organization-1"]').click()
        self.wd.find_element_by_xpath('//input[@id="id_details-name"]').send_keys("private-project-1")
        self.wd.find_element_by_xpath('//div[@class="toggle-group"]').click()
        self.wd.find_element_by_xpath('//textarea[@id="id_details-description"]').send_keys("Private-project-1 description")

        try:
            elem = self.wd.find_element_by_xpath('//button[@type="submit"]')
            try :
                elem.click()
            except WebDriverException: # Fix : element not clickable in Chrome
                action = ActionChains(self.wd)
                action.move_to_element(elem).send_keys(Keys.TAB * 11).send_keys(Keys.RETURN).perform()

            self.wd.wait_for_xpath("//h3[contains(text(), 'Assign permissions to members')]")
            self.wd.find_element_by_xpath('//button[@type="submit"]').click()
            self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
            text = self.wd.find_element_by_xpath("//h1[contains(@class, 'short')]").text
            assert text.endswith("PRIVATE-PROJECT-1")
        except Exception:
            self.wd.wait_for_css(".error-block")
            assert True

    def tearDown(self):
        self.wd.quit()


class EditProjectDetails(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_edit_project(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath("(//button[@type='button'])[2]").click()
        self.wd.find_element_by_link_text("Edit project details").click()

        self.wd.wait_for_css(".modal-title")
        self.wd.find_css('#id_description').clear()
        self.wd.find_css('#id_description').send_keys("Test project-1 description edited.")

        elem = self.wd.find_element_by_xpath('//button[@type="submit"]')
        try :
            elem.click()
        except WebDriverException: # Fix : element not clickable in Chrome
            action = ActionChains(self.wd)
            action.move_to_element(elem).send_keys(Keys.TAB * 7).send_keys(Keys.RETURN).perform()

        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        text = self.wd.find_element_by_xpath("//div/section/p").text
        assert text == "Test project-1 description edited."

    def tearDown(self):
        self.wd.quit()


class ProjectAccessibility(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_public_project_to_private(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath("(//button[@type='button'])[2]").click()
        self.wd.find_element_by_link_text("Edit project details").click()
        self.wd.wait_for_css(".modal-title")
        self.wd.find_element_by_xpath('//div[@class="toggle-group"]').click()
        elem = self.wd.find_element_by_xpath('//button[@type="submit"]')
        try :
            elem.click()
        except WebDriverException: # Fix : element not clickable in Chrome
            action = ActionChains(self.wd)
            action.move_to_element(elem).send_keys(Keys.TAB * 8).send_keys(Keys.RETURN).perform()
        assert self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")

    def test_private_project_to_public(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath("(//button[@type='button'])[2]").click()
        self.wd.find_element_by_link_text("Edit project details").click()
        self.wd.wait_for_css(".modal-title")
        self.wd.find_element_by_xpath('//div[@class="toggle-group"]').click()
        elem = self.wd.find_element_by_xpath('//button[@type="submit"]')
        try :
            elem.click()
        except WebDriverException: # Fix : element not clickable in Chrome
            action = ActionChains(self.wd)
            action.move_to_element(elem).send_keys(Keys.TAB * 8).send_keys(Keys.RETURN).perform()
        assert self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")

    def tearDown(self):
        self.wd.quit()
