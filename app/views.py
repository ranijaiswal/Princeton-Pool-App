from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
import os
# Create your views here.

# @login_required(login_url='/accounts/login/')
def index(request):
	context = {
		'Title': 'Welcome to Princeton Pool!',
	}

	return render(request, 'app/index.html', context)

def about(request):
	context = {
		'Title': 'About Us',
	}
	return render(request, 'app/about.html', context)

def faq(request):
	context = {
		'Title': 'FAQs',
	}
	return render(request, 'app/faq.html', context)

def open_airport(request):
	context = {
		'Title': 'Open Airport Requests',
	}
	return render(request, 'app/open_req_list.html', context)

def open_airport_new(request):
	context = {
		'Title': 'New Airport Request',
	}
	return render(request, 'app/form.html', context)

def join_airport_ride(request):
	context = {
		'Title': 'Join Airport Ride',
	}
	return render(request, 'app/confirm_join.html', context)

def confirm_join_airport(request):
	context = {
		'Title': 'Confirm Join Airport',
	}
	return render(request, 'app/confirmed_join.html', context)

def confirm_new_airport(request):
	context = {
		'Title': 'Confirm New Airport',
	}
	return render(request, 'app/confirm_ride.html', context)

def confirmation_new_airport(request):
	context = {
		'Title': 'New Airport Confirmation',
	}
	return render(request, 'app/confirmed_ride.html', context)

def open_shopping(request):
	context = {
		'Title': 'Open Shopping Requests',
	}
	return render(request, 'app/open_requests.html', context)
