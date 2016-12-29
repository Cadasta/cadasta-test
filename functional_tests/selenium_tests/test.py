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