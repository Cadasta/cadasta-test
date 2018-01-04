import pytest

from selenium.common.exceptions import NoSuchElementException

from ..base_test import SeleniumTestCase
from ..util import random_string


USER_MENU_XPATH_FORMAT = '//header//*[normalize-space()="{}"]'


@pytest.mark.batch1
class TestBrowsing(SeleniumTestCase):

    # ------ Utility functions ------

    def log_in(self, user):
        """Logs in the specified user."""
        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', user['username'])
        self.update_form_field('password', user['password'])
        self.wd.BY_NAME('sign-in').click()
        label = user['full_name'] or user['username']
        self.wd.wait_for_xpath(USER_MENU_XPATH_FORMAT.format(label))

    # ------ Test cases ------

    def test_search_for_an_existing_prj_works(self, basic_prj):
        """Verifies Projects test case #B1."""

        self.wd.BY_LINK('Projects').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(basic_prj['name'])
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="{}"]'.format(basic_prj['name']))

    def test_search_that_results_in_no_prj_works(self):
        """Verifies Projects test case #B2."""

        self.wd.BY_LINK('Projects').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(random_string())
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="No matching records found"]')

    def test_org_member_can_see_all_org_projects_on_projects_lists(
        self, org_member, basic_org, basic_prj, private_prj
    ):
        """Verifies Projects test case #B3."""

        self.log_in(org_member)
        self.wd.BY_LINK('Projects').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(basic_org['name'])
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="{}"]'.format(basic_prj['name']))
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="{} Private"]'.format(private_prj['name']))
        self.open('/organizations/{}/'.format(basic_org['slug']))
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="{}"]'.format(basic_prj['name']))
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="{} Private"]'.format(private_prj['name']))

    def test_non_org_member_can_only_see_public_projects_on_projects_lists(
        self, generic_user, basic_org, basic_prj, private_prj
    ):
        """Verifies Projects test case #B4."""

        self.log_in(generic_user)
        self.wd.BY_LINK('Projects').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(basic_org['name'])
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="{}"]'.format(basic_prj['name']))
        try:
            self.wd.BY_XPATH(
                '//*[@id="DataTables_Table_0"]'
                '//*[normalize-space()="{}"]'.format(private_prj['name']))
            raise AssertionError('Private project is visible')
        except NoSuchElementException:
            pass
        self.open('/organizations/{}/'.format(basic_org['slug']))
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="{}"]'.format(basic_prj['name']))
        try:
            self.wd.BY_XPATH(
                '//*[@id="DataTables_Table_0"]'
                '//*[normalize-space()="{}"]'.format(private_prj['name']))
            raise AssertionError('Private project is visible')
        except NoSuchElementException:
            pass

    def test_anonymous_user_cannot_view_project_data(
        self, basic_org, basic_prj
    ):
        """Verifies Projects test case #B7."""

        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], basic_prj['slug']))
        try:
            self.wd.BY_ID('sidebar')
            raise AssertionError('Project sidebar is present')
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH(
            '//*[contains(@class,"btn-primary") and '
            './/text()[contains(.,"Register now")]]')
        self.wd.BY_XPATH(
            '//*[contains(@class,"btn-primary") and '
            './/text()[contains(.,"Sign in")]]')
        next_url = self.get_url_path() + 'records/locations'
        self.open(next_url)
        assert self.get_url_path() == '/account/login/'
        assert self.get_url_query() == ('next=' + next_url + '/')
        self.wd.BY_XPATH(
            '//h1[contains(normalize-space(), "Hello.Have we met?")]')
