from django.urls import path
from .views import add_event,list_events,delete_event,update_event,optIn_publicEvents, list_publicEvents
urlpatterns = [
    path('', list_publicEvents, name='list_publicEvents'),
    path('list_events', list_events, name='list_events'),
    path('add/', add_event, name='add_event'),
    path('delete/<str:event_id>/', delete_event, name='delete_event'),
    path('update/<str:event_id>/', update_event, name='update_event'),  # Updated line
    path('optIn_publicEvents/<str:event_id>/', optIn_publicEvents, name='optIn_publicEvents'),
]
