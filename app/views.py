from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import RequestForm
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
	form = RequestForm()
	context = {
		'Title': 'New Airport Request',
		'form': form
	}
	return render(request, 'app/form.html', context)

def confirm_new_airport(request):
	form = RequestForm(request.POST)
	if form.is_valid():
		context = {
			'form': form,
			'Title': 'Confirm New Airport',
			'name': form.cleaned_data['name'],
			'dest': form.cleaned_data['destination'],
			'number_going': form.cleaned_data['number_going'],
			'date': form.cleaned_data['date'],
			'time': form.cleaned_data['time'],
		}
		return render(request, 'app/confirm_ride.html', context)
	else: 
		raise Http404

def confirmation_new_airport(request):
	form = RequestForm(request.POST)
	context = {}
	if form.is_valid():
		name = form.cleaned_data['name']
		dest = form.cleaned_data['destination']
		number_going = form.cleaned_data['number_going']
		date = form.cleaned_data['date']
		time = form.cleaned_data['time']
		context = {
			'Title': 'New Airport Confirmation',
			'name': name,
			'dest': dest,
			'number_going': number_going,
			'date': date,
			'time': time,
		}
	return render(request, 'app/confirmed_ride.html', context)

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
def open_shopping(request):
	context = {
		'Title': 'Open Shopping Requests',
	}
	return render(request, 'app/open_requests.html', context)
