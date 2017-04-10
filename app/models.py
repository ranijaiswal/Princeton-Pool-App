from __future__ import unicode_literals

# Create your models here.
import datetime
from django.db import models
from django.utils import timezone

class Rides(models.Model):
    DESTINATIONS = (
        ('EWR', 'EWR'),
        ('JFK', 'JFK'),
        ('LGA', 'LGA'),
        ('PHL', 'PHL'),
        ('PTON', 'Princeton'),
    )
    start_destination = models.CharField(max_length=100, choices = DESTINATIONS)
    end_destination = models.CharField(max_length=100, choices = DESTINATIONS)
    date_time = models.DateTimeField('Date and time')
    req_date_time = models.DateTimeField(auto_now_add=True)
    usrs = models.ManyToManyField('Users')
    seats = models.IntegerField(default=0)
    owner = models.CharField(max_length=200)
    def __int__(self):
        return self.id

class Users(models.Model):
    pools = models.ManyToManyField(Rides)
    full_name = models.CharField(max_length=200)
    def __str__(self):
        return self.full_name
