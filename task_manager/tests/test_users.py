from django.forms.models import model_to_dict
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.apps.users.forms import UserRegisterForm
from task_manager.apps.users.models import User

# Create your tests here.


class AnonymousUserTestCase(TestCase):

    fixtures = ['users_for_tests']

    def test_anonymous_user_create_get(self):
        # get
        response = self.client.get('/users/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')

    def test_anoymous_user_create_post_with_right_data(self):
        response = self.client.post(
            '/users/create/',
            {
            'first_name': 'new_firstname',
            'last_name': 'new_lastname',
            'username': 'new_username',
            'password1': 'new_password',
            'password2': 'new_password'
            }
        )
        user = User.objects.last()
        self.assertEqual(user.username, 'new_username')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_anoymous_user_create_post_with_wrong_data(self):
        user_dict = model_to_dict(
            User.objects.last(),
            ['fist_name',
             'last_name',
             'username',
             'password']
             )
        response = self.client.post('/users/create/', user_dict)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')

        form = UserRegisterForm(data=user_dict)
        self.assertFormError(
            form=form,
            field='username',
            errors='Пользователь с таким именем уже существует.')

    def test_anonymous_user_read(self):
        response = self.client.get('/users/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertTrue(len(response.context['object_list']) == 2)

    def test_anonymous_user_update(self):
        response = self.client.get('/users/1/update/')
        self.assertRedirects(response, reverse_lazy('login'))

    def test_anonymous_user_delete(self):
        response = self.client.get('/users/1/delete/')
        self.assertRedirects(response, reverse_lazy('login'))


class AnotherUserTestCase(TestCase):
    
    fixtures = ['users_for_tests']

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_another_user_read(self):
        response = self.client.get('/users/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertTrue(len(response.context['object_list']) == 2)

    def test_another_user_update(self):
        another_user = User.objects.get(id=2)
        response = self.client.get(f'/users/{another_user.pk}/update/')
        self.assertRedirects(response, reverse_lazy('users_index'))
        self.assertRaisesMessage(
            PermissionError,
            'You do not have permission to update another user.'
            )

    def test_another_user_delete(self):
        another_user = User.objects.get(id=2)
        response = self.client.get(f'/users/{another_user.pk}/delete/')
        self.assertRedirects(response, reverse_lazy('users_index'))
        self.assertRaisesMessage(
            PermissionError,
            'You do not have permission to delete another user.'
            )


class CurrentUserTestCase(TestCase):

    fixtures = ['users_for_tests']

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)

    def test_current_user_read(self):
        response = self.client.get('/users/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertTrue(len(response.context['object_list']) == 2)

    def test_current_user_update_get(self):
        # get
        response = self.client.get('/users/1/update/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('users/update.html')
        
    def test_current_user_update_post(self):
        response = self.client.post(
            '/users/1/update/',
            {
            'first_name': 'updated_firstname',
            'last_name': 'new_lastname',
            'username': 'new_username',
            'password1': 'new_password',
            'password2': 'new_password'
            })
        updated_user = User.objects.get(id=1)
        self.assertRedirects(response, reverse_lazy('users_index'))
        self.assertEqual(updated_user.first_name, 'updated_firstname')

    def test_current_user_delete_get(self):
        response = self.client.get('/users/1/delete/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('users/delete.html')

    def test_current_user_delete_post(self):
        response = self.client.post('/users/1/delete/')
        self.assertRedirects(response, reverse_lazy('users_index'))

        response = self.client.get('/users/')
        self.assertTrue(len(response.context['object_list']) == 1)
