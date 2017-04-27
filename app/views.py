from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import View
from django.utils import timezone
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from .forms import RequestForm
from time import strftime
from django.db import models
from .models import Rides, Users
import os
# Create your views here.
@login_required(login_url='/accounts/login/')

#public facing index page
# def public_index(request):
# 	context = {
# 		'Title': 'Welcome to Princeton Pool!',
# 	}

# 	return render(request, 'app/pre_login.html', context)

#inside index page
def index(request):
	user = request.user
	rider, created = Users.objects.get_or_create(netid=user.username)
	context = {
		'Title': 'Welcome to Princeton Pool!',
		'netid': user.username
	}

	return render(request, 'app/index.html', context)

def about(request):
	user = request.user
	context = {
		'Title': 'About Us',
		'netid': user.username,
	}
	return render(request, 'app/about.html', context)

def faq(request):
	user = request.user
	context = {
		'Title': 'FAQs',
		'netid': user.username,
	}
	return render(request, 'app/faq.html', context)

def feedback(request):
	user = request.user
	context = {
		'Title': 'Feedback',
		'netid': user.username,
	}
	return render(request, 'app/feedback.html', context)

def your_rides(request):
	user = request.user
	theUser = Users.objects.get(netid=user.username) 
	rides = theUser.pools.all()
	context = {
		'Title': 'Your Rides',
		'rides': rides,
		'netid': user.username,
	}
	return render(request, 'app/your_rides.html', context)

def open_airport(request):
	user = request.user
	context = {
		'Title': 'Open Airport Requests',
		'rides': Rides.objects.all(),
		'netid': user.username,
	}
	return render(request, 'app/open_req_list.html', context)

def open_airport_new(request):
	form = RequestForm()
	user = request.user
	context = {
		'Title': 'New Airport Request',
		'form': form,
		'netid': user.username,
	}
	return render(request, 'app/form.html', context)

def confirm_new_airport(request):
	form = RequestForm(request.POST)
	user = request.user
	if form.is_valid():
		context = {
			'Title': 'Confirm New Airport',
			'name': form.cleaned_data['name'],
			'email': form.cleaned_data['email'],
			'dest': form.cleaned_data['destination'],
			'number_going': form.cleaned_data['number_going'],
			'date': form.cleaned_data['date'],
			'time': form.cleaned_data['time'],
			'netid': user.username,
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
	user = request.user
	name = request.session['name']
	email = request.session['email']
	dest = request.session['dest']
	number_going = request.session['number_going']
	date = request.session['date']
	time = request.session['time']


	ride = Rides(ride_type="Airport", start_destination = "PTON", end_destination=dest, 
				 other_destination="", date_time=date + " " + time, req_date_time=timezone.now(),
				 seats = number_going, owner = user.username, full_name=name, own_car=False)

	ride.save()
	rider, created = Users.objects.get_or_create(netid=user.username)
	rider.save()
	rider.pools.add(ride)
	rider.save()
	ride.usrs.add(rider)
	ride.save()
	context = {
		'Title': 'New Airport Confirmation',
		'name': name,
		'email': email,
		'dest': dest,
		'number_going': number_going,
		'date': date,
		'time': time,
		'netid': user.username,
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
	user = request.user
	context = {
		'Title': 'Join Airport Ride',
		'Dest': ride.end_destination,
		'Date': ride.date_time,
		'id': ride_id,
		'Riders': ride.usrs.all(),
		'netid': user.username,
	}
	return render(request, 'app/confirm_join.html', context)

def confirm_join_airport(request, ride_id):
	ride = get_object_or_404(Rides, pk=ride_id)

	name = "netid"+str(ride_id)
	#user = Users(full_name=name)
	#user = request.user
	user = request.user
	rider, created = Users.objects.get_or_create(netid=user.username)
	rider.save()
	#rider.full_name
	#user.pools.add(ride)
	user.save()
	ride.usrs.add(rider)
	ride.save()

	email = user.username + '@princeton.edu'

	context = {

		'Riders': ride.usrs.all(),
		'title': 'Confirm Join Airport',
		'dest': ride.end_destination,
		'date': ride.date_time,
		'netid': user.username,
		'email': user.username + '@princeton.edu',
	}
	# email notif


	subject_line = 'Your Ride Request to ' + ride.end_destination
	message = 'Hello!\n\nYour ride request has been created.\n\n' + 'For your records, we have created a request for ' + str(ride.date_time) + ', for destination ' + ride.end_destination + '. To make any changes, please visit the \"Your Rides\" page on our website.\n' + 'Thank you for using Princeton Go!'
	send_mail(subject_line, message,
			  'Princeton Go <princetongo333@gmail.com>', [email],
			  fail_silently=False,
			  )

	# update DB

	return render(request, 'app/confirmed_join.html', context)

def open_shopping(request):
	user = request.user
	context = {
		'Title': 'Open Shopping Requests',
		'netid': user.username,
	}
	return render(request, 'app/open_req_list.html', context)

def open_other(request):
	user = request.user
	context = {
		'Title': 'Open Miscellaneous Requests',
		'netid': user.username,
	}
	return render(request, 'app/open_req_list.html', context)
