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
	name = forms.CharField(label='Full Name', max_length=100, required=True)
	email = forms.EmailField(label="Email", max_length=100)
	#start = forms.ChoiceField(choices=DESTINATIONS, required=True)
	destination = forms.ChoiceField(choices=DESTINATIONS, required=True)
	number_going = forms.IntegerField(max_value=10, min_value=1, required=True)
	date = forms.DateField(label="Date (MM/DD/YYYY)", required=True)
	time = forms.TimeField(label="Time (HH:MM)", required=True)
