from django.contrib import admin
from .models import UserEvents, UserTodo
# Register your models here.

admin.site.register(UserTodo)
admin.site.register(UserEvents)
