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
    RIDE_TYPES = (
        ('Airport', 'Airport'),
        ('Shopping', 'Shopping'),
        ('Other', 'Other'),
    )
    ride_type = models.CharField(max_length=100, choices=RIDE_TYPES, default="")
    start_destination = models.CharField(max_length=100, choices = DESTINATIONS)
    end_destination = models.CharField(max_length=100, choices = DESTINATIONS)
    other_destination = models.CharField(max_length=100, default="")
    date_time = models.DateTimeField('Date and time')
    req_date_time = models.DateTimeField(auto_now_add=True)
    usrs = models.ManyToManyField('Users')
    seats = models.IntegerField(default=0)
    # owner = models.CharField(max_length=200) #netid
    full_name = models.CharField(max_length=200, default="")
    own_car = models.BooleanField(default=False)

    def __int__(self):
        return self.id
    class Meta: 
        ordering = ["date_time"]

class Users(models.Model):
    pools = models.ManyToManyField(Rides)
    netid = models.CharField(max_length=200, default="")
    def __str__(self):
        return self.netid
