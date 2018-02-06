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
    def get_basic_org(self, basic_org, basic_prj):
        self.org = basic_org
        self.prj = basic_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], basic_prj['slug'])

    # ------ Utility functions ------

    def log_in(self, user):
        """Logs in the specified user."""
        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', user['username'])
        self.update_form_field('password', user['password'])
        self.wd.BY_NAME('sign-in').click()
        label = user['full_name'] or user['username']
        self.wd.wait_for_xpath(USER_MENU_XPATH_FORMAT.format(label))

    def get_gear_menu_button(self):
        return self.wd.BY_XPATH(
            '//*[contains(@class,"page-header")]'
            '//button[.//*[contains(@class,"glyphicon-cog")]]')

    def select_prj_menu_item(self, label):
        """Opens the project gear menu and clicks the specified item."""
        self.get_gear_menu_button().click()
        self.wd.BY_LINK(label).click()

    def click_save_button(self):
        button = self.wd.BY_XPATH('//*[@type="submit" and ./text()="Save"]')
        self.scroll_element_into_view(button)
        button.click()

    # ------ Test cases ------

    def test_pm_can_update_project(self, prj_manager):
        """Verifies Projects test case #U1."""

        self.log_in(prj_manager)
        self.open(self.prj_dashboard_path)
        self.select_prj_menu_item('Edit project details')
        self.update_form_field('name', 'FuncTest Temp Name')
        self.click_save_button()
        assert self.get_url_path() == self.prj_dashboard_path
        self.wd.BY_XPATH(
            '//h1[normalize-space()="{} FuncTest Temp Name"]'.format(
                self.org['name']))
        about = self.wd.BY_CLASS('panel-about')
        about.find_element_by_xpath(
            '//*[.="{}"]'.format(self.prj['description']))
        about.find_element_by_xpath(
            '//*[@href="{}"]'.format(json.loads(self.prj['urls'])[0]))
        contact = self.prj['contacts'][0]
        about.find_element_by_xpath('//*[.="{}"]'.format(contact['name']))
        about.find_element_by_xpath(
            '//*[@href="mailto:{}"]'.format(contact['email']))
        about.find_element_by_xpath(
            '//*[@href="tel:{}"]'.format(contact['tel']))

        # [REVERSION]
        self.select_prj_menu_item('Edit project details')
        self.update_form_field('name', self.prj['name'])
        self.click_save_button()

    def test_non_pm_cannot_update_project(self, org_member):
        """Verifies Projects test case #U2."""

        self.log_in(org_member)
        self.open(self.prj_dashboard_path)
        try:
            self.get_gear_menu_button()
            raise AssertionError('Gear menu is present')
        except NoSuchElementException:
            pass
        self.open(self.get_url_path() + 'edit/details')
        self.wait_for_alert(
            "You don't have permission to update this project")

    def test_anonymous_user_cannot_update_project(self):
        """Verifies Projects test case #U9."""

        self.open(self.prj_dashboard_path)
        try:
            self.get_gear_menu_button()
            raise AssertionError('Gear menu is present')
        except NoSuchElementException:
            pass
        self.open(self.get_url_path() + 'edit/details')
        assert self.get_url_path() == '/account/login/'
        assert self.get_url_query() == (
            'next=' + self.prj_dashboard_path + 'edit/details/')

    def test_public_project_can_be_made_private_vice_versa(self, prj_manager):
        """Verifies Projects test case #U3, #U4."""

        name = self.prj['name']
        self.log_in(prj_manager)
        self.open(self.prj_dashboard_path)

        # Test case #U3
        self.select_prj_menu_item('Edit project details')
        self.wd.BY_CLASS('toggle').click()
        self.click_save_button()
        self.wd.BY_XPATH(
            '//h1[contains(normalize-space(),"{} Private")]'.format(name))

        # [REVERSION] and test case #U4
        self.select_prj_menu_item('Edit project details')
        self.wd.BY_CLASS('toggle').click()
        self.click_save_button()
        self.wd.BY_XPATH(
            '//h1[contains(normalize-space(),"{}")]'.format(name))
        try:
            self.wd.BY_XPATH(
                '//h1[contains(normalize-space(),"{} Private")]'.format(name))
            raise AssertionError('Private tag is present')
        except NoSuchElementException:
            pass

    def test_project_extent_can_be_modified(self, prj_manager):
        """Verifies Projects test case #U5."""
        # TODO
        pass

    def test_project_extent_can_be_replaced(self, prj_manager):
        """Verifies Projects test case #U6."""
        # TODO
        pass

    def test_org_admin_can_archive_and_unarchive_project(self, org_admin):
        """Verifies Projects test case #U7, #U8."""

        self.log_in(org_admin)

        # Test case #U7
        self.open(self.prj_dashboard_path)
        self.select_prj_menu_item('Archive project')
        selector = (By.LINK_TEXT, 'Yes, archive this project')
        self.wd.wait_until_clickable(selector).click()
        self.wd.BY_XPATH('//h1[normalize-space()="{} {} Archived"]'.format(
            self.org['name'], self.prj['name']))
        self.wd.BY_LINK('Projects').click()
        select = Select(self.wd.BY_ID('archive-filter'))
        select.select_by_value('archived-True')
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(self.prj['name'])
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="{} Archived"]'.format(self.prj['name']))

        # [REVERSION] and test case #U8
        self.open(self.prj_dashboard_path)
        self.select_prj_menu_item('Unarchive project')
        selector = (By.LINK_TEXT, 'Yes, unarchive this project')
        self.wd.wait_until_clickable(selector).click()
        self.wd.BY_XPATH('//h1[normalize-space()="{} {}"]'.format(
            self.org['name'], self.prj['name']))
        self.wd.BY_LINK('Projects').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(self.prj['name'])
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="{}"]'.format(self.prj['name']))
