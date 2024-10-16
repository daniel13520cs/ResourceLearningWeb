from django.urls import path
from .views import add_event,list_events,delete_event,update_event
urlpatterns = [
    path('', list_events, name='list_events'),
    path('add/', add_event, name='add_event'),
    path('delete/<str:event_id>/', delete_event, name='delete_event'),
    path('update/<str:event_id>/', update_event, name='update_event'),  # Updated line
]
