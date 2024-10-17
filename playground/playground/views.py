from typing import Any
from django.conf import settings
from django.shortcuts import render
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

class App_list_view(generic.TemplateView):
    # Get the list of installed apps
    template_name = "app_list_site.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['USER_APPS'] = settings.USER_APPS
        return context

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after registration
            login(request, user)
            return redirect('login')  # Redirect to login or another page
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
