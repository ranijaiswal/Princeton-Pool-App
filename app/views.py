from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import View
from django.utils import timezone
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from .forms import RequestForm
from time import strftime
from django.db import models
from .models import Rides, Users
import os
# Create your views here.
@login_required(login_url='/accounts/login/')

def get_netid(r):
	return r.user.username
def index(request):
	context = {
		'Title': 'Welcome to Princeton Pool!',
		'netid': get_netid(request),
	}

	return render(request, 'app/index.html', context)

def about(request):
	context = {
		'Title': 'About Us',
		'netid': get_netid(request),
	}
	return render(request, 'app/about.html', context)

def faq(request):
	context = {
		'Title': 'FAQs',
		'netid': get_netid(request),
	}
	return render(request, 'app/faq.html', context)

def open_airport(request):
	context = {
		'Title': 'Open Airport Requests',
		'rides': Rides.objects.all(),
		'netid': get_netid(request),
	}
	return render(request, 'app/open_req_list.html', context)

def open_airport_new(request):
	form = RequestForm()
	context = {
		'Title': 'New Airport Request',
		'form': form,
		'netid': get_netid(request),
	}
	return render(request, 'app/form.html', context)

def confirm_new_airport(request):
	form = RequestForm(request.POST)
	if form.is_valid():
		context = {
			'Title': 'Confirm New Airport',
			'name': form.cleaned_data['name'],
			'email': form.cleaned_data['email'],
			'dest': form.cleaned_data['destination'],
			'number_going': form.cleaned_data['number_going'],
			'date': form.cleaned_data['date'],
			'time': form.cleaned_data['time'],
			'netid': get_netid(request),
		}
		request.session['name'] = form.cleaned_data['name']
		request.session['email'] = form.cleaned_data['email']
		request.session['dest'] = form.cleaned_data['destination']
		request.session['number_going'] = form.cleaned_data['number_going']
		request.session['date'] = form.cleaned_data['date'].isoformat()
		request.session['time'] = form.cleaned_data['time'].strftime("%H:%M")
		return render(request, 'app/confirm_ride.html', context)
	else: 
		raise Http404

def confirmation_new_airport(request):
	name = request.session['name']
	email = request.session['email']
	dest = request.session['dest']
	number_going = request.session['number_going']
	date = request.session['date']
	time = request.session['time']


	ride = Rides(start_destination = "PTON", end_destination=dest, 
				 date_time=date + " " + time, req_date_time=timezone.now(), 
				 seats = number_going, owner = name)
	
	ride.save()
	user = Users(full_name=name)
	user.save()
	user.pools.add(ride)
	user.save()
	ride.usrs.add(user)
	ride.save()

	context = {
		'Title': 'New Airport Confirmation',
		'name': name,
		'email': email,
		'dest': dest,
		'number_going': number_going,
		'date': date,
		'time': time,
		'netid': get_netid(request),
	}
	subject_line = 'Your Ride Request to ' + dest
	message = 'Hello, ' + name + '!\n\nYour ride request has been created.\n\n' + 'For your records, we have created a request for ' + date + ' at ' + time + ', for destination ' + dest + '. You have indicated that you have ' + str(number_going) + ' seats. To make any changes, please visit the \"Your Rides\" page on our website.\n' + 'Thank you for using Princeton Go!'
	send_mail(subject_line, message, 
			  'Princeton Go <princetongo333@gmail.com>', [email], 
			  fail_silently=False,
			  )
	
	return render(request, 'app/confirmed_ride.html', context)

def join_airport_ride(request, ride_id):

	ride = get_object_or_404(Rides, pk=ride_id)
	
	context = {
		'Title': 'Join Airport Ride',
		'Dest': ride.end_destination,
		'Date': ride.date_time,
		'id': ride_id,
		'netid': get_netid(request),
	}
	return render(request, 'app/confirm_join.html', context)

def confirm_join_airport(request, ride_id):
	ride = get_object_or_404(Rides, pk=ride_id)
	context = {
		'Title': 'Confirm Join Airport',
		'Dest': ride.end_destination,
		'Date': ride.date_time,
		'Users': ride.usrs.all(),
		'netid': get_netid(request),
	}
	# update DB

	return render(request, 'app/confirmed_join.html', context)
def open_shopping(request):
	context = {
		'Title': 'Open Shopping Requests',
		'netid': get_netid(request),
	}
	return render(request, 'app/open_requests.html', context)
