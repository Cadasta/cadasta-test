import pytest

from ..base_test import SeleniumTestCase
from ..util import random_string


@pytest.mark.batch3
class TestTenureRelationshipBrowsing(SeleniumTestCase):

    @pytest.fixture
    def records_org_prj(self, basic_org, records_prj):
        self.org = basic_org
        self.prj = records_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], records_prj['slug'])

    # ------ Test cases ------

    def test_search_for_an_existing_tenure_relationship_works(
        self, records_org_prj, basic_water_rights, prj_user
    ):
        """Verifies Records test case #RB1."""

        self.log_in(prj_user)

        self.open(self.prj_dashboard_path + 'records/locations/{}/'.format(
            basic_water_rights['location']['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Relationships"]').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        name = basic_water_rights['party']['name']
        search_input.send_keys(name + ' ' + basic_water_rights['type_label'])
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]//tr['
            '    ./td[contains(.,"Water Rights")] and'
            '    ./td[contains(.,"{}")]'
            ']'.format(name))

        self.open(self.prj_dashboard_path + 'records/parties/{}/'.format(
            basic_water_rights['party']['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Relationships"]').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys('Parcel Water rights')
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]//tr['
            '    ./td[contains(.,"Water Rights")] and'
            '    ./td[contains(.,"Parcel")]'
            ']')

    def test_search_that_results_in_no_tenure_relationship_works(
        self, records_org_prj, basic_water_rights, prj_user
    ):
        """Verifies Records test case #RB2."""

        self.log_in(prj_user)

        self.open(self.prj_dashboard_path + 'records/locations/{}/'.format(
            basic_water_rights['location']['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Relationships"]').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(random_string())
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="No matching records found"]')

        self.open(self.prj_dashboard_path + 'records/parties/{}/'.format(
            basic_water_rights['party']['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Relationships"]').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(random_string())
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="No matching records found"]')
