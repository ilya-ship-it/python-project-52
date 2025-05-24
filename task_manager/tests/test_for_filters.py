from django.test import TestCase

from ..apps.users.models import User


class FilterTestCase(TestCase):

    fixtures = [
        'users_for_tests',
        'labels_for_tests',
        'tasks_for_tests',
        'statuses_for_tests'
        ]

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_filter_for_status(self):
        response = self.client.get('/tasks/', {'status': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['filter'].qs), 1)

    def test_filter_for_executor(self):
        response = self.client.get('/tasks/', {'executor': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['filter'].qs), 0)

    def test_filter_for_labels(self):
        response = self.client.get('/tasks/', {'labels': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['filter'].qs), 0)