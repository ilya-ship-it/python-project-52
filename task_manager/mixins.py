from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class NoPermissionHandleMixin:

    def handle_no_permission(self):
        messages.error(self.request, self.get_permission_denied_message())
        return redirect(self.permission_denied_url)


class AuthenticationRequiredMixin(LoginRequiredMixin):

    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        
        self.permission_denied_message = _(
            'You are not authorized! Please log in.'
            )
        self.permission_denied_url = reverse_lazy('login')
        return super().dispatch(request, *args, **kwargs)


class UserAuthorizationRequiredMixin(UserPassesTestMixin):

    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _(
            'You do not have permission to update another user.'
        )
        self.permission_denied_url = reverse_lazy('users_index')
        return super().dispatch(request, *args, **kwargs)


class TaskAuthorizationRequiredMixin(UserPassesTestMixin):

    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _(
            'A task can only be deleted by its author.'
            )
        self.permission_denied_url = reverse_lazy('tasks_index')
        return super().dispatch(request, *args, **kwargs)


class ProtectionToDeleteMixin:

    def post(self, request, *args, **kwargs):
        check_result = self.check(request, *args, **kwargs)

        if not check_result:
            messages.error(request, self.protection_error_message)
            return redirect(self.success_url, 302)
        
        self.delete(request, *args, **kwargs)
        messages.success(request, self.success_message)
        return redirect(self.success_url, 200)
