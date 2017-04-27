from django import forms
from .models import Rides
from .models import Users

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
    number_going = forms.IntegerField(label = 'How many go?', max_value=10, min_value=1, required=True)
    date = forms.DateField(label="When go (MM/DD/YYYY)?", required=True)
    time = forms.TimeField(label="What time go (HH:MM)?", required=True)
 
