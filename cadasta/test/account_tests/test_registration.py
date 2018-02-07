import pytest

from selenium.common.exceptions import NoSuchElementException, TimeoutException

from ..base_test import SeleniumTestCase
from ..util import random_string, random_us_number
from .registration_util import RegistrationUtil


@pytest.mark.batch1
class TestRegistration(RegistrationUtil, SeleniumTestCase):

    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        self.username = 'functest_tmp_{}'.format(random_string())
        self.email = 'evillar+tmp_{}@cadasta.org'.format(random_string())
        self.phone = random_us_number()
        self.password = 'XYZ#qwerty'
        self.full_name = 'John Lennon'

    # ------ Test cases ------

    def test_user_can_create_account_using_email(self):
        """Verifies User Accounts test case #R1."""

        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('email')
        self.update_form_field('username', self.username)
        self.update_form_field('email', self.email)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.wait_for_alert(
            'We have created your account. You should have received an email '
            'or a text to verify your account.')
        self.wait_for_alert(
            'Confirmation email sent to {}'.format(self.email))
        self.wd.BY_LINK('Sign in')
        self.wd.BY_LINK('Register')
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

    def test_phone_email_switcher_works(self):
        """Verifies User Accounts test case #R18."""

        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('email')
        assert self.wd.BY_NAME('email').is_displayed()
        assert not self.wd.BY_NAME('phone').is_displayed()
        self.wd.BY_LINK('I want to register with my phone').click()
        assert not self.wd.BY_NAME('email').is_displayed()
        assert self.wd.BY_NAME('phone').is_displayed()
        self.wd.BY_LINK('I want to register with my email').click()
        assert self.wd.BY_NAME('email').is_displayed()
        assert not self.wd.BY_NAME('phone').is_displayed()

    def test_user_can_create_account_using_phone(self):
        """Verifies User Accounts test case #R19."""

        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('phone')
        self.update_form_field('username', self.username)
        self.update_form_field('phone', self.phone)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.wait_for_alert(
            'We have created your account. You should have received an email '
            'or a text to verify your account.')
        self.wait_for_alert(
            'Verification token sent to {}'.format(self.phone))
        self.wd.BY_LINK('Sign in')
        self.wd.BY_LINK('Register')
        self.assert_url_path('/account/accountverification/')

    def test_username_is_required(self):
        """Verifies User Accounts test case #R6."""

        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('email')
        self.update_form_field('email', self.email)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error('username', 'This field is required.')

    def test_username_must_be_unique(self, generic_user):
        """Verifies User Accounts test case #R7."""

        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('email')
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
        self.switch_to_email_or_phone('email')
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
        self.switch_to_email_or_phone('email')
        self.update_form_field('username', self.username)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error('email', 'This field is required.')

    def test_email_address_must_be_unique(self, generic_user):
        """Verifies User Accounts test case #R10."""

        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('email')
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
        self.switch_to_email_or_phone('email')
        self.update_form_field('username', self.username)
        self.update_form_field('email', 'invalid')
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error(
            'email', 'This field should be a valid email.')

    def test_phone_number_is_required(self):
        """Verifies User Accounts test case #R23."""

        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('phone')
        self.update_form_field('username', self.username)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error('phone', 'This field is required.')

    def test_phone_number_must_be_unique(self, generic_phone_user):
        """Verifies User Accounts test case #R24."""

        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('phone')
        self.update_form_field('username', self.username)
        self.update_form_field('phone', generic_phone_user['phone'])
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error(
            'phone', 'User with this Phone number already exists.')

    def test_phone_number_format_is_validated(self):
        """Verifies User Accounts test case #R25."""

        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('phone')
        self.update_form_field('username', self.username)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)

        phone_input = self.wd.BY_NAME('phone')
        error_msg = (
            'Phone numbers must start with a +, followed by a country code '
            'and phone number without spaces or punctuation. Phone numbers '
            'must contain between 5 and 15 digits.')

        def check_invalid_phone(phone):
            phone_input.clear()
            phone_input.send_keys(phone)
            self.click_register_button()
            self.assert_form_field_has_error('phone', error_msg)

        check_invalid_phone('invalid')
        check_invalid_phone('1')
        check_invalid_phone('11111')
        check_invalid_phone('111111')
        check_invalid_phone('11111111111111111111')
        check_invalid_phone('+')
        check_invalid_phone('+1')
        check_invalid_phone('+11111111111111111111')

    def test_password_is_required(self):
        """Verifies User Accounts test case #R12."""

        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('email')
        self.update_form_field('username', self.username)
        self.update_form_field('email', self.email)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error('password', 'This field is required.')

    def test_password_format_is_validated(self):
        """Verifies User Accounts test case #R13."""

        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('email')
        self.update_form_field('username', self.username)
        self.update_form_field('email', self.email)
        self.update_form_field('full_name', self.full_name)

        password_input = self.wd.BY_NAME('password')
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
        self.switch_to_email_or_phone('email')
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
        self.switch_to_email_or_phone('email')
        self.update_form_field('username', self.username)
        self.update_form_field('email', self.email)
        email_username = self.email.split('@')[0]
        self.update_form_field('password', self.password + email_username)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()
        self.assert_form_field_has_error(
            'password',
            'Your password cannot contain your email mailbox name.')

    def test_password_must_not_contain_phone_number(self):
        """Verifies User Accounts test case #R26."""

        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('phone')
        self.update_form_field('username', self.username)
        self.update_form_field('phone', self.phone)
        self.update_form_field('full_name', self.full_name)

        def check_invalid_password(password):
            password_input = self.wd.BY_NAME('password')
            password_input.clear()
            password_input.send_keys(password)
            self.click_register_button()
            self.assert_form_field_has_error(
                'password', 'Passwords cannot contain your phone.')

        check_invalid_password('A' + self.phone)
        check_invalid_password('A#' + self.phone[1:])
        check_invalid_password('A#' + self.phone[2:])

    def test_full_name_is_not_required(self):
        """Verifies User Accounts test case #R16."""

        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('email')
        self.update_form_field('username', self.username)
        self.update_form_field('email', self.email)
        self.update_form_field('password', self.password)
        self.click_register_button()
        self.wait_for_alert(
            'We have created your account. You should have received an email '
            'or a text to verify your account.')
        self.wait_for_alert(
            'Confirmation email sent to {}'.format(self.email))
        self.wd.BY_LINK('Sign in')
        self.wd.BY_LINK('Register')
        self.assert_url_path('/account/accountverification/')

    def test_user_can_select_another_language(self):
        """Verifies User Accounts test case #R17."""

        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('email')
        self.update_form_field('username', self.username)
        self.update_form_field('email', self.email)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.update_form_field('language', 'es')
        self.click_register_button()
        # TODO: This message is not yet translated
        # self.wait_for_alert(
        #     'We have created your account. You should have received an '
        #     'email or a text to verify your account.')
        self.wait_for_alert(
            'Correo de confirmación enviado a {}'.format(self.email))
        self.wd.BY_LINK('Registro')
        self.wd.BY_LINK('Iniciar sesión')
        self.assert_url_path('/account/accountverification/')

        # Revert back to English UI
        self.update_form_field('language', 'en')

    def test_user_can_invoke_resending_of_confirmation_email(self):
        """Verifies User Accounts test case #R27."""

        # Register throwaway user account
        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('email')
        self.update_form_field('username', self.username)
        self.update_form_field('email', self.email)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', self.email)
        self.update_form_field('password', self.password)
        self.wd.BY_NAME('sign-in').click()

        try:
            self.wd.BY_LINK('I want to verify my email').click()
        except NoSuchElementException:
            pass
        self.update_form_field('email', self.email)
        self.wd.BY_XPATH('//button[contains(.,"Send Verification")]').click()

        self.wait_for_alert(
            'Your email address has been submitted. If it matches your '
            'account on Cadasta Platform, you will receive a verification '
            'link to confirm your email.')
        try:
            self.wait_for_alert(
                'Confirmation email sent to {}.'.format(self.email))
            raise AssertionError('Confirmation email alert is shown.')
        except TimeoutException:
            pass
        self.wd.BY_XPATH('//h1[contains(.,"Account Verification")]')
        try:
            self.wd.BY_NAME('token').click()
            raise AssertionError('Token field is shown.')
        except NoSuchElementException:
            pass
        self.assert_url_path('/account/accountverification/')

    def test_user_can_invoke_resending_of_verification_token(self):
        """Verifies User Accounts test case #R31."""

        # Register throwaway user account
        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('phone')
        self.update_form_field('username', self.username)
        self.update_form_field('phone', self.phone)
        self.update_form_field('password', self.password)
        self.update_form_field('full_name', self.full_name)
        self.click_register_button()

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', self.phone)
        self.update_form_field('password', self.password)
        self.wd.BY_NAME('sign-in').click()

        try:
            self.wd.BY_LINK('I want to verify my phone').click()
        except NoSuchElementException:
            pass
        self.update_form_field('phone', self.phone)
        self.wd.BY_XPATH('//button[contains(.,"Send Verification")]').click()

        self.wait_for_alert(
            'Your phone number has been submitted. If it matches your '
            'account on Cadasta Platform, you will receive a verification '
            'token to confirm your phone.')
        self.wd.BY_XPATH('//h1[contains(.,"Account Verification")]')
        self.wd.BY_NAME('token').click()
        self.assert_url_path('/account/accountverification/')
