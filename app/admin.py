from django.contrib import admin
from django.db import models
from app.forms import RequestForm

# Register your models here.
from .models import Rides, Users

admin.site.register(Rides)
admin.site.register(Users)

