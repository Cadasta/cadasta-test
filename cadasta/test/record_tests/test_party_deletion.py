import pytest

from selenium.common.exceptions import NoSuchElementException

from ..base_test import SeleniumTestCase


@pytest.mark.batch2
class TestPartyDeletion(SeleniumTestCase):

    @pytest.fixture
    def records_org_prj(self, basic_org, records_prj):
        self.org = basic_org
        self.prj = records_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], records_prj['slug'])

    # ------ Test cases ------

    def test_unauthorized_user_cannot_delete_party(
        self, records_org_prj, basic_individual, prj_user
    ):
        """Verifies Records test case #PD2."""

        self.log_in(prj_user)
        self.open(self.prj_dashboard_path + 'records/parties/{}/'.format(
            basic_individual['pk']))
        try:
            self.wd.BY_CSS('[title="Delete party"]')
            raise AssertionError('Delete party button is present')
        except NoSuchElementException:
            pass
        self.open(self.get_url_path() + 'delete')
        self.wait_for_alert(
            "You don't have permission to remove this party.")
