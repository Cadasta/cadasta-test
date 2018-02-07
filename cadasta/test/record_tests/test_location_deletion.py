import pytest

from selenium.common.exceptions import NoSuchElementException

from ..base_test import SeleniumTestCase


@pytest.mark.batch3
class TestLocationDeletion(SeleniumTestCase):

    @pytest.fixture
    def records_org_prj(self, basic_org, records_prj):
        self.org = basic_org
        self.prj = records_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], records_prj['slug'])

    # ------ Test cases ------

    def test_unauthorized_user_cannot_delete_party(
        self, records_org_prj, basic_parcel, prj_user
    ):
        """Verifies Records test case #LD2."""

        self.log_in(prj_user)
        self.open(self.prj_dashboard_path + 'records/locations/{}/'.format(
            basic_parcel['pk']))
        try:
            self.wd.BY_CSS('[title="Delete location"]')
            raise AssertionError('Delete location button is present')
        except NoSuchElementException:
            pass
        self.open(self.get_url_path() + 'delete')
        self.wait_for_alert(
            "You don't have permission to remove this location.")
