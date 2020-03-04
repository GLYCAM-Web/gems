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

##TODO: Add better error handling.
##TODO: Use Doxygen-style comments.
"""
Pass in a transaction, if a frontend project is in the request,
a GemsProject is created with any relevant data, and the
transaction is updated with the gemsProject.
If no frontend project is present, the GemsProject is the only
project.
"""
def startProject(thisTransaction: Transaction):
    log.info("startProject() was called.\n")
    request = thisTransaction.request_dict
    project = getFrontendProjectFromTransaction(thisTransaction)
    requestingAgent = getRequestingAgentFromTransaction(thisTransaction)
    gemsProject = buildGemsProject(thisTransaction, requestingAgent)
    output_dir = getOutputDir(thisTransaction)
    if gemsProject.hasInputFiles:
        copyUploadFiles(thisTransaction)
    try:
        logs_dir = setupProjectDirs(output_dir)
        writeRequestToFile(request, logs_dir)
        writeProjectLogFile(gemsProject, logs_dir)
    except Exception as error:
        log.error("There was a problem writing the project logs.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())

    #log.debug("Transaction: " + str(thisTransaction.__dict__))
    return gemsProject

## Pass in a transaction, figure out the requestingAgent.
#   Default is command line, replaced if a frontend project exists.
#   @param transaction
def getRequestingAgentFromTransaction(thisTransaction: Transaction):
    log.info("getRequestingAgentFromTransaction() was called.\n")
    project = getFrontendProjectFromTransaction(thisTransaction)
    requestingAgent = "command_line"
    if project is not None:
        requestingAgent = project['requesting_agent']
    return requestingAgent


##  Pass in a transaction, get the frontend project
#   @param transaction
def getFrontendProjectFromTransaction(thisTransaction: Transaction):
    log.info("getRequestFromTransaction() was called.\n")
    project = thisTransaction.request_dict['project']
    return project

##  Pass in a transaction, get the outputDir
#   @param outputDir
def getOutputDir(thisTransaction: Transaction):
    log.info("getOutputDir() was called.\n")
    output_dir = thisTransaction.response_dict['gems_project']['output_dir']
     ##Check that the outpur_dir exists. Create it if not.
    if not os.path.exists (output_dir):
        log.debug("Creating a output_dir at: " + output_dir)
        os.makedirs(output_dir)
    log.debug("output_dir: " + output_dir)
    return output_dir

##  Creates dirs if needed in preparation for writing files.
#   @param outputDir
def setupProjectDirs(outputDir):
    log.info("setupProjectDirs() was called.\n")
    if not os.path.exists(outputDir):
        log.debug("creating the outputDir")
        os.makedirs(outputDir)

    #Start a log file for the project and put it in uUUID dir
    logs_dir = outputDir + "logs/"
    if not os.path.exists(logs_dir):
        log.debug("creating the logs dir in project")
        os.makedirs(logs_dir)

    log.debug("logs_dir: " + logs_dir)
    return logs_dir


## Write the original request to file.
#   @param request
#   @param logsDir
def writeRequestToFile(request, logsDir):
    log.info("writeRequestToFile() was called.\n")
    requestFileName = os.path.join(logsDir,"request.json")
    log.debug("requestFileName: " + requestFileName)
    with open(requestFileName, 'w', encoding='utf-8') as file:
        json.dump(request, file, ensure_ascii=False, indent=4)


## Writes the gems project to file in json format.
#   @param gemsProject
#   @param logsDir
def writeProjectLogFile(gemsProject, logsDir):
    log.info("writeProjectLogFile() was called.\n")
    logFileName = gemsProject.project_type + "ProjectLog.json"
    project_log_file = os.path.join(logsDir, logFileName)
    log.debug("project_log_file: " + project_log_file)
    with open(project_log_file, 'w', encoding='utf-8') as file:
        jsonString = json.dumps(gemsProject.__dict__, indent=4, sort_keys=True, default=str)
        log.debug("jsonString: \n" + jsonString )
        file.write(jsonString)


##TODO: Refactor for better encapsulation
##  Creates a copy of uploads from the frontend
#   returns the output_dir for the project as a convenience.
#   @param transaction

def copyUploadFiles(thisTransaction : Transaction):
    log.info("copyUploadFiles() was called.\n")
    output_dir = getOutputDir(thisTransaction)
    log.debug("output_dir: " + output_dir)
    project = getFrontendProjectFromTransaction(thisTransaction)
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
            log.debug("Returning an error. Upload_path indicated, but not present.")
            pass
        else:
            log.debug("Copying upload files to the backend.")
            uploads_dir = os.fsencode(uploads_source_dir)

            for upload_file in os.listdir(uploads_dir):
                filename = os.fsdecode(upload_file)
                log.debug("filename: " + filename)

                source_file = os.path.join(uploads_source_dir, filename)
                log.debug("file source: " + source_file)

                destination_file = os.path.join(uploads_dest_dir, filename)
                log.debug("file destination: " + destination_file)

                copyfile(source_file, destination_file)
    else:
        log.debug("no uUUID found. May be ok, if there are no uploads needed.")
        pass
    return output_dir



##TODO: Use Doxygen-style comments.
"""
Pass in a transaction and a string indicating what is requesting this project.
The transaction is updated with any relevant project data.
"""
def buildGemsProject(thisTransaction : Transaction, requestingAgent : str):
    log.info("buildGemsProject() was called.\n")
    gemsProject = GemsProject()
    gemsProject.buildProject(thisTransaction, requestingAgent)
    log.debug("gemsProject: " + str(gemsProject))
    return gemsProject


##If the requesting agent is the website, leave the gems project.
#   Otherwise remove it.
#   @param thisTransaction The transaction object provides the requesting agent.
def cleanGemsProject(thisTransaction : Transaction):
    log.info("cleanGemsProject() was called.\n")
    log.debug("response_dict.keys(): " + str(thisTransaction.response_dict.keys()))
    if 'gems_project' in thisTransaction.response_dict.keys():
        if "website" == thisTransaction.response_dict['gems_project']['requesting_agent']:
            log.debug("Returning response to website.")
        else:
            log.debug("Cleanup for api requests.")
            del thisTransaction.response_dict['gems_project']

##  Looks at the gemsProject in a transaction to return the pUUID.
#   @param thisTransaction Transaction object should contain a gemsProject.Else returns none.
def getProjectpUUID(thisTransaction : Transaction):
    log.info("getProjectpUUID() was called.\n")
    pUUID = None
    if 'gems_project' in thisTransaction.response_dict.keys():
        pUUID = thisTransaction.response_dict['gems_project']['pUUID']
    else:
        log.error("Cannot get pUUID from a transaction that has no gems_project.")
        log.error("thisTransaction: \n" + str(thisTransaction.response_dict.keys()))
    log.debug("pUUID: " + str(pUUID))
    return pUUID


## Pass a pUUID and an appName, get a download url.
#   appNames should look like frontend app abbreviations, cb, pdb, gp etc...
#   @param  pUUID
#   @param  appName
def getDownloadUrl(pUUID : str, appName : str):
    log.info("getDownloadUrl was called.")
    log.debug("pUUID: " + pUUID)
    log.debug("appName: " + appName)
    try:
        versionsFile = "/website/userdata/VERSIONS.sh"
        with open(versionsFile) as file:
            content = file.read()

        siteHostName = getSiteHostName(content)

        ##Note: It may one day be necessary to edit http to https in production responses.
        ##      It also may not be necessary. Doing nothing until need arrises.

        url = "http://" + siteHostName + "/json/download/" + appName +"/" + pUUID
        log.debug("url : " + url )
        return url
    except AttributeError as error:
        log.error("Something went wrong building the downloadUrl.")
        raise error

##  Intended for use by getDownloadUrl. Content is the text contained in
#   the versionsFile.
#   @param content
def getSiteHostName(content):
    log.info("getSiteHostName was called.")
    lines = content.split("\n")
    for line in lines:
        if 'SITE_HOST_NAME' in line:
            start = line.index("=") + 1
            siteHostName = line[start:].replace('"', '')
            log.debug("siteHostName: " + siteHostName)
    if siteHostName is not None:
        return siteHostName
    else:
        log.error("Never did find a siteHostName.")
        raise AttributeError

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