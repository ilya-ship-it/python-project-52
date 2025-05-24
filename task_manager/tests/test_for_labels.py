from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.apps.labels.models import Label
from task_manager.apps.users.models import User


class AnonymousUserTestCase(TestCase):

    def test_create(self):
        response = self.client.get('/tasks/create/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_read(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
    
    def test_update(self):
        response = self.client.get('/tasks/1/update/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_delete(self):
        response = self.client.get('/tasks/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class AuthenticatedUserTestCase(TestCase):

    fixtures = [
        'users_for_tests',
        'labels_for_tests',
        'tasks_for_tests',
        'statuses_for_tests'
        ]

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_label_create(self):
        # get
        response = self.client.get('/labels/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/create.html')

        # Create label
        response = self.client.post(
            '/labels/create/',
            {'name': 'test_label'}
            )
        label = Label.objects.last()
        self.assertEqual(label.name, 'test_label')
        self.assertEqual(Label.objects.count(), 3)
        self.assertRedirects(response, reverse_lazy('labels_index'))

    def test_label_read(self):
        response = self.client.get('/labels/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/index.html')

    def test_label_update(self):
        # get
        response = self.client.get('/labels/1/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/update.html')

        # Update label
        response = self.client.post(
            '/labels/1/update/',
            {'name': 'updated_name'}
            )
        label = Label.objects.get(id=1)
        self.assertRedirects(response, reverse_lazy('labels_index'))
        self.assertEqual(label.name, 'updated_name')
        response = self.client.get('/labels/')
        self.assertContains(response, 'updated_name')
        
    def test_related_label_delete(self):
        # get
        response = self.client.get('/labels/1/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/delete.html')

        # Delete
        response = self.client.post('/labels/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertRaises(ProtectedError)
        self.assertEqual(len(Label.objects.all()), 2)

    def test_unrelated_label_delete(self):

        response = self.client.post('/labels/2/delete/')
        self.assertRedirects(response, reverse_lazy('labels_index'))
        self.assertEqual(len(Label.objects.all()), 1)