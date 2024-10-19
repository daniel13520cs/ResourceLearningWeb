# models.py
from mongoengine import Document, StringField, BooleanField, DateTimeField, ReferenceField
from datetime import datetime
from event.models import Event

class Todo(Document):
    title = StringField(required=True, max_length=100)
    description = StringField()
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    event = ReferenceField(Event, reverse_delete_rule=4)
    
    def __str__(self):
        return self.title
