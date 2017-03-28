from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import _ssl;_ssl.PROTOCOL_SSLv23 = _ssl.PROTOCOL_SSLv3
from .CASClient import CASClient
import os
# Create your views here.
def index(request):
	context = {
		'Title': 'Welcome to Princeton Pool!',
	}
	'''C = CASClient()
	netid = C.Authenticate()

	print("Content-Type: text/html")
	print("")

	print("Hello from the other side, %s\n" % netid)

	print("<p>Think of this as the main page of your application after %s has been authenticated." % (netid))
	'''
	
	return render(request, 'app/main.html', context)
