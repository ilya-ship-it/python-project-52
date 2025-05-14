from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'