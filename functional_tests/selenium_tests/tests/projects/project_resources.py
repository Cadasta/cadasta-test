import os
from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver


class AddResource(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_add_resource(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/projects/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Projects')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/projects/project-1/"]').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/projects/project-1/resources/add/new/"]').click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        path = os.path.abspath("resources/resource-1.pdf")
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector("input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("resource-1")
        self.wd.wait_for_xpath("//a[@class='file-link']")
        self.wd.find_element_by_name("submit").click()

        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        assert self.wd.find_element_by_xpath('//td/div/p/a/strong[contains(text(), "resource-1")]')

    def tearDown(self):
        self.wd.quit()
