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
  i_type = data.getlist('type_of_incident')
  i_managedBy = request.user.username
  i_area = None
  i_region = None
  i_status = None
  i_level = None
  i_created_at_date = None
  i_created_at_time = None
  i_address = data.get('i_address')
  i_postalcode = data.get('i_postalcode')
  i_description = data.get('i_description')

def saveReportToFirebase(i_id, request):
  data = request.POST.copy()
  r_num_of_casualties = data.get('num_of_casualties')
  r_assitance_requested = data.getlist('assitance_requested')
  r_num_ambulance = data.get('num_ambulance_requested')
  r_num_firetruck = data.get('num_firetruck_requested')
  r_num_police = data.get('num_police_requested')
  r_num_gasleak = data.get('num_gasleak_requested')
  r_reporter_name = data.get('reporter_name')
  r_reporter_number = data.get('reporter_number')