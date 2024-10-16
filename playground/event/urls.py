from django.urls import path
from .views import EventListView, EventCreateView, EventDeleteView, EventUpdateView

urlpatterns = [
    path('', EventListView.as_view(), name='list_events'),
    path('add/', EventCreateView.as_view(), name='add_event'),
    path('delete/<int:event_id>/', EventDeleteView.as_view(), name='delete_event'),
    path('update/<int:pk>/', EventUpdateView.as_view(), name='update_event'),  # Updated line
]
