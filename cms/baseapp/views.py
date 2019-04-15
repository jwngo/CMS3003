import os
import sys
sys.path.insert(0, os.path.abspath(".."))
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from .APImodules.FirebaseAPIManager import saveSubscriberToFirebase, saveIncidentToFirebase, saveReportToFirebase, getIncidentFromFirebase, getReportsFromFirebase, getAllSubscribers, getSubscribersByRegion
from .APImodules.SMSAPIManager import sendSMSToSubscribers
from .APImodules.NotificationManager import notify
from .models import Report, Assistance
from threading import Thread
from pprint import pprint
import json

# Public related views


def public_redirect(request):
  return redirect('subscribe')


def dashboard(request):
  return render(request, 'dashboard.html', None)


def login_redirect(request):
  return redirect('user_login')


def user_login(request):
  message = None

  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    # authenticate the user
    user = authenticate(username=username, password=password)
    if (not user):
      # authentication failed
      message = 'Either the username or password is incorrect'
    else:
      login(request, user)
      if request.GET.get("next"):
        return redirect(request.GET.get("next"))
      else:
        return redirect("dashboard")

  return render(request, "registration/login.html", {'message': message})


def user_logout(request):
  logout(request)
  return redirect('user_login')


def subscribe(request):
  message = None

  if request.method == 'POST':
    saveSubscriberToFirebase(request)
    message = 'Successfully Subscribed!'

  return render(request, 'subscribe.html', {'message': message})


# Incident related views


def incidents_map(request):
  # remove assistance if not required
  return render(request, 'map.html', None)


def new_incident_form(request):
  if request.method == 'POST':
    
    # Save to firebase
    incident = saveIncidentToFirebase(request)

    # Send SMS to relevant Subscribers in a new Thread
    # This will improve the time taken to redirect back to dashboard
    thread = Thread(target=sendSMSToSubscribers, args=(incident,))
    thread.start()
    thread = Thread(target=notify, args=(incident,))
    thread.start()

    # Redirect to dashboard after adding new incident
    return redirect('dashboard')

  return render(request, 'new_incident_form.html', None)


def incident_details(request, incident_id):
  if request.method == "POST":
    saveReportToFirebase(incident_id, request)
  incident = getIncidentFromFirebase(incident_id)
  reports = getReportsFromFirebase(incident_id)
  # Wrapping the data in context
  pprint(incident)
  pprint(reports)
  casualties=0
  for key, report in reports.items():
    casualties+= int(report['report_num_of_casualties'])
  context = {
      'incident': incident,
      'reports': reports,
      'casualties': casualties,
  }

  return render(request, 'incident_details.html', context)


def manage_incident(request):
  return render(request, 'manage_incident.html', None)


def new_report_form(request):
  return render(request, 'new_report_form.html', None)
