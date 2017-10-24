import pytest

from ..base_test import SeleniumTestCase
from ..util import random_string


class TestRegistration(SeleniumTestCase):

    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        self.username = 'functest_tmp_{}'.format(random_string())
        self.email = 'evillar+tmp_{}@cadasta.org'.format(random_string())
        self.password = 'XYZ#qwerty'
        self.full_name = 'John Lennon'

    def click_register_button(self):
        button = self.wd.BY_NAME('register')
        self.scroll_element_into_view(button)
        button.click()

    def test_user_can_create_account(self):
        """Verifies User Accounts test case #R1."""

        self.wd.BY_LINK('Register').click()
        self.update_form_field('username', self.username)
        self.update_form_field('email', self.email)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.wait_for_alert(
            'Confirmation email sent to {}'.format(self.email))
        self.assert_url_path('/account/accountverification/')

    def test_show_password_button_works(self):
        """Verifies User Accounts test case #R2."""

        self.wd.BY_LINK('Register').click()
        password_input = self.wd.BY_NAME('password')
        password_input.send_keys(self.password)
        button = self.wd.BY_XPATH(
            '//*[contains(@class, "form-group") and '
            '    //*[@name="password"]]//button'
        )
        button.click()
        assert password_input.get_attribute('type') == 'text'
        button.click()
        assert password_input.get_attribute('type') == 'password'

    def test_username_is_required(self):
        """Verifies User Accounts test case #R6."""

        self.wd.BY_LINK('Register').click()
        self.update_form_field('email', self.email)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error('username', 'This field is required.')

    def test_username_must_be_unique(self, generic_user):
        """Verifies User Accounts test case #R7."""

        self.wd.BY_LINK('Register').click()
        self.update_form_field('username', generic_user['username'])
        self.update_form_field('email', self.email)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error(
            'username', 'A user with that username already exists')

    def test_username_format_is_validated(self):
        """Verifies User Accounts test case #R8."""

        self.wd.BY_LINK('Register').click()
        self.update_form_field('email', self.email)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        username_input = self.wd.BY_NAME('username')
        username_input.send_keys('1234567890' * 20)
        assert username_input.get_attribute('value') == '1234567890' * 15
        username_input.clear()
        username_input.send_keys('with space')
        self.click_register_button()
        self.assert_form_field_has_error(
            'username',
            'Enter a valid username. This value may contain '
            'only letters, numbers, and @/./+/-/_ characters.')

    def test_email_address_is_required(self):
        """Verifies User Accounts test case #R9."""

        self.wd.BY_LINK('Register').click()
        self.update_form_field('username', self.username)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error('email', 'This field is required.')

    def test_email_address_must_be_unique(self, generic_user):
        """Verifies User Accounts test case #R10."""

        self.wd.BY_LINK('Register').click()
        self.update_form_field('username', self.username)
        self.update_form_field('email', generic_user['email'])
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error(
            'email', 'User with this Email address already exists.')

    def test_email_address_format_is_validated(self):
        """Verifies User Accounts test case #R11."""

        self.wd.BY_LINK('Register').click()
        self.update_form_field('username', self.username)
        self.update_form_field('email', 'invalid')
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error(
            'email', 'This field should be a valid email.')

    def test_password_is_required(self):
        """Verifies User Accounts test case #R12."""

        self.wd.BY_LINK('Register').click()
        self.update_form_field('username', self.username)
        self.update_form_field('email', self.email)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error('password', 'This field is required.')

    def test_password_format_is_validated(self):
        """Verifies User Accounts test case #R13."""

        self.wd.BY_LINK('Register').click()
        self.update_form_field('username', self.username)
        self.update_form_field('email', self.email)
        self.update_form_field('full_name', self.full_name)

        password_help = self.wd.BY_XPATH(
            '(//*[@for="id_password"])[1]/following-sibling::p')
        assert 'hidden' in password_help.get_attribute('class')
        password_input = self.wd.BY_NAME('password')
        password_input.click()
        assert 'hidden' not in password_help.get_attribute('class')

        password_input.send_keys('Aa1+')
        self.click_register_button()
        self.assert_form_field_has_error(
            'password',
            'This field is too short. It should have 10 characters or more.')

        error_msg = (
            'Your password must contain at least 3 of the following: '
            'lowercase characters, uppercase characters, special characters, '
            'and/or numerical characters.')

        def check_invalid_password(password):
            password_input.clear()
            password_input.send_keys(password)
            self.click_register_button()
            self.assert_form_field_has_error('password', error_msg)

        check_invalid_password('ABCDEFGHIJ')
        check_invalid_password('abcdefghij')
        check_invalid_password('1234567890')
        check_invalid_password('!@#$%^&*()')
        check_invalid_password('ABCDEabcde')
        check_invalid_password('ABCDE12345')
        check_invalid_password('ABCDE!@#$%')
        check_invalid_password('abcde12345')
        check_invalid_password('abcde!@#$%')
        check_invalid_password('12345!@#$%')

    def test_password_must_not_contain_username(self):
        """Verifies User Accounts test case #R14."""

        self.wd.BY_LINK('Register').click()
        self.update_form_field('username', self.username)
        self.update_form_field('email', self.email)
        self.update_form_field('password', self.password + self.username)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error(
            'password', 'Your password cannot contain your username.')

    def test_password_must_not_contain_email_username(self):
        """Verifies User Accounts test case #R15."""

        self.wd.BY_LINK('Register').click()
        self.update_form_field('username', self.username)
        self.update_form_field('email', self.email)
        email_username = self.email.split('@')[0]
        self.update_form_field('password', self.password + email_username)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error(
            'password',
            'Your password cannot contain your email mailbox name.')

    def test_full_name_is_not_required(self):
        """Verifies User Accounts test case #R16."""

        self.wd.BY_LINK('Register').click()
        self.update_form_field('username', self.username)
        self.update_form_field('email', self.email)
        self.update_form_field('password', self.password)
        self.click_register_button()
        self.wait_for_alert(
            'Confirmation email sent to {}'.format(self.email))
        self.assert_url_path('/account/accountverification/')

    def test_user_can_select_another_language(self):
        """Verifies User Accounts test case #R17."""

        self.wd.BY_LINK('Register').click()
        self.update_form_field('username', self.username)
        self.update_form_field('email', self.email)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.update_form_field('language', 'es')
        self.click_register_button()
        self.wait_for_alert(
            'Correo de confirmación enviado a {}'.format(self.email))
        self.assert_url_path('/account/accountverification/')
        self.wd.BY_LINK('Registro')
        self.wd.BY_LINK('Iniciar sesión')
