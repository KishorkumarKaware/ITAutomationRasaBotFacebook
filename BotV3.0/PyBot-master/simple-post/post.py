#!/usr/bin/env python

import argparse, configparser, sys
from slackclient import SlackClient

def post(client, channel, message):
    channel = channel.lstrip("#")
    chan = client.server.channels.find(channel)
    print(chan)
    if not chan:
        raise Exception("Channel %s not found." % channel)

    my_user_name = client.server.username
    print(my_user_name)
    my_user = None
  
    for User in client.server.users:
        print("userIds below...",client.server.users[User].id)
        print("ChannelIDs below...",client.server.channels[User].id)
        if client.server.users[User].name == my_user_name:
            my_user = client.server.users[User]
            break
    if not my_user:
        raise Exception("User %s missing" % my_user_name)

    if my_user.id not in chan.members:
        raise Exception("%s not in channel %s, please /invite them." % (my_user_name, channel))
    return chan.send_message(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''
        This script posts a message into a slack channel.
        Sample commands:
        post.py mychannel "This is a message."
        ''',epilog='''''' )
    parser.add_argument('channel', type=str, nargs=1,
                        help='Channel to post to')
    parser.add_argument('message', type=str, nargs=1,
                   help='Message to post')
    args = parser.parse_args()
    print(args)

    config = configparser.RawConfigParser()
    config.read('creds.cfg.sample')
  
    token = config.get("Slack","token")

    client = SlackClient(token)
    print(client.rtm_connect())
    

    try:
        post(client, args.channel[0], args.message[0])
    except Exception as e:
        sys.exit("Error: %s" % e.message)

