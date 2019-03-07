
"""
function: send_sms(sms_body, to_phone_no)

parameter:
sms_body: string
to_phone_no: string , in format of E.164 formatting [+][country code][phone number including area code] e.g."+6591330112"
    
important:
now can only send to "+6591330112", since i only verified this number in twilio website

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


def send_sms(sms_body, to_phone_no):
	# Your Account Sid and Auth Token from twilio.com/console
	account_sid = 'AC289e9926f0696f7a5165552cba03e4eb'
	auth_token = '08817625897935ca6b9ce1bdb9ce957c'
	client = Client(account_sid, auth_token)


	message = client.messages \
	                .create(
	                     body=sms_body,
	                     from_='+19705146650',
	                     to=to_phone_no
	                 )

	print(message.sid)

#test case
#send_sms("cms3003 sending sms test", "+6590361726")