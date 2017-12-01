from slackclient import SlackClient

slack_token = "xoxb-274915650144-79SUtKxqc3KekyPsnjWrD0ev"
#sc = SlackClient(slack_token)
client = None
debug = False
my_user_name = ''
#Sending msg to a channel
#sc.api_call(
#  "chat.postMessage",
#  channel="#general",
#  text="Hello from Python! :tada:"
#)

#Know all channels
#print(sc.api_call("channels.list"))
class Converser:
    
    def connect(self, token):
        self.client = SlackClient(token)
        self.client.rtm_connect()
        self.my_user_name = self.client.server.username
        print("Connected to Slack.")

conv=Converser()
conv.connect(token=slack_token)        
