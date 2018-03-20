import json
import pytest

from selenium.common.exceptions import NoSuchElementException

from ..base_test import HOST_URL, SeleniumTestCase
from ..util import random_string


USER_MENU_XPATH_FORMAT = '//header//*[normalize-space()="{}"]'
PROJECT_ROLES = {
    'OA': 'Administrator',
    'PM': 'Project Manager',
    'DC': 'Data Collector',
    'PU': 'Project User',
}


@pytest.mark.batch2
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

    def test_project_member_can_view_project_statistics(
        self, prj_user, basic_org, records_prj
    ):
        """Verifies Projects test case #B10."""

        self.log_in(prj_user)
        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], records_prj['slug']))
        self.wd.BY_XPATH(
            '//*[contains(@class,"tile-box") and'
            '    .//*[contains(@class,"tile-header") and'
            '         contains(.,"Locations")] and'
            '    .//*[contains(@class,"tile-content") and'
            '         .//*[@class="num" and contains(.,"{}")]]]'.format(
                records_prj['num_locations']))
        self.wd.BY_XPATH(
            '//*[contains(@class,"tile-box") and'
            '    .//*[contains(@class,"tile-header") and'
            '         contains(.,"Parties")] and'
            '    .//*[contains(@class,"tile-content") and'
            '         .//*[@class="num" and contains(.,"{}")]]]'.format(
                records_prj['num_parties']))
        self.wd.BY_XPATH(
            '//*[contains(@class,"tile-box") and'
            '    .//*[contains(@class,"tile-header") and'
            '         contains(.,"Resources")] and'
            '    .//*[contains(@class,"tile-content") and'
            '         .//*[@class="num" and contains(.,"{}")]]]'.format(
                records_prj['num_resources']))

    def test_project_manager_is_shown_items_to_populate_an_empty_project(
        self, prj_manager, basic_org, empty_prj
    ):
        """Verifies Projects test cases #B11, #B12, #B18, #B22 (partial)."""

        self.log_in(prj_manager)
        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], empty_prj['slug']))
        about_panel = self.wd.BY_CLASS('panel-about')

        # Test case #B11
        self.wd.BY_XPATH(
            '//*[contains(.,"Welcome to your newly created project!")]')
        link = self.wd.BY_LINK('Define your project map')
        assert (link.get_attribute('href') == HOST_URL +
                '/organizations/{}/projects/{}/edit/geometry/'.format(
                    basic_org['slug'], empty_prj['slug']))
        link = self.wd.BY_LINK('Upload your questionnaire')
        assert (link.get_attribute('href') == HOST_URL +
                '/organizations/{}/projects/{}/edit/details/'.format(
                    basic_org['slug'], empty_prj['slug']))

        # Test case #B12
        self.wd.BY_XPATH(
            '//*[contains(normalize-space(),"You haven\'t designed your data '
            'collection by uploading an XLS Form. Do you want to do that '
            'now?")]')
        self.wd.BY_XPATH(
            '//a[@href="/organizations/{}/projects/{}/edit/details/" and'
            '    contains(@class,"btn-primary") and'
            '    contains(.,"Upload XLS Form")]'.format(
                basic_org['slug'], empty_prj['slug']))

        # Test case #B18
        about_panel.find_element_by_xpath(
            './/*[contains(.,"This project needs a description. '
            'Would you like to add one now?")]')
        about_panel.find_element_by_xpath(
            './/a[@href="/organizations/{}/projects/{}/edit/details/" and'
            '     contains(@class,"btn-primary") and'
            '     contains(.,"Add project description")]'.format(
                basic_org['slug'], empty_prj['slug']))

        # Test case #B22
        about_panel.find_element_by_xpath(
            './/*[contains(@class,"panel-heading")]'
            '//a[@href="/organizations/{}/projects/{}/edit/details/"]'
            '//*[contains(@class,"glyphicon-cog")]'.format(
                basic_org['slug'], empty_prj['slug']))

    def test_project_manager_is_shown_message_on_not_replacing_questionnaire(
        self, prj_manager, basic_org, custom_attrs_prj
    ):
        """Verifies Projects test case #B14."""

        self.log_in(prj_manager)
        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], custom_attrs_prj['slug']))
        self.wd.BY_XPATH(
            '//*[contains(normalize-space(),"Data has already been '
            'contributed to this project. To ensure data integrity, uploading '
            'a new questionnaire is disabled.")]')
        self.wd.BY_XPATH(
            '//*[contains(@class,"alert-info")]'
            '//*[contains(.,"This project is using questionnaire ") and'
            '    .//a[contains(.,"")]]'.format(
                custom_attrs_prj['questionnaire']['original_file']))

    def test_public_user_can_view_project_statistics(
        self, org_member, basic_org, records_prj
    ):
        """Verifies Projects test case #B15."""

        self.log_in(org_member)
        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], records_prj['slug']))
        self.wd.BY_XPATH(
            '//*[contains(@class,"tile-box") and'
            '    .//*[contains(@class,"tile-header") and'
            '         contains(.,"Locations")] and'
            '    .//*[contains(@class,"tile-content") and'
            '         .//*[@class="num" and contains(.,"{}")]]]'.format(
                records_prj['num_locations']))
        self.wd.BY_XPATH(
            '//*[contains(@class,"tile-box") and'
            '    .//*[contains(@class,"tile-header") and'
            '         contains(.,"Parties")] and'
            '    .//*[contains(@class,"tile-content") and'
            '         .//*[@class="num" and contains(.,"{}")]]]'.format(
                records_prj['num_parties']))
        self.wd.BY_XPATH(
            '//*[contains(@class,"tile-box") and'
            '    .//*[contains(@class,"tile-header") and'
            '         contains(.,"Resources")] and'
            '    .//*[contains(@class,"tile-content") and'
            '         .//*[@class="num" and contains(.,"{}")]]]'.format(
                records_prj['num_resources']))

    def test_empty_project_does_not_show_statistics(
        self, any_user, basic_org, basic_prj
    ):
        """Verifies Projects test case #B16."""

        self.log_in(any_user)
        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], basic_prj['slug']))
        try:
            self.wd.BY_XPATH(
                '//*[contains(@class,"tile-box")]'
                '//*[contains(@class,"tile-header") and'
                '    contains(.,"Locations")]')
            raise AssertionError('Location statistics is shown')
        except NoSuchElementException:
            pass
        try:
            self.wd.BY_XPATH(
                '//*[contains(@class,"tile-box")]'
                '//*[contains(@class,"tile-header") and'
                '         contains(.,"Parties")]]')
            raise AssertionError('Party statistics is shown')
        except NoSuchElementException:
            pass
        try:
            self.wd.BY_XPATH(
                '//*[contains(@class,"tile-box")]'
                '//*[contains(@class,"tile-header") and'
                '    contains(.,"Resources")]]')
            raise AssertionError('Resource statistics is shown')
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

    def test_anonymous_user_cannot_view_project_statistics(
        self, basic_org, records_prj
    ):
        """Verifies Projects test case #B26."""

        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], records_prj['slug']))
        try:
            self.wd.BY_XPATH(
                '//*[contains(@class,"tile-box")]'
                '//*[contains(@class,"tile-header") and'
                '    contains(.,"Locations")]')
            raise AssertionError('Location statistics is shown')
        except NoSuchElementException:
            pass
        try:
            self.wd.BY_XPATH(
                '//*[contains(@class,"tile-box")]'
                '//*[contains(@class,"tile-header") and'
                '         contains(.,"Parties")]]')
            raise AssertionError('Party statistics is shown')
        except NoSuchElementException:
            pass
        try:
            self.wd.BY_XPATH(
                '//*[contains(@class,"tile-box")]'
                '//*[contains(@class,"tile-header") and'
                '    contains(.,"Resources")]]')
            raise AssertionError('Resource statistics is shown')
        except NoSuchElementException:
            pass

    def test_project_details_are_shown_on_dashboard(
        self, any_user, basic_org, basic_prj
    ):
        """Verifies Projects test cases #B17, #B20, #B21."""

        self.log_in(any_user)
        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], basic_prj['slug']))
        panel = self.wd.BY_CLASS('panel-about')
        panel.find_element_by_xpath(
            './/p[contains(.,"{}")]'.format(basic_prj['description']))
        prj_url = json.loads(basic_prj['urls'])[0]
        panel.find_element_by_xpath(
            './/a[@href="{}" and'
            '     .//*[contains(@class,"glyphicon-globe")] and'
            '     contains(.,"{}")]'.format(prj_url, prj_url))
        dl_children = [
            el for el in panel.find_elements_by_xpath(
                './/dl[@class="contacts"]/*')
            if el.tag_name in ('dt', 'dd')]
        for contact in basic_prj['contacts']:
            dt = dl_children.pop(0)
            assert dt.tag_name == 'dt'
            assert contact['name'] in dt.text
            dd = dl_children.pop(0)
            assert dd.tag_name == 'dd'
            try:
                dd.find_element_by_xpath(
                    './/a[@href="mailto:{}" and'
                    '     .//*[contains(@class,"glyphicon-envelope")] and'
                    '     contains(.,"{}")]'.format(
                        contact['email'], contact['email']))
            except NoSuchElementException:
                assert not contact['email']
            try:
                dd.find_element_by_xpath(
                    './/a[@href="tel:{}" and'
                    '     .//*[contains(@class,"glyphicon-earphone")] and'
                    '     contains(.,"{}")]'.format(
                        contact['tel'], contact['tel']))
            except NoSuchElementException:
                assert not contact['tel']
        assert len(dl_children) == 0

    def test_public_user_is_shown_message_about_empty_project_on_dashboard(
        self, org_member, basic_org, empty_prj
    ):
        """Verifies Projects test case #B19 (partial)."""

        self.log_in(org_member)
        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], empty_prj['slug']))
        self.wd.BY_XPATH(
            '//*[contains(@class,"panel-about")]'
            '//*[contains(.,"Looks like this project doesn\'t have a '
            'description yet.")]')

    def test_anonymous_user_is_shown_message_about_empty_project_on_dashboard(
        self, org_member, basic_org, empty_prj
    ):
        """Verifies Projects test case #B19 (partial)."""

        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], empty_prj['slug']))
        self.wd.BY_XPATH(
            '//*[contains(@class,"panel-about")]'
            '//*[contains(.,"Looks like this project doesn\'t have a '
            'description yet.")]')

    def test_project_manager_is_shown_gear_icon_on_dashboard(
        self, prj_manager, basic_org, basic_prj
    ):
        """Verifies Projects test case #B22 (partial)."""

        self.log_in(prj_manager)
        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], basic_prj['slug']))
        about_panel = self.wd.BY_CLASS('panel-about')
        about_panel.find_element_by_xpath(
            './/*[contains(@class,"panel-heading")]'
            '//a[@href="/organizations/{}/projects/{}/edit/details/"]'
            '//*[contains(@class,"glyphicon-cog")]'.format(
                basic_org['slug'], basic_prj['slug']))

    def test_non_pm_is_not_shown_gear_icon_on_dashboard(
        self, any_non_pm_user, basic_org, basic_prj
    ):
        """Verifies Projects test case #B23 (partial)."""

        self.log_in(any_non_pm_user)
        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], basic_prj['slug']))
        about_panel = self.wd.BY_CLASS('panel-about')
        try:
            about_panel.find_element_by_xpath(
                './/*[contains(@class,"panel-heading")]'
                '//a[@href="/organizations/{}/projects/{}/edit/details/"]'
                '//*[contains(@class,"glyphicon-cog")]'.format(
                    basic_org['slug'], basic_prj['slug']))
            raise AssertionError('Gear icon is shown')
        except NoSuchElementException:
            pass

    def test_anonymous_user_is_not_shown_gear_icon_on_dashboard(
        self, basic_org, basic_prj
    ):
        """Verifies Projects test case #B23 (partial)."""

        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], basic_prj['slug']))
        about_panel = self.wd.BY_CLASS('panel-about')
        try:
            about_panel.find_element_by_xpath(
                './/*[contains(@class,"panel-heading")]'
                '//a[@href="/organizations/{}/projects/{}/edit/details/"]'
                '//*[contains(@class,"glyphicon-cog")]'.format(
                    basic_org['slug'], basic_prj['slug']))
            raise AssertionError('Gear icon is shown')
        except NoSuchElementException:
            pass

    def test_project_members_are_listed_on_dashboard_for_project_members(
        self, prj_user, basic_org, basic_prj
    ):
        """Verifies Projects test case #B24."""

        self.log_in(prj_user)
        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], basic_prj['slug']))

        # Convert member list into dict
        members = {}
        for (user, role) in basic_prj['members']:
            user['role'] = role
            members[user['username']] = user

        list_items = self.wd.BYS_XPATH(
            '//*[contains(@class,"panel") and'
            '    .//*[contains(@class,"panel-title") and'
            '         contains(.,"Team Members")]]//li')
        for item in list_items:
            username = item.find_element_by_xpath('.//strong').text
            assert username in members
            assert PROJECT_ROLES[members[username]['role']] in item.text
            del members[username]
        assert len(members) == 0

    def test_project_members_are_not_listed_on_dashboard_for_public_users(
        self, org_member, basic_org, basic_prj
    ):
        """Verifies Projects test case #B25 (partial)."""

        self.log_in(org_member)
        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], basic_prj['slug']))
        try:
            self.wd.BY_XPATH(
                '//*[contains(@class,"panel") and'
                '    .//*[contains(@class,"panel-title") and'
                '         contains(.,"Team Members")]]')
            raise AssertionError('Project members are shown')
        except NoSuchElementException:
            pass

    def test_project_members_are_not_listed_on_dashboard_for_anonymous_users(
        self, org_member, basic_org, basic_prj
    ):
        """Verifies Projects test case #B25 (partial)."""

        self.open('/organizations/{}/projects/{}/'.format(
            basic_org['slug'], basic_prj['slug']))
        try:
            self.wd.BY_XPATH(
                '//*[contains(@class,"panel") and'
                '    .//*[contains(@class,"panel-title") and'
                '         contains(.,"Team Members")]]')
            raise AssertionError('Project members are shown')
        except NoSuchElementException:
            pass
