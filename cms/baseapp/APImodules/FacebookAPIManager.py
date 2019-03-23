"""A client for the Facebook Graph API.

    https://developers.facebook.com/docs/graph-api

    The Graph API is made up of the objects in Facebook (e.g., people,
    pages, events, photos) and the connections between them (e.g.,
    friends, photo tags, and event RSVPs). This client provides access
    to those primitive types in a generic way. For example, given an
    OAuth access token, this will fetch the profile of the active user
    and the list of the user's friends:

       graph = facebook.GraphAPI(access_token)
       user = graph.get_object("me")
       friends = graph.get_connections(user["id"], "friends")

    You can see a list of all of the objects and connections supported
    by the API at https://developers.facebook.com/docs/graph-api/reference/.

    You can obtain an access token via OAuth or by using the Facebook
    JavaScript SDK. See
    https://developers.facebook.com/docs/facebook-login for details.

    If you are using the JavaScript SDK, you can use the
    get_user_from_cookie() method below to get the OAuth access token
    for the active user from the cookie saved by the SDK.
    
    from:
    https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=2501670606528884&client_secret=99ef017bf22ed1ffec91049b43733716&fb_exchange_token=EAAjjQZAPY4XQBAGBuiYxZCtoNwv1C0V5HfQAEHMd5ZAMHbhnCM5K4Q6IXDvSSHYPxk0mRzMSTRmQ4saRZAZALGg6swC6SCEw6V8LUOTJaLYZACveWGg8NjaHuEd4QaZCf1RXhiKY1nUhZBf7FMHwBdM7g8nGgW6rmugwBQCr8qQspRCisOMSJwkL43VO8J1OZCZCw8tfJIEUZAXmQZDZD
    
    generate long term token:{"access_token":"EAAjjQZAPY4XQBAMuShU9uBq6zRORcRmZC23UlkxiRJPXPWRSMXoHaLUpePZAjfj4gAxgBle9BxaZAwvsZBvv36ELriZA5JBB8wLKdBjDO36eaEFGaMHlpRXcKzjHypJ5AMlKmDSoaZB3TqF1DZAfax0WdcaYBGPPDbEW55tEzFhKR1TpbyDGrkpg","token_type":"bearer","expires_in":5184000}
    (expires in 600 days)

    """


import facebook
 
token = {'EAAjjQZAPY4XQBAMuShU9uBq6zRORcRmZC23UlkxiRJPXPWRSMXoHaLUpePZAjfj4gAxgBle9BxaZAwvsZBvv36ELriZA5JBB8wLKdBjDO36eaEFGaMHlpRXcKzjHypJ5AMlKmDSoaZB3TqF1DZAfax0WdcaYBGPPDbEW55tEzFhKR1TpbyDGrkpg'}

graph = facebook.GraphAPI(token)

#hardcode data, this parameter expecting a string
information = "This is my testing for fb page"
image = open("../../img.jpg", 'rb')


def facebookShare(info, img):
    # put_object for posting text
    #graph.put_object(parent_object='me', connection_name='feed', message=info)
    # put_photo for posting photo with messsage(text)
    graph.put_photo(image= img, message=info)
    
#facebookShare(information, image)
    
