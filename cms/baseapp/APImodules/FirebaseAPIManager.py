import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pprint import pprint
from datetime import datetime
from .PostalCodeAPIManager import postal_code_to_latlong, postal_code_to_region, postal_code_to_area

# Initialize firebase
cred = credentials.Certificate(
    './baseapp/APImodules/up-childcare-firebase-adminsdk-mb9n5-149f2c0647.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# For updating of incident_id
i_id = 0


def on_snapshot(col_snapshot, changes, read_time):
  print('Updating incident count')
  global i_id
  count = 1

  for doc in col_snapshot:
    count += 1

  i_id = count


incidents_collection_query = db.collection(u'incidents')
incident_query_watch = incidents_collection_query.on_snapshot(on_snapshot)


def saveIncidentToFirebase(request):
  # Extract data from POST request
  global i_id
  data = request.POST.copy()
  incident_id = i_id
  incident_managedBy = request.user.username
  incident_type = data.getlist('incident_type_of_incident')
  incident_address = data.get('incident_address')
  incident_postalcode = data.get('incident_postalcode')
  incident_description = data.get('incident_description')
  incident_lat, incident_lng = postal_code_to_latlong(incident_postalcode)
  incident_region = postal_code_to_region(incident_postalcode)
  incident_area = postal_code_to_area(incident_postalcode)
  incident_status = 'Reported'
  incident_level = 'CAT2'
  incident_created_at_date = '{:%d %B %Y}'.format(datetime.now())
  incident_created_at_time = '{:%H:%M}'.format(datetime.now())

  data = {
      'incident_id': incident_id,
      'incident_type': incident_type,
      'incident_managedBy': incident_managedBy,
      'incident_area': incident_area,
      'incident_region': incident_region,
      'incident_status': incident_status,
      'incident_level': incident_level,
      'incident_created_at_date': incident_created_at_date,
      'incident_created_at_time': incident_created_at_time,
      'incident_address': incident_address,
      'incident_postalcode': incident_postalcode,
      'incident_lat': incident_lat,
      'incident_lng': incident_lng,
      'incident_description': incident_description
  }

  # Save incident data to firestore
  pprint(data)
  db.collection('incidents').document(str(incident_id)).set(data)

  # Save report data to firestore
  saveReportToFirebase(str(incident_id), request)


def saveReportToFirebase(incident_id, request):
  # Extract data from POST request
  data = request.POST.copy()
  report_num_of_casualties = data.get('report_num_of_casualties')
  report_assistance_requested = data.getlist('report_assistance_requested')
  report_num_ambulance = data.get('report_num_ambulance_requested')
  report_num_firetruck = data.get('report_num_firetruck_requested')
  report_num_police = data.get('report_num_police_requested')
  report_num_gasleak = data.get('report_num_gasleak_requested')
  report_reporter_name = data.get('report_reporter_name')
  report_reporter_number = data.get('report_reporter_number')
  report_description = data.get('incident_description')
  report_status = 'Reported'
  report_assistance_dispatch_id = {
    'Ambulance': 0,
    'Fire Fighting': 0,
    'Police': 0,
    'Gasleak': 0
  } 

  data = {
      'report_num_of_casualties': report_num_of_casualties,
      'report_assistance_requested': report_assistance_requested,
      'report_assistance_dispatch_id': report_assistance_dispatch_id,
      'report_num_ambulance': report_num_ambulance,
      'report_num_firetruck': report_num_firetruck,
      'report_num_police': report_num_police,
      'report_num_gasleak': report_num_gasleak,
      'report_reporter_name': report_reporter_name,
      'report_reporter_number': report_reporter_number,
      'report_description': report_description,
      'report_status': report_status
  }

  # Save report data to firestore
  pprint(data)
  db.collection('incidents').document(str(incident_id)).collection(
      'reports').document(str(report_reporter_number)).set(data)

  # # Save assitance data to firestore
  # saveAssistanceToFirebase(
  #     str(incident_id), str(report_reporter_number), request)


# def saveAssistanceToFirebase(incident_id, report_id, request):
#   # Extract data from POST request
#   data = request.POST.copy()
#   report_assitance_requested = data.getlist('report_assitance_requested')

#   # Save assistance data to firestore
#   for assistance_requested in report_assitance_requested:
#     data = {
#         'report_assistance_requested': assistance_requested,
#         'report_assistance_dispatch_id': ''
#     }

#     db.collection('incidents').document(str(incident_id)).collection('reports').document(
#         str(report_id)).collection('assistances').document(str(assistance_requested)).set(data)


def getIncidentFromFirebase(incident_id):
  # Retrieve incident data from firebase with specifed incident_id
  incident_data = db.collection('incidents').document(str(incident_id)).get()

  return incident_data.to_dict()


def getReportsFromFirebase(incident_id):
  reports_data = {}

  # Retrieve reports data from firebase with specifed incident_id
  reports = db.collection('incidents').document(str(incident_id)).collection('reports').get()

  # Starting the count at 1
  for count, report in enumerate(reports, 1):
    reports_data[count] = report.to_dict()

  return reports_data


# def getAssistancesFromFirebase(incident_id, report_id):
#   assitances_data = {}

#   # Retrieve assitances data from firebase with specifed incident_id, report_id
#   assistances = db.collection('incidents').document(str(incident_id)).collection('reports').document(str(report_id)).collection('assistances').get()

#   # Starting the count at 1
#   for count, assistance in enumerate(assistances, 1):
#     assitances_data[count] = assistance.to_dict()
  
#   return assitances_data
