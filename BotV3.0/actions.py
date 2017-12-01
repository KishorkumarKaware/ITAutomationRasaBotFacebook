from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

#from status import callae

import string
import random
import ast
import requests
import json

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



def authenticate():
    post_data = {'username':'FusionAdmin', 'password':'Fusion@123'}
    # POST some form-encoded data:
    post_response = requests.post(url="http://10.41.4.56:8080/aeengine/rest/authenticate", data=post_data)
    token = json.loads(post_response.text)
    token=token['sessionToken']
    return token

def callae(payload):
    token=authenticate()
    headers = {'content-type': 'application/json','X-session-token':token}
    post_response = requests.post(url="http://10.41.4.56:8080/aeengine/rest/execute", data=json.dumps(payload),headers=headers)
    return post_response.text



def para(wfname,slot):
    d={
    "name": "ayz",
    "value":"fx" ,
    "type": "String",
    "order": 1,
    "secret": False,
    "optional": False,
    "defaultValue": None,
    "displayName": "Incident Number",
        
    "extension": None,
    "ServiceRequest": "Add Members to DL",
    
    "poolCredential": False
  }
    e=""   
    for j in range(len(slot)):
        d["name"]=slot[j][0]
        d["value"]=slot[j][1]
        e+=str(",")+str(d)
    e=ast.literal_eval(e[1:])

    payload = {
        "orgCode": "FUSION",
        "workflowName": wfname,
        "userId": "Admin Fusion",
        "sourceId": id_generator(),
        "source": "AutomationEdge HelpDesk",
        "responseMailSubject": "None",
        "params": [{
            "name": "slackChannel",
            "value": "D6MRM1MML",
            "type": "String",
            "order": 2,
            "secret": False,
            "optional": False,
            "defaultValue": None,
            "displayName": "Slack Channel",
            "extension": None,
            "poolCredential": False
            },{
            "name": "slackUser",
            "value": "D7Q7UK2VA",
            "type": "String",
            "order": 2,
            "secret": False,
            "optional": False,
            "defaultValue": None,
            "displayName": "Slack Channel",
            "extension": None,
            "poolCredential": False
            },{
            "name": "clientEmail",
            "value": "saurabh.kulkarni@vyomlabs.com",
            "type": "String",
            "order": 2,
            "secret": False,
            "optional": False,
            "defaultValue": None,
            "displayName": "Client Email",
            "extension": None,
            "poolCredential": False
        }]}
    
    if str(type(e))=="<class 'tuple'>":
        for i in e:
            payload['params'].append(i)
    else:
        payload['params'].append(e)
    return payload




def parasr(srname,slot):
    d={
    "name": "ayz",
    "value":"fx" ,
    "type": "String",
    "order": 1,
    "secret": False,
    "optional": False,
    "defaultValue": None,
    "displayName": "Incident Number",
    "extension": None,
    "poolCredential": False
  }
    e=""   
    for j in range(len(slot)):
        d["question"]=slot[j][0]
        d["answer"]=slot[j][1]
        e+=str(",")+str(d)
    e=ast.literal_eval(e[1:])

    jsonInput={
        "ServiceRequest": srname,
        "params": [{
            "name": "slackChannel",
            "value": "D6MRM1MML"
        }, {
            "name": "slackUser",
            "value": "C6J9JE9GB"
        }]
    }
    
    if str(type(e))=="<class 'tuple'>":
        for i in e:
            jsonInput['params'].append(i)
    else:
        jsonInput['params'].append(e)
    
    
    payload={
	"orgCode": "FUSION",
	"workflowName": "Create Service Request In Remedyforce",
	"userId": "Admin Fusion",
	"sourceId":id_generator(),
	"source": "AutomationEdge HelpDesk",
	"responseMailSubject": "None",
	"params": [{
		"name": "jsonInput",
		"value": json.dumps(jsonInput),
		"type": "String",
		"order": 1,
		"secret": False,
		"optional": False,
		"defaultValue": None,
		"displayName": "Input data in JSON format",
		"extension": None,
		"poolCredential": False
	}, {
		"name": "clientEmail",
		"value": "saurabh.kulkarni@vyomlabs.com",
		"type": "String",
		"order": 2,
		"secret": False,
		"optional": False,
		"defaultValue": None,
		"displayName": "Client Email",
		"extension": None,
		"poolCredential": False
	}]
}
    
    return payload

class ActionIncidentStatus(Action):
    def name(self):
        return 'action_incident_status'

    def run(self, dispatcher, tracker, domain):
        wfname="Get Remedyforce Incident Status"
        incidentNumber = tracker.get_slot("incidentNumber")
        slot=[["incidentNumber",incidentNumber]]
        payload=para(wfname,slot)
        callae(payload)
        dispatcher.utter_message("Yeah sure..!! Please wait while I work on your request for status...")
        return []

class ActionCreateIncident(Action):
    def name(self):
        return 'action_incident'

    def run(self, dispatcher, tracker, domain):
        wfname="Create Incident In Remedyforce"
        description = tracker.get_slot("description")
        slot=[["description",description]]
        payload=para(wfname,slot)   
        callae(payload)
        cslots=tracker.latest_message.parse_data
        srname=cslots['intent']['name']
        entities=cslots['entities']
        dispatcher.utter_message("sorry to hear that.!! Please wait while I work on your request to create incident....")
        return []

    
class ActionCreateServiceRequest(Action):
    def name(self):
        return 'action_CreateServiceRequest'
    def run(self, dispatcher, tracker, domain):
        cslots=tracker.latest_message.parse_data
        srname=cslots['intent']['name']
        entities=cslots['entities']
        slot=[[]]
        for i in entities:
            slot[0].append(i['entity'])
            slot[0].append(i['value'])
        payload=parasr(srname,slot)
        callae(payload)
        dispatcher.utter_message("Thanks..!! I will send you link for your software shortly....")
        return []
    