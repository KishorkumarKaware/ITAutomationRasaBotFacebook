import argparse, configparser, sys, json, os
from slackclient import SlackClient
from time import sleep

class Converser:
  topics = {}
  client = None
  debug = False
  my_user_name = ''

  def connect(self, token):
    self.client = SlackClient(token)
    self.client.rtm_connect()
    self.my_user_name = self.client.server.username
    print("Connected to Slack.")

  def listen(self):
    while True:
      try:
        input = self.client.rtm_read()
        if input:
          for action in input:
            if self.debug:
              print(action)
            if 'type' in action and action['type'] == "message":
              # Uncomment to only respond to messages addressed to us.
              # if 'text' in action
              #   and action['text'].lower().startswith(self.my_user_name):
              #print(action['text'])
              #self.process_message(action)
              channel=action['channel']
              text=action['text']
              self.post(channel, text)
        else:
          sleep(1)
      except Exception as e:
        print("Exception: ", e.message)

  def process_message(self, message):
    for topic in self.topics.keys():
      if topic.lower() in message['text'].lower():
        response = self.topics[topic].format(**message)
        if response.startswith("sys:"):
          response = os.popen(response[4:]).read()
        print("Posting to [%s]: %s" % (message['channel'], response))
        self.post(message['channel'], response)

  def post(self, channel, message):
    chan = self.client.server.channels.find(channel)

    if not chan:
      raise Exception("Channel %s not found." % channel)

    return chan.send_message(message)

if __name__ == "__main__":

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
This script posts responses to trigger phrases.
Run with:
converse.py topics.json
''',
    epilog='''''' )
  parser.add_argument('-d', action='store_true', help="Print debug output.")
  parser.add_argument('topics_file', type=str, nargs=1,
                   help='JSON of phrases/responses to read.')
  args = parser.parse_args()

  # Create a new Converser
  conv = Converser()

  if args.d:
    conv.debug = True

  # Read our token and connect with it
  config = configparser.RawConfigParser()
  config.read('creds.cfg.sample')
  token = config.get("Slack","token")

  conv.connect(token)

  # Add our topics to the converser
  with open(args.topics_file[0]) as data_file:
    conv.topics = json.load(data_file)

  # Run our conversation loop.
  conv.listen()