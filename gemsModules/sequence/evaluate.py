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
from gemsModules.common.loggingConfig import *
from . import settings as sequenceSettings
from . import io as sequenceio
from . import io as sequencelogic

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

def evaluateCondensedSequencePydantic(thisTransaction : sequenceio.Transaction, thisService : sequenceio.sequenceService = None, validateOnly = False):
    log.info("evaluateCondensedSequencePydantic() was called.\n")
    log.debug("thisService: " + str(thisService))
    log.debug("validateOnly: " + str(validateOnly))

    sequence = thisTransaction.getInputSequencePayload()
    #Test that this exists.
    if sequence is None:
        errorMsg = "No sequence found in the transaction."
        log.error(errorMsg)
        raise AttributeError(errorMsg)
    else:
        log.debug("YAY!  Found a sequence: " + sequence)

    ##Generate output first. sequence, validateOnly
    evaluationOutput = sequenceio.SequenceEvaluationOutput()
    evaluationOutput.getEvaluation(sequence, validateOnly)
    log.debug("Evaluation output: " + repr(evaluationOutput))
    sequenceIsValid = evaluationOutput.sequenceIsValid
    log.debug("sequenceIsValid: " + str(sequenceIsValid))
    outputs = []
    outputs.append(evaluationOutput)

    ## serviceType, inputs, and outputs.
    serviceResponse = sequenceio.ServiceResponse(thisService, inputs, outputs)

    ##TODO: get sequenceIsValid and ValidateOnly.
    if sequenceIsValid and not validateOnly: 
        responseObj = serviceResponse.dict(by_alias = True)
        log.debug("responseObj:\n")
        prettyPrint(responseObj)
        commonlogic.updateResponse(thisTransaction, responseObj)
        log.debug("finished building default structure")
    else:
        log.debug("validateOnly was true. Does evaluateCondensedSequence return a well-formed response?")

    log.debug("response_dict, after evaluation: ")
    prettyPrint(thisTransaction.response_dict)
    return sequenceIsValid

##  @brief Pass in validation result and linkages and sequences, get a responseConfig.
#   @param boolean valid
#   @param dict linkages
#   @return dict config
# def buildEvaluationResponseConfig(valid, linkages, sequences):
#     log.info("buildEvaluationResponseConfig() was called. \n")
#     # TODO:  Please someone make this less ugly
# #    if linkages is None:
#     # from gemsModules.sequence import io
#     # entity = io.Entity()
#     # entity.InitializeClass()
#     # print(entity.json())
    # """ Old and ugly """
    # config = {      
    #     "responses" : [{
    #         "entity" : "Sequence",
    #         "type": "Evaluate",
    #         "outputs" : [{
    #             "SequenceValidation" : {
    #                 "SequenceIsValid" : valid
    #             }
    #         },{
    #             "SequenceVariants": sequences
    #         },{
    #             "BuildOptions": {
    #                 "geometricElements" : [
    #                     { "Linkages" : linkages }
    #                 ]
    #             }
    #         }]
    #     }]
    # }

# ## The following might have once been a format for a validation response. 
# ## Keeping it for historical sake.  Today is 2020-08-11.  If there
# ## is no need for this by, say, 2021-08-11, this can go.
# ##
# ##    thisTransaction.response_dict['entity']['responses'].append({
# ##    "condensedSequenceValidation" : {
# ##    'sequence': sequence,
# ##    'valid' : valid,
# ##    }
# ##    })


# I think if we got all the names to match, we could use parse_object_as instead of this. OG.
# Probably it would fail on sub-classes though, but maybe.
def getLinkageOptionsFromGmmlcbBuilder(sequence):
    log.info("getLinkageOptionsFromGmmlcbBuilder() was called.\n")
    log.debug("sequence: " + sequence)
    from gemsModules.sequence import build
    from gemsModules.sequence import io
    cbBuilder = build.getCbBuilderForSequence(sequence)
    gmmllinkageOptionsVector = cbBuilder.GenerateUserOptionsDataStruct()
    log.debug("gmmllinkageOptionsVector: " + repr(gmmllinkageOptionsVector))

    gemsLinkageGeometryOptions = io.LinkageGeometryOptions()
    gemsLinkageGeometryOptions.totalPossibleRotamers = cbBuilder.GetNumberOfShapes()
    likelyOnly = True
    gemsLinkageGeometryOptions.totalLikelyRotamers = cbBuilder.GetNumberOfShapes(likelyOnly)

    for gmmlLinkageOptions in gmmllinkageOptionsVector:

        gemsLinkageOptions = io.LinkageRotamers()

        gemsLinkageOptions.indexOrderedLabel = gmmlLinkageOptions.indexOrderedLabel_
        gemsLinkageOptions.linkageName = gmmlLinkageOptions.linkageName_
        gemsLinkageOptions.firstResidueNumber = gmmlLinkageOptions.firstResidueNumber_
        gemsLinkageOptions.secondResidueNumber = gmmlLinkageOptions.secondResidueNumber_

        """ Likely Rotamers """
        for dihedralOptions in gmmlLinkageOptions.likelyRotamers_:
            gemsRotamers = io.DihedralRotamers() 
            gemsRotamers.dihedralName = dihedralOptions.dihedralName_
            
            for rotamer in dihedralOptions.rotamers_:
                gemsRotamers.dihedralValues.extend([rotamer]);
            
            gemsLinkageOptions.likelyRotamers.append(gemsRotamers)

        """ Possible Rotamers """
        for dihedralOptions in gmmlLinkageOptions.possibleRotamers_:
            gemsRotamers = io.DihedralRotamers()
            gemsRotamers.dihedralName = dihedralOptions.dihedralName_


            for rotamer in dihedralOptions.rotamers_:
                gemsRotamers.dihedralValues.extend([rotamer]);

            gemsLinkageOptions.possibleRotamers.append(gemsRotamers)

            ## dihedralsWithOptions Needed for the website
            gemsLinkageOptions.dihedralsWithOptions.append(gemsRotamers.dihedralName)

        gemsLinkageGeometryOptions.linkageRotamersList.append(gemsLinkageOptions)

    log.debug("gemsLinkageGeometryOptions: " + repr(gemsLinkageGeometryOptions))
    return gemsLinkageGeometryOptions

#### REMOVE after 2021-08-01 if not needed before then
##  @brief Pass a sequence, get linkage options.
#   @param  str sequence 
# #   @return dict linkages
# def getLinkageOptionsFromBuilder(sequence):
#     log.info("getLinkageOptionsFromBuilder() was called.\n")
#     from gemsModules.sequence import build
#     cbBuilder = build.getCbBuilderForSequence(sequence)
#     userOptionsString = cbBuilder.GenerateUserOptionsJSON()
#     userOptionsJSON = json.loads(userOptionsString)
#     optionsResponses = userOptionsJSON['responses']
#     for response in optionsResponses:
#         log.debug("response.keys: " + str(response.keys()))
#         if 'Evaluate' in response.keys():
#             if "glycosidicLinkages" in response['Evaluate'].keys():
#                 linkages = response['Evaluate']['glycosidicLinkages']
#                 if linkages != None:
#                     ## Creating a new dict that can hold a new, derived field.
#                     updatedLinkages = []
#                     for element in linkages:
#                         log.debug("element: " + str(element))
#                         if element == None:
#                             return None
#                         copy = {}
#                         for key in element.keys():
#                             log.debug("key: " + key)
#                             log.debug("element[" + key + "]: " + str(element[key]))
#                             copy[key] = {}
#                             for gmmlKey in element[key]:
#                                 copy[key].update({
#                                     gmmlKey : element[key][gmmlKey],
#                                     'linkageSequence' : element[key]['linkageName']
#                                 })
#                         updatedLinkages.append(copy)
#                 else:
#                     return None
#             else: 
#                 return None

#     log.debug("updatedLinkages: " + str(updatedLinkages))
#     return updatedLinkages


##  @brief Pass a sequence, get linkage options.
#   @param  str sequence 
#   @return dict sequences
def getSequenceVariants(sequence):
    log.info("getSequenceVariants() was called.\n")
    this_sequence = gmml.CondensedSequence(sequence)
    # ## 
    # ##  This function assumes that the validity of the sequence was determined elsewhere
    # ## 
    # ##   So.... this is not needed....  :   if this_sequence.GetIsSequenceOkay()
    Sequences = {}
    Sequences['userSupplied']=sequence
    Sequences['indexOrdered']= this_sequence.BuildLabeledCondensedSequence(
                    this_sequence.Reordering_Approach_LOWEST_INDEX,
                    this_sequence.Reordering_Approach_LOWEST_INDEX,
                    False) 
    Sequences['longestChainOrdered']= this_sequence.BuildLabeledCondensedSequence(
                    this_sequence.Reordering_Approach_LONGEST_CHAIN,
                    this_sequence.Reordering_Approach_LONGEST_CHAIN,
                    False) 
    Sequences['indexOrderedLabeled']= this_sequence.BuildLabeledCondensedSequence(
                    this_sequence.Reordering_Approach_LOWEST_INDEX,
                    this_sequence.Reordering_Approach_LOWEST_INDEX,
                    True) 
    log.debug("Here are the Sequences: " + str(Sequences))
    return Sequences




##  @brief Determine if a sequence is valid
#   @param  sequence - a string
#   @return boolean valid
def checkIsSequenceSane(sequence):
    log.info("~~~ checkIsSequenceSane was called.\n") 
    # ## TODO:  This try-except is a total kluge. 
    # ##  Without it, there is a problem in gmml/swig for bad sequences like:  DManpa1-6-DManpa1-OH
    # ##  The std error:
    # ##        Exception thrown in condensedSequence constructor. Look in the response object.
    # ##  This also goes to std out: 
    # ##        swig/python detected a memory leak of type 'InputOutput::Response *', no destructor found.
    try: 
        this_sequence = gmml.CondensedSequence(sequence) 
        valid = this_sequence.GetIsSequenceOkay()
    except:
        the_response=this_sequence.GetResponse() 
        log.error("Seq is NOT valid.  The following is the response object:")
        log.error(the_response)
        valid=False
    if not valid:
        return valid
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
    except: 
        log.error("Something went wrong while validating this sequence.") 
        log.error("sequence: " + sequence) 
        log.error(traceback.format_exc()) 
        common.settings.appendCommonParserNotice( thisTransaction, 'GmmlError')
        valid = False
    return valid



def main():
    import importlib.util, os, sys
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
    data=utils.JSON_From_Command_Line(sys.argv)




if __name__ == "__main__":
    main()

