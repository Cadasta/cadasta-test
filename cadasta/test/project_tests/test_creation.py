import pytest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from ..base_test import SeleniumTestCase
from ..util import random_string


USER_MENU_XPATH_FORMAT = '//header//*[normalize-space()="{}"]'


class TestCreation(SeleniumTestCase):

    @pytest.fixture(autouse=True)
    def get_standard_fixtures(self, basic_org, org_admin):
        self.org = basic_org
        self.user = org_admin

    # ------ Utility functions ------

    def log_in(self, user=None):
        """Logs in the test user."""
        if user is None:
            user = self.user
        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', user['username'])
        self.update_form_field('password', user['password'])
        self.wd.BY_NAME('sign-in').click()
        label = user['full_name'] or user['username']
        self.wd.wait_for_xpath(USER_MENU_XPATH_FORMAT.format(label))

    def click_wizard_next_button(self):
        button = self.wd.BY_CLASS('btn-primary')
        self.scroll_element_into_view(button)
        button.click()

    def draw_map_rectangle(self):
        self.wd.BY_CLASS('leaflet-draw-draw-rectangle').click()
        actions = ActionChains(self.wd)
        actions.move_to_element(self.wd.BY_ID('id_extents_extent_map'))
        actions.click_and_hold()
        actions.move_by_offset(40, 40)
        actions.release()
        actions.perform()

    # ------ Test cases ------

    def test_org_admin_can_create_public_project(self):
        """Verifies Projects test case #C1, #C11"""

        self.log_in()
        self.wd.BY_LINK('Projects').click()
        self.wd.BY_CLASS('btn-primary').click()  # Add project
        self.draw_map_rectangle()
        self.click_wizard_next_button()
        self.update_form_field('details-organization', self.org['slug'])
        slug_part = random_string()
        name = "FuncTest Tmp " + slug_part
        self.update_form_field('details-name', name)
        self.update_form_field('details-description', "Project description.")
        self.update_form_field('details-url', 'http://example.com')
        self.update_form_field('details-contacts-0-name', 'Contact Person')
        self.update_form_field('details-contacts-0-email', 'cp@example.com')
        self.update_form_field('details-contacts-0-tel', '1234567890')
        self.click_wizard_next_button()
        self.click_wizard_next_button()
        expected_path = '/organizations/{}/projects/functest-tmp-{}/'.format(
            self.org['slug'], slug_part)
        assert self.get_url_path() == expected_path
        self.wd.BY_XPATH('//h1[contains(.,"{}")]'.format(name))
        about = self.wd.BY_CLASS('panel-about')
        about.find_element_by_xpath('//*[.="Project description."]')
        about.find_element_by_xpath('//*[@href="http://example.com"]')
        about.find_element_by_xpath('//*[text()="Contact Person"]')
        about.find_element_by_xpath('//*[@href="mailto:cp@example.com"]')
        about.find_element_by_xpath('//*[@href="tel:1234567890"]')

    def test_org_admin_can_create_private_project(self):
        """Verifies Projects test case #C2."""

        self.log_in()
        self.wd.BY_LINK('Projects').click()
        self.wd.BY_CLASS('btn-primary').click()  # Add project
        self.draw_map_rectangle()
        self.click_wizard_next_button()
        self.update_form_field('details-organization', self.org['slug'])
        slug_part = random_string()
        name = "FuncTest Tmp " + slug_part
        self.update_form_field('details-name', name)
        self.wd.BY_CLASS('toggle').click()
        self.update_form_field('details-description', "Project description.")
        self.update_form_field('details-url', 'http://example.com')
        self.update_form_field('details-contacts-0-name', 'Contact Person')
        self.update_form_field('details-contacts-0-email', 'cp@example.com')
        self.update_form_field('details-contacts-0-tel', '1234567890')
        self.click_wizard_next_button()
        self.click_wizard_next_button()
        expected_path = '/organizations/{}/projects/functest-tmp-{}/'.format(
            self.org['slug'], slug_part)
        assert self.get_url_path() == expected_path
        self.wd.BY_XPATH(
            '//h1[contains(normalize-space(),"{} Private")]'.format(name))
        about = self.wd.BY_CLASS('panel-about')
        about.find_element_by_xpath('//*[.="Project description."]')
        about.find_element_by_xpath('//*[@href="http://example.com"]')
        about.find_element_by_xpath('//*[text()="Contact Person"]')
        about.find_element_by_xpath('//*[@href="mailto:cp@example.com"]')
        about.find_element_by_xpath('//*[@href="tel:1234567890"]')

    def test_non_org_admin_cannot_create_project(self, org_member):
        """Verifies Projects test case #C3."""

        self.log_in(org_member)
        self.wd.BY_LINK('Projects').click()
        try:
            self.wd.BY_CLASS('btn-primary')
            raise AssertionError('Add project button is present')
        except NoSuchElementException:
            pass
        # TODO: Non-org admin can still access project wizard (see #1677)

    def test_extent_description_url_contacts_is_not_required(self):
        """Verifies Projects test case #C4, #C8, #C9, #C12."""

        self.log_in()
        self.open('/projects/new/')
        self.click_wizard_next_button()
        self.update_form_field('details-organization', self.org['slug'])
        slug_part = random_string()
        name = "FuncTest Tmp " + slug_part
        self.update_form_field('details-name', name)
        self.click_wizard_next_button()
        self.click_wizard_next_button()
        expected_path = '/organizations/{}/projects/functest-tmp-{}/'.format(
            self.org['slug'], slug_part)
        assert self.get_url_path() == expected_path
        self.wd.BY_XPATH('//h1[contains(.,"{}")]'.format(name))
        self.wd.BY_CLASS('panel-about').find_element_by_xpath(
            '//*[contains(.,"This project needs a description.")]')

    def test_org_is_required(self):
        """Verifies Projects test case #C5."""

        self.log_in()
        self.open('/projects/new/')
        self.click_wizard_next_button()
        self.update_form_field('details-name', 'Project Name')
        self.update_form_field('details-description', "Project description.")
        self.update_form_field('details-url', 'http://example.com')
        self.update_form_field('details-contacts-0-name', 'Contact Person')
        self.update_form_field('details-contacts-0-email', 'cp@example.com')
        self.update_form_field('details-contacts-0-tel', '1234567890')
        self.click_wizard_next_button()
        self.assert_form_field_has_error(
            'details-organization', 'This field is required.')

    def test_name_is_required(self):
        """Verifies Projects test case #C6."""

        self.log_in()
        self.open('/projects/new/')
        self.click_wizard_next_button()
        self.update_form_field('details-organization', self.org['slug'])
        self.update_form_field('details-description', "Project description.")
        self.update_form_field('details-url', 'http://example.com')
        self.update_form_field('details-contacts-0-name', 'Contact Person')
        self.update_form_field('details-contacts-0-email', 'cp@example.com')
        self.update_form_field('details-contacts-0-tel', '1234567890')
        self.click_wizard_next_button()
        self.assert_form_field_has_error(
            'details-name', 'This field is required.')

    def test_duplicate_name_is_rejected(self, basic_prj, another_prj):
        """Verifies Projects test case #C7, #C16, #C17."""

        self.log_in()
        self.open('/projects/new/')
        self.click_wizard_next_button()
        self.update_form_field('details-organization', self.org['slug'])
        self.update_form_field('details-name', basic_prj['name'])
        self.update_form_field('details-description', "Project description.")
        self.update_form_field('details-url', 'http://example.com')
        self.update_form_field('details-contacts-0-name', 'Contact Person')
        self.update_form_field('details-contacts-0-email', 'cp@example.com')
        self.update_form_field('details-contacts-0-tel', '1234567890')
        self.click_wizard_next_button()
        self.assert_form_field_has_error(
            'details-name', 'Project with this name already exists')

        # Clear the previous error by inducing a different error
        self.update_form_field('details-name', '')
        self.click_wizard_next_button()
        self.assert_form_field_has_error(
            'details-name', 'This field is required.')

        self.update_form_field('details-name', basic_prj['name'].upper())
        self.click_wizard_next_button()
        self.assert_form_field_has_error(
            'details-name', 'Project with this name already exists')

        # Clear the previous error by inducing a different error
        self.update_form_field('details-name', '')
        self.click_wizard_next_button()
        self.assert_form_field_has_error(
            'details-name', 'This field is required.')

        self.update_form_field('details-name', another_prj['name'].upper())
        self.click_wizard_next_button()
        self.assert_form_field_has_error(
            'details-name', 'Project with this name already exists')

    def test_invalid_url_is_rejected(self):
        """Verifies Projects test case #C10."""

        self.log_in()
        self.open('/projects/new/')
        self.click_wizard_next_button()
        self.update_form_field('details-organization', self.org['slug'])
        self.update_form_field('details-name', 'Project Name')
        self.update_form_field('details-description', "Project description.")
        self.update_form_field('details-url', 'invalid')
        self.update_form_field('details-contacts-0-name', 'Contact Person')
        self.update_form_field('details-contacts-0-email', 'cp@example.com')
        self.update_form_field('details-contacts-0-tel', '1234567890')
        self.click_wizard_next_button()
        self.assert_form_field_has_error(
            'details-url', 'This value should be a valid url.')

    def test_contact_name_is_required(self):
        """Verifies Projects test case #C13."""

        self.log_in()
        self.open('/projects/new/')
        self.click_wizard_next_button()
        self.update_form_field('details-organization', self.org['slug'])
        self.update_form_field('details-name', 'Project Name')
        self.update_form_field('details-description', "Project description.")
        self.update_form_field('details-url', 'http://example.com')
        self.update_form_field('details-contacts-0-email', 'cp@example.com')
        self.update_form_field('details-contacts-0-tel', '1234567890')
        self.click_wizard_next_button()
        self.wd.BY_CLASS('contacts-form').find_element_by_xpath(
            '//*[.="Please provide a name."]')

    def test_contact_email_or_phone_is_required(self):
        """Verifies Projects test case #C14."""

        self.log_in()
        self.open('/projects/new/')
        self.click_wizard_next_button()
        self.update_form_field('details-organization', self.org['slug'])
        self.update_form_field('details-name', 'Project Name')
        self.update_form_field('details-description', "Project description.")
        self.update_form_field('details-url', 'http://example.com')
        self.update_form_field('details-contacts-0-name', 'Contact Person')
        self.click_wizard_next_button()
        self.wd.BY_CLASS('contacts-form').find_element_by_xpath(
            '//*[.="Please provide either an email address '
            'or a phone number."]')

    def test_invalid_contact_email_address_is_rejected(self):
        """Verifies Projects test case #C15."""

        self.log_in()
        self.open('/projects/new/')
        self.click_wizard_next_button()
        self.update_form_field('details-organization', self.org['slug'])
        self.update_form_field('details-name', 'Project Name')
        self.update_form_field('details-description', "Project description.")
        self.update_form_field('details-url', 'http://example.com')
        self.update_form_field('details-contacts-0-name', 'Contact Person')
        self.update_form_field('details-contacts-0-email', 'invalid')
        self.update_form_field('details-contacts-0-tel', '1234567890')
        self.click_wizard_next_button()
        self.wd.BY_CLASS('contacts-form').find_element_by_xpath(
            '//*[.="This field should be a valid email."]')
