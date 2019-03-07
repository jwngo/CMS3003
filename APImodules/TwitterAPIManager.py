'''

function: twitterShare(status_text)


parameter:
status_text: string
   

---------------------------------------------------------------------------------------------------------------------
 API.update_status(status[, in_reply_to_status_id][, lat][, long][, source][, place_id])

    Update the authenticated user’s status. Statuses that are duplicates or too long will be silently ignored.
    Parameters:	

        status – The text of your status update.
        in_reply_to_status_id – The ID of an existing status that the update is in reply to.
        lat – The location’s latitude that this tweet refers to.
        long – The location’s longitude that this tweet refers to.
        source – Source of the update. Only supported by Identi.ca. Twitter ignores this parameter.
        place_id – Twitter ID of location which is listed in the Tweet if geolocation is enabled for the user.

    Return type:	

    Status object

'''


import tweepy
 
def twitterShare(status_text):

	# Consumer keys and access tokens, used for OAuth
	consumer_key = '7EyzTcAkINVS3T2pb165'
	consumer_secret = 'a44R7WvbMW7L8I656Y4l'
	access_token = 'z00Xy9AkHwp8vSTJ04L0'
	access_token_secret = 'A1cK98w2NXXaCWMqMW6p'
	 
	# OAuth process, using the keys and tokens
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	 
	# Creation of the actual interface, using authentication
	api = tweepy.API(auth)
	 
	# Sample method, used to update a status
	api.update_status(status_text)



#test case
twitterShare("today is rainy")