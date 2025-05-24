
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import (
    AuthenticationRequiredMixin,
    ProtectionToDeleteMixin,
)

from .forms import StatusCreateForm
from .models import Status


class IndexView(AuthenticationRequiredMixin, ListView):
    
    model = Status
    template_name = 'statuses/index.html'


class StatusCreateView(
    AuthenticationRequiredMixin,
    SuccessMessageMixin,
    CreateView
    ):
    
    model = Status
    form_class = StatusCreateForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status was created successfully')


class StatusUpdateView(
    AuthenticationRequiredMixin,
    SuccessMessageMixin,
    UpdateView
    ):

    model = Status
    form_class = StatusCreateForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status was updated successfully')


class StatusDeleteView(
    AuthenticationRequiredMixin,
    SuccessMessageMixin,
    ProtectionToDeleteMixin,
    DeleteView
    ):

    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_index')
    success_message = _('Status was deleted successfully')
    protection_error_message = _('Cannot delete status because it is in use')

    def check(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        statuses_tasks = Status.objects.get(id=status_id).statuses.all()
        if statuses_tasks:
            return False
        return True