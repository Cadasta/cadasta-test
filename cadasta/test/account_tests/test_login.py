import pytest

from ..base_test import SeleniumTestCase
from ..util import random_string


class TestLogin(SeleniumTestCase):

    @pytest.fixture(autouse=True)
    def get_generic_user(self, generic_user):
        self.user = generic_user

    def test_user_can_login_by_username(self):
        """Verifies User Accounts test case #L1."""

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', self.user['username'])
        self.update_form_field('password', self.user['password'])
        self.wd.BY_NAME('sign-in').click()
        self.wd.wait_for_xpath(
            '//header//*[normalize-space()=""]'.format(self.user['full_name']))
        self.wait_for_alert(
            'Successfully signed in as {}.'.format(self.user['username']))

    def test_user_can_login_by_email(self):
        """Verifies User Accounts test case #L3."""

        self.wd.BY_LINK('Sign in').click()
        self.update_form_field('login', self.user['email'])
        self.update_form_field('password', self.user['password'])
        self.wd.BY_NAME('sign-in').click()
        self.wd.wait_for_xpath(
            '//header//*[normalize-space()=""]'.format(self.user['full_name']))
        self.wait_for_alert(
            'Successfully signed in as {}.'.format(self.user['username']))

    def test_user_cannot_log_in(self):
        """Verifies User Accounts test case #L2."""

        self.wd.BY_LINK('Sign in').click()

        msg = 'The username and/or password you specified are not correct.'

        self.update_form_field('login', self.user['username'])
        self.update_form_field('password', random_string())
        self.wd.BY_NAME('sign-in').click()
        self.wait_for_alert(msg)
        self.wd.BY_LINK('Sign in')
        self.wd.BY_LINK('Register')

        self.update_form_field('login', random_string())
        self.update_form_field('password', self.user['password'])
        self.wd.BY_NAME('sign-in').click()
        self.wait_for_alert(msg)
        self.wd.BY_LINK('Sign in')
        self.wd.BY_LINK('Register')

        msg = ('The e-mail address and/or password you specified are not '
               'correct.')

        self.update_form_field('login', self.user['email'])
        self.update_form_field('password', random_string())
        self.wd.BY_NAME('sign-in').click()
        self.wait_for_alert(msg)
        self.wd.BY_LINK('Sign in')
        self.wd.BY_LINK('Register')

        self.update_form_field('login', random_string() + '@cadasta.org')
        self.update_form_field('password', self.user['password'])
        self.wd.BY_NAME('sign-in').click()
        self.wait_for_alert(msg)
        self.wd.BY_LINK('Sign in')
        self.wd.BY_LINK('Register')
