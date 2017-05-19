import time
from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium_tests.pages import ProjectsPage
from selenium_tests.entities import Project, Organization
from selenium.webdriver.support.ui import Select


class CreatePublicProject(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_new_project(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()
        proj_name_available = False
        index = 1

        self.wd.find_element_by_xpath('//a[@href="/projects/new/"]').click()
        self.wd.wait_for_css(".wizard")
        self.wd.wait_for_xpath('//button[@type="submit"]')
        text = self.wd.find_element_by_xpath('//button[@type="submit"]').text
        assert text == "Next"
        self.wd.find_element_by_xpath('//button[@type="submit"]').click()
        self.wd.wait_for_xpath(
            "//h3[contains(text(), '1. General Information')]")

        while not proj_name_available:
            test_proj_name = (
                Organization.get_test_org_name() + "-project-" + repr(index))
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
                "Project description")
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
                Project().set_test_proj_name(test_proj_name)
                self.wd.wait_for_xpath(
                    "//h3[contains(text(), 'Assign permissions to members')]")
                self.wd.find_element_by_xpath(
                    '//button[@type="submit"]').click()
                self.wd.wait_for_xpath(
                    "//h2[contains(text(), 'Project Overview')]")
                text = self.wd.find_element_by_xpath(
                    "//h1[contains(@class, 'short')]").text
                assert text.endswith("PROJECT-" + repr(index))
            else:
                index = index + 1

    def tearDown(self):
        self.wd.quit()


class CreatePrivateProject(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_new_project(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()
        proj_name_available = False
        index = 1

        self.wd.find_element_by_xpath('//a[@href="/projects/new/"]').click()
        self.wd.wait_for_css(".wizard")
        self.wd.wait_for_xpath('//button[@type="submit"]')
        text = self.wd.find_element_by_xpath('//button[@type="submit"]').text
        assert text == "Next"
        self.wd.find_element_by_xpath('//button[@type="submit"]').click()
        self.wd.wait_for_xpath(
            "//h3[contains(text(), '1. General Information')]")

        while not proj_name_available:
            test_proj_name = "private-project-" + repr(index)
            Select(
                self.wd.find_element_by_name("details-organization")
            ).select_by_visible_text(Organization.get_test_org_name())
            self.wd.find_element_by_xpath(
                '//input[@id="id_details-name"]').clear()
            self.wd.find_element_by_xpath(
                '//input[@id="id_details-name"]').send_keys(test_proj_name)
            self.wd.find_element_by_xpath(
                '//div[@class="toggle-group"]').click()
            self.wd.find_element_by_xpath(
                '//textarea[@id="id_details-description"]').clear()
            self.wd.find_element_by_xpath(
                '//textarea[@id="id_details-description"]').send_keys(
                "Private project description")
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
                assert text.endswith("PRIVATE-PROJECT-" + repr(index))
            else:
                index = index + 1

    def tearDown(self):
        self.wd.quit()


class EditProjectDetails(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_edit_project(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text(Project.get_test_proj_name()).click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath("(//button[@type='button'])[2]").click()
        self.wd.find_element_by_link_text("Edit project details").click()

        self.wd.wait_for_css(".modal-title")
        self.wd.find_css('#id_description').clear()
        self.wd.find_css('#id_description').send_keys(
            "Test project description edited.")

        elem = self.wd.find_element_by_xpath('//button[@type="submit"]')
        try:
            elem.click()
        except WebDriverException:  # Fix : element not clickable in Chrome
            action = ActionChains(self.wd)
            action.move_to_element(elem).send_keys(
                Keys.TAB * 7).send_keys(Keys.RETURN).perform()

        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        text = self.wd.find_element_by_xpath("//div/section/p").text
        assert text == "Test project description edited."

    def tearDown(self):
        self.wd.quit()


class ProjectAccessibility(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_public_project_to_private(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text(Project.get_test_proj_name()).click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath("(//button[@type='button'])[2]").click()
        self.wd.find_element_by_link_text("Edit project details").click()
        self.wd.wait_for_css(".modal-title")
        self.wd.find_element_by_xpath('//div[@class="toggle-group"]').click()
        elem = self.wd.find_element_by_xpath('//button[@type="submit"]')
        try:
            elem.click()
        except WebDriverException:  # Fix : element not clickable in Chrome
            action = ActionChains(self.wd)
            action.move_to_element(elem).send_keys(
                Keys.TAB * 8).send_keys(Keys.RETURN).perform()
        assert self.wd.wait_for_xpath(
            "//h2[contains(text(), 'Project Overview')]")

    def test_private_project_to_public(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text(Project.get_test_proj_name()).click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath("(//button[@type='button'])[2]").click()
        self.wd.find_element_by_link_text("Edit project details").click()
        self.wd.wait_for_css(".modal-title")
        self.wd.find_element_by_xpath('//div[@class="toggle-group"]').click()
        elem = self.wd.find_element_by_xpath('//button[@type="submit"]')
        try:
            elem.click()
        except WebDriverException:  # Fix : element not clickable in Chrome
            action = ActionChains(self.wd)
            action.move_to_element(elem).send_keys(
                Keys.TAB * 8).send_keys(Keys.RETURN).perform()
        assert self.wd.wait_for_xpath(
            "//h2[contains(text(), 'Project Overview')]")

    def tearDown(self):
        self.wd.quit()
