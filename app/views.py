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
		'Title': 'List of open airport requests',
	}
	return render(request, 'app/open_req_list.html', context)

def open_shopping(request):
	context = {
		'Title': 'List of open shopping requests',
	}
	return render(request, 'app/open_requests.html', context)
