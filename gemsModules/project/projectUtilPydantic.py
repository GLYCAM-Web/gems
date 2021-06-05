import gemsModules
from shutil import copyfile
from gemsModules.project import settings as projectSettings
from gemsModules.project import io as projectio
from gemsModules.common import io as commonio
from gemsModules.common import services as commonservices
from gemsModules.common import utils as commonutils
from gemsModules.common.loggingConfig import *
import traceback
from datetime import datetime

import json, os, sys, uuid

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


## TODO - this should be part of Transaction, not Project
## Pass in a transaction, figure out the requestingAgent. OK if it doesn't exist.
#   Default is command line, replaced if a frontend project exists.
#   @param transaction
def getRequestingAgentFromTransaction(thisTransaction: commonio.Transaction):
    log.info("getRequestingAgentFromTransaction() was called.\n")
    projectIn = getProjectFromTransactionIn(thisTransaction)

    requestingAgent = "command_line"
    if projectIn is not None:
        requestingAgent = projectIn.requesting_agent

    log.debug("returning requestingAgent as : " + requestingAgent)
    return requestingAgent




##  Creates dirs if needed in preparation for writing files.
#   @param projectDir
def setupProjectDirs(projectDir):
    log.info("setupProjectDirs() was called.\n")
    
    try:
        if not os.path.exists(projectDir):
            #log.debug("creating the projectDir: " + projectDir)
            os.makedirs(projectDir)
        else:
            log.debug("projectDir exists.")
    except Exception as error:
        log.error("There was a problem with the projectDir.")
        raise error
    #Start a log file for the project and put it in uUUID dir
    logs_dir = projectDir + "/logs/"
    try:
        if not os.path.exists(logs_dir):
            #log.debug("creating the logs dir in project")
            os.makedirs(logs_dir)

        log.debug("projectDir: " + projectDir)
        log.debug("logs_dir: " + logs_dir)
        return logs_dir
    except Exception as error:
        log.error("There was a problem with the logs dir.")
        raise error



### Write the original request to file.
##   @param request
##   @param logsDir
#def writeRequestToFile(request, logsDir):
#    log.info("writeRequestToFile() was called.\n")
#    requestFileName = os.path.join(logsDir,"request.json")
#    log.debug("requestFileName: " + requestFileName)
#    try:
#        with open(requestFileName, 'w', encoding='utf-8') as file:
#            json.dump(request, file, ensure_ascii=False, indent=4)
#    except Exception as error:
#        log.error("There was a problem writing the request to file.")
#        raise error

### Writes the project to file in json format.
##   @param project
##   @param logsDir
#def writeProjectLogFile(project, logsDir):
#    log.info("writeProjectLogFile() was called.\n")
#    logFileName = project.project_type + "ProjectLog.json"
#    project_log_file = os.path.join(logsDir, logFileName)
#    log.debug("project_log_file: " + project_log_file)
#    with open(project_log_file, 'w', encoding='utf-8') as file:
#        jsonString = json.dumps(project.__dict__, indent=4, sort_keys=False, default=str)
#        log.debug("jsonString: \n" + jsonString )
#        file.write(jsonString)

def updateCbProject(thisTransaction, structureInfo):
    log.info("updateCbProject was called")
    log.debug("Requested service: " )
    log.debug(commonservices.prettyString(thisTransaction.transaction_out))
    try:
        projectDir = getProjectDir(thisTransaction)
        log.debug("projectDir: " + projectDir)
    except Exception as error:
        log.error("There was a problem getting the projectDir: " + str(error))
        raise error

##  Pass in a project, and receive the name of the
#   dir that uploaded input files should be copied to.
#   @param project
#   @param project_dir
def getProjectUploadsDir(thisTransaction):
    log.info("getProjectUploadsDir() was called.\n")
    project = getProjectFromTransaction(thisTransaction)
    
    if str(type(project)) == "<class 'gemsModules.project.dataio.PdbProject'>":
        project = project.__dict__

    try:
        projectDir = getProjectDir(thisTransaction)
    except Exception as error:
        log.error("There was a problem getting the projectDir.")
        log.error(traceback.format_exc())
        raise error

    projectUploadsDir = projectDir + "/uploads/"
    log.debug("projectUploadsDir: " + projectUploadsDir)
    if not os.path.exists(projectUploadsDir):
        log.debug("creating the uploads dir")
        os.makedirs(projectUploadsDir)
    return projectUploadsDir


##  Pass a frontend project and get the upload path or an error if
#   it does not exist.
#   @param  project
def getUploadsSourceDir(project):
    log.info("getUploadsSourceDir() was called.\n")
    if str(type(project)) == "<class 'gemsModules.project.dataio.PdbProject'>":
        project = project.__dict__

    log.debug("project obj type: " + str(type(project)))
    log.debug("project.keys(): " + str(project.keys()))

    uploads_source_dir = project['upload_path']
    if not os.path.exists(uploads_source_dir):
        raise FileNotFoundError(uploads_source_dir)
    else:
        return uploads_source_dir

###  Creates a copy of uploads from the frontend
##   @param transaction
#def copyUploadFilesToProject(thisTransaction : commonio.Transaction, project : projectio.Project):
#    log.info("copyUploadFilesToProject() was called.\n")
#    project_dir = getProjectDir(thisTransaction)
#    log.debug("project_dir: " + project_dir)
#
#    ## Find the destination dir
#    try:
#        destination_uploads_dir = getProjectUploadsDir(thisTransaction)
#    except Exception as error:
#        log.error("There was a problem creating the destination for upload files.")
#        log.error("Error type: " + str(type(error)))
#        log.error(traceback.format_exc())
#        raise error
#    # Find the source dir
#    try:
#        uploads_source_dir = getUploadsSourceDir(project)
#        log.debug("uploads_source_dir: " + uploads_source_dir)
#    except Exception as error:
#        log.error("There was a problem finding the upload files.")
#        log.error("Error type: " + str(type(error)))
#        log.error(traceback.format_exc())
#        raise error
#
#    # Find the file name
#    try:
#        target_upload_file = getUploadFileName(project)
#    except Exception as error:
#        log.error("There was a problem finding the upload file name: " + str(error))
#        log.error(traceback.format_exc())
#        raise error
#    try:
#        log.debug("hi")
#        uploads_dir = os.fsencode(uploads_source_dir)
#
#        for upload_file in os.listdir(uploads_dir):
#            filename = os.fsdecode(upload_file)
#            if filename == target_upload_file:
#                log.debug("filename: " + filename)
#                source_file = os.path.join(uploads_source_dir, filename)
#                log.debug("file source: " + source_file)
#                destination_file = os.path.join(destination_uploads_dir, filename)
#                log.debug("file destination: " + destination_file)
#                copyfile(source_file, destination_file)
#                break
#            else:
#                log.debug("Not copying this file: " + filename)
#    except Exception as error:
#        log.error("There was a problem copying the upload files into the project's project_dir.")
#        log.error("Error type: " + str(type(error)))
#        log.error(traceback.format_exc())
#        raise error


## Only gets the file name. Not the path.
#   @aparam project
def getUploadFileName(project):
    log.info("getUploadFileName() was called.\n")
    if str(type(project)) == "<class 'gemsModules.project.dataio.PdbProject'>":
        project = project.__dict__
    
    uploaded_file_name = ""
    if "uploaded_file_name" in project.keys():
        uploaded_file_name = project['uploaded_file_name']
        log.debug("uploaded_file_name: " + uploaded_file_name)
        return uploaded_file_name
    else:
        log.error("No uploaded_file_name found in project.")
        raise AttributeError("uploaded_file_name")

##  Looks at the project in a transaction to return the pUUID.
#   @param thisTransaction Transaction object should contain a project.Else returns none.
def getProjectpUUID(thisProject):
    log.info("getProjectpUUID() was called.\n")
    if thisProject is None :
        log.error("Cannot get pUUID because thisProject is type None.")
        raise AttributeError
    log.debug("thisProject: \n")
    log.debug(thisProject.json(indent=2))
    pUUID = thisProject.pUUID
    log.debug("pUUID: " + str(pUUID))
    if pUUID == "":
        raise AttributeError("pUUID")
    elif pUUID is None:
        raise AttributeError("pUUID")
    else:
        return pUUID

##  Populates the Project model from text contained in the versionsFile.
#   @param versionsFilePath
def getVersionsFileInfo(versionsFilePath : str):
    log.info("getVersionsFileInfo was called.\n")
    import re
    thisDict = {
            'site_version' :  "",
            'site_branch' : "", 
            'gems_version' :  "", 
            'gems_branch' :  "", 
            'md_utils_version' :  "", 
            'md_utils_branch' :  "", 
            'gmml_version' :  "", 
            'gmml_branch' :  "", 
            'gp_version' :  "", 
            'gp_branch' :  "", 
            'site_mode' :  "", 
            'site_host_name' :  ""
            }
    if not os.path.exists(versionsFilePath) :
        log.error("versionsFilePath does not exist.  Cannot set versions info.")
        return thisDict
    with open(versionsFilePath) as file:
        content = file.read()
    lines = content.split("\n")
    for line in lines:
        # Get rid of any whitespace or newline
        trimmed_line = re.sub(r'\s+', '', line)
        theKeyVal =  trimmed_line.split("=")
        if len(theKeyVal) > 1 : 
            theKey=theKeyVal[0]
            theVal=theKeyVal[1].strip('"') 
            lowerKey = theKey.lower()
            if 'git_commit_hash' in  lowerKey : 
                jsonKey=lowerKey.replace('git_commit_hash', 'version')
            elif 'git_branch' in lowerKey :
                jsonKey=lowerKey.replace('git_branch', 'branch')
            else:
                jsonKey=lowerKey
            thisDict[jsonKey]=theVal
    log.debug("the versions dictionary is : " + str(thisDict))
    return thisDict

##  @brief Give a transaction, get a sequence. Note that if more than one input
#   contains a "Sequence" key, only the last sequence is returned.
#   @detail Note that this method is only good for transactions with a single sequence.
#           A new method would be required if/when the need to get a list of sequences arrives.
#   @param Transaction thisTransaction
#   @return String sequence
def getSequenceFromTransaction(thisTransaction: commonio.Transaction, sequenceType:str=None):
    log.info("getSequenceFromTransaction() was called.\n")
    
    inputs = thisTransaction.request_dict['entity']['inputs']
    sequence = ""

    if sequenceType is None:
        log.debug("No sequenceType requested. Grabbing the request payload.")
        for element in inputs:
            #log.debug("element: " + str(element))
            if "Sequence" in element.keys():
                # TODO - make this not rely on 'sequence' being the key.
                #    .... or change the schema....
                sequence = element['Sequence']['payload']
            else:
                log.debug("Skipping")
        if sequence == "":
            raise AttributeError("Sequence")
        else:
            log.debug("returning sequence: " + sequence)
            return sequence
    else:
        log.debug("Looking for the sequenceType: " + str(sequenceType))
        log.debug("response_dict: " )
        prettyPrint(thisTransaction.response_dict)
        responses = thisTransaction.response_dict['entity']['responses']
        for response in responses:
            if 'outputs' in response.keys():
                outputs = response['outputs']
                #log.debug("found the outputs.")
                break

        if outputs == None:
            raise AttributeError("Couldn't find any response outputs.")

        for element in outputs:
            #log.debug("checking input element: " + repr(element))
            ##  TODO: Write this to handle inputs nested inside the service
            if "sequenceVariants" in element.keys():
                if sequenceType in element['sequenceVariants'].keys():
                    sequence = element['sequenceVariants'][sequenceType]
                    log.debug("returning sequence: " + sequence)
                    return sequence


    if thisTransaction.response_dict is not None:
        if 'responses' in thisTransaction.response_dict['entity'].keys():
            responses = thisTransaction.response_dict['entity']['responses']
            #log.debug("The responses. : ")
            #log.debug(str(responses))
            for response in responses:
                if 'outputs' in response.keys():
                    outputs = response['outputs']
                    # log.debug("The outputs: ")
                    # log.debug(str(outputs))
                    if "sequenceVariants" in outputs.keys():
                        if sequenceType in outputs['sequenceVariants'].keys():
                            sequence = outputs['sequenceVariants'][sequenceType]
                            log.debug("returning sequence: " + sequence)
                            return sequence
                    # if 'outputs' in theEvaluations:
                    #         outputs = theEvaluations['outputs']
                    #         log.debug("The second inputs. : ")
                    #         log.debug(str(outputs))
                    #         for element in outputs:
                    #             if "SequenceVariants" in element.keys():
                    #                 if sequenceType in element['SequenceVariants'].keys():
                    #                     sequence = element['SequenceVariants'][sequenceType]
                    #                     return sequence
    log.debug("Still here?   Gosh...   Here is the transaction request: ")
    log.debug(prettyPrint(thisTransaction.request_dict))
    log.debug("...   And here is the transaction response: ")
    log.debug(prettyPrint(thisTransaction.response_dict))
    raise AttributeError("Cannot locate a sequence of type : " + sequenceType)


##  @brief Use a sequence to get a unique seqID.
#   Uses uuid5, which uses SHA-1 rather than Md5Sum
#   @param sequence
#   @return uuid seqID
#   TODO: merge this into the more generic getUuidForString, below
def getSeqIDForSequence(sequence):
    log.info("getSeqUUDIFor() was called. sequence: " + str(sequence))
    if sequence is None :
        raise AttributeError("no sequence to get seqID from")
    seqID = str(uuid.uuid5(uuid.NAMESPACE_OID, sequence))
    log.debug("seqID: " + str(seqID))
    return seqID


##  @brief Use a string to get a unique but repeatable UUID
#   Uses uuid5, which uses SHA-1 rather than Md5Sum
#   @param str string
#   @return uuid seqID
def getUuidForString(theString):
    log.info("getUuidForString() was called. string: " + theString)
    stringID = str(uuid.uuid5(uuid.NAMESPACE_OID, theString))
    log.debug("stringID: " + stringID)
    return stringID

## Build the download URL path for this project/build/whatever
#  Depends on project.settings.
#   @param  hostUrlBasePath
#   @param  pUUID
#   @param  entity_id
#   @param  service_id
#   @param  subdirectory (optional)
#   @return str downloadUrlPath
def buildDownloadUrlPath( 
        hostUrlBasePath : str ,
        entity_id : str ,
        service_id : str ,
        pUUID : str , 
        subdirectory : str = None ):
    log.info("buildDownloadUrlPath was called.\n")
    try :
        downloadUrlPath =  hostUrlBasePath + "/" + "json"+ "/" + "download" + "/" + entity_id + "/" + service_id + "/" + pUUID + "/"
        if subdirectory is not None :
            downloadUrlPath = downloadUrlPath + subdirectory + "/"
        log.debug("downloadUrlPath : " + downloadUrlPath )
        return downloadUrlPath
    except AttributeError as error:
        log.error("Something went wrong building the downloadUrlPath.")
        raise error

def addProjectToResponse(project, thisTransaction):
    log.info("addProjectToResponse() was called.")
    if thisTransaction.response_dict == None:
        thisTransaction.response_dict = {}
    preparedCopy = project.__dict__
    keys = preparedCopy.keys()
    for key in keys:
        preparedCopy[key] = str(preparedCopy[key])
    thisTransaction.response_dict['project'] = preparedCopy
    log.debug("thisTransaction.response_dict: \n" )
    prettyPrint(thisTransaction.response_dict)

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
