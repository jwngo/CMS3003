from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
import json

# Create your views here.

def dashboard(request):
	data = Incident.objects.values()
	incidents = {'incidents': data}
	return render(request, 'dashboard.html', incidents)

def incidents_map(request):
	return render(request, 'map.html', None)

def new_incident_form(request):
	return render(request, 'new_incident_form.html', None)

def incident_details(request, incident_id):
	data = Report.objects.filter(incident=incident_id)
	reports = {'reports' : data}
	print(reports)
	return render(request, 'incident_details.html', reports)

def manage_incident(request):
	return render(request, 'manage_incident.html', None)

def subscribe(request):
	# handle subscription details
	if request.method == 'POST':
		data = request.POST.copy()
		name = data.get('name')
		number = data.get('number')
		region = data.get('region')
		print(name, number, region)

	return render(request, 'subscribe.html', None)
