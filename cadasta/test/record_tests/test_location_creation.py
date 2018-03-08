import pytest
import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from ..base_test import SeleniumTestCase


@pytest.mark.batch3
class TestLocationCreation(SeleniumTestCase):

    @pytest.fixture
    def basic_org_prj(self, basic_org, basic_prj):
        self.org = basic_org
        self.prj = basic_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], basic_prj['slug'])

    @pytest.fixture
    def custom_attrs_org_prj(self, basic_org, custom_attrs_prj):
        self.org = basic_org
        self.prj = custom_attrs_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], custom_attrs_prj['slug'])

    @pytest.fixture
    def conditional_attrs_org_prj(self, basic_org, conditional_attrs_prj):
        self.org = basic_org
        self.prj = conditional_attrs_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], conditional_attrs_prj['slug'])

    # ------ Utility functions ------

    def click_add_location_button(self):
        """Clicks the "Add location" button on the project header."""
        self.wd.BY_XPATH(
            '//*[contains(@class, "btn-primary") and '
            'contains(., "Add location")]').click()

    def click_save_button(self):
        button = self.wd.BY_XPATH('//*[@type="submit" and @value="Save"]')
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

    def test_user_can_create_delete_location(
        self, basic_org_prj, data_collector
    ):
        """Verifies Records test case #LC1, #LD1."""

        # Test case #LC1
        self.log_in(data_collector)
        self.open(self.prj_dashboard_path)
        self.click_add_location_button()
        self.draw_map_rectangle()
        self.update_form_field('type', 'PA')
        self.click_save_button()
        regex = self.prj_dashboard_path + 'records/locations/([a-z0-9]{24})/'
        m = re.fullmatch(regex, self.get_url_path())
        assert m
        location_id = m.group(1)
        self.wd.BY_XPATH('//h2[contains(.,"Location")]')
        self.wd.BY_XPATH('//h2[contains(.,"Parcel")]')
        self.wd.BY_XPATH('//*[@id="overview"]//td[contains(.,"Parcel")]')

        # [REVERSION] and test case #LD1
        self.wd.wait_until_gone((By.ID, 'loading'))
        self.wd.BY_CSS('[title="Delete location"]').click()
        self.wd.BY_XPATH(
            '//button[contains(., "Yes, delete this location")]').click()
        index_url = self.prj_dashboard_path + 'records/locations/'
        assert self.get_url_path() == index_url
        self.open(index_url + location_id + '/')
        h1_text = self.wd.BY_TAG('h1').text
        assert(
            re.search('Page not found', h1_text) or
            re.search('Not Found', h1_text))

    def test_user_can_create_update_location_with_custom_attributes(
        self, custom_attrs_org_prj, data_collector
    ):
        """Verifies Records test case #LC2, #LU4."""

        # Test case #LC2
        self.log_in(data_collector)
        self.open(self.prj_dashboard_path)
        self.click_add_location_button()
        self.draw_map_rectangle()
        self.update_form_field('type', 'PA')
        self.update_form_field('spatialunit::default::location_name', 'Spain')
        self.click_save_button()
        regex = self.prj_dashboard_path + 'records/locations/([a-z0-9]{24})/'
        m = re.fullmatch(regex, self.get_url_path())
        assert m
        location_id = m.group(1)
        self.wd.BY_XPATH('//h2[contains(.,"Location")]')
        self.wd.BY_XPATH('//h2[contains(.,"Parcel")]')
        self.wd.BY_XPATH('//*[@id="overview"]//td[contains(.,"Parcel")]')
        self.wd.BY_XPATH('//*[@id="overview"]//td[contains(.,"Spain")]')

        # Test case #LU4
        self.wd.wait_until_gone((By.ID, 'loading'))
        self.wd.BY_CSS('[title="Edit location"]').click()
        self.update_form_field('type', 'BU')
        self.update_form_field('spatialunit::default::location_name', 'Italy')
        self.click_save_button()
        self.wd.BY_XPATH('//h2[contains(.,"Location")]')
        self.wd.BY_XPATH('//h2[contains(.,"Building")]')
        self.wd.BY_XPATH('//*[@id="overview"]//td[contains(.,"Building")]')
        self.wd.BY_XPATH('//*[@id="overview"]//td[contains(.,"Italy")]')

        # [REVERSION]
        self.wd.wait_until_gone((By.ID, 'loading'))
        self.wd.BY_CSS('[title="Delete location"]').click()
        self.wd.BY_XPATH(
            '//button[contains(., "Yes, delete this location")]').click()
        index_url = self.prj_dashboard_path + 'records/locations/'
        assert self.get_url_path() == index_url
        self.open(index_url + location_id + '/')
        print(index_url + location_id + '/')
        h1_text = self.wd.BY_TAG('h1').text
        assert(
            re.search('Page not found', h1_text) or
            re.search('Not Found', h1_text))

    def test_geometry_is_required(self, basic_org_prj, data_collector):
        """Verifies Records test case #LC3."""

        self.log_in(data_collector)
        self.open(self.prj_dashboard_path)
        self.click_add_location_button()
        self.update_form_field('type', 'PA')
        self.click_save_button()
        self.wd.BY_XPATH(
            '//li[contains(.,"No map location was provided. '
            'Please use the tools provided on the left side '
            'of the map to mark your new location.")]')

    def test_location_type_is_required(self, basic_org_prj, data_collector):
        """Verifies Records test case #LC4."""

        self.log_in(data_collector)
        self.open(self.prj_dashboard_path)
        self.click_add_location_button()
        self.draw_map_rectangle()
        self.click_save_button()
        self.assert_form_field_has_error(
            'type', 'This field is required.')

    def test_unauthorized_user_cannot_create_location(
        self, basic_org_prj, prj_user
    ):
        """Verifies Records test case #LC5."""

        self.log_in(prj_user)
        self.open(self.prj_dashboard_path)
        try:
            self.wd.BY_CSS('.page-header .btn-group').find_element_by_xpath(
                './/*[normalize-space()="Add location"]')
            self.wd.BY_CSS('.page-header .btn-group .dropdown-toggle')
            raise AssertionError('Project add location/menu is present')
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Data"]').click()
        self.open(self.get_url_path() + 'new')
        self.wait_for_alert(
            "You don't have permission to add locations to this project.")
