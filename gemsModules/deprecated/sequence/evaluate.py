#!/usr/bin/env python3
import json
import sys
import os
import re
import importlib.util
import shutil
import uuid
import gemsModules.deprecated
import gmml
import traceback
import gemsModules.deprecated.common.utils
from gemsModules.deprecated.project import projectUtilPydantic as projectUtils
from gemsModules.deprecated.project import settings as projectSettings
from gemsModules.deprecated.common import io as commonio
from gemsModules.deprecated.common import logic as commonlogic
from gemsModules.deprecated.common import services as commonservices
from gemsModules.deprecated.common.loggingConfig import loggers, createLogger
from gemsModules.deprecated.common.settings import generateCommonParserNotice
from gemsModules.deprecated.sequence import io as sequenceio
from gemsModules.deprecated.sequence import settings as sequenceSettings
from gemsModules.deprecated.sequence import io as sequencelogic

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

# I think if we got all the names to match, we could use parse_object_as instead of this. OG.
# Probably it would fail on sub-classes though, but maybe.


def getLinkageOptionsFromGmmlcbBuilder(sequence):
    log.info("getLinkageOptionsFromGmmlcbBuilder() was called.\n")
    log.debug("sequence: " + sequence)
    from gemsModules.deprecated.sequence import build
    cbBuilder = build.getCbBuilderForSequence(sequence)
    gmmllinkageOptionsVector = cbBuilder.GenerateUserOptionsDataStruct()
    log.debug("gmmllinkageOptionsVector: " + repr(gmmllinkageOptionsVector))

    gemsLinkageGeometryOptions = sequenceio.AllLinkageRotamerInfo()
    gemsLinkageGeometryOptions.totalPossibleRotamers = cbBuilder.GetNumberOfShapes()
    likelyOnly = True
    gemsLinkageGeometryOptions.totalLikelyRotamers = cbBuilder.GetNumberOfShapes(
        likelyOnly)

    for gmmlLinkageOptions in gmmllinkageOptionsVector:

        gemsLinkageOptions = sequenceio.SingleLinkageRotamerData()

        gemsLinkageOptions.indexOrderedLabel = gmmlLinkageOptions.indexOrderedLabel_
        gemsLinkageOptions.linkageName = gmmlLinkageOptions.linkageName_
        gemsLinkageOptions.firstResidueNumber = gmmlLinkageOptions.firstResidueNumber_
        gemsLinkageOptions.secondResidueNumber = gmmlLinkageOptions.secondResidueNumber_

        """ Likely Rotamers """
        for dihedralOptions in gmmlLinkageOptions.likelyRotamers_:
            gemsRotamers = sequenceio.TheRotamerDihedralInfo()
            gemsRotamers.dihedralName = dihedralOptions.dihedralName_

            for rotamer in dihedralOptions.rotamers_:
                gemsRotamers.dihedralValues.extend([rotamer])

            gemsLinkageOptions.likelyRotamers.append(gemsRotamers)

        """ Possible Rotamers """
        for dihedralOptions in gmmlLinkageOptions.possibleRotamers_:
            gemsRotamers = sequenceio.TheRotamerDihedralInfo()
            gemsRotamers.dihedralName = dihedralOptions.dihedralName_

            for rotamer in dihedralOptions.rotamers_:
                gemsRotamers.dihedralValues.extend([rotamer])

            gemsLinkageOptions.possibleRotamers.append(gemsRotamers)

            # dihedralsWithOptions Needed for the website
            gemsLinkageOptions.dihedralsWithOptions.append(
                gemsRotamers.dihedralName)

        gemsLinkageGeometryOptions.singleLinkageRotamerDataList.append(
            gemsLinkageOptions)

    log.debug("gemsLinkageGeometryOptions: " +
              repr(gemsLinkageGeometryOptions))
    return gemsLinkageGeometryOptions


# @brief Pass a sequence, get linkage options.
#   @param  str sequence
#   @return dict sequences
def getSequenceVariants(validatedSequence: str):
    log.info("getSequenceVariants() was called.\n")
    #this_sequence = gmml.CondensedSequence(validatedSequence)
    # ##
    # ##  This function assumes that the validity of the sequence was determined elsewhere
    # ##
    Sequences = sequenceio.TheSequenceVariants()
    # #Sequences.userOrdered = validatedSequence
    this_sequence = gmml.Sequence(validatedSequence)
    Sequences.userOrdered = this_sequence.getInterpretedSequence()
    Sequences.indexOrdered = this_sequence.getIndexOrdered()
    Sequences.longestChainOrdered = "Currently unavailble in gmml. Request if needed!"
    Sequences.indexOrderedLabeled = this_sequence.getIndexLabeled()
    log.debug("Here are the new Sequences: " + str(Sequences))

    # this_sequence = gmml.CondensedSequence(validatedSequence)
    # Sequences.userOrdered = validatedSequence
    # Sequences.indexOrdered = this_sequence.BuildLabeledCondensedSequence(this_sequence.Reordering_Approach_LOWEST_INDEX, this_sequence.Reordering_Approach_LOWEST_INDEX, False)
    # Sequences.longestChainOrdered = this_sequence.BuildLabeledCondensedSequence(this_sequence.Reordering_Approach_LONGEST_CHAIN, this_sequence.Reordering_Approach_LONGEST_CHAIN, False)
    # Sequences.indexOrderedLabeled = this_sequence.BuildLabeledCondensedSequence(this_sequence.Reordering_Approach_LOWEST_INDEX, this_sequence.Reordering_Approach_LOWEST_INDEX, True)
    #log.debug("Here are the old Sequences: " + str(Sequences))
    return Sequences


# @brief Determine if a sequence is valid
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
        the_response = this_sequence.GetResponse()
        log.error("Seq is NOT valid.  The following is the response object:")
        log.error(the_response)
        valid = False
    if not valid:
        return valid
    log.debug("getting prepResidues.")
    # Get prep residues
    prepResidues = gmml.condensedsequence_glycam06_residue_tree()
    log.debug("Instantiating an assembly.")
    # Create an assembly
    assembly = gmml.Assembly()
    try:
        log.debug("Checking sequence sanity.")
        # Call assembly.CheckCondensed sequence sanity.
        valid = assembly.CheckCondensedSequenceSanity(sequence, prepResidues)
        log.debug("validation result: " + str(valid))
    except:
        log.error("Something went wrong while validating this sequence.")
        log.error("sequence: " + sequence)
        log.error(traceback.format_exc())
        generateCommonParserNotice(noticeBrief='GmmlError')
        valid = False
    return valid


def main():
    import importlib.util
    import os
    import sys
    if importlib.util.find_spec("deprecated") is None:
        this_dir, this_filename = os.path.split(__file__)
        sys.path.append(this_dir + "/../")
        if importlib.util.find_spec("common") is None:
            print("Something went horribly wrong.  No clue what to do.")
            return
        else:
            from common import utils
    else:
        from gemsModules.deprecated.common import utils
    data = utils.JSON_From_Command_Line(sys.argv)


if __name__ == "__main__":
    main()
