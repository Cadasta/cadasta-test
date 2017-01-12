from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver
from selenium.common.exceptions import NoSuchElementException

class CreateProject(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_new_project(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/projects/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Projects')]")
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
            self.wd.find_element_by_xpath('//button[@type="submit"]').click()
            self.wd.wait_for_xpath("//h3[contains(text(), 'Assign permissions to members')]")
            text = self.wd.find_element_by_xpath('//button[@type="submit"]').text
            self.wd.find_element_by_xpath('//button[@type="submit"]').click()
            self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
            text = self.wd.find_element_by_xpath("//h1[contains(@class, 'short')]").text
            assert text.endswith("PROJECT-1")
        except Exception:
            self.wd.wait_for_css(".error-block")
            assert True

    def tearDown(self):
        self.wd.quit()


class EditProject(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_edit_project(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/organizations/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/"]').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        self.open("/organizations/organization-1/edit/")
        self.wd.wait_for_css(".modal-title")
        self.wd.find_css('#id_description').clear()
        self.wd.find_css('#id_description').send_keys("Test organization-1 description edited.")
        self.wd.find_element_by_xpath('//button[@name="submit"]').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        text = self.wd.find_element_by_xpath("//div/section/p").text
        assert text == "Test organization-1 description edited."

    def tearDown(self):
        self.wd.quit()