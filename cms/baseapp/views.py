from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from .firebase import saveIncidentToFirebase
import json

# Create your views here.

def dashboard(request):
	data = Incident.objects.values()
	incidents = {'incidents': data}
	return render(request, 'dashboard.html', incidents)

def subscribe(request):
	# handle subscription details
	if request.method == 'POST':
		data = request.POST.copy()
		name = data.get('name')
		number = data.get('number')
		region = data.get('region')
		print(name, number, region)

	return render(request, 'subscribe.html', None)

# incident related
def incidents_map(request):
	data = Incident.objects.values()
	incidents = {'incidents': data}
	return render(request, 'map.html', incidents)

def new_incident_form(request):
	if request.method == 'POST':
		saveIncidentToFirebase(request)
		return render(request, 'dashboard.html', None)

	return render(request, 'new_incident_form.html', None)

def incident_details(request, incident_id):
	data = Report.objects.filter(incident=incident_id)
	reports = {'reports' : data}
	return render(request, 'incident_details.html', reports)

def manage_incident(request):
	return render(request, 'manage_incident.html', None)

def new_report_form(request):
	return render(request, 'new_report_form.html', None)
