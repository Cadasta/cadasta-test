import pytest

from ..base_test import SeleniumTestCase
from ..util import random_string


@pytest.mark.batch2
class TestPartyBrowsing(SeleniumTestCase):

    @pytest.fixture
    def records_org_prj(self, basic_org, records_prj):
        self.org = basic_org
        self.prj = records_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], records_prj['slug'])

    # ------ Test cases ------

    def test_search_for_an_existing_party_works(
        self, records_org_prj, basic_individual, prj_user
    ):
        """Verifies Records test case #PB1."""

        self.log_in(prj_user)
        self.open(self.prj_dashboard_path)
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Parties"]').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="paginated-table-filter"]//input[@type="search"]')
        name = basic_individual['name']
        search_input.send_keys(name)
        self.wd.BY_XPATH(
            '//*[@id="paginated-table"]//td[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH(
            '//*[@id="paginated-table"]//td[contains(.,"Individual")]')

    def test_search_that_results_in_no_party_works(
        self, records_org_prj, prj_user
    ):
        """Verifies Records test case #PB2."""

        self.log_in(prj_user)
        self.open(self.prj_dashboard_path)
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Parties"]').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="paginated-table-filter"]//input[@type="search"]')
        search_input.send_keys(random_string())
        self.wd.wait_for_xpath(
            '//*[@id="paginated-table"]'
            '//*[normalize-space()="No matching records found"]')
