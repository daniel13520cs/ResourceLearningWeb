from django.db import models
from mongoengine import Document, StringField, DateTimeField, URLField, ReferenceField
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Event(Document):
    title = StringField(required=True, max_length=100)
    description = StringField(required=True)
    startTime = DateTimeField(required=True, default=datetime.utcnow)
    location = StringField(default='', blank=True, null=True, max_length=255)
    URL = URLField(blank=True, null=True)  # Allow this field to be empty
    userID = StringField(required=True)

    def __str__(self):
        return self.title