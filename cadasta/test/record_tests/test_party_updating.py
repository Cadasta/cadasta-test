import pytest

from selenium.common.exceptions import NoSuchElementException

from ..base_test import SeleniumTestCase


@pytest.mark.batch3
class TestPartyUpdating(SeleniumTestCase):

    @pytest.fixture
    def records_org_prj(self, basic_org, records_prj):
        self.org = basic_org
        self.prj = records_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], records_prj['slug'])

    # ------ Utility functions ------

    def click_save_button(self):
        button = self.wd.BY_XPATH(
            '//*[@type="submit" and normalize-space()="Save"]')
        self.scroll_element_into_view(button)
        button.click()

    # ------ Test cases ------

    def test_user_can_update_party(
        self, records_org_prj, basic_individual, data_collector
    ):
        """Verifies Records test case #PU1."""

        self.log_in(data_collector)
        self.open(self.prj_dashboard_path + 'records/parties/{}/'.format(
            basic_individual['pk']))
        self.wd.BY_CSS('[title="Edit party"]').click()
        self.update_form_field('name', 'FuncTest Temp Name')
        self.update_form_field('type', 'GR')
        self.click_save_button()
        self.wd.BY_XPATH('//h2[contains(.,"FuncTest Temp Name")]')
        self.wd.BY_XPATH('//td[contains(.,"FuncTest Temp Name")]')
        self.wd.BY_XPATH('//td[contains(.,"Group")]')

        # [REVERSION]
        self.wd.BY_CSS('[title="Edit party"]').click()
        self.update_form_field('name', basic_individual['name'])
        self.update_form_field('type', basic_individual['type'])
        self.click_save_button()

    def test_unauthorized_user_cannot_update_party(
        self, records_org_prj, basic_individual, prj_user
    ):
        """Verifies Records test case #PU4."""

        self.log_in(prj_user)
        self.open(self.prj_dashboard_path + 'records/parties/{}/'.format(
            basic_individual['pk']))
        try:
            self.wd.BY_CSS('[title="Edit party"]')
            raise AssertionError('Edit party button is present')
        except NoSuchElementException:
            pass
        self.open(self.get_url_path() + 'edit')
        self.wait_for_alert(
            "You don't have permission to update this party.")
