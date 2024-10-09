from django.urls import path

from .views import add_todo, list_todos, delete_todo

urlpatterns = [
    path('', list_todos, name='list_todos'),
    path('add/', add_todo, name='add_todo'),
    path('list/', list_todos, name='list_todos'),
    path('delete/<str:todo_id>/', delete_todo, name='delete_todo'),
]