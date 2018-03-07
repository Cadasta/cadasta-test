import pytest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from ..base_test import SeleniumTestCase


@pytest.mark.batch3
class TestLocationDeletion(SeleniumTestCase):

    @pytest.fixture
    def records_org_prj(self, basic_org, records_prj):
        self.org = basic_org
        self.prj = records_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], records_prj['slug'])

    # ------ Utility functions ------

    def click_add_location_button(self):
        """Clicks the "Add location" button on the project header."""
        self.wd.BY_XPATH(
            '//*[contains(@class, "btn-primary") and '
            'contains(., "Add location")]').click()

    def click_add_location_save_button(self):
        button = self.wd.BY_XPATH('//*[@type="submit" and @value="Save"]')
        button.click()

    def click_add_relationship_save_button(self):
        button = self.wd.BY_XPATH(
            '//*[@type="submit" and normalize-space()="Save"]')
        self.scroll_element_into_view(button)
        button.click()

    def draw_map_rectangle(self):
        self.wd.BY_CLASS('leaflet-draw-draw-rectangle').click()
        actions = ActionChains(self.wd)
        actions.move_to_element(self.wd.BY_ID('id_geometry_map'))
        # Avoid the equator because of a bug in PostGIS
        # https://gis.stackexchange.com/questions/169436/
        #    postgis-polygons-lying-on-the-equator
        actions.move_by_offset(10, 10)
        actions.click_and_hold()
        actions.move_by_offset(40, 40)
        actions.release()
        actions.perform()

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

    def test_deleting_a_location_deletes_its_tenure_relationships(
        self, records_org_prj, basic_individual, data_collector
    ):
        """Verifies Records test case #LD3."""

        self.log_in(data_collector)

        # Create throwaway location
        self.open(self.prj_dashboard_path)
        self.click_add_location_button()
        self.draw_map_rectangle()
        self.update_form_field('type', 'PA')
        self.click_add_location_save_button()

        # Create throwaway tenure relationship with basic individual
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Relationships"]').click()
        self.wd.BY_LINK('Add relationship').click()
        self.wd.BY_ID('select2-party-select-container').click()
        self.wd.BY_XPATH(
            '//*[contains(@id,"select2-party-select-result-") and '
            '    contains(@id,"-{}")]'.format(basic_individual['pk'])).click()
        assert (
            self.wd.BY_ID('select2-party-select-container').text ==
            basic_individual['name']
        )
        self.update_form_field('tenure_type', 'CR')
        self.click_add_relationship_save_button()

        # Test case #LD3
        self.wd.wait_until_gone((By.ID, 'loading'))
        self.wd.BY_CSS('[title="Delete location"]').click()
        self.wd.BY_XPATH(
            '//button[contains(., "Yes, delete this location")]').click()
        index_url = self.prj_dashboard_path + 'records/locations/'
        assert self.get_url_path() == index_url
        self.open(self.prj_dashboard_path + 'records/parties/{}/'.format(
            basic_individual['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Relationships"]').click()
        try:
            # Party has no relationships, so relationship is indeed deleted
            self.wd.BY_XPATH(
                '//*[normalize-space()="This party does not have any '
                'relationships and is not connected to any locations."]')
        except NoSuchElementException:
            # Party has other relationships, so let's search for our
            # particular relationship
            search_input = self.wd.BY_XPATH(
                '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
            search_input.send_keys('Carbon Rights ' + basic_individual['name'])
            self.wd.BY_XPATH(
                '//*[@id="DataTables_Table_0"]'
                '//*[normalize-space()="No matching records found"]')
