#!/usr/bin/env python3
import json, sys, os, re, importlib.util, shutil, uuid
import gemsModules
import gmml
import traceback
import gemsModules.common.utils
from gemsModules.project.projectUtil import *
from gemsModules.project import settings as projectSettings
from gemsModules.common import io as commonio
from gemsModules.common import logic as commonlogic
from gemsModules.delegator import io as delegatorio
#from gemsModules.common.services import *
#from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common.loggingConfig import *

from gemsModules.sequence import projects as sequenceProjects
from . import settings as sequenceSettings
from .structureInfo import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

##  @brief Pass in a gemsProject and get a responseConfig.
#   @param GemsProject gemsProject
#   @return dict config
def build3dStructureResponseConfig(gemsProject):
    log.info("build3dStructureResponseConfig() was called.\n")
    log.debug("gemsProject: " + str(gemsProject))
    downloadUrl = getDownloadUrl(gemsProject['pUUID'], "cb")
    sequence = gemsProject['sequence']
    config = {
        "entity" : "Sequence",
        "respondingService" : "Build3DStructure",
        "responses" : [{
            'payload' : gemsProject['pUUID'],
            'sequence' : gemsProject['sequence'],
            'seqID' : getSeqIDForSequence(sequence),
            'downloadUrl' : downloadUrl
        }]
    }

    log.debug("returning 3dStructureResponseConfig: " + str(config))

    return config


##  @brief Give a transaction and pUUID, and this method builds the json response and
#   appends that to the transaction.
#   @param Transaction thisTransaction
#   @param String uUUID - Upload ID for user provided input.
def appendBuild3DStructureResponse(thisTransaction : Transaction, pUUID : str):
    log.info("appendBuild3DStructureResonse() was called.\n")
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    if not 'entity' in thisTransaction.response_dict:
        thisTransaction.response_dict['entity']={}
    if not 'type' in thisTransaction.response_dict['entity']:
        thisTransaction.response_dict['entity']['type']='Sequence'
    if not 'responses' in thisTransaction.response_dict:
        thisTransaction.response_dict['responses']=[]

    downloadUrl = getDownloadUrl(pUUID, "cb")
    thisTransaction.response_dict['responses'].append({
        'Build3DStructure': {
            'payload': pUUID ,
            'downloadUrl': downloadUrl
        }
    })


##TODO: Replace this with more generically useful: build3DStructure(transaction, service)
##      Needs to work whether default structure or specific rotamers are requested.

##  @brief Creates a jobsubmission for Amber. Submits that. Updates the transaction to reflect this.
#   @param Transaction thisTransaction
#   @param Service service (optional)
def build3DStructure(buildState : BuildState, thisTransaction : Transaction):
    log.info("Sequence receive.py buildDefault3Dstructure() was called.\n")

    try:
        pUUID=sequenceProjects.getProjectpUUID(thisTransaction)
    except Exception as error:
        log.error("There was a problem finding the project pUUID: " + str(error))
        raise error
    else:
        try:
            sequence = getSequenceFromTransaction(thisTransaction)
        except Exception as error:
            log.error("There was a problem getting a sequence from the transaction: " + str(error))
        else:
            gemsProject = thisTransaction.response_dict['gems_project']
            responseConfig = build3dStructureResponseConfig(gemsProject)
            appendResponse(thisTransaction, responseConfig)

            log.debug("About to getCbBuilderForSequence")
            builder = getCbBuilderForSequence(sequence)
            try:
                projectDir = sequenceProjects.getProjectSubdir(thisTransaction)
            except Exception as error:
                log.error("There was a problem getting this build's subdir: " + str(error))
                raise error
            else:
                try:
#####
#####  START HERE
#####
                    ## Check if this is the default build or if it has user options specified.
                    if sequenceProjects.checkIfDefaultStructureRequest(thisTransaction):
                        destination = projectDir 
                        #destination = projectDir + 'default'
                        log.debug("The request is for a single structure to be placed in: " + destination)
                        # ## Defaults for next build 
                        # ##     output directory: projectDir
                        # ##     types of files to write:  'OFFFILE' -and- 'PDB'
                        # ##     default filename prefix:  'structure'
                        builder.GenerateSingle3DStructureDefaultFiles(destination)
                    else:
                        ##TODO: Test this after GMML can accept user settings.
                        log.debug("The request is for the a set of rotamers.")
                        builder.GenerateRotamerDefaultFiles(destination, buildState)
                except Exception as error:
                    log.error("There was a problem generating this build: " + str(error))
                    raise error
                else:

                    ##TODO This needs to move - Sequence should not be deciding how 
                    ## minimization will happen.  That is the job of mmservice.
                    amberSubmissionJson='{"project" : \
                        {\
                        "id":"' + pUUID + '", \
                        "workingDirectory":"' + projectDir + '", \
                        "type":"minimization", \
                        "system_phase":"gas", \
                        "water_model":"none" \
                        } \
                    }'
                    # TODO:  Make this resemble real code....
                    the_json_file = projectDir + "amber_submission.json"
                    min_json_in = open (the_json_file , 'w')
                    min_json_in.write(amberSubmissionJson)
                    min_json_in.close()

                    from gemsModules.mmservice.amber.amber import manageIncomingString
                    manageIncomingString(amberSubmissionJson)
                    ## everything up to here -- all the amber stuff --
                    ## is what needs to move



##  @brief Pass a sequence string, get a builder for that sequence.
##  @param String sequence - GLYCAM Condensed string sequence.
#   @return CarbohydrateBuilder object from gmml.
def getCbBuilderForSequence(sequence : str):
    log.info("getCbBuilderForSequence() was called.\n")
    GemsPath = getGemsHome()
    log.debug("GemsPath: " + GemsPath )

    prepfile = GemsPath + "/gemsModules/sequence/GLYCAM_06j-1.prep"
    if os.path.exists(prepfile):
        log.debug("Instantiating the carbohydrateBuilder.")
        builder = gmml.carbohydrateBuilder(sequence, prepfile)
        return builder
    else:
        log.error("Prepfile did not exist at: " + prepfile)
        raise FileNotFoundError





def main():
    log.info("buildFromSequence.py was called.")
    log.info("The main function in buildFromSequence.py doesn't do anything.")


if __name__ == "__main__":
    main()
