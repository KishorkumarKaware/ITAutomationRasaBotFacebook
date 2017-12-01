from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.channels import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.channels.facebook import FacebookInput
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

logger = logging.getLogger(__name__)


def run_concertbot_online(interpreter,
                          domain_file="domain.yml",
                          training_data_file='data/stories.md'):
    
    
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
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(), KerasPolicy()],
                  interpreter=interpreter)
    #agent.handle_channel()
    agent.train_online(training_data_file,
                       input_channel=HttpInputChannel(8080, "", input_channel),
                       max_history=2,
                       batch_size=50,
                       epochs=200,
                       max_training_samples=300)
   

    return agent


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    run_concertbot_online(RasaNLUInterpreter(model_directory="C:/Users/Administrator/Desktop/BotV2.0/models/nlu/current",config_file="nlu_model_config.json"))
