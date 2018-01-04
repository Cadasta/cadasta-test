import pytest

from ..base_test import SeleniumTestCase
from ..util import random_string


@pytest.mark.batch1
class TestBrowsing(SeleniumTestCase):

    def test_search_for_an_existing_org_works(self, basic_org):
        """Verifies Organizations test case #B1."""

        self.wd.BY_LINK('Organizations').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(basic_org['name'])
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="{}"]'.format(basic_org['name']))

    def test_search_that_results_in_no_org_works(self):
        """Verifies Organizations test case #B2."""

        self.wd.BY_LINK('Organizations').click()
        search_input = self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
        search_input.send_keys(random_string())
        self.wd.BY_XPATH(
            '//*[@id="DataTables_Table_0"]'
            '//*[normalize-space()="No matching records found"]')
