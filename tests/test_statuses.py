from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.apps.statuses.models import Status
from task_manager.apps.users.models import User


class AnonymousUserTestCase(TestCase):

    def test_create(self):
        response = self.client.get('/statuses/create/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_read(self):
        response = self.client.get('/statuses/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
    
    def test_update(self):
        response = self.client.get('/statuses/1/update/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_delete(self):
        response = self.client.get('/statuses/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class AuthenticatedUserTestCase(TestCase):

    fixtures = ['users_for_tests', 'statuses_for_tests']

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_status_create(self):
        # get
        response = self.client.get('/statuses/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')

        # Create status
        response = self.client.post(
            '/statuses/create/',
            {'name': 'test_status'}
            )
        status = Status.objects.last()
        self.assertEqual(status.name, 'test_status')
        self.assertEqual(Status.objects.count(), 3)
        self.assertRedirects(response, reverse_lazy('statuses_index'))

    def test_status_read(self):

        response = self.client.get('/statuses/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')

    def test_status_update(self):
        # get
        status = Status.objects.get(id=1)
        response = self.client.get('/statuses/1/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')

        # Update status
        response = self.client.post(
            '/statuses/1/update/',
            {'name': 'updated_name'}
            )
        status = Status.objects.get(id=1)
        self.assertRedirects(response, reverse_lazy('statuses_index'))
        self.assertEqual(status.name, 'updated_name')
        
    def test_status_delete(self):
        # get
        response = self.client.get('/statuses/1/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/delete.html')

        # Delete status
        response = self.client.post('/statuses/1/delete/')
        self.assertRedirects(response, reverse_lazy('statuses_index'))
        self.assertEqual(Status.objects.count(), 1)