import facebook

token = {'EAAjjQZAPY4XQBAILMGndeFa93Hfxk31EZAaYzaJt07Rhr6H9BpnWDZAChEYnYtWhDxZBZCRdDJm7TspHJMUbEusTlfuuLd61ZBZBWeZBWz3WhAzZBnzGfZAKpsZAXmTr0ycSAAF3cHd3N4r5da99jKeI2xLZAZAZCjs03HJhcHKaKUZBDkzQL6i9FAoVH18HLVoyHOoW2jT7f1EUJ63ngZDZD'}
graph = facebook.GraphAPI(token)

#hardcode, this parameter expecting a string
info = "I love anime!" 

def facebookShare(info):
    graph.put_object(parent_object='me', connection_name='feed', message=info)

    
facebookShare(info)
    

