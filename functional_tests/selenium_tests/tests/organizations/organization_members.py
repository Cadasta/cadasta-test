from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver
from selenium.common.exceptions import NoSuchElementException

class ViewMembers(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_view_members(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/organizations/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/"]').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/members/"]').click()
        self.wd.wait_for_css('.table')
        elems = self.wd.find_elements_by_css_selector(".linked")
        assert len(elems) != 0

    def tearDown(self):
        self.wd.quit()


class ViewMemberProfile(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_view_member_profile(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/organizations/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/"]').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/members/"]').click()
        self.wd.wait_for_css('.table')
        self.wd.find_element_by_xpath('//tr/td/a').click()
        self.wd.wait_for_css(".member-info")
        text = self.wd.find_css("h2").text
        assert text.startswith("MEMBER:")

    def tearDown(self):
        self.wd.quit()


class AddMember(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_add_member(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/organizations/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/"]').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/members/"]').click()
        self.wd.wait_for_css('.table')
        self.open("/organizations/organization-1/members/add/")
        self.wd.wait_for_css("#id_identifier")
        self.wd.find_element_by_xpath('//input[@name="identifier"]').send_keys("cadasta-test-user1")
        self.wd.find_element_by_xpath('//button[@type="submit"]').click()
        self.wd.wait_for_css(".member-info")
        text = self.wd.find_css("h2").text
        assert text.startswith("MEMBER:")

    def tearDown(self):
        self.wd.quit()


class AddNonExistingMember(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_add_member(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/organizations/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/"]').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/members/"]').click()
        self.wd.wait_for_css('.table')
        self.open("/organizations/organization-1/members/add/")
        self.wd.wait_for_css("#id_identifier")
        self.wd.find_element_by_xpath('//input[@name="identifier"]').send_keys("cadasta-user-x")
        self.wd.find_element_by_xpath('//button[@type="submit"]').click()
        self.wd.wait_for_css(".has-error")
        elems = self.wd.find_elements_by_xpath("//*[contains(text(), 'User with username or email cadasta-user-x does not exist')]")
        assert len(elems) != 0

    def tearDown(self):
        self.wd.quit()


class RemoveMember(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_remove_member(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/organizations/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/"]').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/members/"]').click()
        self.wd.wait_for_css('.table')
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/members/cadasta-test-user1/"]').click()
        self.wd.wait_for_css(".member-info")
        self.wd.find_element_by_xpath('//button[@name="remove"]').click()
        self.wd.wait_for_css(".modal-title")
        self.open("/organizations/organization-1/members/cadasta-test-user1/remove/")

        try:
            self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/members/cadasta-test-user1/"]')
        except NoSuchElementException:
            assert True

    def tearDown(self):
        self.wd.quit()


class SearchMembers(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_search_member(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/organizations/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/"]').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Organization Overview')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/members/"]').click()
        self.wd.wait_for_css('.table')
        self.wd.find_element_by_xpath('//input[@type="search"]').send_keys("cadasta-test-user")
        elems = self.wd.find_elements_by_css_selector(".linked")
        assert len(elems) != 0

    def test_search_non_existing_member(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/organizations/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Organizations')]")
        self.wd.find_element_by_xpath('//input[@type="search"]').send_keys("user-x")
        text = self.wd.find_css(".dataTables_empty").text
        assert text == "No matching records found"

    def tearDown(self):
        self.wd.quit()

