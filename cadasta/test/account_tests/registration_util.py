from selenium.common.exceptions import NoSuchElementException

from ..base_test import SeleniumTestCase


class RegistrationUtil(SeleniumTestCase):

    def click_register_button(self):
        button = self.wd.BY_NAME('register')
        self.scroll_element_into_view(button)
        button.click()

    def switch_to_email_or_phone(self, field):
        """ Email/phone field display is retained for each session and since we
        are reusing the WebDriver, we are not sure which of the two fields are
        displayed at the start of the test. Calling this method ensures that
        the field we are expecting is shown in the registration form. """

        assert field in ['email', 'phone']
        try:
            self.wd.BY_LINK(
                'I want to register with my {}'.format(field)).click()
        except NoSuchElementException:
            pass
