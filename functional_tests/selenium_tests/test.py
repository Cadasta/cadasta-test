from django.test import LiveServerTestCase

class SeleniumTestCase(LiveServerTestCase):
    """
    A base test case for selenium, providing hepler methods for generating
    clients and logging in profiles.
    """
    # live_server_url = "https://platform-staging-api.cadasta.org"
    live_server_url = "http://localhost:8000"

    def open(self, url):
        # print (url)
        self.wd.get("%s%s" % (self.live_server_url, url))

    def user_login(self):
        self.open("/account/login/")
        self.wd.find_css('#id_login').send_keys("cadasta-test-user1")
        self.wd.find_css("#id_password").send_keys('XYZ#qwerty')
        self.wd.find_element_by_xpath('//button[@name="sign-in"]').click()
        self.wd.find_elements_by_xpath("//span[contains(text(), 'cadasta-test-user1')]")

    def restore_password(self, password, changedPassword):
        self.open("/account/password/change/")
        self.wd.find_css('#id_oldpassword').send_keys(changedPassword)
        self.wd.find_css('#id_password1').send_keys(password)
        self.wd.find_css('#id_password2').send_keys(password)
        self.wd.find_elements_by_xpath("//button[contains(text(), 'Change password')]")[0].click()

    def restore_username(self, username):
        self.open("/account/profile/")
        self.wd.find_css('#id_username').clear()
        self.wd.find_css('#id_username').send_keys(username)
        self.wd.find_element_by_xpath('//button[@name="update"]').click()

    def restore_fullname(self, fullname):
        self.open("/account/profile/")
        self.wd.find_css('#id_full_name').clear()
        self.wd.find_css('#id_full_name').send_keys(fullname)
        self.wd.find_element_by_xpath('//button[@name="update"]').click()

