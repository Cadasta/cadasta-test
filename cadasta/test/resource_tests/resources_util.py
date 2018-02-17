import re

from datetime import date, timedelta
from os.path import abspath, dirname, join

from ..base_test import SeleniumTestCase
from ..util import random_string


class ResourcesUtil(SeleniumTestCase):

    def get_test_resource_data(self, filename):
        dir_path = join(dirname(dirname(abspath(__file__))), 'files')
        return {
            'filename': filename,
            'path': join(dir_path, filename),
            'name': 'File ' + random_string(),
            'prefill': re.split('\.', re.sub('_', ' ', filename))[0],
            'description': random_string(),
            'type': re.split('\.', filename)[-1],
        }

    def do_table_search(self, query, filter_id='paginated-table-filter'):
        search_input = self.wd.BY_XPATH(
            '//*[@id="{}"]//input[@type="search"]'.format(filter_id))
        search_input.clear()
        search_input.send_keys(query)

    def get_min_max_date(self):
        max_date = date.today()
        min_date = max_date + timedelta(days=-1)
        max_date = max_date.strftime('%b %-d, %Y')
        min_date = min_date.strftime('%b %-d, %Y')
        return (min_date, max_date)

    def delete_resource(self, resource, is_on_resource_page=True):
        if not is_on_resource_page:
            self.open(self.prj_dashboard_path + 'resources/')
            self.do_table_search(resource['name'])
            self.wd.wait_for_xpath(
                '//tr[contains(.,"{}")]'.format(resource['filename'])).click()
        self.wd.BY_CSS('[title="Delete resource"]').click()
        self.wd.BY_LINK('Yes, delete this resource').click()
        assert self.get_url_path() == self.prj_dashboard_path + 'resources/'
