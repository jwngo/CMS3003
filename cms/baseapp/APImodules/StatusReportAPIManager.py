from .FirebaseAPIManager import getIncidentFromFirebase, getReportsFromFirebase
from pprint import pprint
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


import .FirebaseAPIManager as Fb
from pprint import pprint

import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet

import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as mp
from itertools import cycle, islice

# Initializing current datetime
now = datetime.datetime.now()
currentDateTime = now.strftime("%Y-%m-%d %H:%M")

# Initializing document
doc = SimpleDocTemplate("Status Report " + currentDateTime+".pdf", pagesize=letter)

# Initializing elements to be added into empty pdf file
elements = []

# Initializing styleSheet for document design 
styleSheet = getSampleStyleSheet()


def getDataFromFirebase():
    db = firestore.client()

    # Retrieving the current date, time for comparison to retrieve data
    incident_date = now.strftime("%d %B %Y")

    # Getting all the Incidents in this order: 
    # 1) Cat1 + Reported 2) Cat2 + Reported 3) Cat1 + Closed 4) Cat2 + Reported
    incident_data = db.collection('incidents')
    cat1_incidents_data = incident_data.where(
        u'incident_date', u'==', incident_date).where(
            u'incident_level', u'==', u'CAT1')
    cat2_incidents_data = incident_data.where(
        u'incident_date', u'==', incident_date).where(
            u'incident_level', u'==', u'CAT2')
    cat1_reported_data = cat1_incidents_data.where(
        u'incident_status', u'==', u'Reported').get()
    cat1_closed_data = cat1_incidents_data.where(
        u'incident_status', u'==', u'Closed').get()
    cat2_reported_data = cat2_incidents_data.where(
        u'incident_status', u'==', u'Reported').get()
    cat2_closed_data = cat2_incidents_data.where(
        u'incident_status', u'==', u'Closed').get()
    all_incidents_data = {}
    all_incidents_data.update(cat1_reported_data)
    all_incidents_data.update(cat2_reported_data)
    all_incidents_data.update(cat1_closed_data)
    all_incidents_data.update(cat2_closed_data)

    all_incidents_data_dict = { el.id: el.to_dict() for el in all_incidents_data }
    
    # Getting all the IncidentIDs
    list_of_incident_ids = []
    for keys in all_incidents_data_dict:
        list_of_incident_ids.append(keys)
    # Getting number of Incidents
    number_of_incident_ids = len(list_of_incident_ids)

    i=0;

    # Creation of data ['location', 'crisistype', 'crisislevel', 'status', 'noofcasualties', 'typeandsize']
    list_of_data = []
    while i < number_of_incident_ids:
        current_incident_id = list_of_incident_ids[i]
        list_for_incident_details = []
        # Appending incident location into list_of_data
        list_for_incident_details.append(all_incidents_data_dict[current_incident_id]['incident_address'])
        # Retrieving all the different incident types
        incident_type_list = all_incidents_data_dict[current_incident_id]['incident_type']
        string_for_incident_type = ""
        for x in incident_type_list:
            string_for_incident_type = string_for_incident_type + x + " "
        # Appending incident type(s) into list_of_data
        list_for_incident_details.append(string_for_incident_type)
        # Appending incident level into list_of_data
        list_for_incident_details.append(all_incidents_data_dict[current_incident_id]['incident_level'])
        # Appending incident status into list_of_data
        list_for_incident_details.append(all_incidents_data_dict[current_incident_id]['incident_status'])

        # Retrieving all the reports
        reports = db.collection('incidents').document(str(current_incident_id)).collection('reports').get()
        reports_dict = { el.id: el.to_dict() for el in reports }
        reports_id = []
        for keys in reports_dict:
            reports_id.append(keys)

        #Appending number of casualties into list_of_data
        list_for_incident_details.append(reports_dict[reports_id[i]]['report_num_of_casualties'])

        # Retrieving all the individual help needed
        number_of_ambulance = reports_dict[reports_id[i]]['report_num_ambulance']
        number_of_firetruck = reports_dict[reports_id[i]]['report_num_firetruck']
        number_of_gasleak = reports_dict[reports_id[i]]['report_num_gasleak']
        number_of_police = reports_dict[reports_id[i]]['report_num_police']

        # Creating string to list down the specific help needed
        type_and_size = ""
        if (number_of_ambulance != 0):
            type_and_size = type_and_size + "Ambulance : %d" %number_of_ambulance 
        if (number_of_firetruck != 0):
            type_and_size = type_and_size + "Firetruck : %d" %number_of_firetruck
        if (number_of_gasleak != 0):
            type_and_size = type_and_size + "Gas Leak : %d" %number_of_gasleak
        if (number_of_police != 0):
            type_and_size = type_and_size + "Police : %d" %number_of_police
        # When no help is needed, return this string instead
        if (type_and_size == ''):
            type_and_size = "No Deployments Required"
    
        # Appending help needed into list_of_data
        list_for_incident_details.append(type_and_size)
        list_of_data.append(list_for_incident_details)
        i = i + 1

    # If there are no incidents reported, NIL will be reflected on the Status Report.
    if (list_of_data == []):
        list_of_data = [['NIL', 'NIL','NIL','NIL','NIL','NIL']]

    return list_of_data


#Creating Table that lists down all the different details regarding the Incidents
#Returns table
def createTable(item_data):
    location = Paragraph('''<para align=center><b>Location</b></para>''', styleSheet["h3"])
    type_of_crisis = Paragraph('''<para align=center><b>Type of Crisis</b></para>''', styleSheet["h3"])
    crisis_level = Paragraph('''<para align=center><b>Crisis Level</b></para>''', styleSheet["h3"])
    status = Paragraph('''<para align=centre><b>Status </b></para>''', styleSheet["h3"])
    number_of_casualties = Paragraph('''<para align=center><b>Number of Casualties</b></para>''', styleSheet["h3"])
    type_and_size = Paragraph('''<para align=center><b>Type and Size of Forces Deployed</b></para>''', styleSheet["h3"])
    data = [[location, type_of_crisis, crisis_level, status, number_of_casualties, type_and_size]]
    for i in range (len(item_data)):
        data.append(item_data[i])
    table=Table(data,style=[('BOX',(0,0),(-1,-1),2,colors.black),
                        ('GRID',(0,0),(-1,-1),1,colors.black)])
    table._argW[4]=1.5*inch
    return table 

#Creating graph of Number of Casualities against Number of Incidents and Day
#Returns graph
def drawDayGraph(handlingDayList,resolvedDayList,casualtiesDayList,incidenttype):
    width = .35 # width of a bar

    m1_t = pd.DataFrame({
    'Handling' : handlingDayList,
    'Resolved' : resolvedDayList,
    'No. of casualties' : casualtiesDayList})

    my_colors = list(islice(cycle(['r', 'g']), None, 2))
    m1_t[['Handling','Resolved']].plot(kind='bar', width = width, color = my_colors )
    ax1 = plt.gca()
    ax1.set(xlabel="Day",ylabel='No. of Incidents')
    m1_t['No. of casualties'].plot(secondary_y=True)
    ax = plt.gca()
    plt.gca().get_lines()[0].set_color("brown")
    plt.legend(loc = 'upper center')
    plt.xlim([-width, len(m1_t['Handling'])-width])
    plt.title(incidenttype.format(0))
    ax.set_xticklabels(('Mon', 'Tues', 'Wed', 'Thur', 'Fri','Sat','Sun'))
    ax.set(ylabel='No. of casualties')


    return plt.gcf()   

#Creating graph of Number of Casualities against Number of Incidents and Hours in 5-hours interval
#Returns graph
def drawSixHourGraph(handlingHourList,resolvedHourList,casualtiesHourList,incidenttype):
    width = .35 # width of a bar

    m1_t = pd.DataFrame({
    'Handling' : handlingHourList,
    'Resolved' : resolvedHourList,
    'No. of casualties' : casualtiesHourList})

    my_colors = list(islice(cycle(['r', 'g']), None, 2))
    m1_t[['Handling','Resolved']].plot(kind='bar', width = width, color = my_colors )
    ax1 = plt.gca()
    ax1.set(xlabel="Time",ylabel='No. of Incidents')
    m1_t['No. of casualties'].plot(secondary_y=True)
    ax = plt.gca()
    plt.gca().get_lines()[0].set_color("brown")
    plt.legend(loc = 'upper center')
    plt.xlim([-width, len(m1_t['Handling'])-width])
    plt.title(incidenttype.format(0))
    ax.set_xticklabels(('00:00', '05:00', '10:00', '15:00', '20:00'))
    ax.set(ylabel='No. of casualties')
    
    
    return plt.gcf()


#Creating the style and combining the different elements together
def createPDF():
    cms_name = Paragraph('''Crisis Management System''', styleSheet["Title"])
    current_datetime = now.strftime("<para align=centre>%Y-%m-%d %H:%M</para>")
    print_datetime = Paragraph(current_datetime, styleSheet["h3"])
    title = Paragraph('''<b>Status Report</b>''', styleSheet["Title"])
    item_data = getDataFromFirebase()
    table = createTable(item_data)
    trends = Paragraph('''<para align=centre><b>The next two pages display graphs that summarises key indicators and trends.</b></para>''', styleSheet["h4"])
    six_hours_graph = Paragraph('''<para align=centre><b>Six Hours Graph</b></para>''', styleSheet["h1"])
    daily_graph = Paragraph('''<para align=centre><b>Daily Graph</b></para>''', styleSheet["h1"])
    elements.append(cms_name)
    elements.append(print_datetime)
    elements.append(title)
    elements.append(table)
    elements.append(trends)
    IncidentTypes = ["Haze","Fire","Terrorist"]
    for IncidentType in IncidentTypes:
        drawing_six_hours = Image('plot1' + IncidentType + ".png")
        drawing_daily = Image('plot2' + IncidentType + ".png")
        drawing_six_hours_table = [[drawing_six_hours]]
        drawing_daily_table = [[drawing_daily]]
        t1=Table(drawing_six_hours_table)
        t2=Table(drawing_daily_table)
        elements.append(t1)
        elements.append(six_hours_graph)
        elements.append(t2)
        elements.append(daily_graph)
    
    return elements


#Sending out Email to PMO
def sendEmail():
    fromaddr = "cms3003report@gmail.com"
    toaddr = "cms3003report@gmail.com" #To Prime Minister Office email address
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
    # storing the senders email address   
    msg['From'] = fromaddr 
    # storing the receivers email address  
    msg['To'] = toaddr 
    # storing the subject  
    msg['Subject'] = "Status Report"
    # string to store the body of the mail, add in datetime
    body = "Dear Prime Minister, this is the status report for " + currentDateTime
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
    # open the file to be sent
    filename = "Status Report " + currentDateTime + ".pdf"
    attachment = open(filename, "rb")  
    #instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 
    # To change the payload into encoded form 
    p.set_payload((attachment).read())  
    # encode into base64 
    encoders.encode_base64(p)   
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)   
    # attach the instance 'p' to instance 'msg' 
    msg.attach(p)   
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    # start TLS for security 
    s.starttls() 
    # Authentication 
    s.login(fromaddr, "Abcd1234!") 
    # Converts the Multipart msg into a string
    text = msg.as_string() 
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
    # terminating the session 
    s.quit() 


def sendEmailToPMO():
    IncidentTypes = ["Haze","Fire","Terrorist"]
    for IncidentType in IncidentTypes:
        plot1 = drawSixHourGraph(Fb.handlingHourList(IncidentType),Fb.resolvedHourList(IncidentType),Fb.casualtiesHourList(IncidentType),IncidentType)
        mp.savefig('plot1' + IncidentType + '.png')
        plot2 = drawDayGraph(Fb.handlingHourList(IncidentType),Fb.resolvedHourList(IncidentType),Fb.casualtiesHourList(IncidentType),IncidentType)
        mp.savefig('plot2' + IncidentType + '.png')
    
    elements = createPDF()
    #building of doc
    doc.build(elements)
    sendEmail()
