import pytest
import re

from os.path import abspath, dirname, join
from selenium.webdriver.common.by import By

from ..base_test import SeleniumTestCase


USER_MENU_XPATH_FORMAT = '//header//*[normalize-space()="{}"]'


@pytest.mark.batch2
class TestXLSForm(SeleniumTestCase):

    @pytest.fixture(autouse=True)
    def get_basic_data(self, basic_org, basic_prj):
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

    def wait_and_click_save_button(self):
        """Waits until the save button is enabled then clicks it."""
        button_xpath = '//*[@type="submit" and ./text()="Save"]'
        self.wd.wait_until_clickable((By.XPATH, button_xpath))
        button = self.wd.BY_XPATH(button_xpath)
        self.scroll_element_into_view(button)
        button.click()

    # ------ Test cases ------

    @pytest.mark.uploads
    def test_xlsform_with_invalid_field_is_not_allowed(self, prj_manager):
        """Verifies Forms test cases #X1,#X2,#X3,#X4,#X5,#X6,#X7,#X9,#X10."""

        self.log_in(prj_manager)
        self.open(self.prj_dashboard_path)
        self.wd.BY_LINK("Upload XLS Form").click()

        def verify_invalid_xlsform(filename, msg_pattern):
            dir_path = join(dirname(dirname(abspath(__file__))), 'files')
            input_xpath = '//input[@type="file"]'
            remove_xpath = '//a[contains(@class, "file-remove")]'
            error_xpath = '//*[contains(@class, "file-well")]//li'

            remove = self.wd.BY_XPATH(remove_xpath)
            if (remove.is_displayed()):
                remove.click()

            self.wd.BY_XPATH(input_xpath).send_keys(join(dir_path, filename))
            self.wait_and_click_save_button()
            self.assert_url_path(self.prj_dashboard_path + 'edit/details/')
            msg = self.wd.BY_XPATH(error_xpath).text
            assert re.search(msg_pattern, msg)

        # Test case #X1
        verify_invalid_xlsform(
            'XLSForm X1 missing question name.xlsx',
            '^\[row : \d+\] Question or group with no name\.$')

        # Test case #X2
        verify_invalid_xlsform(
            'XLSForm X2 missing label.xlsx',
            "^The survey element named '[^']+' "
            "has no label or hint\.$")

        # Test case #X3
        verify_invalid_xlsform(
            'XLSForm X3 select_one missing choice type.xlsx',
            "^Unknown question type 'select_one'\.$")

        # Test case #X4
        verify_invalid_xlsform(
            'XLSForm X4 select_one invalid choice type.xlsx',
            "^\[row : \d+\] List name not in choices sheet: .+$")

        # Test case #X5
        verify_invalid_xlsform(
            'XLSForm X5 missspelled type.xlsx',
            "^Unknown question type '[^']+'\.$")

        # Test case #X6
        verify_invalid_xlsform(
            'XLSForm X6 duplicate field names.xlsx',
            "^There are two survey elements named '[^']+' "
            "in the section named '[^']+'\.$")

        # Test case #X7
        verify_invalid_xlsform(
            'XLSForm X7 name with diacritic.xlsx',
            "^\[row : \d+\] Invalid question name \[.+\]Names must begin with "
            "a letter, colon, or underscore.Subsequent characters can include "
            "numbers, dashes, and periods\.$")

        # Test case #X9
        verify_invalid_xlsform(
            'XLSForm X9 missing begin group.xlsx',
            "^\[row : \d+\] Unmatched end statement\. Previous control type: "
            "None, Control type: group$")

        # Test case #X10
        verify_invalid_xlsform(
            'XLSForm X10 missing end group.xlsx',
            "^Unmatched begin statement: group$")

    @pytest.mark.uploads
    def test_xlsform_with_resource_in_group_is_allowed(self, prj_manager):
        """Verifies Forms test case #X8."""

        self.log_in(prj_manager)
        self.open(self.prj_dashboard_path)
        self.wd.BY_LINK("Upload XLS Form").click()
        dir_path = join(dirname(dirname(abspath(__file__))), 'files')
        input_xpath = '//input[@type="file"]'
        path = join(
            dir_path, 'XLSForm X8 image, audio, video type in group.xlsx')
        self.wd.BY_XPATH(input_xpath).send_keys(path)
        self.wait_and_click_save_button()
        self.assert_url_path(self.prj_dashboard_path)
        self.wd.BY_LINK("Upload new XLS Form")
        self.wd.BY_LINK("Download current XLS Form")

        # [REVERSION]
        self.wd.BY_LINK("Upload new XLS Form").click()
        link = self.wd.BY_XPATH('//a[contains(@class, "file-remove")]')
        self.scroll_element_into_view(link)
        link.click()
        self.wait_and_click_save_button()
        self.assert_url_path(self.prj_dashboard_path)
        self.wd.BY_LINK("Upload XLS Form")
