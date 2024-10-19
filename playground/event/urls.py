from django.urls import path
from .views import add_event,list_events,delete_event,update_event
from .views import optIn_publicEvents, list_publicEvents,publish_event,optOut_publicEvents

urlpatterns = [
    path('', list_publicEvents, name='list_publicEvents'),
    path('list_events', list_events, name='list_events'),
    path('add/', add_event, name='add_event'),
    path('delete/<str:event_id>/', delete_event, name='delete_event'),
    path('update/<str:event_id>/', update_event, name='update_event'),  # Updated line
    path('publish/<str:event_id>/', publish_event, name='publish_event'),
    path('optIn_publicEvents/<str:event_id>/', optIn_publicEvents, name='optIn_publicEvents'),
    path('optOut_publicEvents/<str:event_id>/', optOut_publicEvents, name='optOut_publicEvents'),
]
