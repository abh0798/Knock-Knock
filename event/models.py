from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.urls import reverse



# Create your models here.
class CustomUser(AbstractUser):
    score = models.IntegerField(default=0, blank= True)
    contact = models.CharField(max_length=10, blank= True)
    time_submission = models.DateTimeField(default=now)
    strin = "0"
    number=12
    for i in range(1,number):
        strin = strin+"0"
    answered = models.TextField(max_length=200, default=strin)

    def publish(self):
        self.save()

    def get_absolute_url(self):
        return reverse()

class Questions(models.Model):
    number = models.IntegerField(default=0)
    query = models.CharField(max_length=800)
    option1 = models.CharField(max_length=30)
    option2 = models.CharField(max_length=30)
    option3 = models.CharField(max_length=30)
    option4 = models.CharField(max_length=30)
    CHOICE = (
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
        (4, 'D'),
    )
    answer = models.IntegerField(default=0, choices=CHOICE)

class Event(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

class Special(models.Model):
    query = models.TextField(max_length=1200, default=" ")
    answer = models.CharField(max_length=50, default=" ")
