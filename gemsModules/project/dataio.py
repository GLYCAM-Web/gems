#!/usr/bin/env python3
import  os, sys
import json
import uuid
from datetime import datetime
from gemsModules.common.transaction import *
from gemsModules.project import settings as projectSettings
from pydantic import BaseModel, Field
from pydantic.schema import schema

"""
The backend project is not the same as the project model in the frontend.
"""
class GemsProject(BaseModel):
    timestamp : datetime = None
    ## The name of the output dir is the pUUID
    pUUID : str = None
    ## The output path
    output_dir : str = None
    md5sum : str = None
    project_type : str = None
    requesting_agent : str = None

    def buildProject(self, thisTransaction : Transaction, requestingAgent : str):
        #print("buildProject was called.")
       #print("requestingAgent: " + requestingAgent)
        self.requesting_agent = requestingAgent
        self.timestamp = datetime.now()
        request = thisTransaction.request_dict
        #print("request: " + str(request))
        keys = request.keys()
        #print("keys: " + str(keys))
        if self.requesting_agent == 'command_line':
            ##There will be no frontend project here.
            if request['entity']['type'] == 'Sequence':
                self.project_type = "cb"
            if request['entity']['type'] == 'MmService':
                self.project_type = "md"
            pass

        else:
            projectKeys = request['project'].keys()
            ##This is meant to be different from the frontend project timestamp.
            if 'md5sum' in projectKeys:
                self.md5sum = request['project']['md5sum']
            if 'type' in projectKeys:
                self.project_type = request['project']['type']

        self.pUUID = str(uuid.uuid4())
        #print("pUUID: " + str(self.pUUID))

        self.output_dir = projectSettings.output_data_dir + "tools/" + self.project_type + "/git-ignore-me_userdata/" + self.pUUID + "/"
        #print("output_dir: " + self.output_dir)

        ##Check that the outpur_dir exists. Create it if not.
        if not os.path.exists (self.output_dir):
            #print("Creating a output_dir at: " + self.output_dir)
            os.makedirs(self.output_dir)

        self.updateTransaction(thisTransaction)

    def updateTransaction(self, thisTransaction: Transaction):
        if thisTransaction.response_dict is None:
            thisTransaction.response_dict = {}
        if not 'gems_project' in thisTransaction.response_dict:
            thisTransaction.response_dict['gems_project'] = {}

        thisTransaction.response_dict['gems_project']['requesting_agent'] = self.requesting_agent
        thisTransaction.response_dict['gems_project']['timestamp'] = str(self.timestamp)
        thisTransaction.response_dict['gems_project']['pUUID'] = self.pUUID
        thisTransaction.response_dict['gems_project']['output_dir'] = self.output_dir
        if self.md5sum is not None:
            thisTransaction.response_dict['gems_project']['md5sum'] = self.md5sum
        if self.project_type is not None:
            thisTransaction.response_dict['gems_project']['project_type'] = self.project_type

    def __str__(self):
        result = "GemsProject  - requestingAgent: "
        result = result + self.requesting_agent
        if self.project_type is not None:
            result = result + ", type: "
            result = result + self.project_type
        result = result + ", timestamp: "
        result = result + str(self.timestamp)
        result = result + ", pUUID: "
        result = result + self.pUUID
        result = result + ", output_dir: "
        result = result + self.output_dir
        if self.md5sum is not None:
            result = result + ", md5sum: "
            result = result + self.md5sum

        return result


def generateGemsProjectSchema():
    print(GemsProject.schema_json(indent=2))

if __name__ == "__main__":
    generateGemsProjectSchema()
