from django.test import TestCase
from task.models import Task
from task.util import correct_boundary, filter_args, check_filter
from django.contrib.auth.models import User


class UtilTestCase(TestCase):
    """Test util's functions"""
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username='test@test.com',
            password='top_secret')
        cls.filters = ("creating", "name", "done", "spend", None)
        cls.incorrect_filters = ("created", "named", "bolt", "43", "2!@",
                                 123, ["1", 5], 0.54, Task(), ("0", {}))

    @classmethod
    def tearDownClass(cls):
        pass

    def test_check_filter_for_true(self):
        for filter in self.filters:
            self.assertTrue(check_filter(filter))

    def test_check_filter_for_false(self):
        for filter in self.incorrect_filters:
            self.assertFalse(check_filter(filter))

    def test_filter_args(self):
        self.assertEquals(filter_args(self.filters[0]), (("-created", "name")))
        self.assertEquals(filter_args(self.filters[1]), (("name", "-timer")))
        self.assertEquals(filter_args(self.filters[2]), (("-created", "name")))
        self.assertEquals(filter_args(self.filters[3]), (("-timer", "name")))
        for filter in self.incorrect_filters:
            self.assertEquals(filter_args(filter), (("-created", "name")))

    def test_correct_boundary(self):
        total_tasks = 10
        for n in range(total_tasks):
            Task.objects.create(user=self.user,
                                name="Task " + str(n),
                                description="Description " + str(n))

        self.assertEquals(correct_boundary(self.user, self.filters[0], 14),
                          total_tasks)
        self.assertEquals(correct_boundary(self.user, self.filters[0], 4), 4)
