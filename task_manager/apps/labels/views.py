from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import (
    AuthenticationRequiredMixin,
    ProtectionToDeleteMixin,
)

from .forms import LabelCreateForm
from .models import Label


class IndexView(AuthenticationRequiredMixin, ListView):
    
    model = Label
    template_name = 'labels/index.html'


class LabelCreateView(
    AuthenticationRequiredMixin,
    SuccessMessageMixin,
    CreateView
    ):
    
    model = Label
    form_class = LabelCreateForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels_index')
    success_message = _('Label was created successfully')


class LabelUpdateView(
    AuthenticationRequiredMixin,
    SuccessMessageMixin,
    UpdateView
    ):
    
    model = Label
    form_class = LabelCreateForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels_index')
    success_message = _('Label was updated successfully')


class LabelDeleteView(
    AuthenticationRequiredMixin,
    SuccessMessageMixin,
    ProtectionToDeleteMixin,
    DeleteView
    ):
    
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_index')
    success_message = _('Label was deleted successfully')
    protection_error_message = _('Cannot delete label because it is in use')

    def check(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        labels_tasks = Label.objects.get(id=label_id).labels.all()
        if labels_tasks:
            return False
        return True