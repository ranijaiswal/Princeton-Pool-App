from rest_framework import serializers
from .models import Rides

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rides
        fields = ('ride_type', 'start_destination', 'end_destination', 'other_destination',
                  'date_time', 'req_date_time', 'usrs', 'seats')

        # ride_type = models.CharField(max_length=100, choices=RIDE_TYPES, default="")
        # start_destination = models.CharField(max_length=100, choices=DESTINATIONS)
        # end_destination = models.CharField(max_length=100, choices=DESTINATIONS)
        # other_destination = models.CharField(max_length=100, default="")
        # date_time = models.DateTimeField('Date and time')
        # req_date_time = models.DateTimeField(auto_now_add=True)
        # usrs = models.ManyToManyField('Users')
        # seats = models.IntegerField(default=0)