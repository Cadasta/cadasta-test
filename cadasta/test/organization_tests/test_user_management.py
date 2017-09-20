import pytest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from ..base_test import SeleniumTestCase
from ..util import random_string


USER_MENU_XPATH_FORMAT = '//header//*[normalize-space()="{}"]'


class TestUserManagement(SeleniumTestCase):

    @pytest.fixture(autouse=True)
    def get_basic_org(self, basic_org):
        self.org = basic_org

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

    def test_org_member_can_view_the_org_members(
        self, any_org_member, all_org_members
    ):
        """Verifies Organizations test case #M1."""

        self.log_in(any_org_member)
        self.open('/organizations/{}/'.format(self.org['slug']))
        panel = self.wd.BY_XPATH(
            '//*[contains(@class,"panel-default") and '
            '    .//*[contains(@class,"panel-title") and '
            '         normalize-space()="Members"]]')
        for member in all_org_members:
            panel.find_element_by_xpath(
                '//*[.="{}"]'.format(member['username']))
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Members"]').click()
        for member in all_org_members:
            self.wd.BY_XPATH(
                '//*[@id="DataTables_Table_0"]'
                '//td[normalize-space()="{}"]'.format(member['username']))

    def test_search_for_an_existing_member_works(self, org_member):
        """Verifies Organizations test case #M2."""

        self.log_in(org_member)
        self.open('/organizations/{}/'.format(self.org['slug']))
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Members"]').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(org_member['username'])
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//td[normalize-space()="{}"]'.format(org_member['username']))

    def test_search_that_results_in_no_member_works(self, org_member):
        """Verifies Organizations test case #M3."""

        self.log_in(org_member)
        self.open('/organizations/{}/'.format(self.org['slug']))
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Members"]').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(random_string())
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="No matching records found"]')

    def test_non_org_member_cannot_view_the_org_members(self, generic_user):
        """Verifies Organizations test case #M4."""

        self.log_in(generic_user)
        self.open('/organizations/{}/'.format(self.org['slug']))
        try:
            self.wd.BY_XPATH(
                '//*[@id="sidebar"]//a[normalize-space()="Members"]')
            raise AssertionError('Sidebar is present')
        except NoSuchElementException:
            pass
        try:
            self.wd.BY_XPATH(
                '//*[contains(@class,"panel-default") and '
                '    .//*[contains(@class,"panel-title") and '
                '         normalize-space()="Members"]]')
            raise AssertionError('Members panel is present')
        except NoSuchElementException:
            pass
        self.open(self.get_url_path() + 'members')
        self.wait_for_alert(
            "You don't have permission to view members of this organization")

    def test_anonymous_user_cannot_view_the_org_members(self):
        """Verifies Organizations test case #M5."""

        self.open('/organizations/{}/'.format(self.org['slug']))
        try:
            self.wd.BY_XPATH(
                '//*[@id="sidebar"]//a[normalize-space()="Members"]')
            raise AssertionError('Sidebar is present')
        except NoSuchElementException:
            pass
        try:
            self.wd.BY_XPATH(
                '//*[contains(@class,"panel-default") and '
                '    .//*[contains(@class,"panel-title") and '
                '         normalize-space()="Members"]]')
            raise AssertionError('Members panel is present')
        except NoSuchElementException:
            pass
        self.open(self.get_url_path() + 'members')
        assert self.get_url_path() == '/account/login/'
        assert self.get_url_query() == (
            'next=/organizations/{}/members/'.format(self.org['slug']))

    def test_org_admin_can_view_the_membership_page_of_an_org_member(
        self, org_admin, all_org_members
    ):
        """Verifies Organizations test case #M6."""

        self.log_in(org_admin)
        for member in all_org_members:
            self.open('/organizations/{}/members/'.format(self.org['slug']))
            label = member['full_name'] or member['username']
            self.wd.BY_LINK(label).click()
            content = self.wd.BY_CLASS('content-single')

            def content_contains_text(text):
                content.find_element_by_xpath(
                    '//*[text()[contains(.,"{}")]]'.format(text))

            content_contains_text(member['username'])
            if member['full_name']:
                content_contains_text(member['full_name'])
            content_contains_text(member['email'])

            if member['username'] == org_admin['username']:
                content.find_element_by_xpath(
                    '//*[contains(@class,"member-role")]'
                    '//*[text()[contains(.,"Administrator")]]')
            else:
                role_value = 'A' if member['admin'] else 'M'
                select = Select(self.wd.BY_ID('id_org_role'))
                option = select.first_selected_option
                assert option.get_attribute('value') == role_value

    def test_non_org_admin_cannot_view_the_membership_page_of_an_org_member(
        self, org_member, all_org_members
    ):
        """Verifies Organizations test case #M7."""

        self.log_in(org_member)
        for member in all_org_members:
            self.open('/organizations/{}/'.format(self.org['slug']))
            self.wd.BY_LINK(member['username']).click()
            self.wait_for_alert(
                "You don't have permission to edit roles of this organization")

            self.open('/organizations/{}/members/'.format(self.org['slug']))
            label = member['full_name'] or member['username']
            self.wd.BY_LINK(label).click()
            self.wait_for_alert(
                "You don't have permission to edit roles of this organization")

    def test_org_admin_can_add_and_remove_a_member(
        self, org_admin, generic_user
    ):
        """Verifies Organizations test case #M8, #M11."""

        self.log_in(org_admin)

        # Test case #M8
        self.open('/organizations/{}/members/'.format(self.org['slug']))
        self.wd.BY_XPATH(
            '//*[contains(@class,"main-text")]'
            '//*[contains(@class,"btn-primary") and '
            'normalize-space()="Add"]').click()
        self.update_form_field('identifier', generic_user['username'])
        self.wd.BY_XPATH(
            '//*[@type="submit" and normalize-space()="Save"]').click()
        assert self.get_url_path() == (
            '/organizations/{}/members/{}/'.format(
                self.org['slug'], generic_user['username']))
        select = Select(self.wd.BY_ID('id_org_role'))
        assert select.first_selected_option.get_attribute('value') == 'M'

        # [REVERSION] and test case #M11
        self.open('/organizations/{}/members/'.format(self.org['slug']))
        label = generic_user['full_name'] or generic_user['username']
        self.wd.BY_LINK(label).click()
        self.wd.BY_NAME('remove').click()
        selector = (By.LINK_TEXT, 'Yes, remove this member')
        self.wd.wait_until_clickable(selector).click()
        assert self.get_url_path() == (
            '/organizations/{}/members/'.format(self.org['slug']))
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(generic_user['username'])
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="No matching records found"]')

    def test_org_admin_cannot_add_a_nonexisting_member(self, org_admin):
        """Verifies Organizations test case #M9."""

        self.log_in(org_admin)
        self.open('/organizations/{}/members/'.format(self.org['slug']))
        self.wd.BY_XPATH(
            '//*[contains(@class,"main-text")]'
            '//*[contains(@class,"btn-primary") and '
            'normalize-space()="Add"]').click()
        nonsense = random_string()
        self.update_form_field('identifier', nonsense)
        self.wd.BY_XPATH(
            '//*[@type="submit" and normalize-space()="Save"]').click()
        self.assert_form_field_has_error(
            'identifier',
            'User with username or email {} does not exist'.format(nonsense))

    def test_non_org_admin_cannot_add_a_member(self, org_member):
        """Verifies Organizations test case #M10."""

        self.log_in(org_member)
        self.open('/organizations/{}/members/'.format(self.org['slug']))
        # TODO: Add member button is still present (see #1749)
        # try:
        #     self.wd.BY_XPATH(
        #         '//*[contains(@class,"main-text")]'
        #         '//*[contains(@class,"btn-primary") and '
        #         'normalize-space()="Add"]').click()
        #     raise AssertionError('Add member button is present')
        # except NoSuchElementException:
        #     pass
        self.open(self.get_url_path() + 'add')
        self.wait_for_alert(
            "You don't have permission to add members to this organization")

    def test_org_admin_cannot_remove_themself(self, org_admin):
        """Verifies Organizations test case #M12."""

        self.log_in(org_admin)
        self.open('/organizations/{}/members/{}/'.format(
            self.org['slug'], org_admin['username']))
        assert not self.wd.BY_NAME('remove').is_enabled()
        self.open(self.get_url_path() + 'remove')
        self.wait_for_alert('Administrators cannot remove themselves.')
