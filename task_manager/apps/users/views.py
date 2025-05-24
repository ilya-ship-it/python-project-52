from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import (
    AuthenticationRequiredMixin,
    NoPermissionHandleMixin,
    ProtectionToDeleteMixin,
    UserAuthorizationRequiredMixin,
)

from .forms import UserRegisterForm, UserUpdateForm
from .models import User


class IndexView(ListView):

    model = User
    template_name = 'users/index.html'


class UserCreateView(SuccessMessageMixin, CreateView):

    model = User
    form_class = UserRegisterForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('User was added successfully')


class UserUpdateView(
    NoPermissionHandleMixin,
    AuthenticationRequiredMixin,
    UserAuthorizationRequiredMixin,
    SuccessMessageMixin,
    UpdateView
    ):

    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_index')
    success_message = _('User was updated successfully')
    
    def test_func(self):
        user = self.get_object()
        return user == self.request.user


class UserDeleteView(
    NoPermissionHandleMixin,
    AuthenticationRequiredMixin,
    UserAuthorizationRequiredMixin,
    SuccessMessageMixin,
    ProtectionToDeleteMixin,
    DeleteView
    ):

    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_index')
    success_message = _('User was deleted successfully')
    protection_error_message = _('Cannot delete user because it is in use')

    def test_func(self):
        user = self.get_object()
        return user == self.request.user

    def check(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        authors = user.authors.all()
        executors = user.executors.all()

        if authors or executors:
            return False
        return True
    
