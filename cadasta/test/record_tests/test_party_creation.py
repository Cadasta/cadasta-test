import pytest

from selenium.common.exceptions import NoSuchElementException

from ..base_test import SeleniumTestCase
from ..util import random_string


@pytest.mark.batch3
class TestPartyCreation(SeleniumTestCase):

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

    def select_prj_add_menu_item(self, label):
        """Opens the project add menu and clicks the specified item."""
        self.wd.BY_CSS('.page-header .btn-group .dropdown-toggle').click()
        self.wd.BY_LINK(label).click()

    def click_save_button(self):
        button = self.wd.BY_XPATH(
            '//*[@type="submit" and normalize-space()="Save"]')
        self.scroll_element_into_view(button)
        button.click()

    # ------ Test cases ------

    def test_user_can_create_delete_party(self, basic_org_prj, data_collector):
        """Verifies Records test case #PC1, #PD1."""

        # Test case #PC1
        self.log_in(data_collector)
        self.open(self.prj_dashboard_path)
        self.select_prj_add_menu_item('Add party')
        name = 'FuncTest Tmp ' + random_string()
        self.update_form_field('name', name)
        self.update_form_field('type', 'IN')
        self.click_save_button()
        expected_path = self.prj_dashboard_path + 'records/parties/'
        assert self.get_url_path() == expected_path
        search_input = self.wd.BY_XPATH(
            '//*[@id="paginated-table-filter"]//input[@type="search"]')
        search_input.send_keys(name)
        self.wd.wait_for_xpath(
            '//*[@id="paginated-table"]//td[contains(.,"{}")]'.format(name))
        self.wd.wait_for_xpath(
            '//*[@id="paginated-table"]//td[contains(.,"Individual")]')
        self.wd.BY_LINK(name).click()
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH('//td[contains(.,"Individual")]')

        # [REVERSION] and test case #PD1
        self.wd.BY_CSS('[title="Delete party"]').click()
        self.wd.BY_XPATH(
            '//button[contains(., "Yes, delete this party")]').click()
        assert self.get_url_path() == expected_path
        search_input = self.wd.BY_XPATH(
            '//*[@id="paginated-table-filter"]//input[@type="search"]')
        search_input.send_keys(name)
        self.wd.BY_XPATH(
            '//*[@id="paginated-table"]'
            '//*[normalize-space()="No matching records found" or'
            '    normalize-space()="No data available in table"]')

    def test_user_can_create_update_party_with_custom_attributes(
        self, custom_attrs_org_prj, data_collector
    ):
        """Verifies Records test case #PC2, #PU2."""

        # Test case #PC2
        self.log_in(data_collector)
        self.open(self.prj_dashboard_path)
        self.select_prj_add_menu_item('Add party')
        name = 'FuncTest Tmp ' + random_string()
        self.update_form_field('name', name)
        self.update_form_field('type', 'IN')
        self.update_form_field('party::in::registration', '2017-11-13')
        self.click_save_button()
        expected_path = self.prj_dashboard_path + 'records/parties/'
        assert self.get_url_path() == expected_path
        search_input = self.wd.BY_XPATH(
            '//*[@id="paginated-table-filter"]//input[@type="search"]')
        search_input.send_keys(name)
        self.wd.BY_XPATH(
            '//*[@id="paginated-table"]//td[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH(
            '//*[@id="paginated-table"]//td[contains(.,"Individual")]')
        self.wd.BY_LINK(name).click()
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH('//td[contains(.,"Individual")]')
        self.wd.BY_XPATH('//td[contains(.,"2017-11-13")]')

        # Test case #PU2
        self.wd.BY_CSS('[title="Edit party"]').click()
        self.update_form_field('name', 'FuncTest Temp Name')
        self.update_form_field('type', 'GR')
        self.update_form_field('party::gr::registration', '2017-11-14')
        self.click_save_button()
        self.wd.BY_XPATH('//h2[contains(.,"FuncTest Temp Name")]')
        self.wd.BY_XPATH('//td[contains(.,"FuncTest Temp Name")]')
        self.wd.BY_XPATH('//td[contains(.,"Group")]')
        self.wd.BY_XPATH('//td[contains(.,"2017-11-14")]')

        # [REVERSION]
        self.wd.BY_CSS('[title="Delete party"]').click()
        self.wd.BY_XPATH(
            '//button[contains(., "Yes, delete this party")]').click()
        assert self.get_url_path() == expected_path

    def test_user_can_create_update_individual_with_conditional_attributes(
        self, conditional_attrs_org_prj, data_collector
    ):
        """Verifies Records test case #PC3, #PU3."""

        # Test case #PC3
        self.log_in(data_collector)
        self.open(self.prj_dashboard_path)
        self.select_prj_add_menu_item('Add party')
        name = 'FuncTest Tmp ' + random_string()
        self.update_form_field('type', 'IN')
        self.update_form_field('name', name)
        assert self.wd.BY_NAME('party::in::notes').is_displayed()
        assert self.wd.BY_NAME('party::in::birthdate').is_displayed()
        self.update_form_field('party::in::birthdate', '1990-06-30')
        self.click_save_button()
        expected_path = self.prj_dashboard_path + 'records/parties/'
        assert self.get_url_path() == expected_path
        search_input = self.wd.BY_XPATH(
            '//*[@id="paginated-table-filter"]//input[@type="search"]')
        search_input.send_keys(name)
        self.wd.BY_XPATH(
            '//*[@id="paginated-table"]//td[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH(
            '//*[@id="paginated-table"]//td[contains(.,"Individual")]')
        self.wd.BY_LINK(name).click()
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH('//td[contains(.,"Individual")]')
        self.wd.BY_XPATH('//td[contains(.,"1990-06-30")]')

        # Test case #PU3
        self.wd.BY_CSS('[title="Edit party"]').click()
        self.update_form_field('type', 'GR')
        self.update_form_field('name', 'FuncTest Temp Name')
        assert not self.wd.BY_NAME('party::in::notes').is_displayed()
        assert not self.wd.BY_NAME('party::in::birthdate').is_displayed()
        assert self.wd.BY_NAME('party::gr::notes').is_displayed()
        assert self.wd.BY_NAME('party::gr::number_of_members').is_displayed()
        self.update_form_field('party::gr::number_of_members', '12345')
        self.click_save_button()
        self.wd.BY_XPATH('//h2[contains(.,"FuncTest Temp Name")]')
        self.wd.BY_XPATH('//td[contains(.,"FuncTest Temp Name")]')
        self.wd.BY_XPATH('//td[contains(.,"Group")]')
        self.wd.BY_XPATH('//td[contains(.,"12345")]')

        # [REVERSION]
        self.wd.BY_CSS('[title="Delete party"]').click()
        self.wd.BY_XPATH(
            '//button[contains(., "Yes, delete this party")]').click()
        assert self.get_url_path() == expected_path

    def test_user_can_create_corporation_with_conditional_attributes(
        self, conditional_attrs_org_prj, data_collector
    ):
        """Verifies Records test case #PC4."""

        self.log_in(data_collector)
        self.open(self.prj_dashboard_path)
        self.select_prj_add_menu_item('Add party')
        name = 'FuncTest Tmp ' + random_string()
        self.update_form_field('type', 'CO')
        self.update_form_field('name', name)
        assert self.wd.BY_NAME('party::co::notes').is_displayed()
        assert self.wd.BY_NAME('party::co::registration').is_displayed()
        self.update_form_field('party::co::registration', '2010-06-30')
        self.click_save_button()
        expected_path = self.prj_dashboard_path + 'records/parties/'
        assert self.get_url_path() == expected_path
        search_input = self.wd.BY_XPATH(
            '//*[@id="paginated-table-filter"]//input[@type="search"]')
        search_input.send_keys(name)
        self.wd.BY_XPATH(
            '//*[@id="paginated-table"]//td[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH(
            '//*[@id="paginated-table"]//td[contains(.,"Corporation")]')
        self.wd.BY_LINK(name).click()
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH('//td[contains(.,"Corporation")]')
        self.wd.BY_XPATH('//td[contains(.,"2010-06-30")]')

        # [REVERSION]
        self.wd.BY_CSS('[title="Delete party"]').click()
        self.wd.BY_XPATH(
            '//button[contains(., "Yes, delete this party")]').click()
        assert self.get_url_path() == expected_path

    def test_user_can_create_group_with_conditional_attributes(
        self, conditional_attrs_org_prj, data_collector
    ):
        """Verifies Records test case #PC5."""

        self.log_in(data_collector)
        self.open(self.prj_dashboard_path)
        self.select_prj_add_menu_item('Add party')
        name = 'FuncTest Tmp ' + random_string()
        self.update_form_field('type', 'GR')
        self.update_form_field('name', name)
        assert self.wd.BY_NAME('party::gr::notes').is_displayed()
        assert self.wd.BY_NAME('party::gr::number_of_members').is_displayed()
        self.update_form_field('party::gr::number_of_members', '54321')
        self.click_save_button()
        expected_path = self.prj_dashboard_path + 'records/parties/'
        assert self.get_url_path() == expected_path
        search_input = self.wd.BY_XPATH(
            '//*[@id="paginated-table-filter"]//input[@type="search"]')
        search_input.send_keys(name)
        self.wd.BY_XPATH(
            '//*[@id="paginated-table"]//td[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH(
            '//*[@id="paginated-table"]//td[contains(.,"Group")]')
        self.wd.BY_LINK(name).click()
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH('//td[contains(.,"Group")]')
        self.wd.BY_XPATH('//td[contains(.,"54321")]')

        # [REVERSION]
        self.wd.BY_CSS('[title="Delete party"]').click()
        self.wd.BY_XPATH(
            '//button[contains(., "Yes, delete this party")]').click()
        assert self.get_url_path() == expected_path

    def test_name_is_required(self, basic_org_prj, data_collector):
        """Verifies Records test case #PC6."""

        self.log_in(data_collector)
        self.open(self.prj_dashboard_path)
        self.select_prj_add_menu_item('Add party')
        self.update_form_field('type', 'IN')
        self.click_save_button()
        self.assert_form_field_has_error('name', 'This field is required.')

    def test_party_type_is_required(self, basic_org_prj, data_collector):
        """Verifies Records test case #PC7."""

        self.log_in(data_collector)
        self.open(self.prj_dashboard_path)
        self.select_prj_add_menu_item('Add party')
        self.update_form_field('name', 'Party name')
        self.click_save_button()
        self.assert_form_field_has_error('type', 'This field is required.')

    def test_unauthorized_user_cannot_create_party(
        self, basic_org_prj, prj_user
    ):
        """Verifies Records test case #PC8."""

        self.log_in(prj_user)
        self.open(self.prj_dashboard_path)
        try:
            self.wd.BY_CSS('.page-header .btn-group').find_element_by_xpath(
                '//*[normalize-space()="Add location"]')
            self.wd.BY_CSS('.page-header .btn-group .dropdown-toggle')
            raise AssertionError('Project add location/menu is present')
        except NoSuchElementException:
            pass
        self.wd.BY_XPATH(
            '//*[@id="sidebar"]//a[normalize-space()="Parties"]').click()
        self.open(self.get_url_path() + 'new')
        self.wait_for_alert(
            "You don't have permission to add parties to this project.")
