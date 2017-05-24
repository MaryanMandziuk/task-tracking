from selenium import webdriver
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class RegisterAndLoginTest(StaticLiveServerTestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.browser = webdriver \
            .Chrome("/home/maryan/programs/chromedriver/chromedriver",
                    chrome_options=options)

    def tearDown(self):
        self.browser.quit()

    def test_login_validation(self):
        self.browser.get(self.live_server_url)
        self.assertIn("/account/login/?next=/", self.browser.current_url)
        self.browser.find_element_by_id("email").send_keys("test")
        error_spans = self.browser \
            .find_elements_by_class_name("mdl-textfield__error")
        self.assertIn("Incorrect email format!", [s.text for s in error_spans])
        self.browser.find_element_by_id("email").clear()
        passw = self.browser.find_element_by_id("password")
        passw.send_keys("pass1")
        div = passw.find_element_by_xpath("..")
        self.assertIn("is-invalid", div.get_attribute("class"))

    def test_login(self):
        self.browser.get(self.live_server_url)
        User.objects.create_user(username="test@test.com",
                                 password="test1234",
                                 email="test@test.com")
        self.browser.find_element_by_id("email").send_keys("test@test.com")
        self.browser.find_element_by_id("password").send_keys("test1234")
        self.browser.find_element_by_tag_name("button").click()
        self.assertEqual(self.browser.current_url.replace(
                                        self.live_server_url, ''), '/')

    def test_for_invalid_login(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("email") \
            .send_keys("invalid_test@test.com")
        self.browser.find_element_by_id("password") \
            .send_keys("invalid_test1234")
        self.browser.find_element_by_tag_name("button").click()
        self.assertEqual(self.browser.current_url.replace(
                            self.live_server_url, ''), '/account/login/')
        error_spans = self.browser.find_elements_by_tag_name("span")
        self.assertIn("Wrong email or password. Please try again!",
                      [s.text for s in error_spans])

    def test_register(self):
        self.browser.get(self.live_server_url)
        sign_in = self.browser \
            .find_element_by_xpath("/html/body/div/div/main/div[2]/a")
        sign_in.click()
        self.assertEqual(self.browser.current_url.replace(
                            self.live_server_url, ''), '/account/register/')
        self.browser.find_element_by_id("email").send_keys("test@test.com")
        self.browser.find_element_by_id("password1").send_keys("testpassword")
        self.browser.find_element_by_id("password2").send_keys("testpasswor")

        # check for validation password
        self.browser.find_element_by_tag_name("button").click()
        self.assertEqual(self.browser.current_url.replace(
                            self.live_server_url, ''), '/account/register/')
        error_spans = self.browser.find_elements_by_tag_name("span")
        self.assertIn("Incorrect inputs data, please put them carefully!",
                      [s.text for s in error_spans])

        self.browser.find_element_by_id("email").clear()
        self.browser.find_element_by_id("email").send_keys("test@test.com")
        self.browser.find_element_by_id("password1").send_keys("testpassword")
        self.browser.find_element_by_id("password2").send_keys("testpasswor")
        error_spans = self.browser.find_elements_by_tag_name("span")
        self.assertIn("Password don\'t match.",
                      [s.text for s in error_spans])

        self.browser.find_element_by_id("password2").clear()
        self.browser.find_element_by_id("password2").send_keys("testpassword")
        self.browser.find_element_by_tag_name("button").click()
        self.assertIn("Welcome test@test.com", self.browser.page_source)

        self.browser.find_element_by_tag_name("a").click()
        self.assertEqual(self.browser.current_url.replace(
                            self.live_server_url, ''), '/account/login/')

        # register existing account
        sign_in = self.browser \
            .find_element_by_xpath("/html/body/div/div/main/div[2]/a")
        sign_in.click()
        self.browser.find_element_by_id("email").send_keys("test@test.com")
        self.browser.find_element_by_id("password1").send_keys("testpassword")
        self.browser.find_element_by_id("password2").send_keys("testpassword")
        self.browser.find_element_by_tag_name("button").click()
        self.assertIn("User with email: test@test.com has been registered.",
                      self.browser.page_source)

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("email").send_keys("test@test.com")
        self.browser.find_element_by_id("password").send_keys("testpassword")
        self.browser.find_element_by_tag_name("button").click()
        self.assertEqual(self.browser.current_url.replace(
                                        self.live_server_url, ''), '/')
