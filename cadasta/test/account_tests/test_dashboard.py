import pytest

from selenium.common.exceptions import NoSuchElementException

from ..base_test import SeleniumTestCase


SHORT_MONTH_NAMES = (None, 'Jan.', 'Feb.', 'March', 'April', 'May', 'June',
                     'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.')
PROJECT_ROLES = {
    'OA': 'Administrator',
    'PM': 'Project Manager',
    'DC': 'Data Collector',
    'PU': 'Project User',
    'PB': 'Public User',
}


@pytest.mark.batch1
class TestDashboard(SeleniumTestCase):

    # ------ Test cases ------

    def test_user_dashboard(self, any_user):
        """Verifies User Accounts test cases #D1, #D4, #D5, #D6, #D7, #D8,
        #D9, #D10, #D11, #D12, #D13, #D14, #D15, #D16, #D17, #D18, #D19,
        #D20, #D21."""

        self.log_in(any_user)

        # Test cases #D1, #D4
        panel = self.wd.BY_CLASS('panel-about')
        title = any_user['full_name'] or any_user['username']
        panel.find_element_by_xpath(
            './/*[contains(@class,"panel-heading")]'
            '//*[contains(.,"{}")]'.format(title))
        panel.find_element_by_xpath(
            './/*[contains(@class,"panel-heading")]'
            '//a[@href="/account/profile/"]'
            '//*[contains(@class,"glyphicon-cog")]')
        panel.find_element_by_xpath(
            './/*[contains(@class,"panel-body")]'
            '//tr['
            '     .//td[contains(normalize-space(),"Username")] and'
            '     .//td[contains(normalize-space(),"{}")]'
            ']'.format(any_user['username']))
        panel.find_element_by_xpath(
            './/*[contains(@class,"panel-body")]'
            '//tr['
            '     .//td[contains(normalize-space(),"{}")] and'
            '     .//td[contains(normalize-space(),"{}")]'
            ']'.format(
                'Email' if any_user['email'] else 'Phone',
                any_user['email'] or any_user['phone']))
        panel.find_element_by_xpath(
            './/*[contains(@class,"panel-body")]'
            '//tr['
            '     .//td[contains(normalize-space(),"Language")] and'
            '     .//td[contains(normalize-space(),"English")]'
            ']')
        panel.find_element_by_xpath(
            './/*[contains(@class,"panel-body")]'
            '//tr['
            '     .//td[contains(normalize-space(),"Measurement")] and'
            '     .//td[contains(normalize-space(),"{}")]'
            ']'.format(any_user['measurement'].capitalize()))
        joined_on = any_user['created_date']
        panel.find_element_by_xpath(
            './/*[contains(@class,"panel-body")]'
            '//tr['
            '     .//td[contains(normalize-space(),"Joined on")] and'
            '     .//td[contains(normalize-space(),"{}")]'
            ']'.format(joined_on.strftime(
                '{} %-d, %Y'.format(SHORT_MONTH_NAMES[joined_on.month]))))
        # TODO: Add non-English (ex., Spanish) user

        if not any_user['orgs']:
            # Test case #D21
            self.wd.BY_XPATH(
                '//*[contains(.,"Your account is all set. '
                'Now add your first organization.")]')
            self.wd.BY_XPATH(
                '//a[@role="button" and @href="/organizations/new/" and'
                '     contains(.,"Add organization")]')
            return

        for (org, is_admin, prj_data) in any_user['orgs']:
            try:
                # Test case #D5
                panel = self.wd.BY_XPATH(
                    '//*[contains(@class,"panel") and'
                    '    .//*[@class="panel-title" and'
                    '         contains(.,"{}")]]'.format(org['name']))
                assert not org['archived']
            except NoSuchElementException:
                # Test cases #D6, #D7
                assert org['archived']
                continue

            try:
                # Test cases #D8
                panel.find_element_by_xpath(
                    './/*[@class="panel-title" and'
                    '     contains(.,"Administrator")]')
                assert is_admin
            except NoSuchElementException:
                # Test cases #D9
                assert not is_admin

            # Test case #D10
            if org['description']:
                panel.find_element_by_xpath(
                    './/p[contains(.,"{}")]'.format(org['description']))

            # Test case #D11
            panel.find_element_by_xpath(
                './/*[@class="panel-title" and'
                '     .//a[@href="/organizations/{}/" and'
                '          contains(.,"{}")]]'.format(
                    org['slug'], org['name']))

            if not prj_data:
                if is_admin:
                    # Test case #D12
                    panel.find_element_by_xpath(
                        './/*[contains(.,"This organization is all set. '
                        'Now add your first project.")]')
                    panel.find_element_by_xpath(
                        './/a[@role="button" and '
                        '     @href="/organizations/{}/projects/new/" and '
                        '     contains(.,"Add a project")]'.format(
                            org['slug']))
                else:
                    # Test case #D13
                    panel.find_element_by_xpath(
                        './/p[contains(.,"Looks like this organization has no '
                        'projects. As projects are created, they\'ll appear '
                        'here.")]')
                continue

            for (prj, role) in prj_data:
                try:
                    # Test case #D14, #D15 (part 1)
                    row = panel.find_element_by_xpath(
                        './/tr[.//h4[contains(.,"{}")]]'.format(prj['name']))
                except NoSuchElementException:
                    # Test case #D17
                    assert prj['archived'] and not is_admin
                    continue

                # Test case #D15 (part 2)
                if prj['access'] == 'private':
                    row.find_element_by_xpath(
                        './/h4[.//*[contains(@class,"label") and'
                        '           contains(.,"Private")]]')

                # Test case #D16
                if prj['archived'] and is_admin:
                    row.find_element_by_xpath(
                        './/h4[.//*[contains(@class,"label") and'
                        '           contains(.,"Archived")]]')

                # Test case #D18
                    row.find_element_by_xpath(
                        './/td[contains(.,"{}")]'.format(PROJECT_ROLES[role]))

                # Test case #D19
                if prj['description']:
                    row.find_element_by_xpath(
                        './/p[contains(.,"{}")]'.format(prj['description']))
                if prj['country']:
                    row.find_element_by_xpath(
                        './/td[contains(.,"{}")]'.format(prj['country']))

                # Test case #D20
                row.find_element_by_xpath(
                    './/h4[.//a[@href="/organizations/{}/projects/{}/" and'
                    '           contains(.,"{}")]]'.format(
                        org['slug'], prj['slug'], prj['name']))
