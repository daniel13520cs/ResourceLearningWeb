from django.db import models
from mongoengine import Document, StringField, DateTimeField, URLField, ListField, EmbeddedDocumentField
from datetime import datetime

# Create your models here.
class Event(Document):
    title = StringField(required=True, max_length=100)
    description = StringField()
    startTime = DateTimeField(default=datetime.utcnow)
    location = StringField(max_length=255)  # Field for the location of the event
    URL = URLField()  # Field for a URL associated with the event

    def __str__(self):
        return self.title