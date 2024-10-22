from django.db import models
from mongoengine import Document, StringField, DateTimeField, URLField, IntField,BooleanField,ListField
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Event(Document):
    title = StringField(required=True, max_length=100)
    description = StringField(required=True, max_length=400)  # Updated max_length to 400
    startTime = DateTimeField(required=True, default=datetime.utcnow)
    URL = URLField(blank=True, null=True)  # Allow this field to be empty
    ownerUserID = IntField(required=True)
    isPublic = BooleanField(default=False)
    tags = ListField(StringField(), default=[])
    image = StringField(blank=True, null=True, max_length=200)  # Restrict length to 200 chars
    labels = ListField(StringField(), default=[])  # New field for labels

    def __str__(self):
        return self.title

class UserTodo(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User table
    todoID = models.CharField(max_length=24)  # This remains a CharField to store MongoDB ObjectId

    def __str__(self):
        return f'userID: {self.userID} - Todo ID:{self.todoID}'
    
class UserEvents(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User table
    eventID = models.CharField(max_length=24)  # Store MongoDB ObjectId as a string (Event ID)

    def __str__(self):
        return f'userID: {self.userID} - Event ID: {self.eventID}'
    
    
    