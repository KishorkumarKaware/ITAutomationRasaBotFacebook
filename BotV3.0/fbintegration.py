from rasa_core.channels import HttpInputChannel
from rasa_core.channels.facebook import FacebookInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter

# load your trained agent
agent = Agent.load("models/dialogue", interpreter=RasaNLUInterpreter(model_directory="C:/Users/Administrator/Desktop/BotV3.0/models/nlu/current",config_file="nlu_model_config.json"))

YOUR_FB_VERIFY="rasa-bot"
YOUR_FB_SECRET="a9f5370c907e14a983051bd4d266c47b"
YOUR_FB_PAGE_ID="158943344706542"
YOUR_FB_PAGE_TOKEN="EAACZAVkjEPR8BANiwfuKaSVz8yxtLsytuOPvaUzUTlCMAmvuX9TdqGR5P4F1EepBfZCQoKhSR49zM5C9pYX9hmmv3qqiUnRCMDE0eJ1lWRjeqNYTLLA5nbXelSMw0p7neZBSyyIcNHS3e1lbbf2raWPY8IUosJZBMlDLLA7ZBJgTxZAZCvhbO84"

input_channel = FacebookInput(
   fb_verify=YOUR_FB_VERIFY,  # you need tell facebook this token, to confirm your URL
   fb_secret=YOUR_FB_SECRET,  # your app secret
   fb_tokens={YOUR_FB_PAGE_ID: YOUR_FB_PAGE_TOKEN},   # page ids + tokens you subscribed to
   debug_mode=True    # enable debug mode for underlying fb library
)

agent.handle_channel(HttpInputChannel(8080, "", input_channel))