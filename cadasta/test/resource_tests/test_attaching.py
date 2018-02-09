import pytest
import re
import time

from datetime import date, timedelta
from os.path import abspath, dirname, join
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException)
from selenium.webdriver.common.by import By

from ..base_test import SeleniumTestCase
from ..util import random_string


@pytest.mark.batch3
class TestAttaching(SeleniumTestCase):

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

    def get_test_resource_data(self, filename):
        dir_path = join(dirname(dirname(abspath(__file__))), 'files')
        return {
            'path': join(dir_path, filename),
            'name': 'File ' + random_string(),
            'prefill': re.split('\.', re.sub('_', ' ', filename))[0],
            'description': random_string(),
            'type': re.split('\.', filename)[-1],
        }

    def attach_resource_to_project_and_verify(
        self, user, filename, has_description=True, delete_after=True
    ):
        time.sleep(5)
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
        row_febx('//*[contains(.,"{}")]'.format(resource['name']))
        row_febx('//*[contains(.,"{}")]'.format(resource['type']))
        row_febx('//*[contains(.,"{}")]'.format(user['username']))
        row_febx('//*[contains(.,"{}")]'.format(user['full_name']))
        row_febx('//*[contains(.,"{}") or contains(.,"{}")]'.format(
            expected_min_date, expected_max_date))
        row_febx('//button[contains(.,"Detach")]')
        row.click()

        self.wd.wait_for_xpath(
            '//h2[contains(.,"{}")]'.format(resource['name']))
        if has_description:
            self.wd.BY_XPATH(
                '//p[contains(.,"{}")]'.format(resource['description']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(filename))
        self.wd.BY_XPATH('//td[contains(.,"{}") or contains(.,"{}")]'.format(
            expected_min_date.replace(' ', '. ', 1),
            expected_max_date.replace(' ', '. ', 1)))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(user['full_name']))
        row = self.wd.BY_XPATH(
            '//tr[contains(.,"{}")]'.format(self.prj['name']))

        # [REVERSION]
        self.wd.BY_CSS('[title="Delete resource"]').click()
        self.wd.BY_LINK('Yes, delete this resource').click()
        assert self.get_url_path() == self.prj_dashboard_path + 'resources/'

    def do_table_search(self, query, filter_id='paginated-table-filter'):
        search_input = self.wd.BY_XPATH(
            '//*[@id="{}"]//input[@type="search"]'.format(filter_id))
        search_input.send_keys(query)

    def get_min_max_date(self):
        max_date = date.today()
        min_date = max_date + timedelta(days=-1)
        max_date = max_date.strftime('%b %-d, %Y')
        min_date = min_date.strftime('%b %-d, %Y')
        return (min_date, max_date)

    # ------ Test cases ------

    @pytest.mark.uploads
    def test_resource_can_be_attached_to_and_deattached_from_project(
        self, basic_org_prj, data_collector
    ):
        """Verifies Resources test cases #A1, #A2, #A11, #D1, #D2, #X1."""

        filename = 'user_avatar_1.jpg'
        resource = self.get_test_resource_data(filename)

        # Test case #A1
        self.log_in(data_collector)
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
        row = self.wd.wait_for_xpath('//tr[contains(.,"{}")]'.format(filename))
        row_febx = row.find_element_by_xpath
        row_febx('//*[contains(.,"{}")]'.format(resource['name']))
        row_febx('//*[contains(.,"{}")]'.format(resource['type']))
        row_febx('//*[contains(.,"{}")]'.format(data_collector['username']))
        row_febx('//*[contains(.,"{}")]'.format(data_collector['full_name']))
        row_febx('//*[contains(.,"{}") or contains(.,"{}")]'.format(
            expected_min_date, expected_max_date))
        row_febx('//button[contains(.,"Detach")]')
        row.click()

        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(resource['name']))
        self.wd.BY_XPATH(
            '//p[contains(.,"{}")]'.format(resource['description']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(filename))
        self.wd.BY_XPATH('//td[contains(.,"{}") or contains(.,"{}")]'.format(
            expected_min_date.replace(' ', '. ', 1),
            expected_max_date.replace(' ', '. ', 1)))
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
        row = self.wd.wait_for_xpath('//tr[contains(.,"{}")]'.format(filename))
        try:
            row.find_element_by_xpath(
                '//button[contains(.,"Detach")]')
            raise AssertionError('Resource is still attached to project')
        except NoSuchElementException:
            pass

        # Test case #A2
        self.wd.BY_LINK('Attach').click()
        self.do_table_search(resource['name'])
        self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(filename)).click()
        self.wd.BY_XPATH(
            '//button[@type="submit" and contains(.,"Save")]').click()
        self.do_table_search(resource['name'])
        row = self.wd.wait_for_xpath('//tr[contains(.,"{}")]'.format(filename))
        row.find_element_by_xpath(
            '//button[contains(.,"Detach")]')
        row.click()
        self.wd.BY_XPATH('//tr[contains(.,"{}")]'.format(self.prj['name']))

        # Test case #D1
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Resources"]').click()
        self.do_table_search(resource['name'])
        self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'
            '//button[contains(.,"Detach")]'.format(filename)).click()
        self.do_table_search(resource['name'])
        row = self.wd.wait_for_xpath('//tr[contains(.,"{}")]'.format(filename))
        try:
            row.find_element_by_xpath('//button[contains(.,"Detach")]')
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
        self.wd.BY_CSS('[title="Delete resource"]').click()
        self.wd.BY_LINK('Yes, delete this resource').click()
        assert self.get_url_path() == self.prj_dashboard_path + 'resources/'
        self.do_table_search(resource['name'])
        self.wd.wait_for_xpath(
            '//*[@id="paginated-table"]'
            '//*[normalize-space()="No matching records found" or'
            '    normalize-space()="No data available in table"]')

    @pytest.mark.uploads
    def test_resource_can_be_attached_to_and_deattached_from_party(
        self, records_org_prj, basic_individual, data_collector
    ):
        """Verifies Resources test cases #A5, #A6, #D5, #D6."""

        filename = 'user_avatar_2.png'
        resource = self.get_test_resource_data(filename)

        # Test case #A5
        self.log_in(data_collector)
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
        expected_min_date = expected_min_date.replace(' ', '. ', 1)
        expected_max_date = expected_max_date.replace(' ', '. ', 1)
        # DataTables Table 0 is tenure relationships; Table 1 is resources
        self.do_table_search(
            resource['name'], filter_id='DataTables_Table_1_filter')
        row = self.wd.BY_XPATH('//tr[contains(.,"{}")]'.format(filename))
        row_febx = row.find_element_by_xpath
        row_febx('//*[contains(.,"{}")]'.format(resource['name']))
        row_febx('//*[contains(.,"{}")]'.format(resource['type']))
        row_febx('//*[contains(.,"{}")]'.format(data_collector['username']))
        row_febx('//*[contains(.,"{}")]'.format(data_collector['full_name']))
        row_febx('//*[contains(.,"{}") or contains(.,"{}")]'.format(
            expected_min_date, expected_max_date))
        row_febx('//button[contains(.,"Detach")]')
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
            '//tr[contains(.,"{}")]'.format(basic_individual['name']))

        # Test case #D6
        detach_button = row.find_element_by_tag_name('button')
        self.scroll_element_into_view(detach_button)
        detach_button.click()
        try:
            self.wd.BY_XPATH(
                '//tr[contains(.,"{}")]'.format(basic_individual['name']))
            raise AssertionError('Resource is still attached to party')
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Resources"]').click()
        self.do_table_search(resource['name'])
        self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(filename)).click()
        try:
            row = self.wd.BY_XPATH(
                '//tr[contains(.,"{}")]'.format(basic_individual['name']))
            raise AssertionError('Resource is still attached to party')
        except NoSuchElementException:
            pass

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
        row.find_element_by_xpath(
            '//button[contains(.,"Detach")]')
        row.click()
        self.wd.BY_XPATH(
            '//tr[contains(.,"{}")]'.format(basic_individual['name']))

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
            self.do_table_search(resource['name'])
        except NoSuchElementException:
            pass
        try:
            self.wd.wait_for_xpath('//tr[contains(.,"{}")]'.format(filename))
            raise AssertionError('Resource is still attached to party')
        except TimeoutException:
            pass
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Resources"]').click()
        self.do_table_search(resource['name'])
        self.wd.wait_for_xpath(
            '//tr[contains(.,"{}")]'.format(filename)).click()
        try:
            self.wd.BY_XPATH(
                '//tr[contains(.,"{}")]'.format(basic_individual['name']))
            raise AssertionError('Resource is still attached to party')
        except NoSuchElementException:
            pass

        # [REVERSION]
        self.wd.BY_CSS('[title="Delete resource"]').click()
        self.wd.BY_LINK('Yes, delete this resource').click()
        assert self.get_url_path() == self.prj_dashboard_path + 'resources/'

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
