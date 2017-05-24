from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys


class MainTest(StaticLiveServerTestCase):

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

    def test_main(self):
        login(self)

        # Check if user email present
        email_span = self.selenium \
            .find_element_by_xpath("/html/body/div/div/div/header/span[2]")
        self.assertEqual(email_span.text, "user@test.com")

        # Check for 9 tasks card
        tasks = self.selenium.find_elements_by_class_name("mdl-card")
        self.assertEqual(len(tasks), 9)

        # Scrolling bottom to see all tasks
        # wait = WebDriverWait(self.selenium, 5)
        # wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME,
        #                                                   "mdl-card")))

        user = User.objects.get(email="user@test.com")
        tasks = []
        while len(tasks) < user.task_set.count():
            tasks = self.selenium.find_elements_by_class_name("mdl-card")
            self.selenium.execute_script("arguments[0].scrollIntoView(true);",
                                         tasks[-1])
        self.assertEqual(len(tasks), 24)

    def test_about(self):
        login(self)
        button = self.selenium \
            .find_element_by_xpath("/html/body/div/div/header/div[2]/button")
        button.click()
        about_link = self.selenium \
            .find_element_by_xpath(
                "/html/body/div/div/header/div[2]/div[2]/ul/li")
        about_link.send_keys(Keys.ENTER)
        about = self.selenium.find_element_by_id("about")
        self.assertIn("task.tracking.stand@gmail.com", about.text)
        about.find_element_by_tag_name("button").click()

    def test_sort(self):
        login(self)
        # Sort by creating
        self.selenium \
            .find_element_by_xpath("/html/body/div/div/div/nav/a") \
            .click()
        tasks = scroll(self)
        tasks = [t.find_element_by_tag_name("h2").text for t in tasks]
        self.assertTrue(tasks[0] == "1")
        self.assertTrue(tasks[-1] == "Whatch that game")
        # Sort by spend time
        self.selenium \
            .find_element_by_xpath("/html/body/div/div/div/nav/a[2]") \
            .click()
        tasks = scroll(self)
        tasks = [t.find_element_by_tag_name("h2").text for t in tasks]
        self.assertTrue(tasks[0] == "Starcraft")
        self.assertTrue(tasks[1] == "Record video")
        self.assertTrue(tasks[4] == "First task")
        # Sort by name
        self.selenium \
            .find_element_by_xpath("/html/body/div/div/div/nav/a[3]") \
            .click()
        tasks = scroll(self)
        tasks = [t.find_element_by_tag_name("h2").text for t in tasks]
        self.assertTrue(tasks[0] == "1")
        self.assertTrue(tasks[-2] == "To-Do")
        self.assertTrue(tasks[-3] == "Test all views functions")
        # Sort by done
        self.selenium \
            .find_element_by_xpath("/html/body/div/div/div/nav/a[4]") \
            .click()
        tasks = []
        user = User.objects.get(email="user@test.com")
        while len(tasks) < user.task_set.filter(done=True).count():
            tasks = self.selenium.find_elements_by_class_name("mdl-card")
            self.selenium.execute_script("arguments[0].scrollIntoView();",
                                         tasks[-1])
        self.assertEqual(len(tasks), 2)
        tasks = [t.find_element_by_tag_name("h2").text for t in tasks]
        self.assertTrue(tasks[0] == "Record video")
        self.assertTrue(tasks[1] == "Take a rest")


def login(self):
    self.selenium.get(self.live_server_url)
    self.selenium.find_element_by_id("email").send_keys("user@test.com")
    self.selenium.find_element_by_id("password").send_keys("testpassword")
    self.selenium.find_element_by_tag_name("button").click()


def scroll(self):
    user = User.objects.get(email="user@test.com")
    tasks = []
    while len(tasks) < user.task_set.count():
        tasks = self.selenium.find_elements_by_class_name("mdl-card")
        self.selenium.execute_script("arguments[0].scrollIntoView(true);",
                                     tasks[-1])
    return tasks
