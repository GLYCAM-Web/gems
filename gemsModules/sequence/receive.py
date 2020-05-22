#!/usr/bin/env python3
import json, sys, os, re, importlib.util, shutil, uuid
import gemsModules
import gmml
import traceback

## Get rid of these after the bad subprocess code is gone
import subprocess,signal
from subprocess import *
from datetime import datetime

#from gemsModules import common
#from gemsModules import sequence
#from gemsModules.sequence.receive import *
import gemsModules.common.utils
from gemsModules.project.projectUtil import *
from gemsModules.project import settings as projectSettings
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from gemsModules.common.loggingConfig import *
from . import settings

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


##  @brief Evaluate a condensed sequence 
#    @detail Evaluating a sequence requires a sequence string and a path to a prepfile.
#    1) Checks sequence for validity,
#    2) Starts a gemsProject.
#    3) builds a default structure, moving it to the output dir
#    3) appends options to transaction
#    4) returns boolan valid
#   @param Transaction thisTransaction
#   @param Service service
#   @return boolean valid
def evaluateCondensedSequence(thisTransaction : Transaction, thisService : Service = None):
    log.info("evaluateCondensedSequence() was called.\n")
    sequence = getSequenceFromTransaction(thisTransaction)
    #Test that this exists.
    if sequence is None:
        log.error("No sequence found in the transaction.")
        raise AttributeError
    else:
        log.debug("sequence: " + sequence)
    builder = getCbBuilderForSequence(sequence)
    valid = builder.GetSequenceIsValid()
    linkages = getLinkageOptionsFromBuilder(builder)
    responseConfig = buildEvaluationResponseConfig(valid, linkages)
    appendResponse(thisTransaction, responseConfig)
    return valid


##  @brief Pass in validation result and linkages, get a responseConfig.
#   @param boolean valid
#   @param dict linkages
#   @return dict config
def buildEvaluationResponseConfig(valid, linkages):
    log.info("buildEvaluationResponseConfig() was called. \n")
    config = {
        "entity" : "Sequence",
        "respondingService" : "SequenceEvaluation",
        "responses" : [{
            "type": "Evaluate",
            "outputs" : [{
                "SequenceValidation" : {
                    "SequenceIsValid" : valid
                }
            },{
                "BuildOptions": {
                    "geometricElements" : [
                        { "Linkages" : linkages }
                    ]
                }
            }]
        }]
    }

    return config


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


##  @brief Pass a cb builder, get linkage options.
#   @param  CarbohydrateBuilder builder - GMML class.
#   @return dict linkages
def getLinkageOptionsFromBuilder(builder):
    log.info("getLinkageOptionsFromBuilder() was called.\n")
    userOptionsString = builder.GenerateUserOptionsJSON()
    userOptionsJSON = json.loads(userOptionsString)
    optionsResponses = userOptionsJSON['responses']
    for response in optionsResponses:
        log.debug("response.keys: " + str(response.keys()))
        if 'Evaluate' in response.keys():
            if "glycosidicLinkages" in response['Evaluate'].keys():
                linkages = response['Evaluate']['glycosidicLinkages']
                if linkages != None:
                    ## Creating a new dict that can hold a new, derived field.
                    updatedLinkages = []
                    for element in linkages:
                        log.debug("element: " + str(element))
                        if element == None:
                            return None
                        copy = {}
                        for key in element.keys():
                            log.debug("key: " + key)
                            log.debug("element[" + key + "]: " + str(element[key]))
                            copy[key] = {}
                            for gmmlKey in element[key]:
                                copy[key].update({
                                    gmmlKey : element[key][gmmlKey],
                                    'linkageSequence' : element[key]['linkageName']
                                })
                        updatedLinkages.append(copy)
                else:
                    return None
            else: 
                return None

    log.debug("updatedLinkages: " + str(updatedLinkages))
    return updatedLinkages




##  @brief Creates a jobsubmission for Amber. Submits that. Updates the transaction to reflect this.
#   @param Transaction thisTransaction
#   @param Service service
def buildDefault3DStructure(thisTransaction : Transaction, thisService : Service = None):
    log.info("Sequence receive.py buildDefault3Dstructure() was called.\n")
    ##TODO: See if a project has already been started first.
    startProject(thisTransaction)
    try:
        pUUID=getProjectpUUID(thisTransaction)
    except Exception as error:
        log.error("There was a problem finding the project pUUID.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        raise error

    sequence = getSequenceFromTransaction(thisTransaction)

    if sequence is None:
        raise AttributeError("sequence")
    else:
        gemsProject = thisTransaction.response_dict['gems_project']
        responseConfig = build3dStructureResponseConfig(gemsProject)
        appendResponse(thisTransaction, responseConfig)

    builder = getCbBuilderForSequence(sequence)
    try:
        projectDir = getProjectDirSubDir(thisTransaction)
    except Exception as error:
        log.error("There was a problem getting this build's subdir.")
        raise error
    else:
        destination = projectDir + 'structure'
        log.debug("destination: " + destination)
        builder.GenerateSingle3DStructure(destination)

    ## This needs to move - Sequence should not be deciding how 
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

def getProjectDirSubDir(thisTransaction: Transaction):
    log.info("getProjectDirSubDir() was called.")
    project_dir = thisTransaction.response_dict['gems_project']['project_dir']
    log.debug("project_dir: " + project_dir)

    ## If default structure, subdir name is 'default'
    if checkIfDefaultStructureRequest(thisTransaction):
        project_dir = project_dir + "default/"
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

    else:
        log.error("Still writing the logic to handle builds with selectedRotamers.")
        ##TODO: provide the subdir based on this doc: 
        ## http://128.192.9.183/eln/gwscratch/2020/01/10/succinct-rotamer-set-labeling-for-sequences/
        raise AttributeError("rotamerSubdir")
    return project_dir 


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


def getOptionsFromTransaction(thisTransaction: Transaction):
    log.info("getOptionsFromTransaction() was called.")
    if "options" in thisTransaction.request_dict.keys():
        log.debug("Found options.")
        return thisTransaction.request_dict['options']
    else:
        log.debug("No options found.")
        return None

##  @brief Default service is marco polo. Should this be something else?
#   @param Transaction this Transaction
def doDefaultService(thisTransaction : Transaction):
    log.info("doDefaultService() was called.\n")
    # evaluate(thisTransaction : Transaction)
    # build3DStructure(thisTransaction : Transaction)
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    thisTransaction.response_dict['entity']={}
    thisTransaction.response_dict['entity']['type']='SequenceDefault'
    thisTransaction.response_dict['responses']=[]
    thisTransaction.response_dict['responses'].append({'DefaultTest': {'payload':marco('Sequence')}})
    thisTransaction.build_outgoing_string()


##  @brief The main way Delegator interacts with this module. Request handling.
#   @param Transaction thisTransactrion
def receive(thisTransaction : Transaction):
    log.info("receive() was called:\n")
    import gemsModules.sequence
    ## First figure out the names of each of the requested services
    if not 'services' in thisTransaction.request_dict['entity'].keys():
        log.debug("'services' was not present in the request. Do the default.")
        doDefaultService(thisTransaction)
        return
    input_services = thisTransaction.request_dict['entity']['services']
    theServices=getTypesFromList(input_services)
    ## for each requested service
    for i in theServices:
        #####  the automated module loading doesn't work, and I can't figure out how to make it work,
              # that is:
              #  requestedModule='.'+settings.serviceModules[i]
              #  the_spec = importlib.util.find_spec('.sequence.entity.evaluate',gemsModules)
              # .... and many variants thereof
        #####  so, writing something ugly for now
        if i not in settings.serviceModules.keys():
            if i not in common.settings.serviceModules.keys():
                log.error("The requested service is not recognized.")
                common.settings.appendCommonParserNotice( thisTransaction,'ServiceNotKnownToEntity',i)
            else:
                pass
        ## if it is known, try to do it
        elif i == "Validate":
            log.debug("Validate service requested from sequence entity.")
            validateCondensedSequence(thisTransaction, None)
        elif i == "Evaluate":
            log.debug("Evaluate service requested from sequence entity.")
            evaluateCondensedSequence(thisTransaction,  None)
        elif i == 'Build3DStructure':
            log.debug("Build3DStructure service requested from sequence entity.")
            ##first evaluate the requested structure. Only build if valid.
            valid = evaluateCondensedSequence(thisTransaction, None)

            if valid:
                log.debug("Valid sequence. Building default structure.")

                if checkIfDefaultStructureRequest(thisTransaction):
                    if checkIfDefaultStructureExists(thisTransaction):
                        log.debug("Returning response with payload of existing build.")
                        respondWithExistingDefaultStructure(thisTransaction)
                    else:
                        log.debug("Default structure does not exist yet.")
                        buildDefault3DStructure(thisTransaction, None)
                        registerBuild(thisTransaction)
                else:
                    log.error("The code for building structures with selectedRotamers does not exist yet.")
                    
            else:
                log.error("Invalid Sequence. Cannot build.")
                common.settings.appendCommonParserNotice( thisTransaction,'InvalidInput',i)
        else:
            log.error("got to the else, so something is wrong")
            common.settings.appendCommonParserNotice( thisTransaction,'ServiceNotKnownToEntity',i)
    thisTransaction.build_outgoing_string()

def respondWithExistingDefaultStructure(thisTransaction):
    log.info("respondWithExistingDefaultStructure() was called.")
    sequence = getSequenceFromTransaction(thisTransaction)
    seqID = getSeqIDForSequence(sequence)
    
    config = {
        "entity":"Sequence",
        "respondingService":"Build3DStructure",
        "responses": [{
            'payload': seqID,
            'download' : getDownloadUrl(seqID, "cb") 
        }]
    }
    appendResponse(thisTransaction, config)
    



def registerBuild(thisTransaction):
    log.info("registerBuild() was called.")
    structureMap = {}
    sequence = getSequenceFromTransaction(thisTransaction)
    seqID = getSeqIDForSequence(sequence)
    timestamp = str(datetime.now())
    structureMap.update({
        "sequence":sequence,
        "seqID": seqID,
        "timestamp": timestamp
    })

    ## userDataDir is the top level dir that holds all projects, not a specific user's data.
    userDataDir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/"
    seqIDPath = userDataDir + seqID
    
    if not os.path.exists(seqIDPath):
        os.makedirs(seqIDPath)

    projectDir = getProjectDir(thisTransaction)
    try:
        isDefault = checkIfDefaultStructureRequest(thisTransaction)
        log.debug("isDefault: " + str(isDefault))
        if isDefault:
            link = seqIDPath + "/default"
            projectDir = projectDir + "/default"
        else:
            link = buildRotamerDirName(thisTransaction)
        
        if os.path.exists(projectDir):
            target = projectDir
            ##What is being linked to is the projecDir or the 
            log.debug("target: " + target)
            ##This will be the symbolic link
            log.debug("link: " + link)
            os.symlink(target, link)
        else:
            log.error("Failed to find the target dir for the symbolic link.")
            raise FileNotFoundError(projectDir)
        
    except Exception as error:
        log.error("There was a problem creating the symbolic link.")
        raise error
    else:
        ##TODO: Determine if the default structure was requested or not.
        ## For now, assume the default structure was requested.
        
        solvationRequested = checkIfSolvationRequested(thisTransaction)
        if solvationRequested == "Yes":
            solvationShape = getSolvationShape(thisTransaction)
        else:
            solvationShape = ""
        forceField = getForceFieldFromRequest(thisTransaction)

        ##TODO: Update the json file for future reference.
        structureMappingFilename = seqIDPath + "/structureMapping.json"
        structureMap.update({
            "isDefault": isDefault,
            "solvationRequested": solvationRequested,
            "solvationShape": solvationShape,
            "forceField": forceField,
        })
        log.debug("Attempting to write the structure mapping data to file.")
        log.debug("structureMap: " + str(structureMap))
        try:
            if not os.path.exists(structureMappingFilename):
                with open(structureMappingFilename, 'w', encoding='utf-8') as jsonFile:
                    jsonString = json.dump(structureMap, jsonFile, ensure_ascii=False, indent=4)
                    #jsonFile.write(jsonString)
            else:
                log.debug("The structureMapping.json file exists. Adding a new record.")
                ##TODO: Write this logic.
        except Exception as error:
            log.error("There was a problem writing the structure mapping to file.")
            raise error


def buildRotamerDirName(thisTransaction):
    log.info("buildRotamerDirName() was called.")
    ##TODO: Write this logic when building structures with selectedRotamers exists.
    log.error("buildRotamerDirName still needs to be written.")

def getSolvationShape(thisTransaction):
    log.info("getSolvationShape() was called.")
    project = getFrontendProjectFromTransaction(thisTransaction)
    if project is not None:
        return project['solvation_shape']
    else:
        ##TODO: write logic for commandline users to specify solvent shapes other than the default.
        return "REC"



##  @brief Look at the transaction to see if a force field is specified
#   @param Transaction thisTransaction
#   @return String either "default" or the force field name.
def getForceFieldFromRequest(thisTransaction):
    log.info("getForceFieldFromRequest() was called.")
    project = getFrontendProjectFromTransaction(thisTransaction)
    if project is not None:
        if project['force_field'] == "":
            return "default"
        else:
            return project['force_field']

    else:
        ##TODO: write logic for commandline users to specify forcefields other than the default
        return "default"

## @brief Look at the transaction to see if solvation was requested.
#  @param Transaction thisTransaction
#   @return Boolean solvationRequested
def checkIfSolvationRequested(thisTransaction):
    log.info("checkIfSolvationRequested() was called.")
    project = getFrontendProjectFromTransaction(thisTransaction)
    if project is not None:
        if project['solvation'] == "Yes":
            return True
        else:
            return False
    else:
        log.error("This logic is still in development.")
        ##TODO: figure out how one might specify a request for solvation if there is not a frontend project.
        #           This applies to command line users that don't use the website or JSON API

##  @brief In Development!!! Always returns true for now.
#   @param Transaction thisTransaction
#   @return Boolean isDefault
def checkIfDefaultStructureRequest(thisTransaction):
    log.info("checkIfDefaultStructureRequest was called().")
    options  = getOptionsFromTransaction(thisTransaction)
    log.debug("options: " + str(options))

    if options == None:
        return True
    else:
        ## The presense of rotamers in options means this is not a request
        # for the default structure.
        if "rotamers" in options.keys():
            return False
        else:
            return True


##  @brief Looks up the sequence and generates an seqID, then checks for existing builds.
#   @param Transaction thisTransaction
#   @return Boolean structureExists
def checkIfDefaultStructureExists(thisTransaction):
    log.info("checkIfDefaultStructureExists() was called.")
    structureExists = False
    sequence = getSequenceFromTransaction(thisTransaction)
    seqID = getSeqIDForSequence(sequence)
    userDataDir = projectSettings.output_data_dir + "tools/cb/git-ignore-me_userdata/"
    log.debug("userDataDir: " + userDataDir)
    options = getOptionsFromTransaction(thisTransaction)
    try:
        log.debug("Walking the userDataDir.")

        for element in os.walk(userDataDir):
            rootPath = element[0]
            dirNames = element[1]
            fileNames = element[2]

            log.debug("rootPath: " + str(rootPath))
            log.debug("dirNames: " + str(dirNames))
            log.debug("fileNames: " + str(fileNames))
            for dirName in dirNames:
                log.debug("dirName: " + dirName)
                log.debug("seqID: " + seqID)
                if seqID == dirName:
                    return True
                    
    except Exception as error:
        log.error("There was a problem checking if this structure exists.")
        raise error
    else:
        return structureExists


# ##  Looks at a transaction object to see if an evalutaion response exists and returns a boolean.
# def checkEvaluationResponseValidity(thisTransaction):
#     log.info("checkEvaluationResponseValidity() was called.\n")
#     valid = False
#     log.debug("transactionResponses")
#     responses = thisTransaction.response_dict['responses']
#     for response in responses:
#         log.debug("response: " + str(response))
#         if 'SequenceEvaluation' in response.keys():
#             if response['SequenceEvaluation']['type'] == "Evaluate":
#                 outputs = response['SequenceEvaluation']['outputs']
#                 for output in outputs:
#                     log.debug("output: " + str(output))
#                     if "SequenceValidation" in output.keys():
#                         valid = output['SequenceValidation']['SequenceIsValid']
#         else:
#             raise AttributeError
#     return valid

##  @brief Only validate a condensed sequence. Boolean result.
#   @deprecated.
def validateCondensedSequence(thisTransaction : Transaction, thisService : Service = None):
    log.info("~~~ validateCondensedSequence was called.\n")
    #Look in transaction for sequence
    inputs = thisTransaction.request_dict['entity']['inputs']
    log.debug("inputs: " + str(inputs))

    for input in inputs:
        log.debug("input.keys(): " + str(input.keys()))

        keys = input.keys()

        if 'Sequence' in keys:
            payload = input['Sequence']['payload']
            log.debug("payload: " + payload)
            if payload == None:
                log.error("Could not find Sequence in inputs.")
                ##transaction, noticeBrief, blockId
                common.settings.appendCommonParserNotice( thisTransaction, 'EmptyPayload', 'InvalidInputPayload')
            else:
                log.debug("validating input: " + str(input))
                sequence = payload
                log.debug("getting prepResidues.")
                #Get prep residues
                prepResidues = gmml.condensedsequence_glycam06_residue_tree()
                log.debug("Instantiating an assembly.")
                #Create an assembly
                assembly = gmml.Assembly()

                try:
                    log.debug("Checking sequence sanity.")
                    #Call assembly.CheckCondensed sequence sanity.
                    valid = assembly.CheckCondensedSequenceSanity(sequence, prepResidues)
                    log.debug("validation result: " + str(valid))

                    ## Add valid to the transaction responses.
                    if valid:
                        thisTransaction.response_dict={}
                        thisTransaction.response_dict['entity']={
                                'type' : "sequence",
                        }
                        thisTransaction.response_dict['entity']['responses']=[]
                        log.debug("Creating a response for this sequence.")
                        thisTransaction.response_dict['entity']['responses'].append({
                            "condensedSequenceValidation" : {
                                'sequence': sequence,
                                'valid' : valid,
                            }
                        })
                    else:
                        log.error("~~~\nCheckCondensedSequenceSanity returned false. Creating an error response.")
                        log.error("thisTransaction: "  + str(thisTransaction))
                        log.error(traceback.format_exc())
                        ##appendCommonParserNotice(thisTransaction: Transaction,  noticeBrief: str, blockID: str = None)
                        common.settings.appendCommonParserNotice( thisTransaction,  'InvalidInput', 'InvalidInputPayload')
                except:
                    log.error("Something went wrong while validating this sequence.")
                    log.error("sequence: " + sequence)
                    log.error(traceback.format_exc())
                    common.settings.appendCommonParserNotice( thisTransaction, 'InvalidInput', 'InvalidInputPayload')
        else:
            ##Can be ok, inputs may be provided that are not sequences.
            log.debug("no sequence found in this input, skipping.")
            pass


# Some alternate ways to interrogate lists:
#    if any("Evaluate" in s for s in input_services ):
#        print("It is here!")
#    types=[s for s in input_services if "type" in s.values()]
#    evaluations=[s for s in input_services if "Evaluate" in s]
#    print(evaluations)


def main():
    log.info("main() was called.\n")

if __name__ == "__main__":
  main()

