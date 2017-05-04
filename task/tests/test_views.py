from django.test import TestCase
from django.contrib.auth.models import User

from task.views import TaskView
from task.models import Task


class TaskViewTest(TestCase):

    fixtures = ['data_dump.json']

    def setUp(self):
        self.username = "user@test.com"
        self.password = "testpassword"

    def test_redirect_to_login(self):
        self.assertEqual(Task.objects.count(), 27)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_login_user_and_count_tasks(self):
        response = self.client.login(username=self.username,
                                     password=self.password)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task.html')
        user = response.context['user']
        tasks_count = response.context['tasks'].count()
        self.assertEqual(tasks_count, 9)
        self.assertEqual(user.task_set.count(), 22)

    def test_for_creating_filter(self):
        response = self.client.login(username=self.username,
                                     password=self.password)
        response = self.client.get('/')
        tasks = response.context['tasks']
        filter = response.context['filter']
        self.assertEqual(filter, "creating")
        self.assertTrue(check_queryset_order_creating_correct(tasks))

    def test_for_name_filter(self):
        response = self.client.login(username=self.username,
                                     password=self.password)
        response = self.client.get('/name/')
        self.assertEqual(response.context['filter'], 'name')

    def test_for_done_filter(self):
        response = self.client.login(username=self.username,
                                     password=self.password)
        response = self.client.get('/done/')
        self.assertEqual(response.context['filter'], 'done')

    def test_for_spend_filter(self):
        response = self.client.login(username=self.username,
                                     password=self.password)
        response = self.client.get('/spend/')
        self.assertEqual(response.context['filter'], 'spend')

    def test_for_incorrect_filter(self):
        response = self.client.login(username=self.username,
                                     password=self.password)
        response = self.client.get('/okey/')
        self.assertTrue(response.status_code, 404)
        response = self.client.get('/o423')
        self.assertTrue(response.status_code, 404)
        response = self.client.get('/o#$@_DSy/')
        self.assertTrue(response.status_code, 404)

    def test_users_owner_tasks(self):
        user = User.objects.create_user(username="test@test.com",
                                        password="test1234",
                                        email="test@test.com")
        self.client.login(username="test@test.com", password="test1234")
        t = Task.objects.create(user=user, name="task")
        response = self.client.get('/')

        user2 = User.objects.create_user(username="test2@test.com",
                                         password="test1234",
                                         email="test2@test.com")
        self.client.login(username="test2@test.com", password="test1234")
        t2 = Task.objects.create(user=user2, name="task")
        response2 = self.client.get('/')

        self.assertEqual(response.context['tasks'].count(), 1)
        self.assertEqual(response2.context['tasks'].count(), 1)

        self.assertEqual(response.context['tasks'].first(), t)
        self.assertEqual(response2.context['tasks'].first(), t2)
        self.assertNotEqual(response.context['tasks'],
                            response2.context['tasks'])


def check_queryset_order_creating_correct(queryset):
    for i in range(queryset.count() - 1):
        if queryset[i].created < queryset[i+1].created:
            return False
        elif queryset[i].created == queryset[i+1].created:
            if queryset[i].name > queryset[i+1].name:
                return False
    return True
