import pytest

from selenium.common.exceptions import NoSuchElementException

from ..base_test import SeleniumTestCase


@pytest.mark.batch3
class TestLocationUpdating(SeleniumTestCase):

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

    def test_user_can_update_tenure_relationship_type(
        self, records_org_prj, basic_water_rights,
        data_collector
    ):
        """Verifies Records test case #RU1."""

        self.log_in(data_collector)
        self.open(self.prj_dashboard_path + 'relationships/{}/'.format(
            basic_water_rights['pk']))
        self.wd.BY_CSS('[title="Edit relationship"]').click()
        self.update_form_field('tenure_type', 'UC')
        self.click_save_button()
        self.wd.BY_XPATH(
            '//tr['
            '    .//td[contains(.,"Type")] and '
            '    .//td[contains(.,"Undivided Co-ownership")]'
            ']')
        self.wd.BY_XPATH(
            '//tr['
            '    .//td[contains(.,"Party")] and '
            '    .//td//a[contains(.,"{}")]'
            ']'.format(basic_water_rights['party']['name']))

        # [REVERSION]
        self.wd.BY_CSS('[title="Edit relationship"]').click()
        self.update_form_field('tenure_type', 'WR')
        self.click_save_button()

    def test_unauthorized_user_cannot_update_tenure_relationship(
        self, records_org_prj, basic_water_rights, prj_user
    ):
        """Verifies Records test case #RU3."""

        self.log_in(prj_user)
        self.open(self.prj_dashboard_path + 'relationships/{}/'.format(
            basic_water_rights['pk']))
        try:
            self.wd.BY_CSS('[title="Edit relationship"]')
            raise AssertionError('Edit relationship button is present')
        except NoSuchElementException:
            pass
        self.open(self.get_url_path() + 'edit')
        self.wait_for_alert(
            "You don't have permission to update this tenure relationship.")
