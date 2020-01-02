import gemsModules
from gemsModules.project import settings as projectSettings
from gemsModules.project.dataio import *
from gemsModules.common.transaction import *
from gemsModules.common.services import *
from gemsModules.common import utils
from datetime import datetime

import  os, sys, uuid


def receive(thisTransaction: Transaction):
    print("receive() was called.")
    request = thisTransaction.request_dict
    print("type of requestObject: " + str(type(request)))
    if request['project']:
        print("found a project in the request")
        project = request['project']
        if project['_django_version']:
            ##The project was requested via web interface
            startProject(thisTransaction, "website")
        else:
            ##The project was requested via json_api
            print("Project was requested via json_api")

    else:
        ##The request did not come through the frontend, or something went wrong.
        print("No project present in the request.")

    print("Transaction: " + str(thisTransaction.__dict__))

def startProject(thisTransaction : Transaction, requestingAgent : str):
    print("receive() was called.")
    gemsProject = GemsProject()
    gemsProject.buildProject(thisTransaction, requestingAgent)
    print("gemsProject: " + str(gemsProject))
    # project.input_dir =
    # project.output_dir = settings.output_data_root + "tools/" + str(uuid.uuid4())
    # project.requesting_agent = "Command line"
    # log.debug("project: " + str(project))

def main():
    if len(sys.argv) == 2:
        jsonObjectString = utils.JSON_From_Command_Line(sys.argv)
        print("jsonObjectString: " + jsonObjectString)
        thisTransaction=Transaction(jsonObjectString)
        parseInput(thisTransaction)
        receive(thisTransaction)
    else:
        print("You must provide a path to a json request file.")

if __name__ == "__main__":
    main()
