from django.contrib import admin

# Register your models here.
from .models import Rides, Users

admin.site.register(Rides)
admin.site.register(Users)
