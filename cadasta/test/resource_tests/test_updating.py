import pytest
import re

from datetime import timedelta
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from ..base_test import SeleniumTestCase
from .resources_util import ResourcesUtil
from ..util import random_string


@pytest.mark.batch4
class TestUpdating(ResourcesUtil, SeleniumTestCase):

    @pytest.fixture
    def records_org_prj(self, basic_org, records_prj):
        self.org = basic_org
        self.prj = records_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], records_prj['slug'])

    # ------ Test cases ------

    @pytest.mark.uploads
    def test_user_can_update_replace_resource(
        self, records_org_prj, basic_parcel, data_collector
    ):
        """Verifies Resources test cases #U1, #U2, #X2."""

        filename1 = 'user_avatar_1.jpg'
        resource1 = self.get_test_resource_data(filename1)
        filename2 = 'user_avatar_2.png'
        resource2 = self.get_test_resource_data(filename2)
        self.log_in(data_collector)

        # Attach a resource to the basic parcel
        self.open(self.prj_dashboard_path + 'records/locations/{}/'.format(
            basic_parcel['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Resources"]').click()
        self.wd.BY_LINK('Attach').click()
        try:
            self.wd.BY_LINK('Upload new').click()
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH('//input[@type="file"]').send_keys(resource1['path'])
        self.wd.wait_until_clickable((By.CLASS_NAME, 'file-remove'))
        self.update_form_field('name', resource1['name'])
        self.update_form_field('description', resource1['description'])
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()

        # Test case #U1
        self.open(self.prj_dashboard_path + 'resources/')
        self.do_table_search(resource1['name'])
        self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(filename1)).click()
        self.wd.BY_CSS('[title="Edit resource"]').click()
        temp_name = random_string()
        temp_description = random_string()
        self.update_form_field('name', temp_name)
        self.update_form_field('description', temp_description)
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()
        (expected_min_date, expected_max_date) = self.get_min_max_date()
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(temp_name))
        self.wd.BY_XPATH('//p[contains(.,"{}")]'.format(temp_description))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(filename1))
        self.wd.BY_XPATH('//td[contains(.,"{}") or contains(.,"{}")]'.format(
            expected_min_date, expected_max_date))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(
            data_collector['full_name']))

        self.open(self.prj_dashboard_path + 'resources/')
        self.do_table_search(temp_name)
        row = self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(filename1))
        row_febx = row.find_element_by_xpath
        row_febx('.//*[contains(.,"{}")]'.format(temp_name))
        row_febx('.//*[contains(.,"{}")]'.format(resource1['type']))
        row_febx('.//*[contains(.,"{}")]'.format(data_collector['username']))
        row_febx('.//*[contains(.,"{}")]'.format(data_collector['full_name']))
        row_febx('.//*[contains(.,"{}") or contains(.,"{}")]'.format(
            re.sub(r'^(...).*? ', r'\1 ', expected_min_date),
            re.sub(r'^(...).*? ', r'\1 ', expected_max_date)))

        # Test case #U2
        self.do_table_search(temp_name)
        self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(filename1)).click()
        self.wd.BY_CSS('[title="Edit resource"]').click()
        self.wd.BY_LINK('(Remove)').click()
        self.wd.BY_XPATH('//input[@type="file"]').send_keys(resource2['path'])
        self.wd.wait_until_clickable((By.CLASS_NAME, 'file-remove'))
        assert (
            self.wd.BY_NAME('name').get_attribute('value') ==
            resource2['prefill'])
        self.update_form_field('name', resource2['name'])
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()
        (expected_min_date, expected_max_date) = self.get_min_max_date()
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(resource2['name']))
        self.wd.BY_XPATH('//p[contains(.,"{}")]'.format(temp_description))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(filename2))
        self.wd.BY_XPATH('//td[contains(.,"{}") or contains(.,"{}")]'.format(
            expected_min_date, expected_max_date))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(
            data_collector['full_name']))

        self.open(self.prj_dashboard_path + 'resources/')
        self.do_table_search(resource2['name'])
        row = self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(filename2))
        row_febx = row.find_element_by_xpath
        row_febx('.//*[contains(.,"{}")]'.format(resource2['name']))
        row_febx('.//*[contains(.,"{}")]'.format(resource2['type']))
        row_febx('.//*[contains(.,"{}")]'.format(data_collector['username']))
        row_febx('.//*[contains(.,"{}")]'.format(data_collector['full_name']))
        row_febx('.//*[contains(.,"{}") or contains(.,"{}")]'.format(
            re.sub(r'^(...).*? ', r'\1 ', expected_min_date),
            re.sub(r'^(...).*? ', r'\1 ', expected_max_date)))

        # [REVERSION] and test case #X2
        row.click()
        self.wd.BY_CSS('[title="Delete resource"]').click()
        self.wd.BY_LINK('Yes, delete this resource').click()
        assert self.get_url_path() == self.prj_dashboard_path + 'resources/'
        self.do_table_search(resource2['name'])
        self.wd.wait_for_xpath(
            '//*[@id="paginated-table"]'
            '//*[normalize-space()="No matching records found"]')
        self.open(self.prj_dashboard_path + 'records/locations/{}/'.format(
            basic_parcel['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Resources"]').click()
        try:
            # Location has no resources, so it is indeed deleted
            self.wd.BY_XPATH(
                '//*[@id="resources"]//*[contains(.,'
                '"This location does not have any attached resources.")]')
        except NoSuchElementException:
            # Location has other resources, so let's search for our resource
            # DataTables Table 0 is tenure relationships; Table 1 is resources
            self.do_table_search(
                resource2['name'], filter_id='DataTables_Table_1_filter')
            self.wd.BY_XPATH(
                '//*[@id="DataTables_Table_1"]'
                '//*[normalize-space()="No matching records found"]')

    def test_project_user_cannot_update_resource(
        self, records_org_prj, dummy_resource_1, prj_user, data_collector
    ):
        """Verifies Resources test case #B1, #B2, #U3."""

        # Test case #B1
        self.log_in(prj_user)
        self.open(self.prj_dashboard_path)
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Resources"]').click()
        self.do_table_search(dummy_resource_1['name'])
        row = self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(dummy_resource_1['original_file']))
        row_febx = row.find_element_by_xpath
        row_febx('.//*[contains(.,"{}")]'.format(dummy_resource_1['name']))
        row_febx('.//*[contains(.,"{}")]'.format(dummy_resource_1['type']))
        row_febx('.//*[contains(.,"{}")]'.format(data_collector['username']))
        row_febx('.//*[contains(.,"{}")]'.format(data_collector['full_name']))
        max_date = dummy_resource_1['last_updated'].strftime('%b %-d, %Y')
        min_date = dummy_resource_1['last_updated'] + timedelta(days=-1)
        min_date = min_date.strftime('%b %-d, %Y')
        row_febx('.//*[contains(.,"{}") or contains(.,"{}")]'.format(
            max_date, min_date))

        # Test case #B2
        self.do_table_search(random_string())
        self.wd.wait_for_xpath(
            '//*[@id="paginated-table"]'
            '//*[normalize-space()="No matching records found"]')

        # Test case #U3
        self.do_table_search(dummy_resource_1['name'])
        self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(
                dummy_resource_1['original_file'])).click()
        try:
            self.wd.BY_CSS('[title="Edit resource"]').click()
            raise AssertionError('Edit resource button is present')
        except NoSuchElementException:
            pass
        self.open(self.get_url_path() + 'edit')
        self.wait_for_alert(
            "You don't have permission to edit this resource.")
        self.open('/account/logout/')
