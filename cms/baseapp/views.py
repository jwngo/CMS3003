from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from .firebase import saveIncidentToFirebase
import json
from .firebase import getFirebase
# Create your views here.

db = getFirebase()

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
	incident_data = Incident.objects.values()
	# remove assistance if not required 
	assistance_data = Assistance.objects.values()
	context = {'incidents': incident_data, 'assistances': assistance_data }
	print(context)
	return render(request, 'map.html', context)

def new_incident_form(request):
	if request.method == 'POST':
		saveIncidentToFirebase(request)
		return render(request, 'dashboard.html', None)

	return render(request, 'new_incident_form.html', None)

def incident_details(request, incident_id):
	# firebase example
	# incidentData = db.child("incidents").get() 
	# return render(request, 'incident_details.html', {'incidentData': incidentData.val()})
	report_data = Report.objects.filter(incident=incident_id)
	assistance_data = Assistance.objects.values()
	deployed_assistance_data = Assistance.objects.filter(dispatch_id__isnull=False).values() 
	context = {'reports' : report_data, 'assistances' : assistance_data, 'deployed_assistances': deployed_assistance_data}
	return render(request, 'incident_details.html', context)

def manage_incident(request):
	return render(request, 'manage_incident.html', None)

def new_report_form(request):
	return render(request, 'new_report_form.html', None)
