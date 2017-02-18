import os
from selenium_tests.test import SeleniumTestCase
from selenium_tests.webdriver import CustomWebDriver
from selenium_tests.pages import ProjectsPage


class AddResourceType(SeleniumTestCase):

    def setUp(self):
        self.wd = CustomWebDriver()

    def test_add_csv_resource(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        self.wd.find_element_by_link_text("Attach").click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        path = os.path.abspath("resources/csv_file.csv")
        try :
            self.wd.find_element_by_xpath("//*[contains(text(), 'Select the file to upload')]")
        except :
            self.wd.find_element_by_link_text("Upload new").click()
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector("input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("csv-resource-1")
        self.wd.wait_for_xpath("//a[@class='file-link']")
        self.wd.find_element_by_name("submit").click()

        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        assert self.wd.find_element_by_xpath('//td/div/p/a/strong[contains(text(), "csv-resource-1")]')

    def test_add_doc_resource(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        self.wd.find_element_by_link_text("Attach").click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        path = os.path.abspath("resources/doc_file.doc")
        try :
            self.wd.find_element_by_xpath("//*[contains(text(), 'Select the file to upload')]")
        except :
            self.wd.find_element_by_link_text("Upload new").click()
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector("input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("doc-resource-1")
        self.wd.wait_for_xpath("//a[@class='file-link']")
        self.wd.find_element_by_name("submit").click()

        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        assert self.wd.find_element_by_xpath('//td/div/p/a/strong[contains(text(), "doc-resource-1")]')

    def test_add_docx_resource(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        self.wd.find_element_by_link_text("Attach").click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        path = os.path.abspath("resources/docx_file.docx")
        try :
            self.wd.find_element_by_xpath("//*[contains(text(), 'Select the file to upload')]")
        except :
            self.wd.find_element_by_link_text("Upload new").click()
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector("input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("docx-resource-1")
        self.wd.wait_for_xpath("//a[@class='file-link']")
        self.wd.find_element_by_name("submit").click()

        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        assert self.wd.find_element_by_xpath('//td/div/p/a/strong[contains(text(), "docx-resource-1")]')

    def test_add_jpg_resource(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        self.wd.find_element_by_link_text("Attach").click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        path = os.path.abspath("resources/jpg_file.jpg")
        try :
            self.wd.find_element_by_xpath("//*[contains(text(), 'Select the file to upload')]")
        except :
            self.wd.find_element_by_link_text("Upload new").click()
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector("input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("jpg-resource-1")
        self.wd.wait_for_xpath("//a[@class='file-link']")
        self.wd.find_element_by_name("submit").click()

        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        assert self.wd.find_element_by_xpath('//td/div/p/a/strong[contains(text(), "jpg-resource-1")]')

    def test_add_mp3_resource(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        self.wd.find_element_by_link_text("Attach").click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        path = os.path.abspath("resources/mp3_file.mp3")
        try :
            self.wd.find_element_by_xpath("//*[contains(text(), 'Select the file to upload')]")
        except :
            self.wd.find_element_by_link_text("Upload new").click()
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector("input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("mp3-resource-1")
        self.wd.wait_for_xpath("//a[@class='file-link']")
        self.wd.find_element_by_name("submit").click()

        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        assert self.wd.find_element_by_xpath('//td/div/p/a/strong[contains(text(), "mp3-resource-1")]')

    def test_add_mp4_resource(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        self.wd.find_element_by_link_text("Attach").click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        path = os.path.abspath("resources/mp4_file.mp4")
        try :
            self.wd.find_element_by_xpath("//*[contains(text(), 'Select the file to upload')]")
        except :
            self.wd.find_element_by_link_text("Upload new").click()
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector("input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("mp4-resource-1")
        self.wd.wait_for_xpath("//a[@class='file-link']")
        self.wd.find_element_by_name("submit").click()

        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        assert self.wd.find_element_by_xpath('//td/div/p/a/strong[contains(text(), "mp4-resource-1")]')

    def test_add_png_resource(self):
        projects_page = ProjectsPage(self.wd, self)
        projects_page.go_to()

        self.wd.find_element_by_link_text("project-1").click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Project Overview')]")
        self.wd.find_element_by_xpath('//div[@id="sidebar"]/ul/li[@class="resources"]/a').click()
        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        self.wd.find_element_by_link_text("Attach").click()

        self.wd.switch_to_window(self.wd.window_handles[-1])
        path = os.path.abspath("resources/png_file.png")
        try :
            self.wd.find_element_by_xpath("//*[contains(text(), 'Select the file to upload')]")
        except :
            self.wd.find_element_by_link_text("Upload new").click()
        self.wd.find_element_by_css_selector("input.file-input").clear()
        self.wd.find_element_by_css_selector("input.file-input").send_keys(path)
        self.wd.find_element_by_id("id_name").clear()
        self.wd.find_element_by_id("id_name").send_keys("png-resource-1")
        self.wd.wait_for_xpath("//a[@class='file-link']")
        self.wd.find_element_by_name("submit").click()

        self.wd.wait_for_xpath("//h2[contains(text(), 'Resources')]")
        assert self.wd.find_element_by_xpath('//td/div/p/a/strong[contains(text(), "png-resource-1")]')

    def tearDown(self):
        self.wd.quit()

