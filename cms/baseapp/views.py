from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .APImodules.FirebaseAPIManager import saveIncidentToFirebase, getIncidentFromFirebase, getReportsFromFirebase, getAssistancesFromFirebase
from .models import Report, Assistance
from pprint import pprint
import json

# Create your views here.


def dashboard(request):
  return render(request, 'dashboard.html', None)


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
  context = {'incidents': incident_data}
  return render(request, 'map.html', context)


def new_incident_form(request):
  if request.method == 'POST':
    saveIncidentToFirebase(request)
    return redirect('dashboard')

  return render(request, 'new_incident_form.html', None)


def incident_details(request, incident_id):
  # # Firebase example
	# # Incidents
	# incident_data = getIncidentFromFirebase(incident_id)
	
	# # Reports
	# reports_data = getReportsFromFirebase(incident_id)
	# report_id = reports_data[1]['report_reporter_number']

	# # Assistances
	# assistances_data = getAssistancesFromFirebase(incident_id, report_id)

	# pprint(incident_data)
	# pprint('--')
	# pprint(reports_data)
	# pprint('--')
	# pprint(assistances_data)

  # report_data = Report.objects.filter(incident=incident_id)
  # assistance_data = Assistance.objects.values()
  # deployed_assistance_data = Assistance.objects.filter(
  #     dispatch_id__isnull=False).values()
  # context = {'reports': report_data, 'assistances': assistance_data,
  #            'deployed_assistances': deployed_assistance_data}

	return render(request, 'incident_details.html', None)


def manage_incident(request):
  return render(request, 'manage_incident.html', None)


def new_report_form(request):
  return render(request, 'new_report_form.html', None)
