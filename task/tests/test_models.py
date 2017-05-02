from django.test import TestCase
from task.models import Task
from django.contrib.auth.models import User


class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test@test.com',
            password='top_secret')
        self.user2 = User.objects.create_user(
                    username='test2@test.com',
                    password='top_secret')

    def test_string_representation(self):
        task = Task.objects.create(user=self.user, name="Task 1")
        task2 = Task.objects.create(user=self.user)
        self.assertEquals(str(task), "Task 1")
        self.assertEquals(str(task2), "")

    def test_tasks_default_ordering(self):
        task1 = Task.objects.create(user=self.user, name="Do it")
        task2 = Task.objects.create(user=self.user, name="Monte-carlo sim")
        task3 = Task.objects.create(user=self.user, name="Colaider")
        task4 = Task.objects.create(user=self.user, name="Came back")
        self.assertEqual(list(Task.objects.all()),
                         [task4, task3, task1, task2])
