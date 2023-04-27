amberSubmissionJson = '{ \
"molecularSystemType":"Glycan", \
"molecularModelingJobType":"Prep_and_Minimization", \
"jobID":"' + pUUID + '", \
"localWorkingDirectory":"' + outputDirPath + '", \
"comment":"initiated by gemsModules/sequence"\
}'
log.debug(amberSubmissionJson)
from gemsModules.deprecated.mmservice.amber.amber import manageIncomingString
# Using multiprocessing for this function call.
manageIncomingString(amberSubmissionJson)
return gmmlConformerInfo

