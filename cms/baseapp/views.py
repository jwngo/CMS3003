from django.shortcuts import render
from django.http import HttpResponseRedirect
import json

# Create your views here.

def dashboard(request):
	return render(request, 'dashboard.html', None)

def incidents_map(request):
	return render(request, 'map.html', None)

def new_incident_form(request):
	return render(request, 'new_incident_form.html', None)

def incident_details(request):
	return render(request, 'incident_details.html', None)

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
