#!/usr/bin/env python3
import gemsModules
import os
import subprocess
import sys
import json
import re
import csv
import ast
import uuid
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import *
from gemsModules.common.loggingConfig import *
from inspect import currentframe, getframeinfo

# if loggers.get(__name__):
#     pass
# else:
# log = createLogger("run_query")


exitMessages = {
        'GmmlNotFound':'Cannot load the GMML module',
        }
exitCodes = {
        'GmmlNotFound':'12345',
        }

# import gems/gmml stuff
import gmml
if gmml is None:
    log.error(exitMessages["GmmlNotFound"])
    sys.exit(exitCodes["GmmlNotFound"])

def buildQueryString(thisTransaction : Transaction):
    """Build a Query String"""
    #
    # THIS IS A KLUGE!   See the [0]?  That's ugly...  and bad.
    # And, if I knew Python better....
    #
    log.debug("buildQueryString() was called")
    try:
        virtLocation = os.getenv('VIRTUOSO_DB') + ":" + str(8890) + "/sparql"
    except Exception as error:
        log.error("Unable to find the Virtuoso Database.  Quitting. " + str(error))
        log.error(traceback.format_exc())
        raise error
    try:
        GemsPath = os.environ.get('GEMSHOME')
    except Exception as error:
        log.error("Unable to find GEMSHOME " + str(error))
        log.error(traceback.format_exc())
        raise error
    debugFileLocation = GemsPath + "/DebugOutput.txt"
    theseOptions = thisTransaction.request_dict['services'][0]['formQueryString']['options']
    if theseOptions['queryType'] == "Initial":
        log.debug(theseOptions)
        log.debug("Printing the aglycon part:")
        log.debug(theseOptions['aglycon'])
        if theseOptions['aglycon'] == 'None':
            theseOptions['aglycon'] = ""
        temp = gmml.Assembly()
        theQueryString = temp.QueryOntology(
                str(theseOptions['searchType']),
                str(theseOptions['searchTerm']),
                float(theseOptions['resolution_min']),
                float(theseOptions['resolution_max']),
                float(theseOptions['b_factor_min']),
                float(theseOptions['b_factor_max']),
                float(theseOptions['oligo_b_factor_min']),
                float(theseOptions['oligo_b_factor_max']),
                int(theseOptions['isError']),
                int(theseOptions['isWarning']),
                int(theseOptions['isComment']),
                int(theseOptions['isLigand']),
                int(theseOptions['isGlycomimetic']),
                int(theseOptions['isNucleotide']),
                str(theseOptions['aglycon']),
                str(theseOptions['count']),
                int(theseOptions['page']),
                int(theseOptions['resultsPerPage']),
                str(theseOptions['sortBy']),
                str(virtLocation),
                str(theseOptions['output_file_type'])
                )
        log.debug(theQueryString)
    elif theseOptions['queryType'] == "More":
        temp = gmml.Assembly()
        theQueryString = temp.MoreQuery(
                str(theseOptions['pdb_id']),
                str(theseOptions['oligo_sequence']),
                str(theseOptions['oligo']),
                str(virtLocation),
                str(theseOptions['output_file_type'])
                )
    elif theseOptions['queryType'] == "Download_All":
       #Do something here
       log.debug("Running Download request for all data")
       temp = gmml.Assembly()
       log.debug("About to run ontologyDownload")
       theQueryString = temp.ontologyDownload(
               str(theseOptions['searchType']),
               str(theseOptions['searchTerm']),
               float(theseOptions['resolution_min']),
               float(theseOptions['resolution_max']),
               float(theseOptions['b_factor_min']),
               float(theseOptions['b_factor_max']),
               float(theseOptions['oligo_b_factor_min']),
               float(theseOptions['oligo_b_factor_max']),
               int(theseOptions['isError']),
               int(theseOptions['isWarning']),
               int(theseOptions['isComment']),
               int(theseOptions['isLigand']),
               int(theseOptions['isGlycomimetic']),
               int(theseOptions['isNucleotide']),
               str(theseOptions['aglycon']),
               str(theseOptions['count']),
               int(theseOptions['page']),
               int(theseOptions['resultsPerPage']),
               str(theseOptions['sortBy']),
               str(virtLocation),
               str(theseOptions['output_file_type'])
               )
       log.debug("Ran ontologyDownload")
    elif str(theseOptions['queryType'] == "Download_List"):
        log.debug("Running Download request for PDB list")
        # log.debug(theseOptions)
        # log.debug("Printing the aglycon part:")
        # log.debug(theseOptions['aglycon'])
        if theseOptions['aglycon'] == 'None':
            theseOptions['aglycon'] = ""
        temp = gmml.Assembly()
        log.debug("About to run ontologyPDBDownload")
        theQueryString = temp.ontologyPDBDownload(
                    str(theseOptions['searchType']),
                    str(theseOptions['searchTerm']),
                    float(theseOptions['resolution_min']),
                    float(theseOptions['resolution_max']),
                    float(theseOptions['b_factor_min']),
                    float(theseOptions['b_factor_max']),
                    float(theseOptions['oligo_b_factor_min']),
                    float(theseOptions['oligo_b_factor_max']),
                    int(theseOptions['isError']),
                    int(theseOptions['isWarning']),
                    int(theseOptions['isComment']),
                    int(theseOptions['isLigand']),
                    int(theseOptions['isGlycomimetic']),
                    int(theseOptions['isNucleotide']),
                    str(theseOptions['aglycon']),
                    str(theseOptions['count']),
                    int(theseOptions['page']),
                    int(theseOptions['resultsPerPage']),
                    str(theseOptions['sortBy']),
                    str(virtLocation),
                    str(theseOptions['output_file_type'])
                    )
        log.debug("Ran ontologyDownload")
        # log.debug(theQueryString)
        #Popen stays in process.  Look up sytem call instead.



    if ((theseOptions['queryType'] == "Download_All") or (theseOptions['queryType'] == "Download_List")):
        #Deal with writing a file and creating/returning the PUUID
        pUUID = str(uuid.uuid4())
        log.debug(pUUID)
        theQueryString = theQueryString + " > /website/userdata/tools/gf/" + pUUID + "." + theseOptions['output_file_type'] + " 2>&1 &"
        #".out 2>&1 && cp /website/userdata/tools/gf/" + pUUID + ".out /website/userdata/tools/gf/" + pUUID + "." + theseOptions['output_file_type'] + " 2>&1 &"
        log.debug(str(theQueryString))
        subprocess.Popen(theQueryString, shell=True, stdin=None, stdout=None, stderr=None)
        log.debug(pUUID)
        pUUID_JSON = "{\"puuid\": \"" + pUUID + "\"}"
        thisTransaction.outgoing_string = pUUID_JSON
        jsonObj = json.loads(pUUID_JSON)
        thisTransaction.response_dict= jsonObj
    else:
        proc = subprocess.Popen(theQueryString, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log.debug("HEY LOOK AT ME")
        log.debug(theQueryString)
        (out, err) = proc.communicate()
        out = str(out.decode('utf-8'))
        log.debug(out)
        gmml.log(getframeinfo(currentframe()).lineno, getframeinfo(currentframe()).filename, gmml.INF, str(out), GemsPath + "/queryLog.txt")
        # text_file = open(debugFileLocation, "a+")
        # text_file.write(str(out))
        # text_file.write(str(theQueryString))
        # text_file.close()
        #variable out contains results of curl command that returns some unnecessary information about curl version at the begginging
        #to avoid that we consider result string starting from '{'
        # startIndex = out.index('{')
        # out = out[startIndex:]
        # out = "\"" + out + "\""
        # log.debug(out)

        jsonObj = json.loads(out)
        thisTransaction.response_dict= jsonObj
        thisTransaction.outgoing_string= json.dumps(jsonObj)
