import pytest
import re

from os.path import abspath, dirname, join
from selenium.webdriver.support.select import Select

from ..base_test import SeleniumTestCase
from ..util import random_string


TEST_TMP_USERNAME_FORMAT = 'functest_tmp_{}'
TEST_TMP_EMAIL_FORMAT = 'evillar+tmp_{}@cadasta.org'
TEST_TMP_PASSWORD = 'qwerty#XYZ'
USER_MENU_XPATH_FORMAT = '//header//*[normalize-space()="{}"]'


class TestUpdating(SeleniumTestCase):

    @pytest.fixture(autouse=True)
    def get_generic_user(self, generic_user):
        self.user = generic_user

    # ------ Utility functions ------

    def log_in(self, use_username=True):
        """Logs in the test user either by username or email."""
        self.wd.BY_LINK('Sign in').click()
        if use_username:
            self.update_form_field('login', self.user['username'])
        else:
            self.update_form_field('login', self.user['email'])
        self.update_form_field('password', self.user['password'])
        self.wd.BY_NAME('sign-in').click()
        label = self.user['full_name'] or self.user['username']
        self.wd.wait_for_xpath(USER_MENU_XPATH_FORMAT.format(label))

    def click_user_menu(self):
        """Clicks the current user's user menu."""
        label = self.user['full_name'] or self.user['username']
        self.wd.BY_XPATH(USER_MENU_XPATH_FORMAT.format(label)).click()

    def go_to_profile(self):
        """Goes to the current user's profile page via the user menu."""
        self.click_user_menu()
        self.wd.BY_LINK('Edit profile').click()
        self.assert_url_path('/account/profile/')

    def click_update_profile_button(self, label='Save'):
        """Clicks the profile page update button with optional button label
        for multilingual purposes."""
        button = self.wd.BY_XPATH(
            '//*[@type="submit" and normalize-space()="{}"]'.format(label))
        self.scroll_element_into_view(button)
        button.click()

    def invoke_update_profile(
        self,
        button_label='Save',
        alert_msg='Successfully updated profile information'
    ):
        """Fills in the profile page password field and then submits the
        profile page form with optional button and success alert messages for
        multilingual purposes."""
        self.update_form_field('password', self.user['password'])
        self.click_update_profile_button(label=button_label)
        self.wait_for_alert(alert_msg)
        self.assert_url_path('/account/dashboard/')

    def log_out(self):
        """Logs out the current user via the user menu."""
        self.click_user_menu()
        self.wd.BY_LINK('Logout').click()
        self.assert_url_path('/account/login/')

    # ------ Test cases ------

    def test_user_can_invoke_password_reset(self):
        """Verifies User Accounts test case #U1."""

        self.wd.BY_LINK('Sign in').click()
        self.wd.BY_LINK('Forgotten password?').click()
        self.assert_url_path('/account/password/reset/')
        self.update_form_field('email', self.user['email'])
        self.wd.BY_XPATH(
            '//*[@type="submit" and @value="Reset password"]').click()
        self.wd.wait_for_xpath('//h1[normalize-space()="Password reset"]')
        self.assert_url_path('/account/password/reset/done/')

    def test_user_can_change_password(self):
        """Verifies User Accounts test case #U5."""

        self.log_in()
        self.go_to_profile()
        link = self.wd.BY_LINK('Change password')
        self.scroll_element_into_view(link)
        link.click()
        self.assert_url_path('/account/password/change/')

        self.update_form_field('oldpassword', self.user['password'])
        original_password = self.user['password']
        self.user['password'] = TEST_TMP_PASSWORD
        self.update_form_field('password', self.user['password'])
        self.wd.BY_XPATH(
            '//*[@type="submit" and '
            'normalize-space()="Change password"]').click()
        self.wait_for_alert('Password successfully changed.')

        # Try to use the new password
        self.log_out()
        self.log_in()

        # [REVERSION]
        self.open('/account/password/change/')
        self.update_form_field('oldpassword', self.user['password'])
        self.user['password'] = original_password
        self.update_form_field('password', self.user['password'])
        self.wd.BY_XPATH(
            '//*[@type="submit" and '
            'normalize-space()="Change password"]').click()
        self.wait_for_alert('Password successfully changed.')

    def test_user_cannot_change_password_without_current_password(self):
        """Verifies User Accounts test case #U6."""

        self.log_in()
        self.open('/account/password/change/')
        self.update_form_field('oldpassword', random_string())
        self.update_form_field('password', TEST_TMP_PASSWORD)
        self.wd.BY_XPATH(
            '//*[@type="submit" and '
            'normalize-space()="Change password"]').click()
        self.assert_form_field_has_error(
            'oldpassword', 'Please type your current password.')

        # Try to use the old password
        self.log_out()
        self.log_in()

    def test_correct_user_info_is_shown(self):
        """Verifies User Accounts test case #U19."""

        self.log_in()
        self.go_to_profile()

        def assert_field(name, value):
            element = self.wd.BY_NAME(name)
            if element.tag_name == 'select':
                element = Select(element).first_selected_option
            actual_value = element.get_attribute('value')
            assert actual_value == value

        assert_field('username', self.user['username'])
        assert_field('email', self.user['email'])
        assert_field('full_name', self.user['full_name'])
        assert_field('language', self.user['language'])
        assert_field('measurement', self.user['measurement'])

    def test_user_cannot_update_profile_without_password(self):
        """Verifies User Accounts test case #U20."""

        self.log_in()
        self.go_to_profile()
        self.update_form_field('username', random_string())
        self.click_update_profile_button()
        self.assert_form_field_has_error('password', 'This field is required.')

        self.update_form_field('password', random_string())
        self.click_update_profile_button()
        self.wait_for_alert('Failed to update profile information')
        self.assert_form_field_has_error(
            'password',
            'Please provide the correct password for your account.')

        # Try to use the existing username
        self.log_out()
        self.log_in()

    def test_user_can_update_username(self):
        """Verifies User Accounts test case #U8."""

        self.log_in()
        self.go_to_profile()
        original_username = self.user['username']
        self.user['username'] = (
            TEST_TMP_USERNAME_FORMAT.format(random_string()))
        self.update_form_field('username', self.user['username'])
        self.invoke_update_profile()

        # Try to use the new username
        self.log_out()
        self.log_in()

        # [REVERSION]
        self.open('/account/profile/')
        self.user['username'] = original_username
        self.update_form_field('username', self.user['username'])
        self.invoke_update_profile()

    def test_user_can_update_email_address(self):
        """Verifies User Accounts test case #U9."""

        # Create throwaway account because email cannot be verified now
        username = TEST_TMP_USERNAME_FORMAT.format(random_string())
        first_email = TEST_TMP_EMAIL_FORMAT.format(random_string())
        password = 'XYZ#qwerty'
        self.wd.BY_LINK('Register').click()
        self.update_form_field('username', username)
        self.update_form_field('email', first_email)
        self.update_form_field('password', password)
        button = self.wd.BY_NAME('register')
        self.scroll_element_into_view(button)
        button.click()
        self.wd.wait_for_xpath(USER_MENU_XPATH_FORMAT.format(username))

        # Update email address
        self.open('/account/profile/')
        second_email = TEST_TMP_EMAIL_FORMAT.format(random_string())
        self.update_form_field('email', second_email)
        self.update_form_field('password', password)
        self.click_update_profile_button()
        self.wait_for_alert('Successfully updated profile information')
        self.wait_for_alert(
            'Confirmation email sent to {}.'.format(second_email))
        self.wd.BY_NAME('email').get_attribute('value') == first_email
        self.wd.BY_XPATH(
            '//*[contains(@class, "form-group") and //*[@name="email"]]'
            '//*[contains(normalize-space(), '
            '"The email for this account has been changed recently")]')

        # Can only login with the old email address yet
        self.open('/account/logout/')
        self.update_form_field('login', first_email)
        self.update_form_field('password', password)
        self.wd.BY_NAME('sign-in').click()
        self.wd.wait_for_xpath(USER_MENU_XPATH_FORMAT.format(username))

    def test_user_can_update_full_name(self):
        """Verifies User Accounts test case #U12."""

        self.log_in()
        self.go_to_profile()
        tmp_full_name = 'Temp Name'
        self.update_form_field('full_name', tmp_full_name)
        self.invoke_update_profile()
        self.wd.wait_for_xpath(USER_MENU_XPATH_FORMAT.format(tmp_full_name))

        # [REVERSION]
        self.open('/account/profile/')
        self.update_form_field('full_name', self.user['full_name'])
        self.invoke_update_profile()
        self.wd.wait_for_xpath(
            USER_MENU_XPATH_FORMAT.format(self.user['full_name']))

    def test_user_can_update_preferred_language(self):
        """Verifies User Accounts test case #U13."""

        self.log_in()
        self.go_to_profile()
        self.update_form_field('language', 'es')
        self.invoke_update_profile(
            alert_msg='La información del perfil se ha actualizado '
                      'correctamente')
        self.wd.BY_LINK('Proyectos')
        self.wd.BY_LINK('Organizaciones')

        # [REVERSION]
        self.open('/account/profile/')
        self.update_form_field('language', self.user['language'])
        self.invoke_update_profile(button_label='Guardar')
        self.wd.BY_LINK('Projects')
        self.wd.BY_LINK('Organizations')

    def test_user_can_update_preferred_measurement_system(self):
        """Verifies User Accounts test case #U14."""

        self.log_in()
        self.go_to_profile()
        self.update_form_field('measurement', 'imperial')
        self.invoke_update_profile()

        # [REVERSION]
        self.open('/account/profile/')
        self.update_form_field('measurement', 'metric')
        self.invoke_update_profile()

    @pytest.mark.uploads
    def test_user_avatar(self):
        """Verifies User Accounts test case #U15, #U16, #U17, #U18."""

        default_avatar_path = '/static/img/avatar_sm.jpg'
        files_dir_path = join(dirname(dirname(abspath(__file__))), 'files')
        avatar_form_group_xpath = (
            '//*[contains(@class, "form-group") and '
            '//label[normalize-space()="Profile picture"]]')
        img_xpath = avatar_form_group_xpath + '//img'
        file_input_xpath = avatar_form_group_xpath + '//input[@type="file"]'
        remove_xpath = (
            avatar_form_group_xpath + '//*[contains(@class, "file-remove")]')
        file_type_error_xpath = (
            avatar_form_group_xpath +
            '//*[normalize-space()="File type not allowed."]')

        self.log_in()
        self.go_to_profile()

        # Test case #U17
        img = self.wd.BY_XPATH(img_xpath)
        assert default_avatar_path in img.get_attribute('src')
        self.wd.BY_XPATH(file_input_xpath).send_keys(
            join(files_dir_path, 'user_avatar_3.gif'))
        self.wd.BY_XPATH(file_type_error_xpath)

        # Test case #U15
        self.open('/account/profile/')
        img = self.wd.BY_XPATH(img_xpath)
        assert default_avatar_path in img.get_attribute('src')
        self.wd.BY_XPATH(file_input_xpath).send_keys(
            join(files_dir_path, 'user_avatar_1.jpg'))
        self.wd.wait_for_xpath(remove_xpath)
        assert default_avatar_path not in img.get_attribute('src')
        self.invoke_update_profile()

        self.open('/account/profile/')
        img = self.wd.BY_XPATH(img_xpath)
        src = img.get_attribute('src')
        assert default_avatar_path not in src
        assert re.search('[a-z0-9]{24}\.jpg$', src)

        # Test case #U16
        self.open('/account/profile/')
        self.wd.BY_XPATH(remove_xpath).click()
        img = self.wd.BY_XPATH(img_xpath)
        assert default_avatar_path in img.get_attribute('src')
        self.wd.BY_XPATH(file_input_xpath).send_keys(
            join(files_dir_path, 'user_avatar_2.png'))
        self.wd.wait_for_xpath(remove_xpath)
        assert default_avatar_path not in img.get_attribute('src')
        self.invoke_update_profile()

        self.open('/account/profile/')
        img = self.wd.BY_XPATH(img_xpath)
        src = img.get_attribute('src')
        assert default_avatar_path not in src
        assert re.search('[a-z0-9]{24}\.png$', src)

        # [REVERSION] and test case #U18
        self.open('/account/profile/')
        self.wd.BY_XPATH(remove_xpath).click()
        self.invoke_update_profile()

        self.open('/account/profile/')
        img = self.wd.BY_XPATH(img_xpath)
        assert default_avatar_path in img.get_attribute('src')
