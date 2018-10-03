import json
import pytest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from ..base_test import SeleniumTestCase


USER_MENU_XPATH_FORMAT = '//header//*[normalize-space()="{}"]'


@pytest.mark.batch2
class TestUpdating(SeleniumTestCase):

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

    def select_org_menu_item(self, label):
        """Opens the org gear menu and clicks the specified item."""
        self.wd.BY_XPATH(
            '//*[contains(@class,"page-header")]'
            '//button[.//*[contains(@class,"glyphicon-cog")]]').click()
        self.wd.BY_LINK(label).click()

    # ------ Test cases ------

    def test_org_admin_can_update_org(self, org_admin):
        """Verifies Organizations test case #U1."""

        self.log_in(org_admin)
        self.open('/organizations/{}/'.format(self.org['slug']))
        self.select_org_menu_item('Edit organization')
        self.update_form_field('name', 'FuncTest Temp Name')
        self.wd.BY_XPATH(
            '//*[@type="submit" and normalize-space()="Save"]').click()
        expected_path = '/organizations/{}/'.format(self.org['slug'])
        assert self.get_url_path() == expected_path
        self.wd.BY_XPATH('//h1[normalize-space()="FuncTest Temp Name"]')
        about = self.wd.BY_CLASS('panel-about')
        about.find_element_by_xpath(
            './/*[.="{}"]'.format(self.org['description']))
        about.find_element_by_xpath(
            './/*[@href="{}"]'.format(json.loads(self.org['urls'])[0]))
        contact = self.org['contacts'][0]
        about.find_element_by_xpath('.//*[.="{}"]'.format(contact['name']))
        about.find_element_by_xpath(
            './/*[@href="mailto:{}"]'.format(contact['email']))
        about.find_element_by_xpath(
            './/*[@href="tel:{}"]'.format(contact['tel']))

        # [REVERSION]
        self.select_org_menu_item('Edit organization')
        self.update_form_field('name', self.org['name'])
        self.wd.BY_XPATH(
            '//*[@type="submit" and normalize-space()="Save"]').click()

    def test_non_org_admin_cannot_update_org(self, org_member):
        """Verifies Organizations test case #U2."""

        self.log_in(org_member)
        self.open('/organizations/{}/'.format(self.org['slug']))
        try:
            self.wd.BY_XPATH('//a[normalize-space()="Add project"]')
            raise AssertionError('Add project link is present')
        except NoSuchElementException:
            pass
        try:
            self.select_org_menu_item('Edit organization')
            raise AssertionError('Org gear menu is present')
        except NoSuchElementException:
            pass
        self.open(self.get_url_path() + 'edit')
        self.wait_for_alert(
            "You don't have permission to update this organization")

    def test_anonymous_user_cannot_update_org(self):
        """Verifies Organizations test case #U5."""

        self.open('/organizations/{}/'.format(self.org['slug']))
        try:
            self.wd.BY_XPATH('//a[normalize-space()="Add project"]')
            raise AssertionError('Add project link is present')
        except NoSuchElementException:
            pass
        try:
            self.select_org_menu_item('Edit organization')
            raise AssertionError('Org gear menu is present')
        except NoSuchElementException:
            pass
        self.open(self.get_url_path() + 'edit')
        assert self.get_url_path() == '/account/login/'
        assert self.get_url_query() == (
            'next=/organizations/{}/edit/'.format(self.org['slug']))

    def test_org_admin_can_archive_and_unarchive_org(
        self, org_admin, archivable_org
    ):
        """Verifies Organizations test case #U3, #U4."""

        self.log_in(org_admin)
        name = archivable_org['name']

        # Test case #U3
        self.open('/organizations/{}/'.format(archivable_org['slug']))
        self.wd.BY_XPATH('//h1[contains(.,"{}")]'.format(name))
        self.select_org_menu_item('Archive organization')
        selector = (By.LINK_TEXT, 'Yes, archive this organization')
        self.wd.wait_until_clickable(selector).click()
        archived_xpath = 'normalize-space()="{} Archived"'.format(name)
        self.wd.BY_XPATH('//h1[{}]'.format(archived_xpath))
        self.wd.BY_LINK('Organizations').click()
        select = Select(self.wd.BY_ID('archive-filter'))
        select.select_by_value('archived-True')
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(name)
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]//*[{}]'.format(archived_xpath))

        # [REVERSION] and test case #U4
        self.open('/organizations/{}/'.format(archivable_org['slug']))
        self.select_org_menu_item('Unarchive organization')
        selector = (By.LINK_TEXT, 'Yes, unarchive this organization')
        self.wd.wait_until_clickable(selector).click()
        nonarchived_xpath = 'normalize-space()="{}"'.format(name)
        self.wd.BY_XPATH('//h1[{}]'.format(nonarchived_xpath))
        self.wd.BY_LINK('Organizations').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(name)
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]//*[{}]'.format(nonarchived_xpath))
