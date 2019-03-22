
'''https://web.telegram.org/#/im?p=s1409214510_613501089696389297
1409214510
procedure to schive this:
1. create a bot
2. get its token and ksys
3. enter https://api.telegram.org/bot798092482:AAEYOmSAs1rL1ejwfWF5ZbkRaTWeQY11jzw
   as the base url
5. set this bot as administrator of the channel, private channel_id: -100xxxxxxxxx->in the link of your channel
4. https://api.telegram.org/bot798092482:AAEYOmSAs1rL1ejwfWF5ZbkRaTWeQY11jzw/sendMessage?text="text_you_want_to_send"&chat_id=-100xxxxxxxxx


TIPS:
1. remember to add bot as administrator
2. bot api documentation: the methods start with lower letter, 
   when use, the format is like: /method_name?attribute_name=value


'''
'''
telegram_post(string: text, string: gphoto_url, string: chat, default)
'''
'''
#test case
#telegram_post("text_you_want_to_send", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScZ5R7saUPRGc6m7QnAhF0r40MTYMtoELXDyKNuzMSTqydsblb")
'''


import requests

def telegram_post(text, photo_url, chat = "-1001475571282"):
  #this url contained the bot token already
  url_base = "https://api.telegram.org/bot798092482:AAEYOmSAs1rL1ejwfWF5ZbkRaTWeQY11jzw"


  photo_url = url_base + "/sendPhoto?" + "photo=" + photo_url +"&chat_id=" +chat +"&caption="+text

  requests.post(photo_url)

#telegram_post("text_you_want_to_send", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScZ5R7saUPRGc6m7QnAhF0r40MTYMtoELXDyKNuzMSTqydsblb")

