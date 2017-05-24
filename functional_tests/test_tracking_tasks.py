from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from .test_on_main_page import login


class TrackingTest(StaticLiveServerTestCase):

    fixtures = ['data_dump2.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        cls.selenium = webdriver \
            .Chrome("/home/maryan/programs/chromedriver/chromedriver",
                    chrome_options=options)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()

    def test_tracking_tasks(self):
        login(self)
        print("WAIt")
        self.selenium.implicitly_wait(10)
        pass
