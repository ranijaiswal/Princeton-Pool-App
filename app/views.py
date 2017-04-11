from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from .forms import RequestForm
from time import strftime
from django.db import models
from .models import Rides
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
		'rides': Rides.objects.all()
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
			'Title': 'Confirm New Airport',
			'name': form.cleaned_data['name'],
			'dest': form.cleaned_data['destination'],
			'number_going': form.cleaned_data['number_going'],
			'date': form.cleaned_data['date'],
			'time': form.cleaned_data['time'],
		}
		request.session['name'] = form.cleaned_data['name']
		request.session['dest'] = form.cleaned_data['destination']
		request.session['number_going'] = form.cleaned_data['number_going']
		request.session['date'] = form.cleaned_data['date'].isoformat()
		request.session['time'] = form.cleaned_data['time'].strftime("%H:%M")
		return render(request, 'app/confirm_ride.html', context)
	else: 
		raise Http404

def confirmation_new_airport(request):
	name = request.session['name']
	dest = request.session['dest']
	number_going = request.session['number_going']
	date = request.session['date']
	time = request.session['time']

	ride = Rides(start_destination = "PTON", end_destination=dest, 
				 date_time=date + " " + time, req_date_time=timezone.now(), 
				 seats = number_going, owner = name)
	ride.save()
	context = {
		'Title': 'New Airport Confirmation',
		'name': name,
		'dest': dest,
		'number_going': number_going,
		'date': date,
		'time': time,
	}
	send_mail('Subject Test', 'Message test' + name + '\'s Ride!', 
			  'ranijaiswal116@gmail.com', ['cindyliu@princeton.edu'], 
			  fail_silently=False,
			  )
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
