import os
from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium_tests.pages import ProjectsPage


class InvalidFileTypes(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_attempt_add_python_file(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        self.wd.find_element_by_link_text("Attach").click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        path = os.path.abspath("resources/python_file.py")
        try :
            self.wd.find_element_by_xpath("//*[contains(text(), 'Select the file to upload')]")
        except :
            self.wd.find_element_by_link_text("Upload new").click()
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector("input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("python-resource-1")
        self.wd.find_element_by_name("submit").click()
        assert self.wd.wait_for_css('.has-error')

    def test_attempt_add_file_with_no_ext(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        self.wd.find_element_by_link_text("Attach").click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        path = os.path.abspath("resources/no_ext_file")
        try :
            self.wd.find_element_by_xpath("//*[contains(text(), 'Select the file to upload')]")
        except :
            self.wd.find_element_by_link_text("Upload new").click()
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector("input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("no-ext-resource-1")
        self.wd.find_element_by_name("submit").click()
        assert self.wd.wait_for_css('.has-error')

    def tearDown(self):
        self.wd.quit()

