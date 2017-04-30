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
from datetime import datetime
import os
# Create your views here.


#public facing index page
# def public_index(request):
# 	context = {
# 		'Title': 'Welcome to Princeton Pool!',
# 	}

# 	return render(request, 'app/pre_login.html', context)

#inside index page
def index(request):
	user = request.user
	#Rides.objects.filter(date_time__lt=datetime.now()).delete()
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

@login_required(login_url='/accounts/login/')
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

def open_requests(request):
	user = request.user
	context = {}
	rtype = request.path.split('/')[1]
	if rtype == 'airport':
		context = {
			'Title': 'Open Airport Requests',
			'rides': Rides.objects.all().filter(ride_type='airport', seats__gt=0),
			'netid': user.username,
		}
	elif rtype == 'shopping':
		context = {
			'Title': 'Open Shopping Requests',
			'rides': Rides.objects.all().filter(ride_type='shopping', seats__gt=0),
			'netid': user.username,
		}
	else:
		context = {
			'Title': 'Open Miscellaneous Requests',
			'rides': Rides.objects.all().filter(ride_type='other', seats__gt=0),
			'netid': user.username,
		}
	return render(request, 'app/open_req_list.html', context)

@login_required(login_url='/accounts/login/')
def create_new_request(request):
	user = request.user
	form = RequestForm()
	context = {
		'Title': 'New Airport Request',
		'form': form,
		'netid': user.username,
	}
	return render(request, 'app/form.html', context)

@login_required(login_url='/accounts/login/')
def confirm_new_request(request):
	form = RequestForm(request.POST or None)
	user = request.user

	if request.method == 'POST':
		if form.is_valid():
			context = {
				'Title': 'Confirm New Airport',
				'start': form.cleaned_data['starting_destination'],
				'dest': form.cleaned_data['destination'],
				'number_going': form.cleaned_data['number_going'],
				'date': form.cleaned_data['date'],
				'time': form.cleaned_data['time'],
				'netid': user.username,
			}
			request.session['start'] = form.cleaned_data['starting_destination']
			request.session['dest'] = form.cleaned_data['destination']
			request.session['number_going'] = form.cleaned_data['number_going']
			request.session['date'] = form.cleaned_data['date'].isoformat()
			request.session['time'] = form.cleaned_data['time'].strftime("%H:%M")
			return render(request, 'app/confirm_ride.html', context)

	return render(request,'app/form_error.html', {'form': form})
	# else:
	# 	pass
		#raise

@login_required(login_url='/accounts/login/')
def confirmation_new_request(request):
	user = request.user
	start = request.session['start']
	dest = request.session['dest']
	number_going = request.session['number_going']
	date = request.session['date']
	time = request.session['time']

	rtype = request.path.split('/')[1]
	ride = Rides(ride_type=rtype, start_destination = start, end_destination=dest,
				 other_destination="", date_time=date + " " + time, req_date_time=timezone.now(),
				 seats = number_going)

	ride.save()
	rider, created = Users.objects.get_or_create(netid=user.username)
	rider.save()
	rider.pools.add(ride)
	rider.save()
	ride.usrs.add(rider)
	ride.save()
	context = {
		'Title': 'New Airport Confirmation',
		'start': start,
		'dest': dest,
		'number_going': number_going,
		'date': date,
		'time': time,
		'netid': user.username,
		'rtype': request.path.split('/')[1],
	}
	subject_line = 'Your Ride Request from ' + start + ' to ' + dest
	message = 'Hello!\n\nYour ride request has been created.\n\n' + 'For your records, we have created a request for ' + date + ' at ' + time + ', from ' + start + ' to ' + dest + '. You have indicated that you have ' + str(number_going) + ' seats. To make any changes, please visit the \"Your Rides\" page on our website.\n' + 'Thank you for using Princeton Go!'
	send_mail(subject_line, message,
			  'Princeton Go <princetongo333@gmail.com>', [user.username + '@princeton.edu'],
			  fail_silently=False,
			  )

	return render(request, 'app/confirmed_ride.html', context)

@login_required(login_url='/accounts/login/')
def join_ride(request, ride_id):

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

@login_required(login_url='/accounts/login/')
def confirm_join_ride(request, ride_id):
	ride = get_object_or_404(Rides, pk=ride_id)

	name = "netid"+str(ride_id)
	user = request.user
	rider, created = Users.objects.get_or_create(netid=user.username)
	rider.save()
	rider.pools.add(ride)
	rider.save()
	ride.usrs.add(rider)
	ride.seats -= 1
	ride.save()

	context = {

		'Riders': ride.usrs.all(),
		'title': 'Confirm Join Airport',
		'dest': ride.end_destination,
		'date': ride.date_time,
		'netid': user.username,
		'rtype': request.path.split('/')[1],
	}
	# email notif


	subject_line = 'Your Ride Request to ' + ride.end_destination
	message = 'Hello!\n\nYour ride request has been created.\n\n' + 'For your records, we have created a request for ' + str(ride.date_time) + ', for destination ' + ride.end_destination + '. To make any changes, please visit the \"Your Rides\" page on our website.\n' + 'Thank you for using Princeton Go!'
	send_mail(subject_line, message,
			  'Princeton Go <princetongo333@gmail.com>', [user.username + '@princeton.edu'],
			  fail_silently=False,
			  )

	# update DB

	return render(request, 'app/confirmed_join.html', context)

@login_required(login_url='/accounts/login/')
def drop_ride(request, ride_id):
	user = request.user
	ride = Rides.objects.get(pk=ride_id)

	context = {
		'start': ride.start_destination,
		'end': ride.end_destination,
		'time': ride.date_time,
		'netid': user.username,
	}

	rider, created = Users.objects.get_or_create(netid=user.username)
	ride.usrs.remove(rider)
	ride.seats += 1
	rider.pools.remove(ride)
	ride.save()
	rider.save()
	if (ride.usrs.count() == 0):
		ride.delete()
	return render(request, 'app/drop_ride.html', context)
