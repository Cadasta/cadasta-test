class RegistrationPage:

    def __init__(self, web_driver, test_case):
        self.wd = web_driver
        self.test = test_case

    def go_to(self):
        self.open("/dashboard/")
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
        self.wd.find_element_by_xpath('//a[@href="/organizations/new/"]').click()
        self.wd.switch_to_window(self.wd.window_handles[-1])
        self.wd.wait_for_css(".modal-title")

    def open_members_page(self):
        self.wd.find_element_by_link_text("organization-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
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


