import gemsModules
from gemsModules.project import settings as projectSettings
from gemsModules.project.dataio import *
from gemsModules.common.transaction import *
from gemsModules.common.services import *
from gemsModules.common import utils
from datetime import datetime

import  os, sys, uuid

"""
Pass in a transaction, if a frontend project is in the request,
a GemsProject is created with any relevant data, and the
transaction is updated with the gemsProject.
If no frontend project is present, the GemsProject is the only
project.
"""
def startProject(thisTransaction: Transaction):
    print("startProject() was called.")
    request = thisTransaction.request_dict
    keys = request.keys()
    if 'project' in keys:
        print("found a project in the request")
        project = request['project']
        if '_django_version' in project.keys():
            print("website project present.")
            ##The project was requested via web interface
            buildGemsProject(thisTransaction, "website")
        else:
            ##The project was requested via json_api
            print("Project was requested via json_api")
            buildGemsProject(thisTransaction, "json_api")
    else:
        print("Project needs to be created without the frontend.")
        buildGemsProject(thisTransaction, "command_line")

    print("Transaction: " + str(thisTransaction.__dict__))

"""
Pass in a transaction and a string indicating what is requesting this project.
The transaction is updated with any relevant project data.
"""
def buildGemsProject(thisTransaction : Transaction, requestingAgent : str):
    #print("buildGemsProject() was called.")
    gemsProject = GemsProject()
    gemsProject.buildProject(thisTransaction, requestingAgent)
    #print("gemsProject: " + str(gemsProject))


def main():
    if len(sys.argv) == 2:
        jsonObjectString = utils.JSON_From_Command_Line(sys.argv)
        #print("jsonObjectString: " + jsonObjectString)
        thisTransaction=Transaction(jsonObjectString)
        parseInput(thisTransaction)
        startProject(thisTransaction)
    else:
        #print("You must provide a path to a json request file.")
        pass

if __name__ == "__main__":
    main()
