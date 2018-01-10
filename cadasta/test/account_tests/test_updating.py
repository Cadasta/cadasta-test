import pytest
import re

from os.path import abspath, dirname, join
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from ..base_test import SeleniumTestCase
from ..util import random_string, random_us_number


TEST_TMP_USERNAME_FORMAT = 'functest_tmp_{}'
TEST_TMP_EMAIL_FORMAT = 'evillar+tmp_{}@cadasta.org'
TEST_TMP_PASSWORD = 'qwerty#XYZ'
USER_MENU_XPATH_FORMAT = '//header//*[normalize-space()="{}"]'


@pytest.mark.batch1
class TestUpdating(SeleniumTestCase):

    @pytest.fixture(autouse=True)
    def get_generic_user(self, generic_user, generic_phone_user):
        self.email_user = generic_user
        self.phone_user = generic_phone_user

    # ------ Utility functions ------

    def click_user_menu(self, use_phone_user=False):
        """Clicks the current user's user menu."""
        if use_phone_user:
            user = self.phone_user
        else:
            user = self.email_user
        label = user['full_name'] or user['username']
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
        alert_msg='Successfully updated profile information',
        use_phone_user=False
    ):
        """Fills in the profile page password field and then submits the
        profile page form with optional button and success alert messages for
        multilingual purposes.

        Also verifies User Accounts test case #U22 if update is successful."""
        if use_phone_user:
            user = self.phone_user
        else:
            user = self.email_user
        self.update_form_field('password', user['password'])
        self.click_update_profile_button(label=button_label)
        self.wait_for_alert(alert_msg)
        self.assert_url_path('/account/dashboard/')

    def log_out(self):
        """Logs out the current user via the user menu."""
        self.click_user_menu()
        self.wd.BY_LINK('Logout').click()
        self.assert_url_path('/account/login/')

    # ------ Test cases ------

    def test_user_can_invoke_password_reset_by_email(self):
        """Verifies User Accounts test case #U1."""

        self.wd.BY_LINK('Sign in').click()
        self.wd.BY_LINK('Forgotten password?').click()
        self.assert_url_path('/account/password/reset/')
        try:
            self.wd.BY_LINK('I want to reset password with my email').click()
        except NoSuchElementException:
            pass
        self.update_form_field('email', self.email_user['email'])
        self.wd.BY_XPATH('//*[@type="submit"]').click()
        self.wd.wait_for_xpath('//h1[normalize-space()="Password reset"]')
        self.assert_url_path('/account/password/reset/done/')

    def test_user_can_invoke_password_reset_by_phone(self):
        """Verifies User Accounts test case #U23."""

        self.wd.BY_LINK('Sign in').click()
        self.wd.BY_LINK('Forgotten password?').click()
        self.assert_url_path('/account/password/reset/')
        try:
            self.wd.BY_LINK('I want to reset password with my phone').click()
        except NoSuchElementException:
            pass
        self.update_form_field('phone', self.phone_user['phone'])
        self.wd.BY_XPATH('//*[@type="submit"]').click()
        self.wd.wait_for_xpath('//h1[normalize-space()="Password reset"]')
        self.assert_url_path('/account/password/reset/done/')

    def test_user_can_change_password(self):
        """Verifies User Accounts test case #U5."""

        self.log_in(self.email_user)
        self.go_to_profile()
        link = self.wd.BY_LINK('Change password')
        self.scroll_element_into_view(link)
        link.click()
        self.assert_url_path('/account/password/change/')

        self.update_form_field('oldpassword', self.email_user['password'])
        original_password = self.email_user['password']
        self.email_user['password'] = TEST_TMP_PASSWORD
        self.update_form_field('password', self.email_user['password'])
        self.wd.BY_XPATH(
            '//*[@type="submit" and '
            'normalize-space()="Change password"]').click()
        self.wait_for_alert('Password successfully changed.')

        # Try to use the new password
        self.log_out()
        self.log_in(self.email_user)

        # [REVERSION]
        self.open('/account/password/change/')
        self.update_form_field('oldpassword', self.email_user['password'])
        self.email_user['password'] = original_password
        self.update_form_field('password', self.email_user['password'])
        self.wd.BY_XPATH(
            '//*[@type="submit" and '
            'normalize-space()="Change password"]').click()
        self.wait_for_alert('Password successfully changed.')

    def test_user_cannot_change_password_without_current_password(self):
        """Verifies User Accounts test case #U6."""

        self.log_in(self.email_user)
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
        self.log_in(self.email_user)

    def test_correct_user_info_is_shown(self):
        """Verifies User Accounts test case #U19."""

        self.log_in(self.email_user)
        self.go_to_profile()

        def assert_field(name, value):
            element = self.wd.BY_NAME(name)
            if element.tag_name == 'select':
                element = Select(element).first_selected_option
            actual_value = element.get_attribute('value')
            assert actual_value == value

        assert_field('username', self.email_user['username'])
        assert_field('email', self.email_user['email'])
        assert_field('full_name', self.email_user['full_name'])
        assert_field('language', self.email_user['language'])
        assert_field('measurement', self.email_user['measurement'])

    def test_user_cannot_update_profile_without_password(self):
        """Verifies User Accounts test case #U20."""

        self.log_in(self.email_user)
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
        self.log_in(self.email_user)

    def test_user_can_update_username(self):
        """Verifies User Accounts test case #U8."""

        self.log_in(self.email_user)
        self.go_to_profile()
        original_username = self.email_user['username']
        self.email_user['username'] = (
            TEST_TMP_USERNAME_FORMAT.format(random_string()))
        self.update_form_field('username', self.email_user['username'])
        self.invoke_update_profile()

        # Try to use the new username
        self.log_out()
        self.log_in(self.email_user)

        # [REVERSION]
        self.open('/account/profile/')
        self.email_user['username'] = original_username
        self.update_form_field('username', self.email_user['username'])
        self.invoke_update_profile()

    def test_user_can_update_email_address(self):
        """Verifies User Accounts test case #U9, #U21."""

        # Test case #U9
        self.log_in(self.email_user)
        self.open('/account/profile/')
        second_email = TEST_TMP_EMAIL_FORMAT.format(random_string())
        self.update_form_field('email', second_email)
        self.invoke_update_profile()

        self.wait_for_alert('Successfully updated profile information')
        self.wait_for_alert(
            'Confirmation email sent to {}.'.format(second_email))
        self.open('/account/profile/')
        assert (self.wd.BY_NAME('email').get_attribute('value') ==
                self.email_user['email'])
        self.wd.BY_XPATH(
            '//*[contains(@class, "form-group") and //*[@name="email"]]'
            '//*[contains(normalize-space(), '
            '"The email for this account has been changed recently")]')

        # Test case #U21
        self.open('/account/logout/')

        # Cannot login with the new email address
        self.update_form_field('login', second_email)
        self.update_form_field('password', self.email_user['password'])
        self.wd.BY_NAME('sign-in').click()
        self.wait_for_alert(
            'The e-mail address and/or password you specified are not '
            'correct.')

        # Can login with the old email address
        self.update_form_field('login', self.email_user['email'])
        self.update_form_field('password', self.email_user['password'])
        self.wd.BY_NAME('sign-in').click()
        self.wd.wait_for_xpath(
            USER_MENU_XPATH_FORMAT.format(self.email_user['full_name']))
        self.assert_url_path('/account/dashboard/')

    def test_user_can_update_phone_number(self):
        """Verifies User Accounts test case #U36, #U37."""

        # Test case #U36
        self.log_in(self.phone_user)
        self.open('/account/profile/')
        second_phone = random_us_number()
        self.update_form_field('phone', second_phone)
        self.update_form_field('password', self.phone_user['password'])
        self.click_update_profile_button()
        self.wait_for_alert('Successfully updated profile information')
        self.wait_for_alert(
            'Verification Token sent to {}'.format(second_phone))
        self.assert_url_path('/account/accountverification/')

        self.open('/account/profile/')
        assert (self.wd.BY_NAME('phone').get_attribute('value') ==
                self.phone_user['phone'])
        self.wd.BY_XPATH(
            '//*[contains(@class, "form-group") and //*[@name="phone"]]'
            '//*[contains(normalize-space(), '
            '"The phone for this account has been changed recently")]')

        # Test case #U37
        self.open('/account/logout/')

        # Cannot login with the new phone number
        self.update_form_field('login', second_phone)
        self.update_form_field('password', self.phone_user['password'])
        self.wd.BY_NAME('sign-in').click()
        self.wait_for_alert(
            'The username and/or password you specified are not correct.')

        # Can login with the old phone number
        self.update_form_field('login', self.phone_user['phone'])
        self.update_form_field('password', self.phone_user['password'])
        self.wd.BY_NAME('sign-in').click()
        self.wd.wait_for_xpath(
            USER_MENU_XPATH_FORMAT.format(self.phone_user['full_name']))
        self.assert_url_path('/account/dashboard/')

    def test_user_cannot_remove_email_address(self):
        """Verifies User Accounts test case #U55."""

        self.log_in(self.email_user)
        self.open('/account/profile/')
        self.update_form_field('email', '')
        self.update_form_field('password', self.email_user['password'])
        self.click_update_profile_button()
        self.assert_form_field_has_error('email', 'This field is required.')

        self.open('/account/profile/')
        assert (self.wd.BY_NAME('email').get_attribute('value') ==
                self.email_user['email'])

    def test_user_cannot_remove_phone_number(self):
        """Verifies User Accounts test case #U56."""

        self.log_in(self.phone_user)
        self.open('/account/profile/')
        self.update_form_field('phone', '')
        self.update_form_field('password', self.phone_user['password'])
        self.click_update_profile_button()
        self.assert_form_field_has_error('phone', 'This field is required.')

        self.open('/account/profile/')
        assert (self.wd.BY_NAME('phone').get_attribute('value') ==
                self.phone_user['phone'])

    def test_user_can_update_full_name(self):
        """Verifies User Accounts test case #U12."""

        self.log_in(self.email_user)
        self.go_to_profile()
        tmp_full_name = 'Temp Name'
        self.update_form_field('full_name', tmp_full_name)
        self.invoke_update_profile()
        self.wd.wait_for_xpath(USER_MENU_XPATH_FORMAT.format(tmp_full_name))

        # [REVERSION]
        self.open('/account/profile/')
        self.update_form_field('full_name', self.email_user['full_name'])
        self.invoke_update_profile()
        self.wd.wait_for_xpath(
            USER_MENU_XPATH_FORMAT.format(self.email_user['full_name']))

    def test_user_can_update_preferred_language(self):
        """Verifies User Accounts test case #U13."""

        self.log_in(self.email_user)
        self.go_to_profile()
        self.update_form_field('language', 'es')
        self.invoke_update_profile(
            alert_msg='La información del perfil se ha actualizado '
                      'correctamente')
        self.wd.BY_LINK('Proyectos')
        self.wd.BY_LINK('Organizaciones')

        # [REVERSION]
        self.open('/account/profile/')
        self.update_form_field('language', self.email_user['language'])
        self.invoke_update_profile(button_label='Guardar')
        self.wd.BY_LINK('Projects')
        self.wd.BY_LINK('Organizations')

    def test_user_can_update_preferred_measurement_system(self):
        """Verifies User Accounts test case #U14."""

        self.log_in(self.email_user)
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
        file_type_error_xpath = (
            avatar_form_group_xpath +
            '//*[normalize-space()="File type not allowed."]')

        self.log_in(self.email_user)
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
        self.wd.wait_until_clickable((By.CLASS_NAME, 'file-remove'))
        assert default_avatar_path not in img.get_attribute('src')
        self.invoke_update_profile()

        self.open('/account/profile/')
        img = self.wd.BY_XPATH(img_xpath)
        src = img.get_attribute('src')
        assert default_avatar_path not in src
        assert re.search('[a-z0-9]{24}\.jpg$', src)

        # Test case #U16
        self.open('/account/profile/')
        self.wd.BY_CLASS('file-remove').click()
        img = self.wd.BY_XPATH(img_xpath)
        assert default_avatar_path in img.get_attribute('src')
        self.wd.BY_XPATH(file_input_xpath).send_keys(
            join(files_dir_path, 'user_avatar_2.png'))
        self.wd.wait_until_clickable((By.CLASS_NAME, 'file-remove'))
        assert default_avatar_path not in img.get_attribute('src')
        self.invoke_update_profile()

        self.open('/account/profile/')
        img = self.wd.BY_XPATH(img_xpath)
        src = img.get_attribute('src')
        assert default_avatar_path not in src
        assert re.search('[a-z0-9]{24}\.png$', src)

        # [REVERSION] and test case #U18
        self.open('/account/profile/')
        self.wd.BY_CLASS('file-remove').click()
        self.invoke_update_profile()

        self.open('/account/profile/')
        img = self.wd.BY_XPATH(img_xpath)
        assert default_avatar_path in img.get_attribute('src')
