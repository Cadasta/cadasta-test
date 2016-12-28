from django.test import LiveServerTestCase

class SeleniumTestCase(LiveServerTestCase):
    """
    A base test case for selenium, providing hepler methods for generating
    clients and logging in profiles.
    """
        
    def open(self, url):
        # print(self.live_server_url)
        # print (url)
        self.wd.get("%s%s" % ("https://platform-staging-api.cadasta.org", "/account/login/"))
        # self.wd.get("%s%s" % (self.live_server_url, url))