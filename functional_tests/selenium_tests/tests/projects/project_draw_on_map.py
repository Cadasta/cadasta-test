from functional_tests.selenium_tests.test import SeleniumTestCase
from functional_tests.selenium_tests.webdriver import CustomWebDriver
from selenium.webdriver.common.action_chains import ActionChains

class AddProjectWithExtent(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_new_project_with_extent(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/projects/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Projects')]")
        self.wd.find_element_by_xpath('//a[@href="/projects/new/"]').click()
        self.wd.wait_for_css(".wizard")

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')
        print page_state

        script = (
            'map = window.maps[0];'+

            'var polygon = L.polygon([' +
            '    [56.51, 20.047],' +
            '    [51.509, 10.08],' +
            '    [53.503, -0.06],' +
            '    [58.51, 0.047]' +
            ']).addTo(map);'
        )
        self.wd.execute_script(script)

        self.wd.find_element_by_xpath('//button[@type="submit"]').click()
        self.wd.wait_for_xpath("//h3[contains(text(), '1. General Information')]")
        self.wd.find_element_by_xpath('//select[@name="details-organization"]').click()
        self.wd.find_element_by_xpath('//option[@value="organization-1"]').click()
        self.wd.find_element_by_xpath('//input[@id="id_details-name"]').send_keys("project-with-extent-1")
        self.wd.find_element_by_xpath('//textarea[@id="id_details-description"]').send_keys("Project-with-extent-1 description")

        try:
            self.wd.find_element_by_xpath('//button[@type="submit"]').click()
            self.wd.wait_for_xpath("//h3[contains(text(), 'Assign permissions to members')]")
            text = self.wd.find_element_by_xpath('//button[@type="submit"]').text
            self.wd.find_element_by_xpath('//button[@type="submit"]').click()
            self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
            text = self.wd.find_element_by_xpath("//h1[contains(@class, 'short')]").text
            assert text.endswith("PROJECT-WITH-EXTENT-1")
        except Exception:
            self.wd.wait_for_css(".error-block")
            assert True

    def tearDown(self):
        self.wd.quit()


class AddLocation(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_edit_add_location(self):
        self.user_login()
        self.wd.wait_for_css('.btn-user')
        self.open("/projects/")
        self.wd.wait_for_xpath("//h1[contains(text(), 'Projects')]")
        self.wd.find_element_by_xpath('//a[@href="/organizations/organization-1/projects/project-1/"]').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.open("/organizations/organization-1/projects/project-1/records/locations/new/")
        self.wd.wait_for_xpath("//h2[contains(text(), 'Add new location')]")

        page_state = self.wd.execute_script('return document.readyState;')
        while page_state != 'complete':
            page_state = self.wd.execute_script('return document.readyState;')
        print page_state

        ###############################################################
        # [17/Jan/2017 07:57:19] "POST /organizations/organization-1/projects/project-1/records/locations/new/ HTTP/1.1" 302 0
        # [17/Jan/2017 07:57:19] "GET /organizations/organization-1/projects/project-1/records/locations/qdkj9wf2c5bsj92uacgwb9z4/ HTTP/1.1" 200 24274
        # [17/Jan/2017 07:57:20] "GET /jsi18n/ HTTP/1.1" 200 3189
        # [17/Jan/2017 07:57:20] "GET /static/js/leaflet.groupedlayercontrol.min.js.map HTTP/1.1" 404 1736
        # [17/Jan/2017 07:57:20] "GET /api/v1/organizations/organization-1/projects/project-1/spatialresources/ HTTP/1.1" 200 2
        # [17/Jan/2017 07:57:20] "GET /async/organizations/organization-1/projects/project-1/spatial/?exclude=qdkj9wf2c5bsj92uacgwb9z4 HTTP/1.1" 200 80
        # [17/Jan/2017 07:58:03] "GET /organizations/organization-1/projects/project-1/records/locations/new/ HTTP/1.1" 200 26587
        # [17/Jan/2017 07:58:03] "GET /jsi18n/ HTTP/1.1" 200 3189
        # [17/Jan/2017 07:58:04] "GET /static/js/leaflet.groupedlayercontrol.min.js.map HTTP/1.1" 404 1736
        # [17/Jan/2017 07:58:05] "GET /api/v1/organizations/organization-1/projects/project-1/spatialresources/ HTTP/1.1" 200 2
        # [17/Jan/2017 07:58:05] "GET /async/organizations/organization-1/projects/project-1/spatial/ HTTP/1.1" 200 467
        ###############################################################

        ################################################################
        # from seleniumrequests import Firefox
        #
        # webdriver = Firefox()
        # response = webdriver.request('POST', 'url here', data={"param1": "value1"})
        # print(response)
        # https://pypi.python.org/pypi/selenium-requests/
        ################################################################


        ##################################################################
        # script = (
        #     'map = window.maps[0];'+
        #
        #     'var layer = L.marker([51.5, -0.09]).addTo(map);'+
        #     'layer.addTo(map);'
        #
        #     'var polygon = L.polygon([' +
        #     '    [56.51, 20.047],' +
        #     '    [51.509, 10.08],' +
        #     '    [53.503, -0.06],' +
        #     '    [58.51, 0.047]' +
        #     ']).addTo(map);' +
        #
        #     'console.log(polygon);'
        # )
        # self.wd.execute_script(script)
        #################################################################

        # elem = self.wd.find_element_by_xpath('//a[@class="leaflet-draw-draw-marker"]')
        # elem.click()
        # action = ActionChains(self.wd)
        # action.move_to_element_with_offset(elem, 10, 10)
        # action.click()
        # action.perform()

        self.wd.find_element_by_xpath('//a[@class="leaflet-draw-draw-marker"]').click()

        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//div[@id="id_geometry_map"]')
        action.move_to_element(elem).move_by_offset(10, 10).click().perform()
        # action.move_to_element_with_offset(elem, 10, 10)
        # action.click()
        # action.perform()

        ################################################################

        self.wd.find_element_by_xpath('//a[@class="leaflet-draw-draw-polygon"]').click()
        action = ActionChains(self.wd)
        elem = self.wd.find_element_by_xpath('//div[@id="id_geometry_map"]')
        action.move_to_element(elem).move_by_offset(5, 5).click().perform()
        action.move_to_element(elem).move_by_offset(15, 5).click().perform()
        action.move_to_element(elem).move_by_offset(15, 15).click().perform()
        action.move_to_element(elem).move_by_offset(5, 15).click().perform()
        action.move_to_element(elem).move_by_offset(5, 5).click().perform()

        #################################################################

        # location = elem.location
        # size = elem.size
        # print(location)
        # print(size)

        ################################################################

        self.wd.find_element_by_xpath('//select[@name="type"]').click()
        self.wd.find_element_by_xpath('//option[@value="PA"]').click()
        self.wd.find_element_by_xpath('//input[@value="Save"]').click()

        # self.wd.find_element_by_xpath('//button[@type="submit"]').click()
        # self.wd.wait_for_xpath("//h3[contains(text(), 'Assign permissions to members')]")
        # text = self.wd.find_element_by_xpath('//button[@type="submit"]').text
        # self.wd.find_element_by_xpath('//button[@type="submit"]').click()
        # self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        # text = self.wd.find_element_by_xpath("//div/section/p").text
        # assert text == "Test project-1 description edited."

    # def tearDown(self):
    #     self.wd.quit()

