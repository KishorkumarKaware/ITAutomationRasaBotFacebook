from rasa_core.channels import HttpInputChannel
from rasa_core.channels.slack1  import CustomInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter

import argparse, configparser, sys, json, os
from slackclient import SlackClient
from time import sleep


# load your trained agent
agent = Agent.load("models/dialogue", interpreter=RasaNLUInterpreter(model_directory="C:/Users/Administrator/Desktop/BotV3.0/models/nlu/current",config_file="nlu_model_config.json"))


input_channel = CustomInput("http://a17a3259.ngrok.io/app","xoxb-276102566067-nb5vPsJD6WlWFzm7rAmU6cHW")

agent.handle_channel(HttpInputChannel(8080, "", input_channel))