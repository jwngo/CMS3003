import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pprint import pprint
from datetime import datetime
from .PostalCodeAPIManager import postal_code_to_latlong, postal_code_to_region, postal_code_to_area

# Initialize firebase
cred = credentials.Certificate(
    './baseapp/APImodules/cms3003-e1f9c-firebase-adminsdk-3bp9c-6e02ae72ed.json')
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

  # Prepare data to be saved to firebase
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

  # Save incident data to firebase
  pprint(data)
  db.collection('incidents').document(str(incident_id)).set(data)

  # Save report data to firebase
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

  # Prepare data to be saved to firebase
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

  # Save report data to firebase
  pprint(data)
  db.collection('incidents').document(str(incident_id)).collection(
      'reports').document(str(report_reporter_number)).set(data)


def saveSubscriberToFirebase(request):
  # Extract data from POST request
  data = request.POST.copy()
  subscriber_name = data.get('name')
  subscriber_number = data.get('number')
  subscriber_region = data.get('region')

  # Prepare data to be saved to firebase
  data = {
      'subscriber_name': subscriber_name,
      'subscriber_number': subscriber_number,
      'subscriber_region': subscriber_region,
  }

  # Save subscriber data to firebase
  pprint(data)
  db.collection('subscribers').add(data)


def getIncidentFromFirebase(incident_id):
  # Retrieve incident data from firebase with specifed incident_id
  incident_data = db.collection('incidents').document(str(incident_id)).get()

  return incident_data.to_dict()


def getReportsFromFirebase(incident_id):
  reports_data = {}

  # Retrieve reports data from firebase with specifed incident_id
  reports = db.collection('incidents').document(
      str(incident_id)).collection('reports').get()

  # Push each data into the returning dictionary, starting the count at 1
  for count, report in enumerate(reports, 1):
    reports_data[count] = report.to_dict()

  return reports_data


def getAllSubscribers():
  subscribers_data = {}

  # Retrieve all subscribers data from firebase
  subscribers = db.collection('subscribers').get()

  # Push each data into the returning dictionary, starting the count at 1
  for count, subscriber in enumerate(subscribers, 1):
    subscribers_data[count] = subscriber.to_dict()
  
  return subscribers_data


def getSubscribersByRegion(region):
  subscribers_data = {}

  # Retrieve subscribers data from firebase, using the region parameter
  subscribers = db.collection('subscribers').where('subscriber_region', '==', region).get()

  # Push each data into the returning dictionary, starting the count at 1
  for count, subscriber in enumerate(subscribers, 1):
    subscribers_data[count] = subscriber.to_dict()

  return subscribers_data
