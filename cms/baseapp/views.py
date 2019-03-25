from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .APImodules.FirebaseAPIManager import saveIncidentToFirebase, getIncidentFromFirebase, getReportsFromFirebase
from .models import Report, Assistance
from pprint import pprint
import json

# Create your views here.


def public_redirect(request):
  return redirect('subscribe')

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
  incident = getIncidentFromFirebase(incident_id)
  reports = getReportsFromFirebase(incident_id)
  # Wrapping the data in context
  pprint(incident)
  pprint(reports)
  context = {
    'incident': incident,
    'reports': reports,
  }

  return render(request, 'incident_details.html', context)


def manage_incident(request):
  return render(request, 'manage_incident.html', None)


def new_report_form(request):
  return render(request, 'new_report_form.html', None)
