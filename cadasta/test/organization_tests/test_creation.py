import pytest

from ..base_test import SeleniumTestCase
from ..util import random_string


USER_MENU_XPATH_FORMAT = '//header//*[normalize-space()="{}"]'


class TestCreation(SeleniumTestCase):

    @pytest.fixture(autouse=True)
    def get_org_creator_user(self, org_creator):
        self.user = org_creator

    # ------ Utility functions ------

    def log_in(self):
        """Logs in the test user."""
        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', self.user['username'])
        self.update_form_field('password', self.user['password'])
        self.wd.BY_NAME('sign-in').click()
        label = self.user['full_name'] or self.user['username']
        self.wd.wait_for_xpath(USER_MENU_XPATH_FORMAT.format(label))

    def click_save_button(self):
        self.wd.BY_XPATH(
            '//*[@type="submit" and normalize-space()="Save"]').click()

    # ------ Test cases ------

    def test_user_can_create_an_org(self):
        """Verifies Organizations test case #C1."""

        self.log_in()
        self.wd.BY_LINK('Organizations').click()
        self.wd.BY_CLASS('add-org').click()
        slug_part = random_string()
        name = "FuncTest Tmp " + slug_part
        self.update_form_field('name', name)
        self.update_form_field('description', "Organization description.")
        self.update_form_field('urls', 'http://example.com')
        self.update_form_field('contacts-0-name', 'Contact Person')
        self.update_form_field('contacts-0-email', 'contact@example.com')
        self.update_form_field('contacts-0-tel', '1234567890')
        self.click_save_button()
        expected_path = '/organizations/functest-tmp-{}/'.format(slug_part)
        assert self.get_url_path() == expected_path
        self.wd.BY_XPATH('//h1[contains(.,"{}")]'.format(name))
        about = self.wd.BY_CLASS('panel-about')
        about.find_element_by_xpath('//*[.="Organization description."]')
        about.find_element_by_xpath('//*[@href="http://example.com"]')
        about.find_element_by_xpath('//*[text()="Contact Person"]')
        about.find_element_by_xpath('//*[@href="mailto:contact@example.com"]')
        about.find_element_by_xpath('//*[@href="tel:1234567890"]')
        self.wd.BY_XPATH('//*[contains(.,"Now add your first project.")]')

    def test_name_is_required(self):
        """Verifies Organizations test case #C2."""

        self.log_in()
        self.wd.BY_LINK('Organizations').click()
        self.wd.BY_CLASS('add-org').click()
        self.update_form_field('description', "Organization description.")
        self.update_form_field('urls', 'http://example.com')
        self.update_form_field('contacts-0-name', 'Contact Person')
        self.update_form_field('contacts-0-email', 'contact@example.com')
        self.update_form_field('contacts-0-tel', '1234567890')
        self.click_save_button()
        self.assert_form_field_has_error('name', 'This field is required.')

    def test_duplicate_name_is_rejected(self, basic_org):
        """Verifies Organizations test case #C3, #C11."""

        self.log_in()
        self.wd.BY_LINK('Organizations').click()
        self.wd.BY_CLASS('add-org').click()
        self.update_form_field('name', basic_org['name'])
        self.update_form_field('description', "Organization description.")
        self.update_form_field('urls', 'http://example.com')
        self.update_form_field('contacts-0-name', 'Contact Person')
        self.update_form_field('contacts-0-email', 'contact@example.com')
        self.update_form_field('contacts-0-tel', '1234567890')
        self.click_save_button()
        self.assert_form_field_has_error(
            'name', 'Organization with this name already exists.')

        # Clear the previous error by inducing a different error
        self.update_form_field('name', '')
        self.click_save_button()
        self.assert_form_field_has_error('name', 'This field is required.')

        self.update_form_field('name', basic_org['name'].upper())
        self.click_save_button()
        self.assert_form_field_has_error(
            'name', 'Organization with this name already exists.')

    def test_description_url_contacts_is_not_required(self):
        """Verifies Organizations test case #C4, #C5, #C7."""

        self.log_in()
        self.wd.BY_LINK('Organizations').click()
        self.wd.BY_CLASS('add-org').click()
        slug_part = random_string()
        name = "FuncTest Tmp " + slug_part
        self.update_form_field('name', name)
        self.click_save_button()
        expected_path = '/organizations/functest-tmp-{}/'.format(slug_part)
        assert self.get_url_path() == expected_path
        self.wd.BY_XPATH('//h1[contains(.,"{}")]'.format(name))
        self.wd.BY_XPATH('//*[contains(.,"Now add your first project.")]')

    def test_invalid_url_is_rejected(self):
        """Verifies Organizations test case #C6."""

        self.log_in()
        self.wd.BY_LINK('Organizations').click()
        self.wd.BY_CLASS('add-org').click()
        self.update_form_field('name', 'Organization Name')
        self.update_form_field('description', "Organization description.")
        self.update_form_field('urls', 'invalid')
        self.update_form_field('contacts-0-name', 'Contact Person')
        self.update_form_field('contacts-0-email', 'contact@example.com')
        self.update_form_field('contacts-0-tel', '1234567890')
        self.click_save_button()
        self.assert_form_field_has_error(
            'urls', 'This value should be a valid url.')

    def test_contact_name_is_required(self):
        """Verifies Organizations test case #C8."""

        self.log_in()
        self.wd.BY_LINK('Organizations').click()
        self.wd.BY_CLASS('add-org').click()
        self.update_form_field('name', 'Organization Name')
        self.update_form_field('description', "Organization description.")
        self.update_form_field('urls', 'http://example.com')
        self.update_form_field('contacts-0-email', 'contact@example.com')
        self.update_form_field('contacts-0-tel', '1234567890')
        self.click_save_button()
        self.wd.BY_CLASS('contacts-form').find_element_by_xpath(
            '//*[.="Please provide a name."]')

    def test_contact_email_or_phone_is_required(self):
        """Verifies Organizations test case #C9."""

        self.log_in()
        self.wd.BY_LINK('Organizations').click()
        self.wd.BY_CLASS('add-org').click()
        self.update_form_field('name', 'Organization Name')
        self.update_form_field('description', "Organization description.")
        self.update_form_field('urls', 'http://example.com')
        self.update_form_field('contacts-0-name', 'Contact Person')
        self.click_save_button()
        self.wd.BY_CLASS('contacts-form').find_element_by_xpath(
            '//*[.="Please provide either an email address '
            'or a phone number."]')

    def test_invalid_contact_email_address_is_rejected(self):
        """Verifies Organizations test case #C10."""

        self.log_in()
        self.wd.BY_LINK('Organizations').click()
        self.wd.BY_CLASS('add-org').click()
        self.update_form_field('name', 'Organization Name')
        self.update_form_field('description', "Organization description.")
        self.update_form_field('urls', 'http://example.com')
        self.update_form_field('contacts-0-name', 'Contact Person')
        self.update_form_field('contacts-0-email', 'invalid')
        self.update_form_field('contacts-0-tel', '1234567890')
        self.click_save_button()
        self.wd.BY_CLASS('contacts-form').find_element_by_xpath(
            '//*[.="This field should be a valid email."]')
