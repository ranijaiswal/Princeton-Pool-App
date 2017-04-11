from django import forms

class RequestForm(forms.Form):
	name = forms.CharField(label='Full Name', max_length=100)
	email = forms.EmailField(label="Email", max_length=100)
	destination = forms.CharField(label="Destination", max_length=100)
	number_going = forms.IntegerField(max_value=10, min_value=1)
	date = forms.DateField(label="MM/DD/YYYY")
	time = forms.TimeField(label="HH:MM, military time")
	
