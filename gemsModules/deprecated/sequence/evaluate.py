#!/usr/bin/env python3
import gmml
from gemsModules.deprecated.common.loggingConfig import loggers, createLogger
from gemsModules.deprecated.common.settings import generateCommonParserNotice
from gemsModules.deprecated.sequence import io as sequenceio

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

# I think if we got all the names to match, we could use parse_object_as instead of this. OG.
# Probably it would fail on sub-classes though, but maybe.
## if gmml returned a properly json-formatted string it should all work fine.  BLF.


def getLinkageOptionsFromGmmlcbBuilder(sequence):
    # log.info("getLinkageOptionsFromGmmlcbBuilder() was called.\n")
    # log.debug("sequence: " + sequence)
    from gemsModules.deprecated.sequence import build
    cbBuilder = build.getCbBuilderForSequence(sequence)
    gmmllinkageOptionsVector = cbBuilder.GenerateUserOptionsDataStruct()
    # log.debug("gmmllinkageOptionsVector: " + repr(gmmllinkageOptionsVector))

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

    # log.debug("gemsLinkageGeometryOptions: " +
    #           repr(gemsLinkageGeometryOptions))
    return gemsLinkageGeometryOptions


def get_index_ordered_sequene(validatedSequence: str):
    log.info("get_index_ordered_sequence() was called.\n")
    # ##
    # ##  This function assumes that the validity of the sequence was determined elsewhere
    # ##
    this_sequence = gmml.Sequence(validatedSequence)
    return this_sequence.getIndexOrdered()


# @brief Pass a sequence, get linkage options.
#   @param  str sequence
#   @return dict sequences
def getSequenceVariants(validatedSequence: str):
    # log.info("getSequenceVariants() was called.\n")
    # ##
    # ##  This function assumes that the validity of the sequence was determined elsewhere
    # ##
    Sequences = sequenceio.TheSequenceVariants()
    this_sequence = gmml.Sequence(validatedSequence)
    Sequences.userOrdered = this_sequence.getInterpretedSequence()
    Sequences.indexOrdered = this_sequence.getIndexOrdered()
    Sequences.longestChainOrdered = "Currently unavailble in gmml. Request if needed!"
    Sequences.indexOrderedLabeled = this_sequence.getIndexLabeled()
    from gemsModules.deprecated.project.projectUtilPydantic import getSeqIdForSequence
    Sequences.suuid = getSeqIdForSequence(Sequences.indexOrdered)
    # log.debug("Here are the new Sequences: " + str(Sequences))
    return Sequences



