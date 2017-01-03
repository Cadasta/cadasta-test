from django.test import LiveServerTestCase

class SeleniumTestCase(LiveServerTestCase):
    """
    A base test case for selenium, providing hepler methods for generating
    clients and logging in profiles.
    """
    live_server_url = "https://platform-staging-api.cadasta.org"

    def open(self, url):
        # print (url)
        self.wd.get("%s%s" % (self.live_server_url, url))


    def user_login(self):
        self.open("/account/login/")
        self.wd.find_css('#id_login').send_keys("cadasta-test-user1")
        self.wd.find_css("#id_password").send_keys('XYZ#qwerty')
        self.wd.find_element_by_xpath('//button[@name="sign-in"]').click()
        self.wd.find_elements_by_xpath("//span[contains(text(), 'cadasta-test-user1')]")
