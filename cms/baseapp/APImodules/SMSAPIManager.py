"""
function: send_sms(sms_body, to_phone_no)



parameter:
sms_body: string
to_phone_no: string , in format of E.164 formatting [+][country code][phone number including area code] e.g."+6591330112"
    


important:
now can only send to "+6591330112", since i only verified this number in twilio website
error:
Trial accounts cannot send messages to unverified numbers; verify  at twilio.com/user/account/phone-numbers/verified, or purchase a Twilio number to send messages to unverified numbers.


account_sid
auth_token
from phone number
are provided by the account: cby0929@gmail.com registered in twilio
-----------------------------------------------------------------------------------------
Requirments:
    twilio installed
"""


# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from pprint import pprint


def sendSMS(to_phone_number, message):
	# Your Account Sid and Auth Token from twilio.com/console
	account_sid = 'AC0fa4615e2b0b368896bc92db9ff12c30'
	auth_token = 'f9fcc33e564a5d31a6ecae07d62e8013'
	client = Client(account_sid, auth_token)

	message = client.messages \
	                .create(
	                     body = message,
	                     from_ = '+12023355301',
	                     to= to_phone_number
	                 )

	print(message.sid)

def sendSMSToSubscribers(subscribers, incident):
	"""
	Dear {subscriber_name},
	there is {types_of_incident} at
	{incident_address}.
	"""
	# Extract necessary incident details
	types_of_incident = ', '.join(incident['incident_type'])
	incident_address = incident['incident_address']

	# Craft the message and send it out
	for count, subscriber in subscribers.items():
		# { count : { data: value } }

		# Craft the message
		subscriber_name = subscriber['subscriber_name']
		message = 'Dear, {}\nthere is {} \nat {}.'.format(
			subscriber_name, types_of_incident, incident_address)
		
		# Send it out
		subscriber_number = '+65' + subscriber['subscriber_number']
		sendSMS(subscriber_number, message)

