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
    ##TODO: Add logic to return errors if things go wrong.
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

    #Start a log file for the project and put it in uUUID dir
    output_dir = thisTransaction.response_dict['gems_project']['output_dir']
    print("output_dir: " + output_dir)

    if not os.path.exists(output_dir):
        print("creating the output_dir")
        os.makdirs(output_dir)

    if 'u_uuid' in project.keys():
        uUUID = project['u_uuid']
        uploads_copy_dir = output_dir + "Uploads/" + uUUID + "/"
        print("uploads_copy_dir: " + uploads_copy_dir)
        if not os.path.exists(uploads_copy_dir):
            print("creating the uploads_copy_dir")
            os.makedirs(uploads_copy_dir)
        upload_dir = project['upload_path']
        if not os.path.exists(upload_dir):
            print("Returning an error. Upload_path indicated, but not present.")
        else:
            print("Copying upload files to the backend.")
            ##TODO: copy em ova.

    else:
        print("no uUUID found. May be ok, if there are no uploads needed.")




    #Save all upload files and logs into the pUUID dir

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
