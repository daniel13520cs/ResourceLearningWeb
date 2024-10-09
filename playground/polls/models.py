# models.py
from mongoengine import Document, StringField, BooleanField, DateTimeField
from datetime import datetime

class Todo(Document):
    title = StringField(required=True, max_length=100)
    description = StringField()
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return self.title
