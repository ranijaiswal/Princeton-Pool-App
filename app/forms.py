from django import forms
from .models import Rides
from .models import Users
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.forms.extras.widgets import SelectDateWidget

AIRPORT_DESTINATIONS = (
    ('PTON', 'Princeton'),
    ('EWR', 'EWR'),
    ('JFK', 'JFK'),
    ('LGA', 'LGA'),
    ('PHL', 'PHL'),
)

SHOPPING_DESTINATIONS = (
    ('Princeton', 'Princeton'),
    ('Wegman\'s', 'Wegman\'s'),
    ('Shop Rite', 'Shop Rite'),
    ('Trader Joe\'s', 'Trader Joe\'s'),
    ('Target', 'Target'),
    ('Walmart', 'Walmart'),
    ('Costco', 'Costco'),
    ('Asian Foods Market Plainsboro', 'Asian Foods Market Plainsboro')
)

class RequestForm(forms.Form):

    # class Meta:
    #     widgets = {'date': SelectDateWidget()}

    def __init__(self,*args,**kwargs):
        rtype = kwargs.pop("rtype")
        super(RequestForm, self).__init__(*args, **kwargs)
        
        if rtype == 'airport':
            self.fields['starting_destination'] = forms.ChoiceField(label='Starting Destination?', choices=AIRPORT_DESTINATIONS)
            self.fields['destination'] = forms.ChoiceField(label='Where go?', choices=AIRPORT_DESTINATIONS)
        
        elif rtype == 'shopping':
            self.fields['starting_destination'] = forms.ChoiceField(label='Starting Destination?', choices=SHOPPING_DESTINATIONS)
            self.fields['destination'] = forms.ChoiceField(label='Where go?', choices=SHOPPING_DESTINATIONS)
        elif rtype == 'other':
            self.fields['starting_destination'] = forms.CharField(label='Starting Destination?')
            self.fields['destination'] = forms.CharField(label='Where go?')
        self.fields['number_going'] = forms.IntegerField(label = 'How many go?')
        self.fields['date'] = forms.DateField(widget=SelectDateWidget, label="When go (MM/DD/YYYY)?")
        self.fields['time'] = forms.TimeField(label="What time go (HH:MM)?")

    # def clean_date_time(self):
    #     ride_date = self.cleaned_data['date']
    #     ride_time = self.cleaned_data['time']
    #     date_time = ('%s %s' % (ride_date, ride_time))
    #     date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    #     if datetime.now() >= date_time:
    #         raise forms.ValidationError(u'Invalid Date or Time! "%s"' % date_time)
    #     return date_time

    def clean(self):
        cleaned_data = self.cleaned_data;
        starting_destination = cleaned_data.get('starting_destination')
        destination = cleaned_data.get('destination')
        number_going = cleaned_data.get('number_going')

        if (number_going < 1):
            raise forms.ValidationError(u'So lonely. Only room for yourself?')

        if (number_going > 200):
            raise forms.ValidationError(u'Sorry, we are not handling large rideshares. ')
        ride_date = cleaned_data.get('date')
        ride_time = cleaned_data.get('time')
        date_time = ('%s %s' % (ride_date, ride_time))
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        if datetime.now() >= date_time:
            raise forms.ValidationError(u'Invalid Date or Time! "%s"' % date_time)


        if (starting_destination == destination):
            raise forms.ValidationError(u'Starting and end location cannot be the same!')

        #raise forms.ValidationError("%s" %destination)
        return cleaned_data
