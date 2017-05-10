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

def init_User(netid):
	if not Users.objects.filter(netid=netid).exists():
		full_name = scrape_name(netid)
		Users.objects.create(netid=netid, first_name=full_name[0], last_name=full_name[1])

@login_required(login_url='/accounts/login/')
def my_rides(request):
	user = request.user
	init_User(user.username)

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
	init_User(user.username)

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
	init_User(user.username)
	rtype = request.path.split('/')[1]
	theUser = Users.objects.get(netid=user.username)

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
		'first_name': theUser.first_name,
	}
	return render(request, 'app/form.html', context)

@login_required(login_url='/accounts/login/')
def confirm_new_request(request):
	rtype = request.path.split('/')[1]
	form = RequestForm(request.POST or None, rtype=rtype)
	user = request.user
	init_User(user.username)
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
	init_User(user.username)
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
	rider = Users.objects.get(netid=user.username)
	rider.save()
	rider.pools.add(ride)
	rider.save()
	ride.usrs.add(rider)
	ride.save()

	datetime_object = datetime.strptime(ride.date_time, '%Y-%m-%d %H:%M')

	context = {
		'Title': 'New Airport Confirmation',
		'start': start,
		'dest': dest,
		'number_going': number_going,
		'date': datetime_object.date(),
		'time': datetime_object.time(),
		'netid': user.username,
		'rtype': request.path.split('/')[1],
	}

	datetime_object = datetime.strptime(ride.date_time, '%Y-%m-%d %H:%M')
	date_obj_str = datetime_object.strftime('%m/%d/%Y %I:%M %p')[0:date_length]
	time_obj_str = datetime_object.strftime('%m/%d/%Y %I:%M %p')[date_length:] + ' EST'
	
	mail = EmailMultiAlternatives(
		subject= 'Ride #' + str(ride.id) + ' To ' + ride.end_destination,
		body= 'Idk what goes here?',
		from_email= 'Princeton Go <princetongo333@gmail.com>',
		to=[user.username + '@princeton.edu']
		)
	# Add template
	mail.template_id = '4f75a67a-64a9-47f5-9a59-07646a578b9f'

	# Replace substitutions in template
	message = 'Your ride request has been created! Below you can find the information for your ride.'
	theUser = Users.objects.get(netid=user.username)
	closing = 'Thank you for using Princeton Go! We hope you enjoy your ride.'
	mail.substitutions = {'%names%': theUser.first_name, '%body%': message, '%date%': date_obj_str, 
						  '%time%': time_obj_str, '%destination%': start + ' to ' + dest, 
						  '%riders%': theUser.first_name + " " + theUser.last_name, '%seats%': number_going,
						  '%closing%': closing}

	mail.attach_alternative(
    "<p>This is a simple HTML email body</p>", "text/html"
	)
	mail.send()
	return render(request, 'app/confirmed_ride.html', context)

@login_required(login_url='/accounts/login/')
def join_ride(request, ride_id):

	ride = get_object_or_404(Rides, pk=ride_id)
	user = request.user
	init_User(user.username)
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
	init_User(user.username)
	rider = Users.objects.get(netid=user.username)
	rider.save()
	rider.pools.add(ride)
	rider.save()
	ride.usrs.add(rider)
	ride.seats -= 1
	ride.save()

	context = {

		'Riders': ride.usrs.all(),
		'title': 'Successfully Joined Ride',
		'dest': ride.end_destination,
		'date': ride.date_time,
		'netid': user.username,
		'rtype': request.path.split('/')[1],
	}

	# email to everyone in the ride

	# list of all the riders
	riders_emails = []
	riders_firstnames = ""
	riders_fullnames = ""
	for rider in ride.usrs.all():
		riders_emails.append(rider.netid + '@princeton.edu')
		riders_firstnames = riders_firstnames + ", " + rider.first_name
		riders_fullnames = riders_fullnames + rider.first_name + " " + rider.last_name + ', '
	riders_firstnames = riders_firstnames.lstrip(', ')
	# put 'and' and delete comma if only two riders
	split_firsts = riders_firstnames.split(', ')
	num_riders = len(split_firsts)
	if num_riders == 2: 
		riders_firstnames = (' and ').join(split_firsts)
	else:
		riders_firstnames = (', ').join(split_firsts[0:(num_riders - 1)])
		riders_firstnames = riders_firstnames + ', and ' + split_firsts[num_riders - 1]

	riders_fullnames = riders_fullnames.rstrip(', ')
	
	date_obj_str = ride.date_time.strftime('%m/%d/%Y %I:%M %p')[0:date_length]
	time_obj_str = ride.date_time.strftime('%m/%d/%Y %I:%M %p')[date_length:] + ' EST'
	
	mail_to_riders = EmailMultiAlternatives(
		subject= 'Ride #' + str(ride.id) + ' To ' + ride.end_destination,
		body= 'Idk what goes here?',
		from_email= 'Princeton Go <princetongo333@gmail.com>',
		to=riders_emails
		)
	# Add template
	mail_to_riders.template_id = '4f75a67a-64a9-47f5-9a59-07646a578b9f'

	# Replace substitutions in template
	theUser = Users.objects.get(netid=user.username)
	message = theUser.first_name + ' ' + theUser.last_name +' has joined your ride! Below you can find the information for this ride.'
	closing = 'Thank you for using Princeton Go! We hope you enjoy your ride.'
	mail_to_riders.substitutions = {'%names%': riders_firstnames, '%body%': message, '%date%': date_obj_str, 
									'%time%': time_obj_str, '%destination%': ride.start_destination + ' to ' + ride.end_destination, 
									'%riders%': riders_fullnames, '%seats%': ride.seats, '%closing%': closing}

	mail_to_riders.attach_alternative(
    "<p>This is a simple HTML email body</p>", "text/html" #don't know what this does but it doesn't work w/o it, don't delete
	)
	mail_to_riders.send()

	return render(request, 'app/confirmed_join.html', context)

@login_required(login_url='/accounts/login/')
def drop_ride(request, ride_id):
	user = request.user
	init_User(user.username)
	ride = Rides.objects.get(pk=ride_id)
	idnum = str(ride.id)
	context = {
		'start': ride.start_destination,
		'end': ride.end_destination,
		'time': ride.date_time,
		'netid': user.username,
	}

	rider = Users.objects.get(netid=user.username)
	ride.usrs.remove(rider)
	ride.seats += 1
	rider.pools.remove(ride)
	ride.save()
	rider.save()

	# list of all the riders
	riders_emails = []
	riders_firstnames = ""
	riders_fullnames = ""
	for rider in ride.usrs.all():
		riders_emails.append(rider.netid + '@princeton.edu')
		riders_firstnames = riders_firstnames + ", " + rider.first_name
		riders_fullnames = riders_fullnames + rider.first_name + " " + rider.last_name + ', '

	riders_firstnames = riders_firstnames.lstrip(', ')
	# put 'and' and delete comma if only two riders
	split_firsts = riders_firstnames.split(', ')
	num_riders = len(split_firsts)
	if num_riders == 2: 
		riders_firstnames = (' and ').join(split_firsts)
	elif num_riders > 2:
		riders_firstnames = (', ').join(split_firsts[0:(num_riders - 1)])
		riders_firstnames = riders_firstnames + ', and ' + split_firsts[num_riders - 1]

	riders_fullnames = riders_fullnames.rstrip(', ')

	# email to dropper
	date_obj_str = ride.date_time.strftime('%m/%d/%Y %I:%M %p')[0:date_length]
	time_obj_str = ride.date_time.strftime('%m/%d/%Y %I:%M %p')[date_length:] + ' EST'
	
	mail_to_dropper= EmailMultiAlternatives(
		subject= 'Ride #' + str(ride.id) + ' To ' + ride.end_destination,
		body= 'Idk what goes here?',
		from_email= 'Princeton Go <princetongo333@gmail.com>',
		to=[user.username + '@princeton.edu']
		)
	# Add template
	mail_to_dropper.template_id = '4f75a67a-64a9-47f5-9a59-07646a578b9f'

	# Replace substitutions in template
	message = 'You have dropped a ride. For your records, below you can find the ride information.'
	theUser = Users.objects.get(netid=user.username)
	closing = 'Thank you for using Princeton Go!'
	mail_to_dropper.substitutions = {'%names%': theUser.first_name, '%body%': message, '%date%': date_obj_str, 
									 '%time%': time_obj_str, '%destination%': ride.start_destination + ' to ' + ride.end_destination, 
									 '%riders%': riders_fullnames, '%seats%': ride.seats, '%closing%': closing}

	mail_to_dropper.attach_alternative(
    "<p>This is a simple HTML email body</p>", "text/html" #don't know what this does but it doesn't work w/o it, don't delete
	)
	mail_to_dropper.send()

	# email to everyone in the ride
	
	mail_to_riders = EmailMultiAlternatives(
		subject= 'Ride #' + str(ride.id) + ' To ' + ride.end_destination,
		body= 'Idk what goes here?',
		from_email= 'Princeton Go <princetongo333@gmail.com>',
		to=riders_emails
		)
	# Add template
	mail_to_riders.template_id = '4f75a67a-64a9-47f5-9a59-07646a578b9f'

	# Replace substitutions in template
	message = theUser.first_name + ' ' + theUser.last_name +' has dropped your ride. We have increased the number of available seats, as you can see below in the ride information.'
	closing = 'Thank you for using Princeton Go! We hope you enjoy your ride.'
	mail_to_riders.substitutions = {'%names%': riders_firstnames, '%body%': message, '%date%': date_obj_str, 
									'%time%': time_obj_str, '%destination%': ride.start_destination + ' to ' + ride.end_destination, 
									'%riders%': riders_fullnames, '%seats%': ride.seats, '%closing%': closing}

	mail_to_riders.attach_alternative(
    "<p>This is a simple HTML email body</p>", "text/html" #don't know what this does but it doesn't work w/o it, don't delete
	)
	mail_to_riders.send()

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
	search_terms=[]
	if (request.method == "GET"):
		search_text = request.GET.get("rides_search_text", "").strip().upper()
		search_terms = search_text.split(" ")
		#if (len(search_terms) > 1):

	ride_type = request.GET.get('ride_type')


	user = request.user
	search_results=Rides.objects.all().filter(ride_type=ride_type, seats__gt=0, date_time__gt=datetime.now()).exclude(usrs__netid__contains = user.username)
	if (search_text != ""):
		#search_results = Rides.objects.all().filter(ride_type=ride_type, seats__gt=0, date_time__gt=datetime.now(), end_destination__contains=search_text).exclude(usrs__netid__contains = user.username)
		for term in search_terms:
			search_results = search_results.filter(end_destination__icontains=term) | search_results.filter(start_destination__icontains=term)
	context = {
		"search_text": search_text,
		"search_results": search_results,
	}


	return render(request, 'app/open_req_list_snippet.html',
						  context)