
'''https://web.telegram.org/#/im?p=s1409214510_613501089696389297
1409214510
{
  "ok": true,
  "result": {
    "message_id": 2,
    "chat": {
      "id": -1001363941800,
      "title": "TestChannel",
      "username": "usefulmix_channel",
      "type": "channel"
    },
    "date": 1538926255,
    "text": "Test message"
  }
}
'''



#pip3 install telethon
from telethon import TelegramClient, events, sync

def telegram_post():
	# These example values won't work. You must get your own api_id and
	# api_hash from https://my.telegram.org, under API Development.
	api_id = -1001409214510
	api_hash = '5c7a824ef6a40a24fe978a46d7ca3a9c'

	client = TelegramClient('session_name', api_id, api_hash)
	client.start()

	print(client.get_me().stringify())

	client.send_message('username', 'Hello! Talking to you from Telethon')
	# client.send_file('username', 'http://www.bigredchilli.com/wp-content/uploads/2016/08/Singapore_36x24_colour1_on_blue_etsy1.jpg')

	client.download_profile_photo('me')
	# messages = client.get_messages('username')
	# messages[0].download_media()

	@client.on(events.NewMessage(pattern='(?i)hi|hello'))
	async def handler(event):
	    await event.respond('Hey!')

telegram_post()