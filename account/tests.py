from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth


class RegisterTest(TestCase):

    def test_register_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/login/?next=/')

    def test_register_method_get(self):
        response = self.client.get('/account/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

    def test_valid_new_user(self):
        response = self.client.post('/account/register/', data={
                                   'email': 'new_test_user@test.com',
                                   'password1': 'testpassword',
                                   'password2': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('new_test_user@test.com',
                      [user.email for user in User.objects.all()])

    def test_on_existing_email(self):
        User.objects.create_user(username="test2@test.com",
                                 password="test1234",
                                 email="test2@test.com")
        response = self.client.post('/account/register/', data={
                                   'email': 'test2@test.com',
                                   'password1': 'testpassword',
                                   'password2': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register_failed.html')
        self.assertEqual(User.objects.count(), 1)

    def test_on_invalid_input_data(self):
        response = self.client.post('/account/register/', data={
                                   'email': 'new_test_user@com',
                                   'password1': 'testpassword',
                                   'password2': 'testpassword'})

        same_asserts_on_invalid_register_data(self, response)

        response = self.client.post('/account/register/', data={
                                   'email': 'new_test_user@test.com',
                                   'password1': 'testpd432423',
                                   'password2': 'testpassword'})

        same_asserts_on_invalid_register_data(self, response)

        response = self.client.post('/account/register/', data={
                                   'email': 'new_test_usertest.com',
                                   'password1': 'testpassword',
                                   'password2': 'testpassword'})

        same_asserts_on_invalid_register_data(self, response)

        response = self.client.post('/account/register/', data={
                                   'email': 'new_test_user@test.c',
                                   'password1': 'testpassword',
                                   'password2': 'testpassword'})

        same_asserts_on_invalid_register_data(self, response)


class UserLoginTest(TestCase):

    def test_login_method_get(self):
        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_on_valid_user(self):
        User.objects.create_user(username="test2@test.com",
                                 password="test1234",
                                 email="test2@test.com")
        response = self.client.post('/account/login/', data={
                                    'email': 'test2@test.com',
                                    'password': 'test1234'})
        self.assertEqual(response.status_code, 302)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())
        self.assertRedirects(response, '/')

    def test_on_invalid_user(self):
        User.objects.create_user(username="test2@test.com",
                                 password="test1234",
                                 email="test2@test.com")
        response = self.client.post('/account/login/', data={
                                    'email': 'test2@test.co',
                                    'password': 'test1234'})
        self.assertIn('error', response.context)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())

        response = self.client.post('/account/login/', data={
                                    'email': 'test2@test.com',
                                    'password': 'incorrectpassword'})
        self.assertIn('error', response.context)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())


def same_asserts_on_invalid_register_data(self, response):
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'account/register.html')
    self.assertEqual(User.objects.count(), 0)
