import pytest
import re

from selenium.common.exceptions import (NoSuchElementException,
                                        ElementNotInteractableException,
                                        ElementNotVisibleException)
from selenium.webdriver.common.by import By

from ..base_test import SeleniumTestCase
from ..util import random_string


@pytest.mark.batch3
class TestTenureRelationshipCreation(SeleniumTestCase):

    @pytest.fixture
    def records_org_prj(self, basic_org, records_prj):
        self.org = basic_org
        self.prj = records_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], records_prj['slug'])

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

    @pytest.fixture
    def custom_party_attrs_org_prj(self, basic_org, custom_party_attrs_prj):
        self.org = basic_org
        self.prj = custom_party_attrs_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], custom_party_attrs_prj['slug'])

    @pytest.fixture
    def custom_tenure_attrs_org_prj(self, basic_org, custom_tenure_attrs_prj):
        self.org = basic_org
        self.prj = custom_tenure_attrs_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], custom_tenure_attrs_prj['slug'])

    @pytest.fixture
    def custom_conditional_attrs_org_prj(
        self, basic_org, custom_conditional_attrs_prj
    ):
        self.org = basic_org
        self.prj = custom_conditional_attrs_prj
        self.prj_dashboard_path = '/organizations/{}/projects/{}/'.format(
            basic_org['slug'], custom_conditional_attrs_prj['slug'])

    # ------ Utility functions ------

    def click_save_button(self):
        button = self.wd.BY_XPATH(
            '//*[@type="submit" and normalize-space()="Save"]')
        self.scroll_element_into_view(button)
        button.click()

    def go_to_add_tenure_relationship_form(self, location):
        """Goes to the add tenure relationship form given the location."""
        self.open(self.prj_dashboard_path + 'records/locations/{}/'.format(
            location['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Relationships"]').click()
        try:
            # Has existing relationships
            div = self.wd.BY_XPATH('//*[@id="relationships" and .//table]')
            div.find_element_by_link_text('Add').click()
        except NoSuchElementException:
            # Has no relationships yet
            self.wd.BY_LINK('Add relationship').click()

    def verify_tenure_relationship_details(
        self, rel, tenure_type_field_label="Type", other_fields={}
    ):
        """Verifies that the tenure relationship is created by verifying its
        details right after it is created then returns its ID. The details are
        checked on the tenure relationships table on the "Relationships" tab of
        the location page, and in the tenure relationship page itself. Also
        returns the ID of the relationship."""

        # Check tenure relationships table
        row = self.wd.BY_XPATH(
            '//tr['
            '    .//td[contains(.,"{}")] and '
            '    .//td[contains(.,"{}")]'
            ']'.format(rel['type_label'], rel['party']['name']))

        # Check tenure relationship page
        row.find_element_by_link_text(rel['type_label']).click()
        self.wd.BY_XPATH(
            '//tr['
            '    .//td[contains(.,"{}")] and '
            '    .//td[contains(.,"{}")]'
            ']'.format(tenure_type_field_label, rel['type_label']))
        self.wd.BY_XPATH(
            '//tr['
            '    .//td[contains(.,"Party")] and '
            '    .//td//a[contains(.,"{}")]'
            ']'.format(rel['party']['name']))
        for field_name, field_label in other_fields.items():
            self.wd.BY_XPATH(
                '//tr['
                '    .//td[contains(.,"{}")] and '
                '    .//td[contains(.,"{}")]'
                ']'.format(field_label, str(rel[field_name])))

        regex = self.prj_dashboard_path + 'relationships/([a-z0-9]{24})/'
        m = re.fullmatch(regex, self.get_url_path())
        assert m
        return m.group(1)

    def delete_location(self, location):
        """Goes to the given location's page and then deletes the location."""
        self.open(self.prj_dashboard_path + 'records/locations/{}/'.format(
            location['pk']))
        self.wd.wait_until_gone((By.ID, 'loading'))
        self.wd.BY_CSS('[title="Delete location"]').click()
        self.wd.BY_XPATH(
            '//button[contains(., "Yes, delete this location")]').click()
        expected_path = self.prj_dashboard_path + 'records/locations/'
        assert self.get_url_path() == expected_path

    def delete_party(self, party):
        """Goes to the given party's page and then deletes the party."""
        self.open(self.prj_dashboard_path + 'records/parties/{}/'.format(
            party['pk']))
        self.wd.BY_CSS('[title="Delete party"]').click()
        self.wd.BY_XPATH(
            '//button[contains(., "Yes, delete this party")]').click()
        expected_path = self.prj_dashboard_path + 'records/parties/'
        assert self.get_url_path() == expected_path

    def delete_tenure_relationship(self):
        """Deletes the tenure relationship while on its page."""
        self.wd.BY_CSS('[title="Delete relationship"]').click()
        self.wd.BY_XPATH(
            '//button[contains(., "Yes, delete this relationship")]').click()
        assert (
            self.get_url_path() ==
            self.prj_dashboard_path + 'records/locations/'
        )

    def verify_tenure_relationship_is_deleted(self, rel, via='location'):
        """Verifies that the given tenure relationship is gone by looking at
        the relationships table of its still-existing location or party."""

        assert via in ('location', 'party')

        self.open(self.prj_dashboard_path + 'records/{}/{}/'.format(
            'locations' if via == 'location' else 'parties', rel[via]['pk']))
        self.wd.BY_XPATH(
            '//a[@role="tab" and normalize-space()="Relationships"]').click()
        try:
            # Location/party has no relationships, so it is indeed deleted
            if via == 'location':
                self.wd.BY_LINK('Add relationship')
            else:
                self.wd.BY_XPATH(
                    '//*[normalize-space()="This party does not have any '
                    'relationships and is not connected to any locations."]')
        except NoSuchElementException:
            # Location/party has other relationships, so let's search for our
            # particular relationship
            search_input = self.wd.BY_XPATH(
                '//*[@id="DataTables_Table_0_filter"]//input[@type="search"]')
            if via == 'location':
                extra_search_term = rel['party']['name']
            else:
                extra_search_term = rel['location']['type_label']
            search_input.send_keys(rel['type_label'] + ' ' + extra_search_term)
            self.wd.BY_XPATH(
                '//*[@id="DataTables_Table_0"]'
                '//*[normalize-space()="No matching records found"]')

    # ------ Test cases ------

    def test_user_can_create_delete_relationship_with_existing_party(
        self, records_org_prj, basic_parcel, basic_individual, data_collector
    ):
        """Verifies Records test case #RC1, #RD1."""

        temp_rel = {
            'location': basic_parcel,
            'party': basic_individual,
            'type': 'CR',
            'type_label': 'Carbon Rights',
        }
        self.log_in(data_collector)

        # Test case #RC1
        self.go_to_add_tenure_relationship_form(basic_parcel)
        self.wd.BY_ID('select2-party-select-container').click()
        self.wd.BY_XPATH(
            '//*[contains(@id,"select2-party-select-result-") and '
            '    contains(@id,"-{}")]'.format(basic_individual['pk'])).click()
        assert (
            self.wd.BY_ID('select2-party-select-container').text ==
            basic_individual['name']
        )
        self.update_form_field('tenure_type', temp_rel['type'])
        self.click_save_button()
        self.verify_tenure_relationship_details(temp_rel)

        # [REVERSION] and test case #RD1
        self.delete_tenure_relationship()
        self.verify_tenure_relationship_is_deleted(temp_rel)

    def test_user_can_create_relationship_with_new_party(
        self, records_org_prj, basic_parcel, data_collector
    ):
        """Verifies Records test case #RC2, #PD3."""

        temp_party = {
            'name': 'FuncTest Tmp ' + random_string(),
            'type': 'CO',
        }
        temp_rel = {
            'location': basic_parcel,
            'party': temp_party,
            'type': 'CO',
            'type_label': 'Concessionary Rights',
        }
        self.log_in(data_collector)

        # Test case #RC2
        self.go_to_add_tenure_relationship_form(basic_parcel)
        self.wd.BY_ID('add-party').click()
        self.update_form_field('name', temp_party['name'])
        self.update_form_field('party_type', temp_party['type'])
        self.update_form_field('tenure_type', temp_rel['type'])
        self.click_save_button()
        self.verify_tenure_relationship_details(temp_rel)
        self.wd.BY_LINK(temp_party['name']).click()
        regex = self.prj_dashboard_path + 'records/parties/([a-z0-9]{24})/'
        m = re.fullmatch(regex, self.get_url_path())
        assert m
        temp_party['pk'] = m.group(1)
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"Corporation")]')

        # [REVERSION] and test case #PD3
        self.delete_party(temp_party)
        self.verify_tenure_relationship_is_deleted(temp_rel)

    def test_user_can_create_relationship_with_new_custom_party(
        self, custom_party_attrs_org_prj, basic_rightofway, data_collector
    ):
        """Verifies Records test case #RC3."""

        temp_party = {
            'name': 'FuncTest Tmp ' + random_string(),
            'type': 'GR',
            'registration': '2001-02-03'
        }
        temp_rel = {
            'location': basic_rightofway,
            'party': temp_party,
            'type': 'CU',
            'type_label': 'Customary Rights',
        }
        self.log_in(data_collector)

        self.go_to_add_tenure_relationship_form(basic_rightofway)
        try:
            self.wd.BY_ID('add-party').click()
        except (ElementNotInteractableException, ElementNotVisibleException):
            pass
        self.update_form_field('name', temp_party['name'])
        self.update_form_field('party_type', temp_party['type'])
        assert self.wd.BY_NAME('party::gr::registration').is_displayed()
        self.update_form_field(
            'party::gr::registration', temp_party['registration'])
        self.update_form_field('tenure_type', temp_rel['type'])
        self.click_save_button()
        self.verify_tenure_relationship_details(
            temp_rel, tenure_type_field_label="Relationship type")
        self.wd.BY_LINK(temp_party['name']).click()
        regex = self.prj_dashboard_path + 'records/parties/([a-z0-9]{24})/'
        m = re.fullmatch(regex, self.get_url_path())
        assert m
        temp_party['pk'] = m.group(1)
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(
            temp_party['registration']))
        self.wd.BY_XPATH('//td[contains(.,"Group")]')

        # [REVERSION]
        self.delete_party(temp_party)
        self.verify_tenure_relationship_is_deleted(temp_rel)

    def test_user_can_create_relationship_with_new_conditional_individual(
        self, conditional_attrs_org_prj, basic_apartment, data_collector
    ):
        """Verifies Records test case #RC4."""

        temp_party = {
            'name': 'FuncTest Tmp ' + random_string(),
            'type': 'IN',
            'notes': random_string(),
            'birthdate': '2002-03-04',
        }
        temp_rel = {
            'location': basic_apartment,
            'party': temp_party,
            'type': 'EA',
            'type_label': 'Easement',
        }
        self.log_in(data_collector)

        self.go_to_add_tenure_relationship_form(basic_apartment)
        try:
            self.wd.BY_ID('add-party').click()
        except (ElementNotInteractableException, ElementNotVisibleException):
            pass
        self.update_form_field('name', temp_party['name'])
        self.update_form_field('party_type', temp_party['type'])
        assert self.wd.BY_NAME('party::in::notes').is_displayed()
        self.update_form_field('party::in::notes', temp_party['notes'])
        assert self.wd.BY_NAME('party::in::birthdate').is_displayed()
        self.update_form_field('party::in::birthdate', temp_party['birthdate'])
        self.update_form_field('tenure_type', temp_rel['type'])
        self.click_save_button()
        self.verify_tenure_relationship_details(
            temp_rel, tenure_type_field_label="Relationship type")
        self.wd.BY_LINK(temp_party['name']).click()
        regex = self.prj_dashboard_path + 'records/parties/([a-z0-9]{24})/'
        m = re.fullmatch(regex, self.get_url_path())
        assert m
        temp_party['pk'] = m.group(1)
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['notes']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(
            temp_party['birthdate']))
        self.wd.BY_XPATH('//td[contains(.,"Individual")]')

        # [REVERSION]
        self.delete_party(temp_party)
        self.verify_tenure_relationship_is_deleted(temp_rel)

    def test_user_can_create_relationship_with_new_conditional_corporation(
        self, conditional_attrs_org_prj, basic_apartment, data_collector
    ):
        """Verifies Records test case #RC5."""

        temp_party = {
            'name': 'FuncTest Tmp ' + random_string(),
            'type': 'CO',
            'notes': random_string(),
            'registration': '2003-04-05',
        }
        temp_rel = {
            'location': basic_apartment,
            'party': temp_party,
            'type': 'ES',
            'type_label': 'Equitable Servitude',
        }
        self.log_in(data_collector)

        self.go_to_add_tenure_relationship_form(basic_apartment)
        try:
            self.wd.BY_ID('add-party').click()
        except (ElementNotInteractableException, ElementNotVisibleException):
            pass
        self.update_form_field('name', temp_party['name'])
        self.update_form_field('party_type', temp_party['type'])
        assert self.wd.BY_NAME('party::co::notes').is_displayed()
        self.update_form_field('party::co::notes', temp_party['notes'])
        assert self.wd.BY_NAME('party::co::registration').is_displayed()
        self.update_form_field(
            'party::co::registration', temp_party['registration'])
        self.update_form_field('tenure_type', temp_rel['type'])
        self.click_save_button()
        self.verify_tenure_relationship_details(
            temp_rel, tenure_type_field_label="Relationship type")
        self.wd.BY_LINK(temp_party['name']).click()
        regex = self.prj_dashboard_path + 'records/parties/([a-z0-9]{24})/'
        m = re.fullmatch(regex, self.get_url_path())
        assert m
        temp_party['pk'] = m.group(1)
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['notes']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(
            temp_party['registration']))
        self.wd.BY_XPATH('//td[contains(.,"Corporation")]')

        # [REVERSION]
        self.delete_party(temp_party)
        self.verify_tenure_relationship_is_deleted(temp_rel)

    def test_user_can_create_relationship_with_new_conditional_group(
        self, conditional_attrs_org_prj, basic_apartment, data_collector
    ):
        """Verifies Records test case #RC6."""

        temp_party = {
            'name': 'FuncTest Tmp ' + random_string(),
            'type': 'GR',
            'notes': random_string(),
            'number_of_members': 12345,
        }
        temp_rel = {
            'location': basic_apartment,
            'party': temp_party,
            'type': 'FH',
            'type_label': 'Freehold',
        }
        self.log_in(data_collector)

        self.go_to_add_tenure_relationship_form(basic_apartment)
        try:
            self.wd.BY_ID('add-party').click()
        except (ElementNotInteractableException, ElementNotVisibleException):
            pass
        self.update_form_field('name', temp_party['name'])
        self.update_form_field('party_type', temp_party['type'])
        assert self.wd.BY_NAME('party::gr::notes').is_displayed()
        self.update_form_field('party::gr::notes', temp_party['notes'])
        assert self.wd.BY_NAME('party::gr::number_of_members').is_displayed()
        self.update_form_field(
            'party::gr::number_of_members', temp_party['number_of_members'])
        self.update_form_field('tenure_type', temp_rel['type'])
        self.click_save_button()
        self.verify_tenure_relationship_details(
            temp_rel, tenure_type_field_label="Relationship type")
        self.wd.BY_LINK(temp_party['name']).click()
        regex = self.prj_dashboard_path + 'records/parties/([a-z0-9]{24})/'
        m = re.fullmatch(regex, self.get_url_path())
        assert m
        temp_party['pk'] = m.group(1)
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['notes']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(
            str(temp_party['number_of_members'])))
        self.wd.BY_XPATH('//td[contains(.,"Group")]')

        # [REVERSION]
        self.delete_party(temp_party)
        self.verify_tenure_relationship_is_deleted(temp_rel)

    def test_user_can_create_custom_relationship_with_existing_party(
        self, custom_tenure_attrs_org_prj, basic_national_park, basic_group,
        data_collector
    ):
        """Verifies Records test case #RC7."""

        temp_rel = {
            'location': basic_national_park,
            'party': basic_group,
            'type': 'GR',
            'type_label': 'Grazing Rights',
            'number_of_documents': 1024,
        }
        self.log_in(data_collector)

        self.go_to_add_tenure_relationship_form(basic_national_park)
        self.wd.BY_ID('select2-party-select-container').click()
        self.wd.BY_XPATH(
            '//*[contains(@id,"select2-party-select-result-") and '
            '    contains(@id,"-{}")]'.format(basic_group['pk'])).click()
        assert (
            self.wd.BY_ID('select2-party-select-container').text ==
            basic_group['name']
        )
        self.update_form_field('tenure_type', temp_rel['type'])
        assert self.wd.BY_NAME(
            'tenurerelationship::default::number_of_documents').is_displayed()
        self.update_form_field(
            'tenurerelationship::default::number_of_documents',
            temp_rel['number_of_documents'])
        self.click_save_button()
        temp_rel['pk'] = self.verify_tenure_relationship_details(
            temp_rel,
            tenure_type_field_label="Relationship type",
            other_fields={'number_of_documents': 'Number of documents'},
        )

        # [REVERSION]
        self.delete_tenure_relationship()
        self.verify_tenure_relationship_is_deleted(temp_rel)

    def test_user_can_create_custom_relationship_with_new_party(
        self, custom_tenure_attrs_org_prj, basic_national_park, data_collector
    ):
        """Verifies Records test case #RC8."""

        temp_party = {
            'name': 'FuncTest Tmp ' + random_string(),
            'type': 'CO',
        }
        temp_rel = {
            'location': basic_national_park,
            'party': temp_party,
            'type': 'HR',
            'type_label': 'Hunting/Fishing/Harvest Rights',
            'number_of_documents': 1048576,
        }
        self.log_in(data_collector)

        self.go_to_add_tenure_relationship_form(basic_national_park)
        self.wd.BY_ID('add-party').click()
        self.update_form_field('name', temp_party['name'])
        self.update_form_field('party_type', temp_party['type'])
        self.update_form_field('tenure_type', temp_rel['type'])
        assert self.wd.BY_NAME(
            'tenurerelationship::default::number_of_documents').is_displayed()
        self.update_form_field(
            'tenurerelationship::default::number_of_documents',
            temp_rel['number_of_documents'])
        self.click_save_button()
        temp_rel['pk'] = self.verify_tenure_relationship_details(
            temp_rel,
            tenure_type_field_label="Relationship type",
            other_fields={'number_of_documents': 'Number of documents'},
        )
        self.wd.BY_LINK(temp_party['name']).click()
        regex = self.prj_dashboard_path + 'records/parties/([a-z0-9]{24})/'
        m = re.fullmatch(regex, self.get_url_path())
        assert m
        temp_party['pk'] = m.group(1)
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"Corporation")]')

        # [REVERSION]
        self.delete_party(temp_party)
        self.verify_tenure_relationship_is_deleted(temp_rel)

    def test_user_can_create_update_custom_relationship_with_new_custom_party(
        self, custom_attrs_org_prj, custom_building, data_collector
    ):
        """Verifies Records test case #RC9, #RU2."""

        temp_party = {
            'name': 'FuncTest Tmp ' + random_string(),
            'type': 'IN',
            'registration': '2004-05-06',
        }
        temp_rel = {
            'location': custom_building,
            'party': temp_party,
            'type': 'IN',
            'type_label': 'Indigenous Land Rights',
            'number_of_documents': 100,
        }
        self.log_in(data_collector)

        # Test case #RC9
        self.go_to_add_tenure_relationship_form(custom_building)
        try:
            self.wd.BY_ID('add-party').click()
        except (ElementNotInteractableException, ElementNotVisibleException):
            pass
        self.update_form_field('name', temp_party['name'])
        self.update_form_field('party_type', temp_party['type'])
        assert self.wd.BY_NAME('party::in::registration').is_displayed()
        self.update_form_field(
            'party::in::registration', temp_party['registration'])
        self.update_form_field('tenure_type', temp_rel['type'])
        assert self.wd.BY_NAME(
            'tenurerelationship::default::number_of_documents').is_displayed()
        self.update_form_field(
            'tenurerelationship::default::number_of_documents',
            temp_rel['number_of_documents'])
        self.click_save_button()
        temp_rel['pk'] = self.verify_tenure_relationship_details(
            temp_rel,
            tenure_type_field_label="Relationship type",
            other_fields={'number_of_documents': 'Number of documents'},
        )
        self.wd.BY_LINK(temp_party['name']).click()
        regex = self.prj_dashboard_path + 'records/parties/([a-z0-9]{24})/'
        m = re.fullmatch(regex, self.get_url_path())
        assert m
        temp_party['pk'] = m.group(1)
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(
            temp_party['registration']))
        self.wd.BY_XPATH('//td[contains(.,"Individual")]')

        # Test case #RU2
        self.open(self.prj_dashboard_path + 'relationships/{}/'.format(
            temp_rel['pk']))
        self.wd.BY_CSS('[title="Edit relationship"]').click()
        self.update_form_field('tenure_type', 'UC')
        self.update_form_field(
            'tenurerelationship::default::number_of_documents', 200)
        self.click_save_button()
        self.wd.BY_XPATH(
            '//tr['
            '    .//td[contains(.,"Relationship type")] and '
            '    .//td[contains(.,"Undivided Co-ownership")]'
            ']')
        self.wd.BY_XPATH(
            '//tr['
            '    .//td[contains(.,"Party")] and '
            '    .//td//a[contains(.,"{}")]'
            ']'.format(temp_party['name']))
        self.wd.BY_XPATH(
            '//tr['
            '    .//td[contains(.,"Number of documents")] and '
            '    .//td[contains(.,"200")]'
            ']')

        # [REVERSION]
        self.delete_party(temp_party)
        self.verify_tenure_relationship_is_deleted(temp_rel)

    def test_user_can_create_custom_rel_with_new_conditional_individual(
        self, custom_conditional_attrs_org_prj, basic_community_boundary,
        data_collector
    ):
        """Verifies Records test case #RC10."""

        temp_party = {
            'name': 'FuncTest Tmp ' + random_string(),
            'type': 'IN',
            'notes': random_string(),
            'birthdate': '2005-06-07',
        }
        temp_rel = {
            'location': basic_community_boundary,
            'party': temp_party,
            'type': 'JT',
            'type_label': 'Joint Tenancy',
            'number_of_documents': 100,
        }
        self.log_in(data_collector)

        self.go_to_add_tenure_relationship_form(basic_community_boundary)
        try:
            self.wd.BY_ID('add-party').click()
        except (ElementNotInteractableException, ElementNotVisibleException):
            pass
        self.update_form_field('name', temp_party['name'])
        self.update_form_field('party_type', temp_party['type'])
        assert self.wd.BY_NAME('party::in::notes').is_displayed()
        self.update_form_field('party::in::notes', temp_party['notes'])
        assert self.wd.BY_NAME('party::in::birthdate').is_displayed()
        self.update_form_field('party::in::birthdate', temp_party['birthdate'])
        self.update_form_field('tenure_type', temp_rel['type'])
        assert self.wd.BY_NAME(
            'tenurerelationship::default::number_of_documents').is_displayed()
        self.update_form_field(
            'tenurerelationship::default::number_of_documents',
            temp_rel['number_of_documents'])
        self.click_save_button()
        temp_rel['pk'] = self.verify_tenure_relationship_details(
            temp_rel,
            tenure_type_field_label="Relationship type",
            other_fields={'number_of_documents': 'Number of documents'},
        )
        self.wd.BY_LINK(temp_party['name']).click()
        regex = self.prj_dashboard_path + 'records/parties/([a-z0-9]{24})/'
        m = re.fullmatch(regex, self.get_url_path())
        assert m
        temp_party['pk'] = m.group(1)
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['notes']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(
            temp_party['birthdate']))
        self.wd.BY_XPATH('//td[contains(.,"Individual")]')

        # [REVERSION]
        self.delete_party(temp_party)
        self.verify_tenure_relationship_is_deleted(temp_rel)

    def test_user_can_create_custom_rel_with_new_conditional_corporation(
        self, custom_conditional_attrs_org_prj, basic_community_boundary,
        data_collector
    ):
        """Verifies Records test case #RC11."""

        temp_party = {
            'name': 'FuncTest Tmp ' + random_string(),
            'type': 'CO',
            'notes': random_string(),
            'registration': '2006-07-08',
        }
        temp_rel = {
            'location': basic_community_boundary,
            'party': temp_party,
            'type': 'LH',
            'type_label': 'Leasehold',
            'number_of_documents': 200,
        }
        self.log_in(data_collector)

        self.go_to_add_tenure_relationship_form(basic_community_boundary)
        try:
            self.wd.BY_ID('add-party').click()
        except (ElementNotInteractableException, ElementNotVisibleException):
            pass
        self.update_form_field('name', temp_party['name'])
        self.update_form_field('party_type', temp_party['type'])
        assert self.wd.BY_NAME('party::co::notes').is_displayed()
        self.update_form_field('party::co::notes', temp_party['notes'])
        assert self.wd.BY_NAME('party::co::registration').is_displayed()
        self.update_form_field(
            'party::co::registration', temp_party['registration'])
        self.update_form_field('tenure_type', temp_rel['type'])
        assert self.wd.BY_NAME(
            'tenurerelationship::default::number_of_documents').is_displayed()
        self.update_form_field(
            'tenurerelationship::default::number_of_documents',
            temp_rel['number_of_documents'])
        self.click_save_button()
        temp_rel['pk'] = self.verify_tenure_relationship_details(
            temp_rel,
            tenure_type_field_label="Relationship type",
            other_fields={'number_of_documents': 'Number of documents'},
        )
        self.wd.BY_LINK(temp_party['name']).click()
        regex = self.prj_dashboard_path + 'records/parties/([a-z0-9]{24})/'
        m = re.fullmatch(regex, self.get_url_path())
        assert m
        temp_party['pk'] = m.group(1)
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['notes']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(
            temp_party['registration']))
        self.wd.BY_XPATH('//td[contains(.,"Corporation")]')

        # [REVERSION]
        self.delete_party(temp_party)
        self.verify_tenure_relationship_is_deleted(temp_rel)

    def test_user_can_create_custom_rel_with_new_conditional_group(
        self, custom_conditional_attrs_org_prj, basic_community_boundary,
        data_collector
    ):
        """Verifies Records test case #RC12."""

        temp_party = {
            'name': 'FuncTest Tmp ' + random_string(),
            'type': 'GR',
            'notes': random_string(),
            'number_of_members': 67890,
        }
        temp_rel = {
            'location': basic_community_boundary,
            'party': temp_party,
            'type': 'LL',
            'type_label': 'Longterm leasehold',
            'number_of_documents': 300,
        }
        self.log_in(data_collector)

        self.go_to_add_tenure_relationship_form(basic_community_boundary)
        try:
            self.wd.BY_ID('add-party').click()
        except (ElementNotInteractableException, ElementNotVisibleException):
            pass
        self.update_form_field('name', temp_party['name'])
        self.update_form_field('party_type', temp_party['type'])
        assert self.wd.BY_NAME('party::gr::notes').is_displayed()
        self.update_form_field('party::gr::notes', temp_party['notes'])
        assert self.wd.BY_NAME('party::gr::number_of_members').is_displayed()
        self.update_form_field(
            'party::gr::number_of_members', temp_party['number_of_members'])
        self.update_form_field('tenure_type', temp_rel['type'])
        assert self.wd.BY_NAME(
            'tenurerelationship::default::number_of_documents').is_displayed()
        self.update_form_field(
            'tenurerelationship::default::number_of_documents',
            temp_rel['number_of_documents'])
        self.click_save_button()
        temp_rel['pk'] = self.verify_tenure_relationship_details(
            temp_rel,
            tenure_type_field_label="Relationship type",
            other_fields={'number_of_documents': 'Number of documents'},
        )
        self.wd.BY_LINK(temp_party['name']).click()
        regex = self.prj_dashboard_path + 'records/parties/([a-z0-9]{24})/'
        m = re.fullmatch(regex, self.get_url_path())
        assert m
        temp_party['pk'] = m.group(1)
        self.wd.BY_XPATH('//h2[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['name']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(temp_party['notes']))
        self.wd.BY_XPATH('//td[contains(.,"{}")]'.format(
            str(temp_party['number_of_members'])))
        self.wd.BY_XPATH('//td[contains(.,"Group")]')

        # [REVERSION]
        self.delete_party(temp_party)
        self.verify_tenure_relationship_is_deleted(temp_rel)

    def test_party_is_required_while_creating_tenure_relationship(
        self, records_org_prj, basic_parcel, basic_individual, data_collector
    ):
        """Verifies Records test case #RC15."""

        self.log_in(data_collector)
        self.go_to_add_tenure_relationship_form(basic_parcel)
        self.update_form_field('tenure_type', 'CR')
        self.click_save_button()
        self.assert_form_field_has_error('id', 'This field is required.')

    def test_tenure_relationship_type_is_required(
        self, records_org_prj, basic_parcel, basic_individual, data_collector
    ):
        """Verifies Records test case #RC13."""

        self.log_in(data_collector)
        self.go_to_add_tenure_relationship_form(basic_parcel)
        self.wd.BY_ID('select2-party-select-container').click()
        self.wd.BY_XPATH(
            '//*[contains(@id,"select2-party-select-result-") and '
            '    contains(@id,"-{}")]'.format(basic_individual['pk'])).click()
        assert (
            self.wd.BY_ID('select2-party-select-container').text ==
            basic_individual['name']
        )
        self.click_save_button()
        self.assert_form_field_has_error(
            'tenure_type', 'This field is required.')

    def test_unauthorized_user_cannot_create_tenure_relationship(
        self, records_org_prj, basic_parcel, prj_user
    ):
        """Verifies Records test case #RC14."""

        self.log_in(prj_user)
        self.open(self.prj_dashboard_path + 'records/locations/{}/'.format(
            basic_parcel['pk']))
        # TODO: Add relationship button is still present (see #xxxx)
        # self.wd.BY_XPATH(
        #     '//a[@role="tab" and normalize-space()="Relationships"]').click()
        # try:
        #     # Has existing relationships
        #     div = self.wd.BY_XPATH('//*[@id="relationships" and .//table]')
        #     try:
        #         div.find_element_by_link_text('Add')
        #         raise AssertionError('Add relationship button is present')
        #     except NoSuchElementException
        #         pass
        # except NoSuchElementException:
        #     # Has no relationships yet
        #     try:
        #         self.wd.BY_LINK('Add relationship').click()
        #         raise AssertionError('Add relationship button is present')
        #     except NoSuchElementException
        #         pass
        self.open(self.get_url_path() + 'relationships/new')
        self.wait_for_alert(
            "You don't have permission to add tenure relationships to this "
            "project.")
