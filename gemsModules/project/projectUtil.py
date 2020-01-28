import gemsModules
from shutil import copyfile
from gemsModules.project import settings as projectSettings
from gemsModules.project.dataio import *
from gemsModules.common.transaction import *
from gemsModules.common.services import *
from gemsModules.common import utils
from gemsModules.common.loggingConfig import *
import traceback
from datetime import datetime

import json, os, sys, uuid

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.DEBUG

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)

"""
Pass in a transaction, if a frontend project is in the request,
a GemsProject is created with any relevant data, and the
transaction is updated with the gemsProject.
If no frontend project is present, the GemsProject is the only
project.
"""
def startProject(thisTransaction: Transaction):
    log.info("startProject() was called.")
    ##TODO: Add logic to return errors if things go wrong.
    request = thisTransaction.request_dict
    keys = request.keys()
    if 'project' in keys:
        log.debug("found a project in the request")
        project = request['project']
        if '_django_version' in project.keys():
            log.debug("website project present.")
            ##The project was requested via web interface
            buildGemsProject(thisTransaction, "website")
        else:
            ##The project was requested via json_api
            log.debug("Project was requested via json_api")
            buildGemsProject(thisTransaction, "json_api")

    else:
        log.debug("Project needs to be created without the frontend.")
        buildGemsProject(thisTransaction, "command_line")

    log.debug("project type: " + project.project_type)
    output_dir = copyUploadFiles(thisTransaction)
    #Start a log file for the project and put it in uUUID dir
    logs_dir = output_dir + "logs/"
    if not os.path.exists(logs_dir):
        log.debug("creating the logs dir in project")
        os.makedirs(logs_dir)

    request_file = os.path.join(logs_dir,"request.json")
    log.debug("request_file: " + request_file)

    with open(request_file, 'w', encoding='utf-8') as f:
        json.dump(request, f, ensure_ascii=False, indent=4)

    log.debug("Transaction: " + str(thisTransaction.__dict__))

"""
Creates a copy of uploads from the frontend
returns the output_dir for the project as a convenience.
"""
def copyUploadFiles(thisTransaction : Transaction):
    log.info("copyUploadFiles() was called.")
    #Root of entire project
    output_dir = thisTransaction.response_dict['gems_project']['output_dir']
    log.debug("output_dir: " + output_dir)

    if not os.path.exists(output_dir):
        log.debug("creating the output_dir")
        os.makedirs(output_dir)

    project = thisTransaction.request_dict['project']
    if 'u_uuid' in project.keys():
        uUUID = project['u_uuid']
        uploads_dest_dir = output_dir + "uploads/" + uUUID + "/"
        log.debug("uploads_dest_dir: " + uploads_dest_dir)

        if not os.path.exists(uploads_dest_dir):
            #print("creating the uploads dir")
            os.makedirs(uploads_dest_dir)

        uploads_source_dir = project['upload_path']
        log.debug("uploads_source_dir: " + uploads_source_dir)

        if not os.path.exists(uploads_source_dir):
            ##TODO: return the actual error.
            log.dbug("Returning an error. Upload_path indicated, but not present.")
            pass
        else:
            log.debug("Copying upload files to the backend.")
            uploads_dir = os.fsencode(uploads_source_dir)

            for upload_file in os.listdir(uploads_dir):
                filename = os.fsdecode(upload_file)
                log.debug("filename: " + filename)

                source_file = os.path.join(uploads_source_dir, filename)
                log.DEBUG("file source: " + source_file)

                destination_file = os.path.join(uploads_dest_dir, filename)
                log.debug("file destination: " + destination_file)

                copyfile(source_file, destination_file)
    else:
        log.debug("no uUUID found. May be ok, if there are no uploads needed.")
        pass
    return output_dir

"""
Pass in a transaction and a string indicating what is requesting this project.
The transaction is updated with any relevant project data.
"""
def buildGemsProject(thisTransaction : Transaction, requestingAgent : str):
    log.info("buildGemsProject() was called.")
    gemsProject = GemsProject()
    gemsProject.buildProject(thisTransaction, requestingAgent)
    log.debug("gemsProject: " + str(gemsProject))


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
