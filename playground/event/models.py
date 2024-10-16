from django.db import models
from mongoengine import Document, StringField, DateTimeField, URLField, ListField, EmbeddedDocumentField
from datetime import datetime

# Create your models here.
class Event(Document):
    title = StringField(required=True, max_length=100)
    description = StringField(required=True)
    startTime = DateTimeField(required=True, default=datetime.utcnow)
    location = StringField(default='', blank=True, null=True, max_length=255)
    URL = URLField(blank=True, null=True)  # Allow this field to be empty

    def __str__(self):
        return self.title