from .FacebookAPIManager import facebookShare
from .TelegramAPIManager import telegram_post
#From .TwitterAPIManager import twitterShare
from .FirebaseAPIManager import getIncidentFromFirebase
from PIL import Image
import requests
from io import BytesIO
import datetime

################## hard code data ####################
# List of CAT2 incident that is posted
cat2_posted = []
# time interval between CAT2 posts(senconds): 6hours
interval1=21600
# civil defense shelter web page url
url_cd = 'https://www.scdf.gov.sg/home/civil-defence-shelter'
#image includes information list of hospitals and polyclinics
url = 'https://firebasestorage.googleapis.com/v0/b/cz2006project.appspot.com/o/hospitalInfo.jpeg?alt=media&token=be53232a-7e7e-450e-a1da-6f035d837750'
response = requests.get(url)
image = Image.open(BytesIO(response.content))

################## functions ####################
#call notify() when sending the incident to firebase
def notify(incident):
    incident_id = int(incident['incident_id'])
    message = get_message(incident)
    incident_level=incident['incident_level']
    
    #For CAT1 incident, send immediately
    if(incident_level == 'CAT1'):
        facebookShare(message, image)
        telegram_post(message, url)
    #For CAT2, update when >= 6 hours from last CAT2 post
    elif(incident_level == 'CAT2'):
        check_update(incident_id)
    

def check_update(incident_id):
    if cat2_posted:
        last_post_id = cat2_posted[-1]
        last_post_incident = getIncidentFromFirebase(last_post_id)
        last_post_dateTime = last_post_incident['incident_created_at_date']+last_post_incident['incident_created_at_time']
        datetimeFormat = '%d %B %Y%H:%M'
        current = datetime.now()
        diff = current - datetime.strptime(last_post_dateTime, dateFormat)
        message = ''
        if(diff.senconds >= interval):
            for cid in range(last_posted, incident_id):
                incident = getIncidentFromFirebase(cid)
                message += get_message(incident)
                cat2_posted.append(cid)
            facebookShare(message, image)
            telegram_post(message, url)
        
    
def get_message(incident):
    types_of_incident = ', '.join(incident['incident_type'])
    incident_level = incident['incident_level']
    incident_region = incident['incident_region']
    incident_address = incident['incident_address']
    
    alert_message = 'Incident Alert! There is a ' + incident_level +' incident in ' + incident_region + ', '+ incident_address +', types of incident:' + types_of_incident + '.'
    shelter_info = 'See civil defense shelter info at: '+url_cd
    hospital_info = 'List of Hospitals and polyclinlcs: see the image below'
    message = alert_message + '\n' + shelter_info + '\n' + hospital_info+'\n'
    
    return message
    

def test():
    notify(getIncidentFromFirebase(1))
