import time

from selenium.common.exceptions import NoSuchElementException

from .entities import Organization, Project


class RegistrationPage:

    def __init__(self, web_driver, test_case):
        self.wd = web_driver
        self.test = test_case

    def go_to(self):
        self.test.open("/dashboard/")
        self.wd.find_element_by_xpath('//a[@href="/account/signup/"]').click()
        self.wd.wait_for_css("#signup_form")


class OrganizationsPage:

    def __init__(self, web_driver, test_case):
        self.wd = web_driver
        self.test = test_case

    def go_to(self):
        self.test.user_login()
        self.wd.wait_for_css('.btn-user')
        self.wd.find_element_by_link_text("Organizations").click()
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")

    def create_new_org_form(self):
        self.go_to()
        self.wd.find_element_by_xpath(
            '//a[@href="/organizations/new/"]').click()
        self.wd.switch_to_window(self.wd.window_handles[-1])
        self.wd.wait_for_css(".modal-title")

    def open_members_page(self):
        self.wd.find_element_by_link_text(
            Organization.get_test_org_name()).click()
        self.wd.wait_for_xpath(
            "//h2[contains(text(), 'Organization Overview')]")
        self.wd.find_element_by_css_selector("span.icon.members").click()
        self.wd.wait_for_css('.table')


class ProjectsPage:

    def __init__(self, web_driver, test_case):
        self.wd = web_driver
        self.test = test_case

    def go_to(self):
        self.test.user_login()
        self.wd.wait_for_css('.btn-user')
        self.wd.find_element_by_link_text("Projects").click()
        self.wd.wait_for_xpath("//h1[contains(text(), 'Projects')]")

    def open_parties_page(self):
        self.wd.find_element_by_link_text(Project.get_test_proj_name()).click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath(
            '//div[@id="sidebar"]/ul/li[@class="parties"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Parties')]")


class ResourcesPage:
    def __init__(self, web_driver, test_case):
        self.wd = web_driver
        self.test = test_case

    def go_to(self):
        self.wd.find_element_by_link_text(Project.get_test_proj_name()).click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath(
            '//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")

    def upload_resource(self, file_path, resource_name):
        self.wd.find_element_by_link_text("Attach").click()
        self.wd.switch_to_window(self.wd.window_handles[-1])
        try:
            self.wd.find_element_by_xpath(
                "//*[contains(text(), 'Select the file to upload')]")
        except NoSuchElementException:
            self.wd.find_element_by_link_text("Upload new").click()
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector("input.file-input").send_keys(
            file_path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys(resource_name)
        self.wd.wait_for_xpath("//a[@class='file-link']")
        while self.wd.find_element_by_name("submit").get_attribute("disabled"):
            time.sleep(1)
        self.wd.find_element_by_name("submit").click()
