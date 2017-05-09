from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import View
from django.utils import timezone
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from .forms import RequestForm, FeedbackForm
from time import strftime
from django.db import models
from .models import Rides, Users
from datetime import datetime
import os
from django.utils.timezone import activate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .serializers import RideSerializer

activate(settings.TIME_ZONE)
date_length=10

# jquery.autocomplete
# web request to web url - hits django function - parameter of query - django function - wrap in json blob (django query data to json) - send back w/ ajax ()
# jquery autocomplete django example


from bs4 import BeautifulSoup
from .scrape_name import scrape_name

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
	form = FeedbackForm()
	context = {
		'Title': 'Anonymous Feedback',
		'netid': user.username,
		'form': form
	}
	return render(request, 'app/feedback.html', context)

def feedback_thanks(request):
	user = request.user
	form = FeedbackForm(request.POST or None)
	if form.is_valid():

		message_name = form.cleaned_data['name']
		if message_name == "":
			message_name = "anonymous"

		message_email = ", whose email address is " + form.cleaned_data['email']
		if message_email == ", whose email address is ":
			message_email = ", who did not give an email address"

		message = form.cleaned_data['feedback']
		send_mail("Feedback",
				  "You have received feedback from " + message_name + message_email + ". They left the following message: \n\n" + message,
				  'Princeton Go <princetongo333@gmail.com>', ['princetongo333@gmail.com'],
				  fail_silently=False,
				  )
	context = {
		'Title': 'Thank you for the feedback!'
	}
	return render(request, 'app/feedback_thanks.html', context)

@login_required(login_url='/accounts/login/')
def my_rides(request):
	user = request.user
	theUser = Users.objects.get(netid=user.username)
	rides = theUser.pools.all()
	context = {
		'Title': 'My Rides',
		'rides': rides,
		'netid': user.username,
	}
	return render(request, 'app/my_rides.html', context)

@login_required(login_url='/accounts/login/')
def open_requests(request):
	user = request.user
	context = {}
	rtype = request.path.split('/')[1]
	if rtype == 'airport':
		context = {
			'Title': 'Open Airport Requests',
			'rides': Rides.objects.all().filter(ride_type='airport', seats__gt=0, date_time__gt=datetime.now()).exclude(usrs__netid__contains = user.username),
			'netid': user.username,
		}
	elif rtype == 'shopping':
		context = {
			'Title': 'Open Shopping Requests',
			'rides': Rides.objects.all().filter(ride_type='shopping', seats__gt=0, date_time__gt=datetime.now()).exclude(usrs__netid__contains = user.username),
			'netid': user.username,
		}
	else:
		context = {
			'Title': 'Open Miscellaneous Requests',
			'rides': Rides.objects.all().filter(ride_type='other', seats__gt=0, date_time__gt=datetime.now()).exclude(usrs__netid__contains = user.username),
			'netid': user.username,
		}
	return render(request, 'app/open_req_list.html', context)

@login_required(login_url='/accounts/login/')
def create_new_request(request):
	user = request.user
	rtype = request.path.split('/')[1]
	full_name = scrape_name(user.username)

	form = RequestForm(rtype=rtype)
	#form = RequestForm()

	title = "New Request"
	if rtype == 'airport':
		title = 'New Airport Request'
	elif rtype == 'shopping':
		title = 'New Shopping Request'
	context = {
		'Title': title,
		'form': form,
		'netid': user.username,
		'first_name': full_name[0],
	}
	return render(request, 'app/form.html', context)

@login_required(login_url='/accounts/login/')
def confirm_new_request(request):
	rtype = request.path.split('/')[1]
	form = RequestForm(request.POST or None, rtype=rtype)
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


	datetime_object = datetime.strptime(ride.date_time, '%Y-%m-%d %H:%M')

	subject_line = 'Ride #' + str(ride.id) + ' To ' + ride.end_destination

	message = 'Hello!\n\nYour ride request has been created.\n\n' + 'For your records, we have created a request for ' + datetime_object.strftime('%m/%d/%Y %I:%M %p')[0:date_length] + ' at ' + \
			  datetime_object.strftime('%m/%d/%Y %I:%M %p')[date_length:] + ', from ' + start + ' to ' + dest + '. You have indicated that you have ' + str(number_going) + ' seats. To make any changes, please visit the <a href="http://princeton-pool.herokuapp.com/my-rides"> My Rides</a> page on our website.\n' + 'Thank you for using Princeton Go!'
	send_mail(subject_line, message,
			  'Princeton Go <princetongo333@gmail.com>', [user.username + '@princeton.edu'],
			  html_message=message,
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


	# email to joiner
	subject_line = 'You Have Joined Ride #' + str(ride.id) + ' To ' + ride.end_destination
	message = 'Hello!\n\nYou have joined a ride!\n\n' + 'For your records, this ride is for ' + ride.date_time.strftime('%m/%d/%Y %I:%M %p')[0:date_length] + ' at ' + \
			  ride.date_time.strftime('%m/%d/%Y %I:%M %p')[date_length:] + ' EST' + ', from ' + ride.start_destination + ' to ' + ride.end_destination +\
			  '. To make any changes, please visit the <a href="http://princeton-pool.herokuapp.com/my-rides"> My Rides</a> page on our website.\n' + 'Thank you for using Princeton Go!'
	send_mail(subject_line, message, 'Princeton Go <princetongo333@gmail.com>',
			  [user.username + '@princeton.edu'], html_message=message,
			  fail_silently=False,
			  )

	# email to everyone in the ride
	subject_line = 'Ride #' + str(ride.id) + ' To ' + ride.end_destination

	# list of all the riders
	riders = []
	for rider in ride.usrs.all():
		riders.append(rider.netid + '@princeton.edu')
	message = 'Hello!\n\n' + user.username + ' has joined your ride. Happy travels!'
	send_mail(subject_line, message, 'Princeton Go <princetongo333@gmail.com>', riders, fail_silently=False)
	# update DB

	return render(request, 'app/confirmed_join.html', context)

@login_required(login_url='/accounts/login/')
def drop_ride(request, ride_id):
	user = request.user
	ride = Rides.objects.get(pk=ride_id)
	idnum = str(ride.id)
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

	# email to dropper
	subject_line = 'You Have Dropped Ride #' + idnum
	message = 'Hello!\n\nYou have dropped a ride.\n\n' + 'For your records, this ride was for ' + ride.date_time.strftime('%m/%d/%Y %I:%M %p')[0:date_length] + ' at ' + \
			  ride.date_time.strftime('%m/%d/%Y %I:%M %p')[date_length:] + ' EST' + ', from ' + ride.start_destination + ' to ' + ride.end_destination + '. Thank you for using Princeton Go!'
	send_mail(subject_line, message, 'Princeton Go <princetongo333@gmail.com>',
			  [user.username + '@princeton.edu'],
			  fail_silently=False,
			  )

	# email to everyone in the ride
	subject_line = 'Ride #' + str(ride.id) + ' To ' + ride.end_destination

	# list of all the riders
	riders = []
	for rider in ride.usrs.all():
		riders.append(rider.netid + '@princeton.edu')
	message = 'Hello!\n\n' + user.username + ' has dropped your ride. We have increased the number of available seats. Happy travels!'
	send_mail(subject_line, message, 'Princeton Go <princetongo333@gmail.com>', riders, fail_silently=False)

	#make sure this is the last thing done in the view
	if (ride.usrs.count() == 0):
		ride.delete()
	return render(request, 'app/drop_ride.html', context)


class RidesList(generics.ListAPIView):
	# model = Rides
	# context_object_name = "rides"

	serializer_class = RideSerializer

	def get_queryset(self):
		query_ride_type = self.kwargs['ride_type']
		return Rides.objects.filter(ride_type=query_ride_type)


def submit_search_from_ajax(request):
	rides=[]
	search_text=""
	if (request.method == "GET"):
		search_text = request.GET.get("rides_search_text", "").strip().upper()
	search_results=[]
	if (search_text != ""):
		search_results = Rides.objects.all()#filter(end_destination__contains=search_text)

	context = {
		"search_text": search_text,
		"search_results": search_results,
	}


	return render(request, 'app/open_req_list_snippet.html',
						  context)