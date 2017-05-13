from django import forms
from .models import Rides
from .models import Users
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from datetime import date
from django.forms.extras.widgets import SelectDateWidget
from .SelectTimeWidget import SelectTimeWidget

AIRPORT_DESTINATIONS = (
    ('Princeton', 'Princeton'),
    ('Newark (EWR)', 'Newark (EWR)'),
    ('John F. Kennedy (JFK)', 'John F. Kennedy (JFK)'),
    ('LaGuardia (LGA)', 'LaGuardia (LGA)'),
    ('Philadelphia (PHL)', 'Philadelphia (PHL)'),
)

SHOPPING_DESTINATIONS = (
    ('Princeton', 'Princeton'),
    ('Wegman\'s', 'Wegman\'s'),
    ('Shop Rite', 'Shop Rite'),
    ('Trader Joe\'s', 'Trader Joe\'s'),
    ('Target', 'Target'),
    ('Walmart', 'Walmart'),
    ('Costco', 'Costco'),
    ('Asian Food Markets (Plainsboro)', 'Asian Food Markets (Plainsboro)')
)
class FeedbackForm(forms.Form):
    name=forms.CharField(label="Name (optional)", required=False)
    email=forms.EmailField(label = "Email (optional)", required=False)
    feedback = forms.CharField(widget=forms.Textarea)

class RequestForm(forms.Form):

    # class Meta:
    #     widgets = {'date': SelectDateWidget()}

    def __init__(self,*args,**kwargs):
        kwargs.setdefault('label_suffix', '')
        rtype = kwargs.pop("rtype")
        super(RequestForm, self).__init__(*args, **kwargs)

        if rtype == 'airport':

            self.fields['starting_destination'] = forms.ChoiceField(label='Starting Destination?', choices=AIRPORT_DESTINATIONS)
            self.fields['destination'] = forms.ChoiceField(label='Where go?', choices=AIRPORT_DESTINATIONS)

        elif rtype == 'shopping':
            self.fields['starting_destination'] = forms.ChoiceField(label='Starting Destination ', choices=SHOPPING_DESTINATIONS)
            self.fields['destination'] = forms.ChoiceField(label='Where go? ', choices=SHOPPING_DESTINATIONS)
        elif rtype == 'other':


            self.fields['starting_destination'] = forms.CharField(label='Starting Destination?')
            self.fields['destination'] = forms.CharField(label='Where go?')
        self.fields['number_going'] = forms.IntegerField(label = 'How many others can go?', min_value=1, max_value=10)
        self.fields['date'] = forms.DateField(widget=SelectDateWidget, label="When go?",

                                              initial=date.today())
        self.fields['time'] = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, minute_step=5, use_seconds=False), label="What time go? ")
        #forms.TimeField(widget=Select label="What time go (HH:MM)?")

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

        ride_date = cleaned_data.get('date')
        ride_time = cleaned_data.get('time')
        date_time = ('%s %s' % (ride_date, ride_time))
        if (date_time[0:4] == "None"):
            raise forms.ValidationError("")

        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        if datetime.now() >= date_time:
            raise forms.ValidationError(u'Invalid input: Please enter a future time and date! "%s"' % date_time)


        if (starting_destination.upper() == destination.upper()):
            raise forms.ValidationError(u'Invalid input: Start and end location cannot be the same!')

        #raise forms.ValidationError("%s" %destination)
        return cleaned_data
