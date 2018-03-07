import pytest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from ..base_test import SeleniumTestCase
from .resources_util import ResourcesUtil


@pytest.mark.batch4
class TestSpatialResources(ResourcesUtil, SeleniumTestCase):

    @pytest.fixture
    def basic_org_prj(self, basic_org, basic_prj):
        self.org = basic_org
        self.prj = basic_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], basic_prj['slug'])

    def attach_gpx_resource(self, resource):
        self.open(self.prj_dashboard_path + 'resources/')
        self.wd.BY_LINK('Attach').click()
        try:
            self.wd.BY_LINK('Upload new').click()
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH('//input[@type="file"]').send_keys(resource['path'])
        self.wd.wait_until_clickable((By.CLASS_NAME, 'file-remove'))
        self.update_form_field('name', resource['name'])
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()

    def activate_map_layer_switcher(self):
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Data"]').click()
        actions = ActionChains(self.wd)
        actions.move_to_element(
            self.wd.BY_CLASS('leaflet-control-layers-toggle'))
        actions.perform()
        self.wd.wait_until_clickable(
            (By.CLASS_NAME, 'leaflet-control-layers-list'))

    # ------ Test cases ------

    @pytest.mark.uploads
    def test_gpx_resource_with_waypoints_generate_map_layer(
        self, basic_org_prj, data_collector
    ):
        """Verifies Resources test case #S1."""

        filename = 'gpx_waypoints.gpx'
        resource = self.get_test_resource_data(filename)
        self.log_in(data_collector)
        self.attach_gpx_resource(resource)
        self.activate_map_layer_switcher()
        assert self.wd.BY_XPATH(
            '//*['
            '    contains(@class,"leaflet-control-layers-group") and'
            '    .//span[contains(.,"{}")] and'
            '    .//span[contains(.,"waypoints")]'
            ']'.format(resource['name'])).is_displayed()

        # [REVERSION]
        self.delete_resource(resource, is_on_resource_page=False)

    @pytest.mark.uploads
    def test_gpx_resource_with_routes_generate_map_layer(
        self, basic_org_prj, data_collector
    ):
        """Verifies Resources test case #S2."""

        filename = 'gpx_routes.gpx'
        resource = self.get_test_resource_data(filename)
        self.log_in(data_collector)
        self.attach_gpx_resource(resource)
        self.activate_map_layer_switcher()
        assert self.wd.BY_XPATH(
            '//*['
            '    contains(@class,"leaflet-control-layers-group") and'
            '    .//span[contains(.,"{}")] and'
            '    .//span[contains(.,"routes")]'
            ']'.format(resource['name'])).is_displayed()

        # [REVERSION]
        self.delete_resource(resource, is_on_resource_page=False)

    @pytest.mark.uploads
    def test_gpx_resource_with_tracks_generate_map_layer(
        self, basic_org_prj, data_collector
    ):
        """Verifies Resources test case #S3."""

        filename = 'gpx_tracks.gpx'
        resource = self.get_test_resource_data(filename)
        self.log_in(data_collector)
        self.attach_gpx_resource(resource)
        self.activate_map_layer_switcher()
        assert self.wd.BY_XPATH(
            '//*['
            '    contains(@class,"leaflet-control-layers-group") and'
            '    .//span[contains(.,"{}")] and'
            '    .//span[contains(.,"tracks")]'
            ']'.format(resource['name'])).is_displayed()

        # [REVERSION]
        self.delete_resource(resource, is_on_resource_page=False)
