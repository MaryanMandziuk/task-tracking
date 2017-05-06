from django.test import TestCase
from django.contrib.auth.models import User
import json
import datetime

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


class CreateTaskTest(TestCase):

    def setUp(self):
        User.objects.create_user(username="test2@test.com",
                                 password="test1234",
                                 email="test2@test.com")
        self.client.login(username="test2@test.com", password="test1234")

    def test_create_task_post(self):
        response = self.client.post('/create/', data={'name': "Name",
                                    'description': 'des'})
        self.assertRedirects(response, '/')
        self.assertEqual(Task.objects.count(), 1)

    def test_create_task_with_get(self):
        response = self.client.get('/create/', data={'name': "Name",
                                   'description': 'des'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_with_filter_option(self):
        response = self.client.post('/creating/create/', data={'name': "Name",
                                    'description': 'des'})
        self.assertRedirects(response, '/creating/')
        response = self.client.post('/spend/create/', data={'name': "Name",
                                    'description': 'des'})
        self.assertRedirects(response, '/spend/')
        response = self.client.post('/done/create/', data={'name': "Name",
                                    'description': 'des'})
        self.assertRedirects(response, '/done/')
        response = self.client.post('/name/create/', data={'name': "Name",
                                    'description': 'des'})
        self.assertRedirects(response, '/name/')


class RemoveTaskTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test2@test.com",
                                             password="test1234",
                                             email="test2@test.com")
        self.client.login(username="test2@test.com", password="test1234")

    def test_remove(self):
        task = Task.objects.create(user=self.user, name="Name",
                                   description="des")
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.get('/remove/'+str(task.pk) + '/')
        self.assertRedirects(response, '/')
        self.assertEqual(Task.objects.count(), 0)

    def test_remove_with_filter(self):
        task = Task.objects.create(user=self.user, name="Name",
                                   description="des")
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.get('/creating/remove/' + str(task.pk) + '/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/creating/')
        self.assertEqual(Task.objects.count(), 0)

    def test_remove_for_uncreated_pk(self):
        response = self.client.get('/remove/' + str(2433324) + '/')
        self.assertEqual(response.status_code, 404)


class EditTaskTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test2@test.com",
                                             password="test1234",
                                             email="test2@test.com")
        self.client.login(username="test2@test.com", password="test1234")
        self.task = Task.objects.create(user=self.user, name="Task name",
                                        description="")

    def test_edit_task(self):
        response = self.client.post('/edit/' + str(self.task.pk) + '/',
                                    data={'name': 'New name',
                                          'description': 'New description'})
        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, '/creating/')
        self.assertEqual(Task.objects.count(), 1)
        self.task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(self.task.name, 'New name')
        self.assertEqual(self.task.description, 'New description')

    def test_edit_task_with_filter(self):
        response = self.client.post('/done/edit/' + str(self.task.pk) + '/',
                                    data={'name': 'New name',
                                          'description': 'New description'})
        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, '/done/')
        self.assertEqual(Task.objects.count(), 1)
        self.task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(self.task.name, 'New name')
        self.assertEqual(self.task.description, 'New description')

    def test_edit_task_with_incorrect_filter(self):
        response = self.client.post('/ran/edit/' + str(self.task.pk) + '/',
                                    data={'name': 'New name',
                                          'description': 'New description'})
        self.assertTrue(response.status_code, 404)

    def test_edit_task_with_incorrect_pk(self):
        response = self.client.post('/done/edit/' + str(32313) + '/',
                                    data={'name': 'New name',
                                          'description': 'New description'})
        self.assertTrue(response.status_code, 404)

    def test_edit_task_get_method(self):
        response = self.client.get('/edit/' + str(self.task.pk) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tasks'].count(), 1)
        self.assertEqual(response.context['task'], self.task)
        self.assertEqual(response.context['filter'], 'creating')


class IsDoneTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test2@test.com",
                                             password="test1234",
                                             email="test2@test.com")
        self.client.login(username="test2@test.com", password="test1234")
        self.task = Task.objects.create(user=self.user, name="Task name",
                                        description="")

    def test_is_done(self):
        response = self.client.get('/is_done/', {'id': self.task.pk,
                                                 'done': "1"},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['done'], "1")
        self.assertEqual(Task.objects.get(pk=self.task.pk).done, True)

    def test_is_done_400(self):
        response = self.client.get('/is_done/', {'id': 2, 'done': "0"})
        self.assertEqual(response.status_code, 400)

    def test_is_done_404(self):
        response = self.client.get('/is_done/', {'id': 2, 'done': "0"},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)


class SetTimerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test2@test.com",
                                             password="test1234",
                                             email="test2@test.com")
        self.client.login(username="test2@test.com", password="test1234")
        self.task = Task.objects.create(user=self.user, name="Task name",
                                        description="")

    def test_set_timer(self):
        response = self.client.get('/set_timer/', {'id': self.task.pk,
                                                   'timer': 1000},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.get(pk=self.task.pk).timer,
                         datetime.timedelta(seconds=1000))

    def test_is_done_400(self):
        response = self.client.get('/set_timer/', {'id': 2, 'done': "0"})
        self.assertEqual(response.status_code, 400)

    def test_is_done_404(self):
        response = self.client.get('/set_timer/', {'id': 2, 'done': "0"},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)


class GetTimerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test2@test.com",
                                             password="test1234",
                                             email="test2@test.com")
        self.client.login(username="test2@test.com", password="test1234")
        self.task = Task.objects.create(user=self.user, name="Task name",
                                        description="")

    def test_get_timer(self):
        response = self.client.get('/get_timer/', {'id': self.task.pk},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['timer'], 0)

    def test_is_done_400(self):
        response = self.client.get('/get_timer/', {'id': 2})
        self.assertEqual(response.status_code, 400)

    def test_is_done_404(self):
        response = self.client.get('/get_timer/', {'id': 2},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)


class PaginationAjaxTest(TestCase):

    fixtures = ['data_dump.json']

    def setUp(self):
        self.client.login(username="user@test.com", password="testpassword")

    def test_pagination_ajax(self):
        response = self.client.get('/pagination_ajax/',
                                   {'offset': 9,
                                    'filter': 'creating'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 9)

        response2 = self.client.get('/pagination_ajax/',
                                    {'offset': 15,
                                     'filter': 'creating'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response2.status_code, 200)
        data2 = json.loads(response2.content)
        self.assertEqual(len(data2), 7)

        # offset is bigger than amount of user's tasks
        response3 = self.client.get('/pagination_ajax/',
                                    {'offset': 31,
                                     'filter': 'creating'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response3.status_code, 200)
        data3 = json.loads(response3.content)
        self.assertEqual(len(data3), 0)

    def test_pagination_ajax_400(self):
        response = self.client.get('/pagination_ajax/',
                                   {'offset': 12,
                                    'filter': 'creating'})
        self.assertEqual(response.status_code, 400)

    def test_pagination_ajax_icorrect_filter(self):
        response = self.client.get('/pagination_ajax/',
                                   {'offset': 12,
                                    'filter': 'incorrect'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)


class SearchTest(TestCase):

    fixtures = ['data_dump.json']

    def setUp(self):
        self.client.login(username="user@test.com", password="testpassword")

    def test_search(self):
        response = self.client.get('/search/?q=Task')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('search/search.html')
        self.assertEqual(len(response.context['results']), 5)
        self.assertEqual(response.context['query'], "Task")
        results = response.context['results']
        user = User.objects.get(username="user@test.com")
        for r in results:
            self.assertEqual(r.object.user, user)

    def test_search_for_invalid_task(self):
        response = self.client.get('/search/?q=invalid task')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['results']), 0)
        self.assertEqual(response.context['query'], "invalid task")


class EditOnSearchPage(TestCase):

    fixtures = ['data_dump.json']

    def setUp(self):
        self.client.login(username="user@test.com", password="testpassword")

    def test_edit_task_method_post(self):
        response = self.client.post('/search/edit/105/Task/',
                                    data={'name': "Edited name",
                                          'description': "Edited desc"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/search/Task/')
        task = Task.objects.get(pk=105)
        self.assertEqual(task.name, "Edited name")
        self.assertEqual(task.description, "Edited desc")

    def test_edit_task_method_get(self):
        response = self.client.get('/search/edit/105/Task')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/edit.html')
        self.assertEqual(response.context['query'], "Task")
        self.assertEqual(response.context['task'],
                         Task.objects.get(pk=105))
        results = response.context['results']
        user = User.objects.get(username="user@test.com")
        for r in results:
            self.assertEqual(r.object.user, user)

    def test_edit_task_for_invalid_task(self):
        response = self.client.get('/search/edit/106/Task')
        self.assertEqual(response.status_code, 404)


class RemoveOnSearchPage(TestCase):

    fixtures = ['data_dump.json']

    def setUp(self):
        self.client.login(username="user@test.com", password="testpassword")

    def test_remove(self):
        response = self.client.get('/search/remove/105/Task')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/search/Task')

    def test_remove_invalid_task(self):
        response = self.client.get('/search/remove/106/Task')
        self.assertEqual(response.status_code, 404)


def check_queryset_order_creating_correct(queryset):
    for i in range(queryset.count() - 1):
        if queryset[i].created < queryset[i+1].created:
            return False
        elif queryset[i].created == queryset[i+1].created:
            if queryset[i].name > queryset[i+1].name:
                return False
    return True
