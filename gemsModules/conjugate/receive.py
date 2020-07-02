#!/usr/bin/env python3
import gemsModules
from gemsModules.batchcompute.receive import *
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common.loggingConfig import *
from gemsModules.project.projectUtil import *
from gemsModules.structureFile.amber.receive import *
import gemsModules.conjugate.settings as conjugateSettings
import subprocess
import urllib.request

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

def doDefaultService(thisTransaction):
    log.info("doDefaultService() was called.\n")
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    thisTransaction.response_dict['entity']={}
    thisTransaction.response_dict['entity']['type']='Conjugate'
    thisTransaction.response_dict['responses']=[]
    buildGlycoprotein(thisTransaction)

    #thisTransaction.response_dict['responses'].append({'payload':marco('Conjugate')})


def receive(thisTransaction):
    log.info("receive() was called.\n")

    ##Begin building a response dict for holding output
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict = {}
    thisTransaction.response_dict['entity'] = {}
    thisTransaction.response_dict['entity']['type'] = "Conjugate"
    thisTransaction.response_dict['responses'] = []

    ##Look in transaction for the requested service. If none, do default service.
    if 'services' not in thisTransaction.request_dict['entity'].keys():
        log.debug("could not find the services key in ['entity']")
        doDefaultService(thisTransaction)
    else:
        services = getTypesFromList(thisTransaction.request_dict['entity']['services'])
        log.debug("requestedServices: " + str(services))
        for requestedService in services:
            log.debug("requestedService: " + str(requestedService))
            if requestedService not in conjugateSettings.serviceModules.keys():
                log.error("The requested service is not recognized.")
                log.error("services: " + str(conjugateSettings.serviceModules.keys()))
                appendCommonParserNotice(thisTransaction,'ServiceNotKnownToEntity', requestedService)
            elif requestedService == "BuildGlycoprotein":
                buildGlycoprotein(thisTransaction)
            else:
                log.error("Logic should never reach this point. Look at congugate/receive.py.")

    thisTransaction.build_outgoing_string()

##TODO: Have errors stop the process and return responses. Not happening this way yet.
def buildGlycoprotein(thisTransaction):
    log.info("buildGlycoprotein() was called.\n")
    pdbFileName = ""
    pdbID = ""
    attachmentSites = []

    attachmentSites = getAttachmentSitesFromTransaction(thisTransaction)
    log.debug("attachmentSites: " + str(attachmentSites))

    ##For now, require attachmentSites.
    if len(attachmentSites) == 0:
        log.error("BuildGlycoprotein requests require 'attachmentSites'.")
        appendCommonParserNotice(thisTransaction, 'InvalidInput' )
    else:
        log.debug("attachmentSites present.")
        if "gems_project" not in thisTransaction.response_dict.keys():
            log.debug("Need to create a new project.")
            gemsProject = startProject(thisTransaction)
            log.debug("\ngpProject: \n")
            prettyPrint(gemsProject.__dict__)
        else:
            log.debug("gemsProject already present.")

        log.debug("\n1)First, preprocess the PDB file.\n")
        preprocessPdbForAmber(thisTransaction)
        log.debug("\nFinished preprocessing pdb.\n")
        inputFileName = writeGpInputFile(gemsProject, attachmentSites)
        log.debug("Finished writing GP input file: " + inputFileName)
        sbatchArg = writeGpScript(inputFileName, gemsProject)
        log.debug("Finished writing the GP script: " + sbatchArg)

        try:
            log.debug("\n2)Then build the cocomplex.\n")
            response = submitGpScriptToSlurm(thisTransaction, gemsProject, sbatchArg)
            log.debug("response from batchcompute: \n" + str(response))

        except Exception as error:
            log.error("There was a problem calling the GlycoProteinBuilder program.")
            log.error("Error type: " + str(type(error)))
            log.error(traceback.format_exc())
        else:
            responseConfig = buildGPResponseConfig(gemsProject)
            appendResponse(thisTransaction, responseConfig)
            log.debug("Finished submitting GP request to slurm.")



##Pass in a gemsProject and get a responseConfig dict.
def buildGPResponseConfig(gemsProject):
    log.info("buildGPResponseConfig() was called.\n")
    try:
        downloadUrl = getDownloadUrl(gemsProject.pUUID, "gp")
    except AttributeError as error:
        raise error
    else:
        config = {
            "entity" : "Conjugate",
            "respondingService" : "BuildGlycoprotein",
            "responses" : [
                {
                    'project_status' : gemsProject.status,
                    'payload' : gemsProject.pUUID,
                    'downloadUrl' : downloadUrl
                }
            ]
        }
    return config



##  Writes the file that slurm is expected to run. Returns the sbatchArg needed for submission
#   @param inputFileName
#   @param gemsProject
def writeGpScript(inputFileName, gemsProject):
    log.info("writeGpScript() was called.\n")
    ##Build the command to run gp
    builderPath = "/programs/GlycoProteinBuilder/bin/gp_builder"
    log.debug("builderPath: " + builderPath)
    log.debug("inputFileName: " + inputFileName)

    outputDir = gemsProject.project_dir
    #/programs/GlycoProteinBuilder/bin/ /website/userdata/tools/gp/git-ignore-me_userdata/4f18b278-d9bb-4111-b502-d91945639fa6/ > /website/userdata/tools/gp/git-ignore-me_userdata/4f18b278-d9bb-4111-b502-d91945639fa6/gp.log
    sbatchArg = "gpScript.sh"
    script = outputDir + sbatchArg
    try:
        with open(script, 'w', encoding='utf-8') as file:
            file.write("#!/bin/bash\n")
            file.write('GPPATH="' + builderPath + '"\n')
            file.write('WorkDir="' + outputDir + '"\n')
            file.write('COMMAND="${GPPATH} ${WorkDir} > ${WorkDir}/logs/gp.log"\n')
            file.write('eval ${COMMAND}')
        return sbatchArg

    except Exception as error:
        log.error("There was a problem writing the gp script for slurm.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc)




def writeGpInputFile(gemsProject, attachmentSites):
    log.info("writeGpInputFile() was called.\n")
    ##Write the Input file, which GP uses to know what to do.
    outputDir = gemsProject.project_dir
    preprocessedPdbFileName = "updated_pdb.pdb"
    log.debug("preprocessedPdbFileName: " + preprocessedPdbFileName)
    inputFileName = outputDir + "input.txt"
    log.debug("inputFileName: " + inputFileName)
    ##Build input.txt
    ##For now, assuming that sites are specified in the request.
    try:
        with open(inputFileName, 'w', encoding='utf-8') as file:
            file.write("Protein:\n")
            file.write(preprocessedPdbFileName + "\n\n")
            file.write("Protein Residue, Glycan Name:\n")
            ##GP requires input to look like this: "A_83, Man9"
            ##  There are two formats we allow in requests:
            ##  glycan : "Man9"
            ##  site : "A_83"
            ##  OR
            ##  glycan : "Man9"
            ##  chain : "A"
            ##  residue_number : "83"
            for attachment in attachmentSites:
                if "site" in attachment.keys():
                    file.write(attachment['site'] + "," + attachment['glycan'] + "\n")
                else:
                    file.write(attachment['chain'] + "_" + attachment['residue_number'] + "," + attachment['glycan'] + "\n")

            file.write("END")
            log.debug("Finished writing input.txt")
        return inputFileName
    except Exception as error:
        log.error("Failed to create input.txt")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        raise error

##Pass a transaction, get a dict of attachmentSites if present, otherwise error.
#   @param transaction
def getAttachmentSitesFromTransaction(thisTransaction):
    log.info("getAttachmentSitesFromTransaction() was called.\n")

    if "inputs" in thisTransaction.request_dict['entity'].keys():
        inputs = thisTransaction.request_dict['entity']['inputs']
        attachmentSitesFound = False
        for element in inputs:
            log.debug("element: " + str(element))
            log.debug("keys: " + str(element.keys()))
            if "attachments" in element.keys():
                attachmentSites = element['attachments']
                attachmentSitesFound = True
        if attachmentSitesFound:
            return attachmentSites
        else:
            raise AttributeError("Could not find attachments in request inputs.")
    else:
        raise AttributeError("Could not find inputs.")

def main():
  import importlib.util, os, sys
  #from importlib import util
  if importlib.util.find_spec("gemsModules") is None:
    this_dir, this_filename = os.path.split(__file__)
    sys.path.append(this_dir + "/../")
    if importlib.util.find_spec("common") is None:
      print("Something went horribly wrong.  No clue what to do.")
      return
    else:
      from common import utils
  else:
    from gemsModules.common import utils

  jsonObjectString=utils.JSON_From_Command_Line(sys.argv)
  responseObjectString=delegate(jsonObjectString)
  print(responseObjectString)


if __name__ == "__main__":
  main()

