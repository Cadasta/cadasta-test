import pytest

from ..base_test import SeleniumTestCase
from ..util import random_string, random_us_number
from .registration_util import RegistrationUtil


@pytest.mark.batch1
class TestLogin(RegistrationUtil, SeleniumTestCase):

    @pytest.fixture(autouse=True)
    def get_generic_user(self, generic_user, generic_phone_user):
        self.email_user = generic_user
        self.phone_user = generic_phone_user

    @pytest.fixture
    def throwaway_user(self):
        return {
            'username': 'functest_tmp_{}'.format(random_string()),
            'email': 'evillar+tmp_{}@cadasta.org'.format(random_string()),
            'phone': random_us_number(),
            'password': 'XYZ#qwerty',
            'full_name': 'John Lennon',
        }

    # ------ Utility functions ------

    def check_login_failure(self, label):
        self.wd.BY_NAME('sign-in').click()
        self.wait_for_alert(
            'The {} and/or password you specified are not correct.'.format(
                label))
        self.wd.BY_LINK('Sign in')
        self.wd.BY_LINK('Register')

    def check_unverified_login_failure(self):
        self.wd.BY_NAME('sign-in').click()
        self.wait_for_alert(
            'You have not verified your phone or email. We request you to '
            'verify your registered phone or email in order to access your '
            'account.')
        self.wd.BY_LINK('Sign in')
        self.wd.BY_LINK('Register')
        self.assert_url_path('/account/resendtokenpage/')

    # ------ Test cases ------

    def test_user_can_login_by_username(self):
        """Verifies User Accounts test case #L1, #L4"""

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', self.email_user['username'])
        self.update_form_field('password', self.email_user['password'])
        self.wd.BY_NAME('sign-in').click()
        self.wd.wait_for_xpath(
            '//header//*[contains(., "{}")]'.format(
                self.email_user['full_name']))
        self.wait_for_alert(
            'Successfully signed in as {}.'.format(
                self.email_user['username']))
        self.assert_url_path('/account/dashboard/')

    def test_user_can_login_by_email_address(self):
        """Verifies User Accounts test case #L3, #L4"""

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', self.email_user['email'])
        self.update_form_field('password', self.email_user['password'])
        self.wd.BY_NAME('sign-in').click()
        self.wd.wait_for_xpath(
            '//header//*[contains(., "{}")]'.format(
                self.email_user['full_name']))
        self.wait_for_alert(
            'Successfully signed in as {}.'.format(
                self.email_user['username']))
        self.assert_url_path('/account/dashboard/')

    def test_user_can_login_by_phone_number(self):
        """Verifies User Accounts test case #L5, #L4"""

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', self.phone_user['phone'])
        self.update_form_field('password', self.phone_user['password'])
        self.wd.BY_NAME('sign-in').click()
        self.wd.wait_for_xpath(
            '//header//*[contains(., "{}")]'.format(
                self.phone_user['full_name']))
        self.wait_for_alert(
            'Successfully signed in as {}.'.format(
                self.phone_user['username']))
        self.assert_url_path('/account/dashboard/')

    def test_user_cannot_log_in_with_correct_username_wrong_password(self):
        """Verifies User Accounts test case #L2."""

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', self.email_user['username'])
        self.update_form_field('password', random_string())
        self.check_login_failure('username')

    def test_user_cannot_log_in_with_wrong_username_correct_password(self):
        """Verifies User Accounts test case #L6."""

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', random_string())
        self.update_form_field('password', self.email_user['password'])
        self.check_login_failure('username')

    def test_user_cannot_log_in_with_correct_email_wrong_password(self):
        """Verifies User Accounts test case #L7."""

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', self.email_user['email'])
        self.update_form_field('password', random_string())
        self.check_login_failure('e-mail address')

    def test_user_cannot_log_in_with_wrong_email_correct_password(self):
        """Verifies User Accounts test case #L8."""

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', random_string() + '@cadasta.org')
        self.update_form_field('password', self.email_user['password'])
        self.check_login_failure('e-mail address')

    def test_user_cannot_log_in_with_correct_phone_wrong_password(self):
        """Verifies User Accounts test case #L9."""

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', self.phone_user['phone'])
        self.update_form_field('password', random_string())
        self.check_login_failure('username')

    def test_user_cannot_log_in_with_wrong_phone_correct_password(self):
        """Verifies User Accounts test case #L10."""

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', random_us_number())
        self.update_form_field('password', self.phone_user['password'])
        self.check_login_failure('username')

    def test_user_cannot_log_in_with_unverified_email_address(
        self, throwaway_user
    ):
        """Verifies User Accounts test case #L11."""

        # Register throwaway user account
        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('email')
        self.update_form_field('username', throwaway_user['username'])
        self.update_form_field('email', throwaway_user['email'])
        self.update_form_field('password', throwaway_user['password'])
        self.update_form_field('full_name', throwaway_user['full_name'])
        self.click_register_button()

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', throwaway_user['email'])
        self.update_form_field('password', throwaway_user['password'])
        self.check_unverified_login_failure()

    def test_user_cannot_log_in_with_unverified_phone_number(
        self, throwaway_user
    ):
        """Verifies User Accounts test case #L11."""

        # Register throwaway user account
        self.wd.BY_LINK('Register').click()
        self.switch_to_email_or_phone('phone')
        self.update_form_field('username', throwaway_user['username'])
        self.update_form_field('phone', throwaway_user['phone'])
        self.update_form_field('password', throwaway_user['password'])
        self.update_form_field('full_name', throwaway_user['full_name'])
        self.click_register_button()

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', throwaway_user['phone'])
        self.update_form_field('password', throwaway_user['password'])
        self.check_unverified_login_failure()
