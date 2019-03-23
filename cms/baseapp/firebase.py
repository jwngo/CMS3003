import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from .models import *

# Initialize firebase
cred = credentials.Certificate('./ssadproject-1551665312466-c888723cff4c.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def saveIncidentToFirebase(request):
  data = request.POST.copy()
  incident_type = data.getlist('type_of_incident')
  incident_managedBy = request.user.username
  incident_area = None
  incident_region = None
  incident_status = None
  incident_level = None
  incident_created_at_date = None
  incident_created_at_time = None
  incident_address = data.get('i_address')
  incident_postalcode = data.get('i_postalcode')
  incident_description = data.get('i_description')

def saveReportToFirebase(i_id, request):
  data = request.POST.copy()
  report_num_of_casualties = data.get('num_of_casualties')
  report_assitance_requested = data.getlist('assitance_requested')
  report_num_ambulance = data.get('num_ambulance_requested')
  report_num_firetruck = data.get('num_firetruck_requested')
  report_num_police = data.get('num_police_requested')
  report_num_gasleak = data.get('num_gasleak_requested')
  report_reporter_name = data.get('reporter_name')
  report_reporter_number = data.get('reporter_number')