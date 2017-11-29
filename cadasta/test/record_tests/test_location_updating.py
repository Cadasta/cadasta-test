import pytest
import time

from selenium.common.exceptions import NoSuchElementException

from ..base_test import SeleniumTestCase


class TestLocationUpdating(SeleniumTestCase):

    @pytest.fixture
    def records_org_prj(self, basic_org, records_prj):
        self.org = basic_org
        self.prj = records_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], records_prj['slug'])

    # ------ Utility functions ------

    def click_save_button(self):
        button = self.wd.BY_XPATH('//*[@type="submit" and @value="Save"]')
        button.click()

    # ------ Test cases ------

    def test_user_can_update_location_type(
        self, records_org_prj, basic_parcel, data_collector
    ):
        """Verifies Records test case #LU3."""

        self.log_in(data_collector)
        self.open(self.prj_dashboard_path + 'records/locations/{}/'.format(
            basic_parcel['pk']))
        self.wd.BY_CSS('[title="Edit location"]').click()
        time.sleep(1)  # Wait for the map editing to finish setting up
        self.update_form_field('type', 'BU')
        self.click_save_button()
        self.wd.BY_XPATH('//h2[contains(.,"Location")]')
        self.wd.BY_XPATH('//h2[contains(.,"Building")]')
        self.wd.BY_XPATH('//*[@id="overview"]//td[contains(.,"Building")]')

        # [REVERSION]
        self.wd.BY_CSS('[title="Edit location"]').click()
        self.update_form_field('type', basic_parcel['type'])
        self.click_save_button()

    def test_unauthorized_user_cannot_update_location(
        self, records_org_prj, basic_parcel, prj_user
    ):
        """Verifies Records test case #LU5."""

        self.log_in(prj_user)
        self.open(self.prj_dashboard_path + 'records/locations/{}/'.format(
            basic_parcel['pk']))
        try:
            self.wd.BY_CSS('[title="Edit location"]')
            raise AssertionError('Edit location button is present')
        except NoSuchElementException:
            pass
        self.open(self.get_url_path() + 'edit')
        self.wait_for_alert(
            "You don't have permission to update this location.")
