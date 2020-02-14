#!/usr/bin/env python3
import gemsModules
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common.loggingConfig import *
from gemsModules.project.projectUtil import *
from gemsModules.structureFile.amber.receive import *
import gemsModules.conjugate.settings as conjugateSettings
import subprocess
import urllib.request

##TO set logging verbosity for just this file, edit this var to one of the following:
## logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logLevel = logging.ERROR

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__, logLevel)

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

##TODO: Refactor so errors stop the process and return responses. Not happening this way yet.
def buildGlycoprotein(thisTransaction):
    log.info("buildGlycoprotein() was called.\n")
    request = thisTransaction.request_dict
    log.debug("request: " + str(request))
    pdbFileName = ""
    pdbID = ""
    attachments = []
    if 'inputs' in request['entity'].keys():
        inputs = request['entity']['inputs']
        log.debug("inputs: " + str(inputs))
        for element in inputs:
            log.debug("element: " + str(element))
            log.debug("keys: " + str(element.keys()))
            if "pdb_file_name" in element.keys():
                pdbFileName = element['pdb_file_name']['payload']
                log.debug("pdbFileName: " + pdbFileName)
            elif "pdb_ID" in element.keys():
                pdbID = element['pdb_ID']
            elif "attachments" in element.keys():
                attachments = element['attachments']
                log.debug("attachments: " + str(attachments))
            else:
                log.debug("found: " + str(element.keys()))

        ##Verify that the pdb is in fact of type PDB.
        if pdbFileName != "":
            ##TODO: find a better way to verify that a file is a pdb file, as some may
            ##  legitimately not have the .pdb extension.
            if ".pdb" not in pdbFileName:
                noticeBrief = "For now, pdb files must have the .pdb extension. May change later."
                log.error(noticeBrief)
                ##Transaction, noticeBrief, blockID
                appendCommonParserNotice(thisTransaction, 'InvalidInput' )
            else:
                log.debug("Looks like a pdb file. Moving forward.")
        elif pdbID != "":
            ##Query rcsb for the pdbID. Be prepared for failures.
            log.debug("Requesting pdbID: " + pdbID + " from rcsb.org")
            ##TODO: Break this up. Trying too much in a single try/except block.
            try:
                ##Sideload pdb from rcsb.org
                pdbID = pdbID.upper()
                rcsbURL = "https://files.rcsb.org/download/" + pdbID + ".pdb1"
                log.debug("rcsbURL: " + rcsbURL)
                with urllib.request.urlopen(rcsbURL) as response:
                    contentBytes = response.read()

                contentString = str(contentBytes, 'utf-8')
                log.debug("Response content object type: " + str(type(contentString)))
                log.debug("Response content: \n" + str(contentString))
                ##Get the uploads dir
                if "project" in request.keys():
                    uploadDir = request['project']['upload_path']
                    if not os.path.exists(uploadDir):
                        os.mkdir(uploadDir)
                    log.debug("uploadDir: " + uploadDir)
                    uploadFileName = uploadDir  + pdbID + ".pdb"
                    request['project']['uploaded_file_name'] = uploadFileName
                else:
                    log.error("Need a project to find the upload dir.")

                log.debug("uploadFileName: " + uploadFileName)
                ##Save the string to file in the uploads dir.
                with open(uploadFileName, "w") as uploadFile:
                    uploadFile.write(contentString)

                log.debug("Finished side-loading pdb from rcsb.org.")

            except Exception as error:
                log.error("There was a problem submitting the request to rcsb.org.")
                log.error("pdbID: " + pdbID)
                log.error("Error type: " + str(type(error)))
                log.error(traceback.format_exc())
        else:
            log.error("Failed to find a value for pdb_file_name or pdb_ID.")
            appendCommonParserNotice(thisTransaction, 'InvalidInput' )


        ##For now, require attachments.
        if len(attachments) == 0:
            log.error("BuildGlycoprotein requests require 'attachments'.")
            appendCommonParserNotice(thisTransaction, 'InvalidInput' )
        else:
            log.debug("Attachments present. Moving forward.")

        log.debug("Still here. Starting a project.")
        gemsProject = startProject(thisTransaction)

        ##Return response that the project has been started.
        thisTransaction.response_dict['responses'].append({
            "BuildGlycoprotein" : {
                'project_status' : gemsProject.status,
                'payload' : gemsProject.pUUID
            }
        })

        ##Preprocess pdb file
        preprocessPdbForAmber(thisTransaction)

        ##Ask Glycoproteinbuilder to do its stuff.
        ##Get the name of the preprocessed file:
        outputDir = gemsProject.output_dir
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
                for attachment in attachments:
                    file.write(attachment['chain'] + "_" + attachment['residue_number'] + "," + attachment['glycan'] + "\n")
                file.write("END")
                log.debug("Finished writing input.txt")
        except Exception as error:
            log.error("Failed to create input.txt")
            log.error("Error type: " + str(type(error)))
            log.error(traceback.format_exc())

        log.debug("Input file created. Calling the Glycoprotein Builder Program.")
        ##Build the command to run gp
        builderPath = "/programs/GlycoProteinBuilder/bin/gp_builder"
        log.debug("builderPath: " + builderPath)
        log.debug("inputFileName: " + inputFileName)
        #/programs/GlycoProteinBuilder/bin/ /website/userdata/tools/gp/git-ignore-me_userdata/4f18b278-d9bb-4111-b502-d91945639fa6/ > /website/userdata/tools/gp/git-ignore-me_userdata/4f18b278-d9bb-4111-b502-d91945639fa6/gp.log
        command = builderPath + " " + outputDir + " > " + outputDir + "gp.log"
        log.debug("command: " + command)

        try:
            subprocess.call(command,stdout=sys.stdout, stderr=sys.stderr, shell=True)
        except Exception as error:
            log.error("There was a problem calling the GlycoproteinBuilder program.")
            log.error("Error type: " + str(type(error)))
            log.error(traceback.format_exc())

        ##Return the pUUID as the payload.
        thisTransaction.response_dict['responses'].append({
            "BuildGlycoprotein" : {
                "payload" : gemsProject.pUUID
            }
        })


        ##Cleanup for non-website requesting_agents.
        if 'gems_project' in thisTransaction.response_dict.keys():
            if "website" == thisTransaction.response_dict['gems_project']['requesting_agent']:
                log.debug("Returning response to website.")
            else:
                log.debug("Cleanup for api requests.")
                del thisTransaction.response_dict['gems_project']

    else:
        ##TODO: attach an error response.
        log.error("Could not find inputs in the request.")
        log.error(str(request.keys()))


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

