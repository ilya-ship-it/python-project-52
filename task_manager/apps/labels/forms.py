from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Label


class LabelCreateForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ['name']

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Name')
                    }
                )
        }

        labels = {
            'name': _('Name'),
        }
