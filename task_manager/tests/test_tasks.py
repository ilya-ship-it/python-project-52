from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.apps.tasks.models import Task
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
        'statuses_for_tests',
        'tasks_for_tests',
        'labels_for_tests'
        ]

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_task_create(self):
        # get
        response = self.client.get('/tasks/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')

        # Create task
        response = self.client.post(
            '/tasks/create/',
            {
                'name': 'test_task',
                'description': 'test_description',
                'status': 1,
                'author': 1,
                'executor': 2,
                'labels': [1, 2],
                'created_at': "2025-03-03 14:28:00",
            }
        )
        task = Task.objects.last()
        self.assertEqual(task.name, 'test_task')
        self.assertEqual(Task.objects.count(), 3)
        self.assertRedirects(response, reverse_lazy('tasks_index'))

    def test_task_read(self):

        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')

    def test_task_update(self):
        # get
        task = Task.objects.get(id=1)
        response = self.client.get('/tasks/1/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')

        # Update task
        response = self.client.post(
            '/tasks/1/update/',
            {
                'name': 'updated_task',
                'description': 'updated_description',
                'status': 1,
                'author': 1,
                'executor': 2,
                'labels': [1],
                'created_at': "2025-03-03 14:28:00"
            }
        )
        task = Task.objects.get(id=1)
        self.assertRedirects(response, reverse_lazy('tasks_index'))
        self.assertEqual(task.name, 'updated_task')
        
    def test_task_delete(self):
        # get
        task = Task.objects.get(id=1)
        url = f'/tasks/{task.id}/delete/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete.html')

        # Delete task
        response = self.client.post('/tasks/1/delete/')
        self.assertRedirects(response, reverse_lazy('tasks_index'))
        self.assertEqual(Task.objects.count(), 1) 