#!/usr/bin/env python3
import  os, sys
import json
import uuid
from datetime import datetime
from gemsModules.common.transaction import *
from gemsModules.project import settings as projectSettings
from pydantic import BaseModel, Field
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
import traceback

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.ERROR

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)

##TODO: Use Doxygen-style comments.
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
    status : str = "submitted"
    hasInputFiles : bool = False

    def buildProject(self, thisTransaction : Transaction, requestingAgent : str):
        log.info("buildProject was called.\n")
        log.debug("requestingAgent: " + requestingAgent)
        request = thisTransaction.request_dict
        self.requesting_agent = requestingAgent
        self.timestamp = datetime.now()
        self.pUUID = str(uuid.uuid4())

        if self.requesting_agent != 'command_line':
            if request['entity']['type'] == 'MmService':
                self.hasInputFiles = True
            elif request['entity']['type'] == 'Conjugate':
                self.hasInputFiles = True
            elif request['entity']['type'] == "StructureFile":
                self.hasInputFiles = True

            if 'md5Sum' in request['project'].keys():
                self.md5sum = request['project']['md5Sum']
            if 'type' in request['project'].keys():
                self.project_type = request['project']['type']
        else:
            ##There will be no frontend project here.
            log.error("Still developing command_line logic for projects.")

        self.output_dir = projectSettings.output_data_dir + "tools/" + self.project_type + "/git-ignore-me_userdata/" + self.pUUID + "/"

        ##Check that the outpur_dir exists. Create it if not.
        if not os.path.exists (self.output_dir):
            os.makedirs(self.output_dir)

        self.updateTransaction(thisTransaction)

    def updateTransaction(self, thisTransaction: Transaction):
        log.info("updateTransaction() was called.\n")
        if thisTransaction.response_dict is None:
            thisTransaction.response_dict = {}
        if not 'entity' in thisTransaction.response_dict:
            thisTransaction.response_dict['entity'] = {}
            thisTransaction.response_dict['entity']['type'] = thisTransaction.request_dict['entity']['type']

        if not 'gems_project' in thisTransaction.response_dict:
            thisTransaction.response_dict['gems_project'] = {}

        thisTransaction.response_dict['gems_project']['status'] = self.status
        thisTransaction.response_dict['gems_project']['requesting_agent'] = self.requesting_agent
        thisTransaction.response_dict['gems_project']['timestamp'] = str(self.timestamp)
        thisTransaction.response_dict['gems_project']['pUUID'] = self.pUUID
        thisTransaction.response_dict['gems_project']['output_dir'] = self.output_dir
        thisTransaction.response_dict['gems_project']['hasInputFiles'] = self.hasInputFiles
        if self.md5sum is not None:
            thisTransaction.response_dict['gems_project']['md5sum'] = self.md5sum
        if self.project_type is not None:
            thisTransaction.response_dict['gems_project']['project_type'] = self.project_type

    def __str__(self):
        result = "\nGemsProject:\nrequestingAgent: "
        result = result + self.requesting_agent
        if self.project_type is not None:
            result = result + "\ntype: "
            result = result + self.project_type
        result = result + "\nstatus: "
        result = result + self.status
        result = result + "\ntimestamp: "
        result = result + str(self.timestamp)
        result = result + "\npUUID: "
        result = result + self.pUUID
        result = result + "\noutput_dir: "
        result = result + self.output_dir
        result = result + "\nhasInputFiles: "
        result = result + str(self.hasInputFiles)
        if self.md5sum is not None:
            result = result + "\nmd5sum: "
            result = result + self.md5sum

        return result

##  Figures out the type of structure file being preprocessed.
def getStructureFileProjectType(request):
    projectType = "not set"
    services = request['entity']['services']
    for service in services:
        if 'Preprocess' in service.keys():
            if 'type' in service['Preprocess'].keys():
                if 'PreprocessPdbForAmber' == service['Preprocess']['type']:
                    projectType = "pdb"

    return projectType


def generateGemsProjectSchema():
    print(GemsProject.schema_json(indent=2))

if __name__ == "__main__":
    generateGemsProjectSchema()
