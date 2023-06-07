#!/usr/bin/env python3
import gemsModules.deprecated
import os
import subprocess
import sys
import json
import re
import csv
import ast
import uuid
from gemsModules.deprecated import common
from gemsModules.deprecated.common.services import *
from gemsModules.deprecated.common.transaction import *
from gemsModules.deprecated.common.loggingConfig import *
from inspect import currentframe, getframeinfo
from gemsModules.deprecated.query import plotlyChiEnergy
# from . import plotlyChiEnergy

if loggers.get(__name__):
    pass
else:
  log = createLogger("run_query")


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
    # """Build a Query String"""
    #
    # THIS IS A KLUGE!   See the [0]?  That's ugly...  and bad.
    # And, if I knew Python better....
    #
    log.info("buildQueryString() was called")
    
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
        log.debug("More query")
        temp = gmml.Assembly()
        theQueryString = temp.MoreQuery(
                str(theseOptions['pdb_id']),
                str(theseOptions['oligo_sequence']),
                str(theseOptions['oligo']),
                str(virtLocation),
                str(theseOptions['output_file_type'])
                )
        log.debug(theQueryString)
        
    elif theseOptions['queryType'] == "plotlyCHI":
      log.debug("plotlyCHI query")
      log.debug("oligo: " + str(theseOptions['oligo']))
      try:
        theQueryString = plotlyChiEnergy.createLinkagesQuery(str(theseOptions['oligo']))
      except Exception as error:
        log.error("Unable to generate CHI Energy queries. " + str(error))
        log.error(traceback.format_exc())
        raise error       
      # log.debug(theQueryString)
      proc = subprocess.Popen(theQueryString, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      (out, err) = proc.communicate()
      out = str(out.decode('utf-8'))
      # log.debug(out)
      linkageJson = json.loads(out)
      log.debug(linkageJson)
      
      for link in linkageJson["results"]["bindings"]:
        cmd = "python3 " + GemsPath + "/gemsModules/deprecated/query/generatePlotlyDivs.py " + str(theseOptions['oligo']) + " " + str(link["LinkageID"]["value"]) + " &"
        log.debug(cmd)
        try:
          p = subprocess.run(cmd, shell=True)
        except Exception as error:
          log.error("Unable to generate Plotly Divs. " + str(error))
          link["plotlyJobSubmitted"] = "False"
        else:
          # (out, err) = p.communicate()
          # out = str(out.decode('utf-8'))
          # log.debug(out)
          link["LinkageName"]["value"] = str(link["LinkageName"]["value"]).replace('_?_?_1', '')
          link["LinkageID"]["plotlyJobSubmitted"] = "True"
          
      jsonObj = linkageJson
      
        
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
    else:
      log.error("Unknown query type: " + str(theseOptions['queryType']))




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
      # thisTransaction.outgoing_string = pUUID_JSON
      jsonObj = json.loads(pUUID_JSON)
      # thisTransaction.response_dict= jsonObj
    elif theseOptions['queryType'] != "plotlyCHI":
    #   log.debug(theQueryString)
      proc = subprocess.Popen(theQueryString, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      (out, err) = proc.communicate()
      out = str(out.decode('utf-8'))
      log.debug(out)
      jsonObj = json.loads(out)
            
      
      
    thisTransaction.response_dict= jsonObj
    thisTransaction.outgoing_string= json.dumps(jsonObj)
