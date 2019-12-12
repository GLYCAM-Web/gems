#!/usr/bin/env python3
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
    gems_project_id : str = None
    output_dir : str = None
    md5sum : str = None
    project_type : str = None
    requesting_agent : str = None

    def buildProject(self, thisTransaction : Transaction, requestingAgent : str):
        print("buildProject was called.")
        print("requestingAgent: " + requestingAgent)

        self.requestingAgent = requestingAgent
        request = thisTransaction.request_dict
        print(str(request))
        if request['project']['timestamp']:
            self.timestamp = request['project']['timestamp']
        else:
            print("No timestamp present in project, go ahead and make one.")
            self.timestamp = datetime.now()

        if request['project']['md5sum']:
            self.md5sum = request['project']['md5sum']
        if request['project']['type']:
            self.project_type = request['project']['type']

        self.gems_project_id = str(uuid.uuid4())
        print("gems_project_id: " + str(self.gems_project_id))
        self.project_root =  str(uuid.uuid4())
        print("project_root: " + self.project_root)
        self.output_dir = projectSettings.output_data_dir + self.project_root
        print("output_dir: " + self.output_dir)
        self.updateTransaction(thisTransaction)

    def updateTransaction(self, thisTransaction: Transaction):
        if thisTransaction.response_dict is None:
            thisTransaction.response_dict = {}
        if not 'gemsProject' in thisTransaction.response_dict:
            thisTransaction.response_dict['gemsProject'] = {}

        thisTransaction.response_dict['gemsProject']['requestingAgent'] = self.requesting_agent
        thisTransaction.response_dict['gemsProject']['timestamp'] = str(self.timestamp)
        thisTransaction.response_dict['gemsProject']['gems_project_id'] = self.gems_project_id
        thisTransaction.response_dict['gemsProject']['output_dir'] = self.output_dir
        if self.md5sum is not None:
            thisTransaction.response_dict['gemsProject']['md5sum'] = self.md5sum
        if self.project_type is not None:
            thisTransaction.response_dict['gemsProject']['project_type'] = self.project_type

    def __str__(self):
        result = "GemsProject  - requestingAgent: "
        result = result + self.requestingAgent
        if self.project_type is not None:
            result = result + ", type: "
            result = result + self.project_type
        result = result + ", timestamp: "
        result = result + str(self.timestamp)
        result = result + ", gems_project_id: "
        result = result + self.gems_project_id
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
