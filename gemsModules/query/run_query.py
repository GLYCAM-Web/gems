#!/usr/bin/env python3
import gemsModules
import os
import subprocess
import sys
import json
import re
import csv
import ast
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import *

exitMessages = {
        'GmmlNotFound':'Cannot load the GMML module',
        }
exitCodes = {
        'GmmlNotFound':'12345',
        }

# import gems/gmml stuff
import gmml
if gmml is None:
    print(exitMessages["GmmlNotFound"])
    sys.exit(exitCodes["GmmlNotFound"])

def buildQueryString(thisTransaction : Transaction):
    """Build a Query String"""
    #
    # THIS IS A KLUGE!   See the [0]?  That's ugly...  and bad.
    # And, if I knew Python better....
    #
    try:
        virtLocation = os.getenv('VIRTUOSO_DB') + ":" + str(8890) + "/sparql"
    except:
        print("Unable to find the Virtuoso Database.  Quitting.")
        sys.exit(1)
    theseOptions = thisTransaction.transaction_in['services'][0]['formQueryString']['options']
    if theseOptions['queryType'] == "Initial":
        print(theseOptions)
        print("Printing the aglycon part:")
        print(theseOptions['aglycon'])
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
    elif theseOptions['queryType'] == "More":
        temp = gmml.Assembly()
        theQueryString = temp.MoreQuery(
                str(theseOptions['pdb_id']),
                str(theseOptions['oligo_sequence']),
                str(theseOptions['oligo']),
                str(virtLocation),
                str(theseOptions['output_file_type'])
                )
    elif theseOptions['queryType'] == "Download_List":
       #Do something here
      log.debug("Running Download request for PDB list") 
        
    elif theseOptions['queryType'] == "Download_All":
        log.debug("Running Download request for all data")
        
    proc = subprocess.Popen(theQueryString, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(theQueryString)
    (out, err) = proc.communicate()
    out = str(out.decode('utf-8'))
    #variable out contains results of curl command that returns some unnecessary information about curl version at the begginging
    #to avoid that we consider result string starting from '{'
    startIndex = out.index('{')
    out = out[startIndex:]
    # out = "\"" + out + "\""
    print(out)
    jsonObj = json.loads(out)
    thisTransaction.response_dict= jsonObj
