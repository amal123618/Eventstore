import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Guest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='guests')
    rsvp_token = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.name
   