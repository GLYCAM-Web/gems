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


##  Pass in a transaction, if a project is in the request,
#   a project is created with any relevant data, and the
#   transaction is updated with the project.
#   @param transaction
def startProject(thisTransaction):
    log.info("startProject() was called.\n")
    try:
        # The requesting entity should have already initialized the transaction_in
        #     AND the transaction_out
        entity = thisTransaction.transaction_in.entity.entityType
    except Exception as error:
        log.error("There was a problem finding the entity in this transaction: " + str(error))
        raise error
    try:
        ### Start a project
        thisProjectIn = thisTransaction.transaction_in.project
        thisProjectOut = thisTransaction.transaction_out.project
        if entity == "Sequence":
            log.debug("building a cb project.")
            thisProjectOut = projectio.CbProject()
        elif entity == "StructureFile":
            log.debug("building a pdb project.")
            thisProjectOut = projectio.PdbProject()
        elif entity == "Conjugate":
            log.debug("building a gp project.")
            thisProjectOut = projectio.GpProject()
        else:
            log.error("Need to write code to instantiate projects for entity type: " + entity)
            raise TypeError("entity: " + entity)

    except Exception as error:
        log.error("There was a problem starting the project: " + str(error))
        raise error

    thisProjectOut.startMeUp(thisTransaction)
    log.debug("project.project_dir, after instantiation: " + thisProjectOut.project_dir)
#    try:
#        addProjectToResponse(projectio.project, thisTransaction)
#    except Exception as error:
#        log.error("There was a problem updating thisTransaction: " + str(error))
#        raise error
    ### Find the projectDir.
    try:
        project_dir = thisProjectOut.project_dir
        logs_dir = setupProjectDirs(project_dir)
    except Exception as error:
        log.error("There was a problem getting the projectDir: " + str(error))
        raise error
    ### Copy any upload files.
    log.debug("project.has_input_files: " + str(thisProjectOut.has_input_files))
    if thisProjectOut.has_input_files == "True":
        try:
            copyUploadFilesToProject(thisTransaction, thisProjectOut)
        except Exception as error:
            log.error("There was a problem uploading the input: " + str(error))
            raise error

    ### Write the logs to file.
    try:
        request = thisTransaction.request_dict
        writeRequestToFile(request, logs_dir)
        writeProjectLogFile(thisProjectOut, logs_dir)
        return thisProjectOut
    except Exception as error:
        log.error("There was a problem writing the project logs: " + str(error))
        raise error

    return thisProjectOut

## Pass in a transaction, figure out the requestingAgent. OK if it doesn't exist.
#   Default is command line, replaced if a frontend project exists.
#   @param transaction
def getRequestingAgentFromTransaction(thisTransaction: commonio.Transaction):
    log.info("getRequestingAgentFromTransaction() was called.\n")

    project = getFrontendProjectFromTransaction(thisTransaction)
    requestingAgent = "command_line"
    if project is not None:
        requestingAgent = project['requesting_agent']

    log.debug("requestingAgent: " + requestingAgent)
    return requestingAgent


##  Pass in a transaction, get the frontend project
#   @param transaction
def getProjectFromTransaction(thisTransaction: commonio.Transaction):
    log.info("getProjectFromTransaction() was called.\n")
    if 'project' in thisTransaction.request_dict.keys():
        project = thisTransaction.request_dict['project']
        log.debug("Object type for project: " + str(type(project)))
        return project
    else:
        return None

##  @brief Pass in a transaction, get the projectDir
#   @param Transaction thisTransaction
#   @return project_dir
def setProjectDir(thisTransaction):
    # do we need this?
    pass


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


## Write the original request to file.
#   @param request
#   @param logsDir
def writeRequestToFile(request, logsDir):
    log.info("writeRequestToFile() was called.\n")
    requestFileName = os.path.join(logsDir,"request.json")
    log.debug("requestFileName: " + requestFileName)
    try:
        with open(requestFileName, 'w', encoding='utf-8') as file:
            json.dump(request, file, ensure_ascii=False, indent=4)
    except Exception as error:
        log.error("There was a problem writing the request to file.")
        raise error



## Writes the project to file in json format.
#   @param project
#   @param logsDir
def writeProjectLogFile(project, logsDir):
    log.info("writeProjectLogFile() was called.\n")
    logFileName = project.project_type + "ProjectLog.json"
    project_log_file = os.path.join(logsDir, logFileName)
    log.debug("project_log_file: " + project_log_file)
    with open(project_log_file, 'w', encoding='utf-8') as file:
        jsonString = json.dumps(project.__dict__, indent=4, sort_keys=False, default=str)
        log.debug("jsonString: \n" + jsonString )
        file.write(jsonString)

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


##  Creates a copy of uploads from the frontend
#   @param transaction
def copyUploadFilesToProject(thisTransaction : commonio.Transaction, project : projectio.Project):
    log.info("copyUploadFilesToProject() was called.\n")
    project_dir = getProjectDir(thisTransaction)
    log.debug("project_dir: " + project_dir)

    ## Find the destination dir
    try:
        destination_uploads_dir = getProjectUploadsDir(thisTransaction)
    except Exception as error:
        log.error("There was a problem creating the destination for upload files.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        raise error
    # Find the source dir
    try:
        uploads_source_dir = getUploadsSourceDir(project)
        log.debug("uploads_source_dir: " + uploads_source_dir)
    except Exception as error:
        log.error("There was a problem finding the upload files.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        raise error

    # Find the file name
    try:
        target_upload_file = getUploadFileName(project)
    except Exception as error:
        log.error("There was a problem finding the upload file name: " + str(error))
        log.error(traceback.format_exc())
        raise error
    try:
        log.debug("hi")
        uploads_dir = os.fsencode(uploads_source_dir)

        for upload_file in os.listdir(uploads_dir):
            filename = os.fsdecode(upload_file)
            if filename == target_upload_file:
                log.debug("filename: " + filename)
                source_file = os.path.join(uploads_source_dir, filename)
                log.debug("file source: " + source_file)
                destination_file = os.path.join(destination_uploads_dir, filename)
                log.debug("file destination: " + destination_file)
                copyfile(source_file, destination_file)
                break
            else:
                log.debug("Not copying this file: " + filename)
    except Exception as error:
        log.error("There was a problem copying the upload files into the project's project_dir.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        raise error


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


## Pass a pUUID and an appName, get a download url.
#   appNames should look like frontend app abbreviations, cb, pdb, gp etc...
#   @param  pUUID
#   @param  appName
def getDownloadUrl(pUUID : str, appName : str, optionalSubDir : str = ""):
    log.info("getDownloadUrl was called.\n")
    log.debug("pUUID: " + pUUID)
    log.debug("appName: " + appName)
    log.debug("optionalSubDir: " + optionalSubDir)
    try:
        versionsFile = "/website/userdata/VERSIONS.sh"
        with open(versionsFile) as file:
            content = file.read()
        siteHostName = getSiteHostName(content)
        url = "http://" + siteHostName + "/json/download/" + appName +"/" + pUUID + "/" + optionalSubDir
        log.debug("downloadUrl : " + url )
        return url
    except AttributeError as error:
        log.error("Something went wrong building the downloadUrl.")
        raise error

##  Intended for use by getDownloadUrl. Content is the text contained in
#   the versionsFile.
#   @param content
def getSiteHostName(content):
    log.info("getSiteHostName was called.\n")
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
def getUuidForString(string):
    log.info("getUuidForString() was called. string: " + string)
    stringID = str(uuid.uuid5(uuid.NAMESPACE_OID, string))
    log.debug("stringID: " + stringID)
    return stringID


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
