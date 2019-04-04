from FacebookAPIManager import facebookShare
from TelegramAPIManager import telegram_post
#from TwitterAPIManager import twitterShare
from FirebaseAPIManager import getIncidentFromFirebase
from PIL import Image
import requests
from io import BytesIO
from datetime import datetime
import time

################## hard code data ####################
# List of CAT2 incident that is posted
cat2_posted = []

# time interval between CAT2 posts(senconds): 6hours
interval = 21600
hrs_24 = 86400
# civil defense shelter web page url
url_cd = 'https://www.scdf.gov.sg/home/civil-defence-shelter'
url_cdMap = 'https://www.onemap.sg/main/v2/'

#image includes information list of hospitals and polyclinics
url = 'https://firebasestorage.googleapis.com/v0/b/cz2006project.appspot.com/o/hospitalInfo.jpeg?alt=media&token=be53232a-7e7e-450e-a1da-6f035d837750'
response = requests.get(url)
image = Image.open(BytesIO(response.content))
buf = BytesIO()
image.save(buf, 'jpeg')
buf.seek(0)
image = buf.read()
buf.close()

shelter_info = 'See details of civil defense shelters at: '+url_cd +'\n'
hospital_info = 'List of Hospitals and polyclinlcs: see the image below\n'

################## functions ####################
#send shelter info every 24 hours
def send_info_24hrs():
    message = 'Crisis Management System: Useful information and safety tips.\n1.Install smoke alarms on every level of your home, inside bedrooms and outside sleeping areas.\n2.In haze, stay in doors, put on protection when going out and requently wash your hands and face after outdoor activities.\n3.During event of terrorism, stay calm, follow the advice of local emergency officials and check for news and instructions.'+ shelter_info + hospital_info
    while true:
        facebookShare(message, image)
        telegram_post(message, url)
        time.sleep(hrs_24)


#call notify() when sending the incident to firebase
def notify(incident):
    incident_id = int(incident['incident_id'])

    message = get_message(incident) + shelter_info + hospital_info
    incident_level = incident['incident_level']

    #For CAT1 incident, send immediately
    if incident_level == 'CAT1':
        facebookShare(message, image)
        telegram_post(message, url)
    #For CAT2, update when >= 6 hours from last CAT2 post
    elif incident_level == 'CAT2':

        check_update(incident_id)
    

def check_update(incident_id):
    #if this is not the first CAT1 incident
    if cat2_posted:
        last_post_id = cat2_posted[-1]
        last_post_incident =getIncidentFromFirebase(last_post_id)
        last_post_dateTime = last_post_incident['incident_created_at_date']+last_post_incident['incident_created_at_time']
        datetimeFormat = '%d %B %Y%H:%M'
        current = datetime.now()
        diff = current - datetime.strptime(last_post_dateTime, datetimeFormat)
        message = ''
        if diff.seconds >= interval:
            for cid in range(last_post_id+1, incident_id+1):
                incident = getIncidentFromFirebase(cid)
                if incident['incident_level'] == 'CAT2':
                    message += get_message(incident)
                    cat2_posted.append(cid)
            message = message + shelter_info + hospital_info
            facebookShare(message, image)
            telegram_post(message, url)
    #if this is first CAT2 incident
    else:
        incident = getIncidentFromFirebase(incident_id)
        message = get_message(incident)+ shelter_info + hospital_info
        cat2_posted.append(incident_id)
        facebookShare(message, image)
        telegram_post(message, url)
        
    
def get_message(incident):
    types_of_incident = incident['incident_type']
    incident_level = incident['incident_level']
    incident_region = incident['incident_region']
    incident_address = incident['incident_address']
    incident_status = incident['incident_status']
    # different messages for reported and handling, default return empty string(closed). However, when incident is closed, NotificationManager shouldn't be called !
    if incident_status == 'Reported':
        message = 'Incident Alert! There is a [possible] '
    elif incident_status == 'Handling':
        message = 'We are currently handling a '
    else:
        return ''
    alert_message = message + incident_level +' incident in ' + incident_region + ', '+ incident_address +', types of incident:' + types_of_incident + '.\n'
    return alert_message

    