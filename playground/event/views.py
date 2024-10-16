from django.db.models.query import QuerySet
from django.views.generic import ListView
from .models import Event
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import Event

class EventListView(ListView):
    model = Event
    template_name = 'list_events.html'  # Template for listing events
    context_object_name = 'events'  # Context variable for the template
    def get_queryset(self):
        return Event.objects().all()

class EventCreateView(CreateView):
    model = Event
    template_name = 'add_event.html'  # Template for adding an event
    fields = ['title', 'description', 'startTime', 'location', 'URL']  # Fields to be included in the form
    success_url = reverse_lazy('list_events')  # Redirect to the event list after adding


class EventDeleteView(DeleteView):
    model = Event
    template_name = 'delete_event.html'  # Template for deleting an event
    context_object_name = 'event'  # Context variable for the template
    success_url = reverse_lazy('list_events')  # Redirect to the event list after deletion


class EventUpdateView(UpdateView):
    model = Event
    template_name = 'update_event.html'  # Your template for updating the event
    fields = ['title', 'description', 'startTime', 'location', 'URL']  # Fields to be included in the form

    def get_success_url(self):
        return reverse_lazy('list_events')  # Redirect to the event list after updating
