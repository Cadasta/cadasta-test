import pytest

from selenium.common.exceptions import NoSuchElementException

from ..base_test import SeleniumTestCase


@pytest.mark.batch3
class TestTenureRelationshipDeletion(SeleniumTestCase):

    @pytest.fixture
    def records_org_prj(self, basic_org, records_prj):
        self.org = basic_org
        self.prj = records_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], records_prj['slug'])

    # ------ Test cases ------

    def test_unauthorized_user_cannot_delete_tenure_relationship(
        self, records_org_prj, basic_water_rights, prj_user
    ):
        """Verifies Records test case #RD2."""

        self.log_in(prj_user)
        self.open(self.prj_dashboard_path + 'relationships/{}/'.format(
            basic_water_rights['pk']))
        try:
            self.wd.BY_CSS('[title="Delete relationship"]')
            raise AssertionError('Delete relationship button is present')
        except NoSuchElementException:
            pass
        self.open(self.get_url_path() + 'delete')
        self.wait_for_alert(
            "You don't have permission to remove this tenure relationship.")
