from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.

def base(request):
	return render(request, 'base.html', None)

def map(request):
	return render(request, 'map.html', None)

def new_incident_form(request):
	return render(request, 'new_incident_form.html', None)

def incident_details(request):
	return render(request, 'incident_manage.html', None)