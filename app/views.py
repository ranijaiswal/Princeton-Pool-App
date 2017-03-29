from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
import os
# Create your views here.

@login_required
def index(request):
	context = {
		'Title': 'Welcome to Princeton Pool!!',
	}
	
	return render(request, 'app/main.html', context)
