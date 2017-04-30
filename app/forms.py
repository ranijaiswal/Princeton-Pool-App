from django import forms
from .models import Rides
from .models import Users
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

DESTINATIONS = (
    ('EWR', 'EWR'),
    ('JFK', 'JFK'),
    ('LGA', 'LGA'),
    ('PHL', 'PHL'),
    ('PTON', 'Princeton'),
)

class RequestForm(forms.Form):
    starting_destination = forms.ChoiceField(label='Starting Destination?', choices=DESTINATIONS)
    destination = forms.ChoiceField(label='Where go?', choices=DESTINATIONS, required=True)
    number_going = forms.IntegerField(label = 'How many go?', required=True)
    date = forms.DateField(label="When go (MM/DD/YYYY)?", required=True)
    time = forms.TimeField(label="What time go (HH:MM)?", required=True)
 
