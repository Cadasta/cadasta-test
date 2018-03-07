import pytest
import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from ..base_test import SeleniumTestCase
from .resources_util import ResourcesUtil


@pytest.mark.batch3
class TestAttaching(ResourcesUtil, SeleniumTestCase):

    @pytest.fixture
    def basic_org_prj(self, basic_org, basic_prj):
        self.org = basic_org
        self.prj = basic_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], basic_prj['slug'])

    @pytest.fixture
    def records_org_prj(self, basic_org, records_prj):
        self.org = basic_org
        self.prj = records_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], records_prj['slug'])

    # ------ Utility functions ------

    def attach_resource_to_project_and_verify(
        self, user, filename, has_description=True, delete_after=True
    ):
        resource = self.get_test_resource_data(filename)
        self.open(self.prj_dashboard_path + 'resources/')
        self.wd.BY_LINK('Attach').click()
        try:
            self.wd.BY_LINK('Upload new').click()
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH('//input[@type="file"]').send_keys(resource['path'])
        self.wd.wait_until_clickable((By.CLASS_NAME, 'file-remove'))
        self.update_form_field('name', resource['name'])
        if has_description:
            self.update_form_field('description', resource['description'])
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()

        (expected_min_date, expected_max_date) = self.get_min_max_date()
        self.do_table_search(resource['name'])
        row = self.wd.wait_for_xpath('//tr[contains(.,"{}")]'.format(filename))
        row_febx = row.find_element_by_xpath
        row_febx('.//*[contains(.,"{}")]'.format(resource['name']))
        row_febx('.//*[contains(.,"{}")]'.format(resource['type']))
        row_febx('.//*[contains(.,"{}")]'.format(user['username']))
        row_febx('.//*[contains(.,"{}")]'.format(user['full_name']))
        row_febx('.//*[contains(.,"{}") or contains(.,"{}")]'.format(
            re.sub(r'^(...).*? ', r'\1 ', expected_min_date),
            re.sub(r'^(...).*? ', r'\1 ', expected_max_date)))
        row_febx('.//button[contains(.,"Detach")]')
        row.click()

        self.wd.wait_for_xpath(
            '//h2[contains(.,"{}")]'.format(resource['name']))
        if has_description:
            self.wd.BY_XPATH(
                '//p[contains(.,"{}")]'.format(resource['description']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(filename))
        self.wd.BY_XPATH('//td[contains(.,"{}") or contains(.,"{}")]'.format(
            expected_min_date, expected_max_date))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(user['full_name']))
        row = self.wd.BY_XPATH(
            '//tr[contains(.,"{}")]'.format(self.prj['name']))

        # [REVERSION]
        self.delete_resource(resource)

    # ------ Test cases ------

    @pytest.mark.uploads
    def test_resource_can_be_attached_to_and_deattached_from_project(
        self, basic_org_prj, data_collector
    ):
        """Verifies Resources test cases #A1, #A2, #A11, #D1, #D2, #X1."""

        filename = 'user_avatar_1.jpg'
        resource = self.get_test_resource_data(filename)
        self.log_in(data_collector)

        # Test case #A1
        self.open(self.prj_dashboard_path)
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Resources"]').click()
        self.wd.BY_LINK('Attach').click()
        try:
            self.wd.BY_LINK('Upload new').click()
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH('//input[@type="file"]').send_keys(resource['path'])
        self.wd.wait_until_clickable((By.CLASS_NAME, 'file-remove'))

        # Minor check: Test case #A11
        assert (
            self.wd.BY_NAME('name').get_attribute('value') ==
            resource['prefill'])

        self.update_form_field('name', resource['name'])
        self.update_form_field('description', resource['description'])
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()

        (expected_min_date, expected_max_date) = self.get_min_max_date()
        self.do_table_search(resource['name'])
        row = self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(resource['name']))
        row_febx = row.find_element_by_xpath
        row_febx('.//*[contains(.,"{}")]'.format(resource['name']))
        row_febx('.//*[contains(.,"{}")]'.format(resource['type']))
        row_febx('.//*[contains(.,"{}")]'.format(data_collector['username']))
        row_febx('.//*[contains(.,"{}")]'.format(data_collector['full_name']))
        row_febx('.//*[contains(.,"{}") or contains(.,"{}")]'.format(
            re.sub(r'^(...).*? ', r'\1 ', expected_min_date),
            re.sub(r'^(...).*? ', r'\1 ', expected_max_date)))
        row_febx('.//button[contains(.,"Detach")]')

        # Continuation of test case #A1
        row.click()
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(resource['name']))
        self.wd.BY_XPATH(
            '//p[contains(.,"{}")]'.format(resource['description']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(filename))
        self.wd.BY_XPATH('//td[contains(.,"{}") or contains(.,"{}")]'.format(
            expected_min_date, expected_max_date))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(
            data_collector['full_name']))
        row = self.wd.BY_XPATH(
            '//tr[contains(.,"{}")]'.format(self.prj['name']))

        # Test case #D2
        detach_button = row.find_element_by_tag_name('button')
        self.scroll_element_into_view(detach_button)
        detach_button.click()
        try:
            self.wd.BY_XPATH(
                '//tr[contains(.,"{}")]'.format(self.prj['name']))
            raise AssertionError('Resource is still attached to project')
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Resources"]').click()
        self.do_table_search(resource['name'])
        row = self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(resource['name']))
        try:
            row.find_element_by_xpath('.//button[contains(.,"Detach")]')
            raise AssertionError('Resource is still attached to project')
        except NoSuchElementException:
            pass

        # Test case #A2
        self.wd.BY_LINK('Attach').click()
        self.do_table_search(
            resource['name'], filter_id='DataTables_Table_0_filter')
        self.wd.BY_XPATH(
            '//tr[contains(.,"{}")]'.format(resource['name'])).click()
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()
        self.do_table_search(resource['name'])
        row = self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(resource['name']))
        row.find_element_by_xpath('.//button[contains(.,"Detach")]')
        row.click()
        self.wd.BY_XPATH('//tr[contains(.,"{}")]'.format(self.prj['name']))

        # Test case #D1
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Resources"]').click()
        self.do_table_search(resource['name'])
        self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'
            '//button[contains(.,"Detach")]'.format(resource['name'])).click()
        self.do_table_search(resource['name'])
        row = self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(resource['name']))
        try:
            row.find_element_by_xpath('.//button[contains(.,"Detach")]')
            raise AssertionError('Resource is still attached to project')
        except NoSuchElementException:
            pass
        row.click()
        try:
            self.wd.BY_XPATH(
                '//tr[contains(.,"{}")]'.format(self.prj['name']))
            raise AssertionError('Resource is still attached to project')
        except NoSuchElementException:
            pass

        # [REVERSION] and test case #X1
        self.delete_resource(resource)
        self.do_table_search(resource['name'])
        self.wd.wait_for_xpath(
            '//*[@id="paginated-table"]'
            '//*[normalize-space()="No matching records found"]')

    @pytest.mark.uploads
    def test_resource_can_be_attached_to_and_deattached_from_location(
        self, records_org_prj, basic_parcel, data_collector
    ):
        """Verifies Resources test cases #A3, #A4, #D3, #D4."""

        filename = 'user_avatar_2.png'
        resource = self.get_test_resource_data(filename)
        self.log_in(data_collector)

        # Test case #A3
        self.open(self.prj_dashboard_path + 'records/locations/{}/'.format(
            basic_parcel['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Resources"]').click()
        self.wd.BY_LINK('Attach').click()
        try:
            self.wd.BY_LINK('Upload new').click()
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH('//input[@type="file"]').send_keys(resource['path'])
        self.wd.wait_until_clickable((By.CLASS_NAME, 'file-remove'))
        self.update_form_field('name', resource['name'])
        self.update_form_field('description', resource['description'])
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()
        (expected_min_date, expected_max_date) = self.get_min_max_date()
        # DataTables Table 0 is tenure relationships; Table 1 is resources
        self.do_table_search(
            resource['name'], filter_id='DataTables_Table_1_filter')
        row = self.wd.BY_XPATH('//tr[contains(.,"{}")]'.format(filename))
        row_febx = row.find_element_by_xpath
        row_febx('.//*[contains(.,"{}")]'.format(resource['name']))
        row_febx('.//button[contains(.,"Detach")]')
        row.click()

        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(resource['name']))
        self.wd.BY_XPATH(
            '//p[contains(.,"{}")]'.format(resource['description']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(filename))
        self.wd.BY_XPATH('//td[contains(.,"{}") or contains(.,"{}")]'.format(
            expected_min_date, expected_max_date))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(
            data_collector['full_name']))
        row = self.wd.BY_XPATH(
            '//tr['
            '     .//td[contains(.,"Location")] and'
            '     .//td[contains(.,"{}")]'
            ']'.format(basic_parcel['type_label']))

        # Test case #D4
        detach_button = row.find_element_by_tag_name('button')
        self.scroll_element_into_view(detach_button)
        detach_button.click()
        try:
            self.wd.BY_XPATH(
                '//tr['
                '     .//td[contains(.,"Location")] and'
                '     .//td[contains(.,"{}")]'
                ']'.format(basic_parcel['type_label']))
            raise AssertionError('Resource is still attached to location')
        except NoSuchElementException:
            pass
        self.open(self.prj_dashboard_path + 'records/locations/{}/'.format(
            basic_parcel['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Resources"]').click()
        try:
            # Location has no resources, so it is indeed detached
            self.wd.BY_XPATH(
                '//*[@id="resources"]//*[contains(.,'
                '"This location does not have any attached resources.")]')
        except NoSuchElementException:
            # Location has other resources, so let's search for our resource
            # DataTables Table 0 is tenure relationships; Table 1 is resources
            self.do_table_search(
                resource['name'], filter_id='DataTables_Table_1_filter')
            self.wd.BY_XPATH(
                '//*[@id="DataTables_Table_1"]'
                '//*[normalize-space()="No matching records found"]')

        # Test case #A4
        self.open(self.prj_dashboard_path + 'records/locations/{}/'.format(
            basic_parcel['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Resources"]').click()
        self.wd.BY_LINK('Attach').click()
        self.do_table_search(
            resource['name'], filter_id='DataTables_Table_0_filter')
        self.wd.BY_XPATH('//tr[contains(.,"{}")]'.format(filename)).click()
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()
        # DataTables Table 0 is tenure relationships; Table 1 is resources
        self.do_table_search(
            resource['name'], filter_id='DataTables_Table_1_filter')
        row = self.wd.BY_XPATH('//tr[contains(.,"{}")]'.format(filename))
        row.find_element_by_xpath('.//button[contains(.,"Detach")]')
        row.click()
        self.wd.BY_XPATH(
            '//tr['
            '     .//td[contains(.,"Location")] and'
            '     .//td[contains(.,"{}")]'
            ']'.format(basic_parcel['type_label']))

        # Test case #D3
        self.open(self.prj_dashboard_path + 'records/locations/{}/'.format(
            basic_parcel['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Resources"]').click()
        # DataTables Table 0 is tenure relationships; Table 1 is resources
        self.do_table_search(
            resource['name'], filter_id='DataTables_Table_1_filter')
        self.wd.BY_XPATH(
            '//tr[contains(.,"{}")]'
            '//button[contains(.,"Detach")]'.format(filename)).click()
        try:
            # Location has no resources, so it is indeed detached
            self.wd.BY_XPATH(
                '//*[@id="resources"]//*[contains(.,'
                '"This location does not have any attached resources.")]')
        except NoSuchElementException:
            # Location has other resources, so let's search for our resource
            # DataTables Table 0 is tenure relationships; Table 1 is resources
            self.do_table_search(
                resource['name'], filter_id='DataTables_Table_1_filter')
            self.wd.BY_XPATH(
                '//*[@id="DataTables_Table_1"]'
                '//*[normalize-space()="No matching records found"]')
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Resources"]').click()
        self.do_table_search(resource['name'])
        self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(filename)).click()
        try:
            self.wd.BY_XPATH(
                '//tr['
                '     .//td[contains(.,"Location")] and'
                '     .//td[contains(.,"{}")]'
                ']'.format(basic_parcel['type_label']))
            raise AssertionError('Resource is still attached to location')
        except NoSuchElementException:
            pass

        # [REVERSION]
        self.delete_resource(resource)

    @pytest.mark.uploads
    def test_resource_can_be_attached_to_and_deattached_from_party(
        self, records_org_prj, basic_individual, data_collector
    ):
        """Verifies Resources test cases #A5, #A6, #D5, #D6."""

        filename = 'user_avatar_3.gif'
        resource = self.get_test_resource_data(filename)
        self.log_in(data_collector)

        # Test case #A5
        self.open(self.prj_dashboard_path + 'records/parties/{}/'.format(
            basic_individual['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Resources"]').click()
        self.wd.BY_LINK('Attach').click()
        try:
            self.wd.BY_LINK('Upload new').click()
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH('//input[@type="file"]').send_keys(resource['path'])
        self.wd.wait_until_clickable((By.CLASS_NAME, 'file-remove'))
        self.update_form_field('name', resource['name'])
        self.update_form_field('description', resource['description'])
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()
        (expected_min_date, expected_max_date) = self.get_min_max_date()
        # DataTables Table 0 is tenure relationships; Table 1 is resources
        self.do_table_search(
            resource['name'], filter_id='DataTables_Table_1_filter')
        row = self.wd.BY_XPATH('//tr[contains(.,"{}")]'.format(filename))
        row_febx = row.find_element_by_xpath
        row_febx('.//*[contains(.,"{}")]'.format(resource['name']))
        row_febx('.//*[contains(.,"{}")]'.format(resource['type']))
        row_febx('.//*[contains(.,"{}")]'.format(data_collector['username']))
        row_febx('.//*[contains(.,"{}")]'.format(data_collector['full_name']))
        row_febx('.//*[contains(.,"{}") or contains(.,"{}")]'.format(
            expected_min_date, expected_max_date))
        row_febx('.//button[contains(.,"Detach")]')
        row.click()

        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(resource['name']))
        self.wd.BY_XPATH(
            '//p[contains(.,"{}")]'.format(resource['description']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(filename))
        self.wd.BY_XPATH('//td[contains(.,"{}") or contains(.,"{}")]'.format(
            expected_min_date, expected_max_date))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(
            data_collector['full_name']))
        row = self.wd.BY_XPATH(
            '//tr['
            '     .//td[contains(.,"Party")] and'
            '     .//td[contains(.,"{}")]'
            ']'.format(basic_individual['name']))

        # Test case #D6
        detach_button = row.find_element_by_tag_name('button')
        self.scroll_element_into_view(detach_button)
        detach_button.click()
        try:
            self.wd.BY_XPATH(
                '//tr['
                '     .//td[contains(.,"Party")] and'
                '     .//td[contains(.,"{}")]'
                ']'.format(basic_individual['name']))
            raise AssertionError('Resource is still attached to party')
        except NoSuchElementException:
            pass
        self.open(self.prj_dashboard_path + 'records/parties/{}/'.format(
            basic_individual['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Resources"]').click()
        try:
            # Party has no resources, so it is indeed detached
            self.wd.BY_XPATH(
                '//*[@id="resources"]//*[contains(.,'
                '"This party does not have any attached resources.")]')
        except NoSuchElementException:
            # Party has other resources, so let's search for our resource
            # DataTables Table 0 is tenure relationships; Table 1 is resources
            self.do_table_search(
                resource['name'], filter_id='DataTables_Table_1_filter')
            self.wd.BY_XPATH(
                '//*[@id="DataTables_Table_1"]'
                '//*[normalize-space()="No matching records found"]')

        # Test case #A6
        self.open(self.prj_dashboard_path + 'records/parties/{}/'.format(
            basic_individual['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Resources"]').click()
        self.wd.BY_LINK('Attach').click()
        self.do_table_search(
            resource['name'], filter_id='DataTables_Table_0_filter')
        self.wd.BY_XPATH('//tr[contains(.,"{}")]'.format(filename)).click()
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()
        # DataTables Table 0 is tenure relationships; Table 1 is resources
        self.do_table_search(
            resource['name'], filter_id='DataTables_Table_1_filter')
        row = self.wd.BY_XPATH('//tr[contains(.,"{}")]'.format(filename))
        row.find_element_by_xpath('.//button[contains(.,"Detach")]')
        row.click()
        self.wd.BY_XPATH(
            '//tr['
            '     .//td[contains(.,"Party")] and'
            '     .//td[contains(.,"{}")]'
            ']'.format(basic_individual['name']))

        # Test case #D5
        self.open(self.prj_dashboard_path + 'records/parties/{}/'.format(
            basic_individual['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Resources"]').click()
        # DataTables Table 0 is tenure relationships; Table 1 is resources
        self.do_table_search(
            resource['name'], filter_id='DataTables_Table_1_filter')
        self.wd.BY_XPATH(
            '//tr[contains(.,"{}")]'
            '//button[contains(.,"Detach")]'.format(filename)).click()
        try:
            # Party has no resources, so it is indeed detached
            self.wd.BY_XPATH(
                '//*[@id="resources"]//*[contains(.,'
                '"This party does not have any attached resources.")]')
        except NoSuchElementException:
            # Party has other resources, so let's search for our resource
            # DataTables Table 0 is tenure relationships; Table 1 is resources
            self.do_table_search(
                resource['name'], filter_id='DataTables_Table_1_filter')
            self.wd.BY_XPATH(
                '//*[@id="DataTables_Table_1"]'
                '//*[normalize-space()="No matching records found"]')
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Resources"]').click()
        self.do_table_search(resource['name'])
        self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(filename)).click()
        try:
            self.wd.BY_XPATH(
                '//tr['
                '     .//td[contains(.,"Party")] and'
                '     .//td[contains(.,"{}")]'
                ']'.format(basic_individual['name']))
            raise AssertionError('Resource is still attached to party')
        except NoSuchElementException:
            pass

        # [REVERSION]
        self.delete_resource(resource)

    @pytest.mark.uploads
    def test_resource_can_be_attached_to_and_deattached_from_tenure_rel(
        self, records_org_prj, basic_water_rights, data_collector
    ):
        """Verifies Resources test cases #A7, #A8, #D7, #D8."""

        filename = 'user_avatar_1.jpg'
        resource = self.get_test_resource_data(filename)
        self.log_in(data_collector)

        # Test case #A7
        self.open(self.prj_dashboard_path + 'relationships/{}/'.format(
            basic_water_rights['pk']))
        self.wd.BY_LINK('Attach').click()
        try:
            self.wd.BY_LINK('Upload new').click()
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH('//input[@type="file"]').send_keys(resource['path'])
        self.wd.wait_until_clickable((By.CLASS_NAME, 'file-remove'))
        self.update_form_field('name', resource['name'])
        self.update_form_field('description', resource['description'])
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()
        (expected_min_date, expected_max_date) = self.get_min_max_date()
        self.do_table_search(
            resource['name'], filter_id='DataTables_Table_0_filter')
        row = self.wd.BY_XPATH('//tr[contains(.,"{}")]'.format(filename))
        row_febx = row.find_element_by_xpath
        row_febx('.//*[contains(.,"{}")]'.format(resource['name']))
        row_febx('.//button[contains(.,"Detach")]')
        row.click()

        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(resource['name']))
        self.wd.BY_XPATH(
            '//p[contains(.,"{}")]'.format(resource['description']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(filename))
        self.wd.BY_XPATH('//td[contains(.,"{}") or contains(.,"{}")]'.format(
            expected_min_date, expected_max_date))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(
            data_collector['full_name']))
        row = self.wd.BY_XPATH(
            '//tr['
            '     .//td[contains(.,"Relationship")] and'
            '     .//td[contains(.,"<{}> {} <{}>")]'
            ']'.format(
                basic_water_rights['party']['name'],
                basic_water_rights['tenure_type'],
                basic_water_rights['location']['type_label']))

        # Test case #D8
        detach_button = row.find_element_by_tag_name('button')
        self.scroll_element_into_view(detach_button)
        detach_button.click()
        try:
            self.wd.BY_XPATH(
                '//tr['
                '     .//td[contains(.,"Relationship")] and'
                '     .//td[contains(.,"<{}> {} <{}>")]'
                ']'.format(
                    basic_water_rights['party']['name'],
                    basic_water_rights['tenure_type'],
                    basic_water_rights['location']['type_label']))
            raise AssertionError('Resource is still attached to relationship')
        except NoSuchElementException:
            pass
        self.open(self.prj_dashboard_path + 'relationships/{}/'.format(
            basic_water_rights['pk']))
        try:
            # Relationship has no resources, so it is indeed detached
            self.wd.BY_XPATH(
                '//p[contains(.,'
                '"This relationship does not have any attached resources.")]')
        except NoSuchElementException:
            # Relationship has other resources, so let's search for our
            # resource
            self.do_table_search(
                resource['name'], filter_id='DataTables_Table_0_filter')
            self.wd.BY_XPATH(
                '//*[@id="DataTables_Table_0"]'
                '//*[normalize-space()="No matching records found"]')

        # Test case #A8
        self.open(self.prj_dashboard_path + 'relationships/{}/'.format(
            basic_water_rights['pk']))
        self.wd.BY_LINK('Attach').click()
        self.do_table_search(
            resource['name'], filter_id='DataTables_Table_0_filter')
        self.wd.BY_XPATH('//tr[contains(.,"{}")]'.format(filename)).click()
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()
        self.do_table_search(
            resource['name'], filter_id='DataTables_Table_0_filter')
        row = self.wd.BY_XPATH('//tr[contains(.,"{}")]'.format(filename))
        row.find_element_by_xpath('.//button[contains(.,"Detach")]')
        row.click()
        self.wd.BY_XPATH(
            '//tr['
            '     .//td[contains(.,"Relationship")] and'
            '     .//td[contains(.,"<{}> {} <{}>")]'
            ']'.format(
                basic_water_rights['party']['name'],
                basic_water_rights['tenure_type'],
                basic_water_rights['location']['type_label']))

        # Test case #D7
        self.open(self.prj_dashboard_path + 'relationships/{}/'.format(
            basic_water_rights['pk']))
        self.do_table_search(
            resource['name'], filter_id='DataTables_Table_0_filter')
        self.wd.BY_XPATH(
            '//tr[contains(.,"{}")]'
            '//button[contains(.,"Detach")]'.format(filename)).click()
        try:
            # Relationship has no resources, so it is indeed detached
            self.wd.BY_XPATH(
                '//p[contains(.,'
                '"This relationship does not have any attached resources.")]')
        except NoSuchElementException:
            # Relationship has other resources, so let's search for our
            # resource
            self.do_table_search(
                resource['name'], filter_id='DataTables_Table_0_filter')
            self.wd.BY_XPATH(
                '//*[@id="DataTables_Table_0"]'
                '//*[normalize-space()="No matching records found"]')
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Resources"]').click()
        self.do_table_search(resource['name'])
        self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(filename)).click()
        try:
            self.wd.BY_XPATH(
                '//tr['
                '     .//td[contains(.,"Relationship")] and'
                '     .//td[contains(.,"<{}> {} <{}>")]'
                ']'.format(
                    basic_water_rights['party']['name'],
                    basic_water_rights['tenure_type'],
                    basic_water_rights['location']['type_label']))
            raise AssertionError('Resource is still attached to relationship')
        except NoSuchElementException:
            pass

        # [REVERSION]
        self.delete_resource(resource)

    def test_file_is_required(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A9."""

        filename = 'user_avatar_1.jpg'
        resource = self.get_test_resource_data(filename)
        self.log_in(data_collector)

        self.open(self.prj_dashboard_path + 'resources/')
        self.wd.BY_LINK('Attach').click()
        try:
            self.wd.BY_LINK('Upload new').click()
        except NoSuchElementException:
            pass
        self.update_form_field('name', resource['name'])
        self.update_form_field('description', resource['description'])
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()
        self.wd.wait_for_xpath(
            '//*[contains(@class, "form-group") and '
            '    contains(@class, "has-error") and '
            '    .//*[@type="file"] and '
            '    .//*[normalize-space()="This field is required."]]')

    @pytest.mark.uploads
    def test_name_is_required(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A10."""

        filename = 'user_avatar_1.jpg'
        resource = self.get_test_resource_data(filename)
        self.log_in(data_collector)

        self.open(self.prj_dashboard_path + 'resources/')
        self.wd.BY_LINK('Attach').click()
        try:
            self.wd.BY_LINK('Upload new').click()
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH('//input[@type="file"]').send_keys(resource['path'])
        self.wd.wait_until_clickable((By.CLASS_NAME, 'file-remove'))
        self.update_form_field('name', '')
        self.update_form_field('description', resource['description'])
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()
        self.assert_form_field_has_error('name', 'This field is required.')

    @pytest.mark.uploads
    def test_description_is_not_required(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A12."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'user_avatar_1.jpg', has_description=False)

    @pytest.mark.uploads
    def test_csv_file_can_be_uploaded(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A13."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'csv_file.csv')

    @pytest.mark.uploads
    def test_doc_file_can_be_uploaded(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A14."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'doc_file.doc')

    @pytest.mark.uploads
    def test_docx_file_can_be_uploaded(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A15."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'docx_file.docx')

    @pytest.mark.uploads
    def test_gif_file_can_be_uploaded(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A28."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'gif_file.gif')

    @pytest.mark.uploads
    def test_gpx_file_can_be_uploaded(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A16."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'gpx_file.gpx')

    @pytest.mark.uploads
    def test_jpeg_file_can_be_uploaded(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A17."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'jpeg_file.jpg')

    @pytest.mark.uploads
    def test_mp3_file_can_be_uploaded(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A18."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'mp3_file.mp3')

    @pytest.mark.uploads
    def test_mp4_file_can_be_uploaded(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A19."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'mp4_file.mp4')

    @pytest.mark.uploads
    def test_ods_file_can_be_uploaded(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A29."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'ods_file.ods')

    @pytest.mark.uploads
    def test_odt_file_can_be_uploaded(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A30."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'odt_file.odt')

    @pytest.mark.uploads
    def test_pdf_file_can_be_uploaded(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A20."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'pdf_file.pdf')

    @pytest.mark.uploads
    def test_png_file_can_be_uploaded(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A21."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'png_file.png')

    @pytest.mark.uploads
    def test_tiff_file_can_be_uploaded(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A22."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'tiff_file.tif')

    @pytest.mark.uploads
    def test_xml_file_can_be_uploaded(self, basic_org_prj, data_collector):
        """Verifies Resources test case #A23."""

        self.log_in(data_collector)
        self.attach_resource_to_project_and_verify(
            data_collector, 'xml_file.xml')

    @pytest.mark.uploads
    def test_file_with_no_extension_cannot_be_uploaded(
        self, basic_org_prj, data_collector
    ):
        """Verifies Resources test case #A24."""

        self.log_in(data_collector)
        resource = self.get_test_resource_data('no_ext_file')
        self.open(self.prj_dashboard_path + 'resources/')
        self.wd.BY_LINK('Attach').click()
        try:
            self.wd.BY_LINK('Upload new').click()
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH('//input[@type="file"]').send_keys(resource['path'])
        self.wd.wait_for_xpath(
            '//*[contains(@class, "file-well")]'
            '//*[normalize-space()="File type not allowed."]')

    @pytest.mark.uploads
    def test_file_with_nonacceptable_mime_type_cannot_be_uploaded(
        self, basic_org_prj, data_collector
    ):
        """Verifies Resources test case #A25."""

        self.log_in(data_collector)
        resource = self.get_test_resource_data('python_file.py')
        self.open(self.prj_dashboard_path + 'resources/')
        self.wd.BY_LINK('Attach').click()
        try:
            self.wd.BY_LINK('Upload new').click()
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH('//input[@type="file"]').send_keys(resource['path'])
        self.wd.wait_for_xpath(
            '//*[contains(@class, "file-well")]'
            '//*[normalize-space()="File type not allowed."]')

    @pytest.mark.uploads
    def test_multiple_existing_resources_from_different_pages_can_be_attached(
        self, records_org_prj, data_collector
    ):
        """Verifies Resources test case #A26."""

        self.log_in(data_collector)
        self.open(self.prj_dashboard_path + 'resources/')
        self.wd.BY_LINK('Attach').click()
        tr = self.wd.BY_XPATH('//*[@id="DataTables_Table_0"]//tbody//tr')
        name = re.search('FuncTest Dummy Resource [0-9]+', tr.text).group(0)
        attached_resource_names = [name]
        tr.click()
        self.wd.BY_XPATH('//*[@id="DataTables_Table_0_next"]//a').click()
        tr = self.wd.BY_XPATH('//*[@id="DataTables_Table_0"]//tbody//tr')
        name = re.search('FuncTest Dummy Resource [0-9]+', tr.text).group(0)
        attached_resource_names.append(name)
        tr.click()
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()
        for name in attached_resource_names:
            self.open(self.prj_dashboard_path + 'resources/')
            self.do_table_search(name)
            self.wd.wait_for_xpath(
                '//tr[contains(.,"{}") and '
                '     .//button[contains(.,"Detach")]]'.format(name)).click()
            self.wd.BY_XPATH('//tr[contains(.,"{}")]'.format(self.prj['name']))

        # [REVERSION]
        for name in attached_resource_names:
            self.open(self.prj_dashboard_path + 'resources/')
            self.do_table_search(name)
            self.wd.wait_for_xpath(
                '//tr[contains(.,"{}")]'.format(name)).click()
            row = self.wd.BY_XPATH(
                '//tr[contains(.,"{}")]'.format(self.prj['name']))
            detach_button = row.find_element_by_tag_name('button')
            self.scroll_element_into_view(detach_button)
            detach_button.click()

    @pytest.mark.uploads
    def test_large_resource_file_cannot_be_uploaded(
        self, basic_org_prj, data_collector
    ):
        """Verifies Resources test case #A31."""

        self.log_in(data_collector)
        resource = self.get_test_resource_data('very_large_file.tiff')
        self.open(self.prj_dashboard_path + 'resources/')
        self.wd.BY_LINK('Attach').click()
        try:
            self.wd.BY_LINK('Upload new').click()
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH('//input[@type="file"]').send_keys(resource['path'])
        self.wd.wait_for_xpath(
            '//*[contains(@class, "file-well")]'
            '//*[normalize-space()="Not able to upload file. The size of the '
            'file exceeds the maximum allowed size of 10MB."]')

    def test_project_user_cannot_attach_resource(
        self, basic_org_prj, prj_user
    ):
        """Verifies Resources test case #A27."""

        self.log_in(prj_user)
        self.open(self.prj_dashboard_path + 'resources/')
        try:
            self.wd.BY_LINK('Attach')
            raise AssertionError('Attach button is displayed')
        except NoSuchElementException:
            pass
        self.open(self.get_url_path() + 'add')
        self.wait_for_alert(
            "You don't have permission to add resources.")
