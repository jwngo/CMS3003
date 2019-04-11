import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pprint import pprint
from datetime import datetime
from datetime import timedelta
from datetime import date
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

  return data


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
  
  return data


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

def getTime(date_Now):
    time_Now =  date_Now.time() 
    if(1 <= int(time_Now.minute) <= 9):
        return (str(time_Now.hour)+":"+"0"+str(time_Now.minute))
    else:
        return (str(time_Now.hour)+":"+str(time_Now.minute)) 

def getHandlingHourList(type_incident):
# handlingHourList = [3,2,2,2,1]
   handlingHourList = [0, 0, 0, 0, 0, 0]
   incident_documents_list = []
   # In firebase's object form
   incident_documents = db.collection('incidents').where('incident_type', 'array_contains', str(type_incident)).where('incident_status', '==', 'Handling').get()
    #get time
   date_Now = datetime.now()
   labelTuple = (getTime(date_Now),)

   for i in range(1,6):
        labelTuple = labelTuple + (getTime(date_Now - timedelta(hours=i)),)
   reverseTuple = labelTuple[::-1]
  
   for document in incident_documents:
        incident_documents_list.append(document.to_dict())

   # if no documents
   if(len(incident_documents_list) == 0):
        return handlingHourList
   else:
    # go through each document and classify document into specified time range
    for i in range(len(incident_documents_list)):
        #check dateTime and make sure that it is within 24 hours from the time now
        time = incident_documents_list[i]['incident_created_at_time']
        date=incident_documents_list[i]['incident_created_at_date']
        dateTime = time+' '+date
        check = datetime.strptime(dateTime, '%H:%M %d %B %Y')
        date_Now = datetime.now()
        if(check > (date_Now - timedelta(hours =24))):
            for i in range(6):
                start = (datetime.strptime(reverseTuple[i], "%H:%M")-timedelta(hours =1)).time()
                startRange = str(start.hour)+":"+str(start.minute)
                endRange = reverseTuple[i]
                if(time_in_range(startRange,endRange,datetime.time(datetime.strptime(time, "%H:%M")))):
                    handlingHourList[i]+=1
    return handlingHourList


def getClosedHourList(type_incident):
# closedHourList = [3,2,2,2,1]
   # handlingHourList = [3,2,2,2,1]
    closedHourList = [0, 0, 0, 0, 0]
    incident_documents_list = []
   # In firebase's object form
    incident_documents = db.collection('incidents').where('incident_type', 'array_contains', str(type_incident)).where('incident_status', '==', 'Closed').get()
    #get time
    date_Now = datetime.now()
    labelTuple = (getTime(date_Now),)

    for i in range(1,6):
            labelTuple = labelTuple + (getTime(date_Now - timedelta(hours=i)),)
    reverseTuple = labelTuple[::-1]
    
    for document in incident_documents:
            incident_documents_list.append(document.to_dict())

    # if no documents
    if(len(incident_documents_list) == 0):
            return closedHourList
    else:
        # go through each document and classify document into specified time range
        for i in range(len(incident_documents_list)):
            #check dateTime and make sure that it is within 24 hours from the time now
            time = incident_documents_list[i]['incident_created_at_time']
            date=incident_documents_list[i]['incident_created_at_date']
            dateTime = time+' '+date
            check = datetime.strptime(dateTime, '%H:%M %d %B %Y')
            date_Now = datetime.now()
            if(check > (date_Now - timedelta(hours =24))):
                for i in range(6):
                    start = (datetime.strptime(reverseTuple[i], "%H:%M")-timedelta(hours =1)).time()
                    startRange = str(start.hour)+":"+str(start.minute)
                    endRange = reverseTuple[i]
                    if(time_in_range(startRange,endRange,datetime.time(datetime.strptime(time, "%H:%M")))):
                        closedHourList[i]+=1
    return closedHourList


def getCasualtiesHourList(type_incident):
# casualtiesHourList = [3,3,4,5,10]
    casualtiesHourList = [0, 0, 0, 0, 0]

    incident_documents_list = []
    # In firebase's object form
    incident_documents = db.collection('incidents').where('incident_type', 'array_contains', str(type_incident)).get()

     #get time
    date_Now = datetime.now()
    labelTuple = (getTime(date_Now),)

    for i in range(1,6):
            labelTuple = labelTuple + (getTime(date_Now - timedelta(hours=i)),)
    reverseTuple = labelTuple[::-1]

    for document in incident_documents:
        incident_documents_list.append(document.to_dict())
    #if no documents
    if(len(incident_documents_list) == 0):
        return casualtiesHourList
    else:
        # go through each document and classify document into specified time range
        for i in range(len(incident_documents_list)):
            #check dateTime and make sure that it is within 24 hours from the time now
            time = incident_documents_list[i]['incident_created_at_time']
            date=incident_documents_list[i]['incident_created_at_date']
            dateTime = time+' '+date
            check = datetime.strptime(dateTime, '%H:%M %d %B %Y')
            date_Now = datetime.now()
            if(check > (date_Now - timedelta(hours =24))):
                for i in range(6):
                    start = (datetime.strptime(reverseTuple[i], "%H:%M")-timedelta(hours =1)).time()
                    startRange = str(start.hour)+":"+str(start.minute)
                    endRange = reverseTuple[i]
                    if(time_in_range(startRange,endRange,datetime.time(datetime.strptime(time, "%H:%M")))):
                        casualtiesHourList[i]+= countCasualties(incident_documents_list,i)
    return casualtiesHourList


def getHandlingDayList(type_incident):
    # handlingDayList = [3,2,2,2,1,4,4]
   handlingDayList = [0, 0, 0, 0, 0, 0, 0]
   incident_documents_list = []
   # In firebase's object form
   incident_documents = db.collection('incidents').where('incident_type', 'array_contains', str(type_incident)).where('incident_status', '==', 'Handling').get()
   for document in incident_documents:
    incident_documents_list.append(document.to_dict())

   # if no documents
   if(len(incident_documents_list) == 0):
       return handlingDayList
   else:
        # go through each document and classify document into specified time range
        for i in range(len(incident_documents_list)):
            
            date_raw = incident_documents_list[i]['incident_created_at_date']
            date = datetime.strptime(str(date_raw), '%d %B %Y')
            date_Now = datetime.now()
            boundary = date_Now - timedelta(days = 7)
            if(date>boundary):
                if(datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Monday"):
                    handlingDayList[0] += 1
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Tuesday"):
                    handlingDayList[1] += 1
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Wednesday"):
                    handlingDayList[2] += 1
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Thursday"):
                    handlingDayList[3] += 1
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Friday"):
                    handlingDayList[4] += 1
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Saturday"):
                    handlingDayList[5] += 1
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Sunday"):
                    handlingDayList[6] += 1

        return handlingDayList


def getClosedDayList(type_incident):
# closedDayList = [3,2,2,2,1,3,3]

    
   closedDayList = [0, 0, 0, 0, 0, 0, 0]
   incident_documents_list = []
   # In firebase's object form
   incident_documents = db.collection('incidents').where('incident_type', 'array_contains', str(type_incident)).where('incident_status', '==', 'Closed').get()
   for document in incident_documents:
    incident_documents_list.append(document.to_dict())

   # if no documents
   if(len(incident_documents_list) == 0):
       return closedDayList
   else:
        # go through each document and classify document into specified time range
        for i in range(len(incident_documents_list)):
            date_raw = incident_documents_list[i]['incident_created_at_date']
            date = datetime.strptime(str(date_raw), '%d %B %Y')
            date_Now = datetime.now()
            boundary = date_Now - timedelta(days = 7)
            if(date>boundary):
                if(datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Monday"):
                    closedDayList[0] += 1
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Tuesday"):
                    closedDayList[1] += 1
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Wednesday"):
                    closedDayList[2] += 1
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Thursday"):
                    closedDayList[3] += 1
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Friday"):
                    closedDayList[4] += 1
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Saturday"):
                    closedDayList[5] += 1
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Sunday"):
                    closedDayList[6] += 1

        return closedDayList

def getCasualtiesDayList(type_incident):
# casualtiesDayList = [3,3,4,5,10,2,3]

    casualtiesDayList=[0, 0, 0, 0, 0, 0, 0]
    incident_documents_list = []
    i=0
    # In firebase's object form
    incident_documents = db.collection('incidents').where('incident_type', 'array_contains', str(type_incident)).get()

    for document in incident_documents:
        incident_documents_list.append(document.to_dict())
    #if no documents
    if(len(incident_documents_list) == 0):
        return casualtiesDayList
        # loop through all reports to add up all casualties
    else:
        for i in range(len(incident_documents_list)):
            date_raw = incident_documents_list[i]['incident_created_at_date']
            date = datetime.strptime(str(date_raw), '%d %B %Y')
            date_Now = datetime.now()
            boundary = date_Now - timedelta(days = 7)
            if(date>boundary):
                if(datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Monday"):
                    casualtiesDayList[0] += countCasualties(incident_documents_list,i)
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Tuesday"):
                    casualtiesDayList[1] += countCasualties(incident_documents_list,i)
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Wednesday"):
                    casualtiesDayList[2] += countCasualties(incident_documents_list,i)
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Thursday"):
                    casualtiesDayList[3] += countCasualties(incident_documents_list,i)
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Friday"):
                    casualtiesDayList[4] += countCasualties(incident_documents_list,i)
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Saturday"):
                    casualtiesDayList[5] += countCasualties(incident_documents_list,i)
                elif (datetime.strptime(str(date_raw), '%d %B %Y').strftime('%A') == "Sunday"):
                    casualtiesDayList[6] += countCasualties(incident_documents_list,i)


    return casualtiesDayList

def time_in_range(start, end, x):
  startObj=datetime.strptime(start, "%H:%M").time()
  endObj=datetime.strptime(end, "%H:%M").time()
  if startObj <= endObj:
      #e,g (4,5]
        return startObj < x <= endObj
  else:
        return startObj <= x or x <= endObj


def countCasualties(incident_documents_list,i):
    casualties_incident = []
    casualties_incidents = []
    casualties = 0
    
    report_documents = db.collection('incidents').document(str(incident_documents_list[i]['incident_id'])).collection('reports').get()
    # loop through all reports to add up all casualties
    # get the maximum number of casualties for each incident
    for r_document in report_documents:
        num_str = r_document.to_dict()['report_num_of_casualties']
        if(num_str != ''):
            casualties_incident.append(num_str)
    if(len(casualties_incident)!=0):
        casualties_incidents.append(max(casualties_incident))
    for j in range(len(casualties_incidents)):
        casualties += int(casualties_incidents[j])
    return casualties
