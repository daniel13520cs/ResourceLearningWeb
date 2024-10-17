from typing import Any
from django.conf import settings
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView

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

class LoginView(LoginView):
    # Specify the template for login
    template_name = 'registration/login.html'

    # Specify the URL to redirect to after successful login
    success_url = reverse_lazy('list_events')

    def get_success_url(self):
        # Override this method to customize the success URL after login
        return self.success_url

    # Optionally override the form_valid method if you need to perform additional actions after the form is validated
    def form_valid(self, form):
        # Log the user in
        login(self.request, form.get_user())
        # You can add custom logic here if needed (e.g., sending a welcome message)
        return super().form_valid(form)

    # Optionally handle unsuccessful login attempts
    def form_invalid(self, form):
        # Add custom error handling if required
        return super().form_invalid(form)
    
class LogoutView(LogoutView):
    template_name = 'registration/logout.html'
    next_page = reverse_lazy('logout')