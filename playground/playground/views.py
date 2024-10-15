from typing import Any
from django.conf import settings
from django.shortcuts import render
from django.views import generic

class App_list_view(generic.TemplateView):
    # Get the list of installed apps
    template_name = "app_list_site.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['USER_APPS'] = settings.USER_APPS
        return context