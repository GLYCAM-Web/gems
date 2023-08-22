#!/usr/bin/env python3

import gemsModules.deprecated
from gemsModules.deprecated import common
from gemsModules.deprecated.common.services import *
from gemsModules.deprecated.common.transaction import *
from gemsModules.deprecated.common.loggingConfig import *

#Imports for Utilities
import json
import csv
import re
import os
import subprocess
import sys
import traceback

#Imports for plots
import numpy
import plotly.express as px
import plotly.io
import pandas
import plotly.graph_objects as go

if loggers.get(__name__):
    pass
else:
  log = createLogger(__name__)
  



def createLinkagesQuery(oligoID):
    
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
  
  
  log.info("Getting all of the Linkages") 
  
  
  prefixString = ( \
    "curl -g -s -H "
    "\'Accept: application/json\' " 
    + virtLocation + " "
    "--data-urlencode query=\' "
  )  
  sourcesString = ( \
    "PREFIX : <http://gmmo.uga.edu/#>\n"
    "PREFIX gmmo: <http://gmmo.uga.edu/#>\n"
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
    "PREFIX owl: <http://www.w3.org/2002/07/owl#>\n"
    "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
    "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n\n"
  )
  
  selectString = ("SELECT (STRAFTER(str(?glycoLink), \"#\") AS ?LinkageID)\n"
                + "?LinkageName\n"               
  )
  
  queryLogicString = ( "WHERE\n"
      "{\n"
      "  :"+  oligoID + " :hasGlycosidicLinkage ?glycoLink.\n"
      "  ?glycoLink  :residueLinkage     ?LinkageName.\n"
      "}\n"
  )
  
  suffixString = "\'"
  
  queryString = prefixString + sourcesString + selectString + queryLogicString + suffixString
  
  log.debug("queryString: \n" + queryString)
  
  
  return queryString
    
  
def createPlotlyQuery(oligoID, linkage):
    
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
  # Create a query to get the linkages and their information
  # This query will be used to create the plotly html figures
  
  # oligoID should be in the format PDBID_oligoN, ie 2dw2_oligo1
  
  
  #########################################################
  ## This was hacked together to get done in time for a  ##
  ## presentation.  It is not a good way to do this.     ##
  ## Please don't use it as a guide.                     ##
  #########################################################
  
  # TODO: Move this where it belongs, fix it, and clean it up.
  
  log.info("createPlotlyQuery() was called")
    
  queryString = ""
  
  prefixString = ( \
    "curl -g -s -H "
    "\'Accept: application/json\' " 
    + virtLocation + " "
    "--data-urlencode query=\' "
  )  
  sourcesString = ( \
    "PREFIX : <http://gmmo.uga.edu/#>\n"
    "PREFIX gmmo: <http://gmmo.uga.edu/#>\n"
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
    "PREFIX owl: <http://www.w3.org/2002/07/owl#>\n"
    "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
    "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n\n"
  )
  selectString = ( \
    "SELECT DISTINCT\n"
    "  ?Linkage\n"
    "  ?oligoResidueLinks\n"
    # "  ?LinkageName\n"
    "  ?LinkageResidueNames\n\n"
    
    "  (xsd:float(?Phi) as ?phi)\n" 
    "  (xsd:float(?Psi) as ?psi)\n\n"
      
    "  (xsd:float(?totalCHIEnergy) as ?TotalCHIEnergy)\n"
    "  (xsd:decimal(?phiCHIFunction) as ?PhiCHIFunction)\n"
    "  (xsd:decimal(?psiCHIFunction) as ?PsiCHIFunction)\n\n"
      
    "  ?mono1ID ?mono1BFMP\n"
    "  ?mono2ID ?mono2BFMP\n"
  )
  queryLogicString = ( \
    "WHERE\n"
    "{\n"
    "  :" + oligoID + "\n"
    "    :hasGlycosidicLinkage :" + linkage + ".\n"
    "  :" + oligoID + "\n"
    "    :oligoResidueLinks ?oligoResidueLinks;\n"
    "    :hasMono ?mono1;\n"
    "    :hasMono ?mono2.\n"
    "  :" + linkage + "\n"
    "    :hasParentMono              ?mono2;\n"
    "    :hasChildMono          ?mono1;\n"
    "    :residueLinkage     ?LinkageResidueNames;\n"
    "    :glycosidicLinkage            ?Linkage;\n"
    "    :phiCHIFunction         ?phiCHIFunction;\n"
    "    :psiCHIFunction         ?psiCHIFunction;\n"
    "    :hasPhiAngle          ?Phi;\n"
    "    :hasPsiAngle          ?Psi;\n"
    "    :totalCHIEnergy         ?totalCHIEnergy.\n\n"
    "  ?mono1\n"
    "    :identifier ?mono1ID;\n"
    "    :BFMP ?mono1BFMP;\n"
    "    :isNucleotide false.\n"
    "  ?mono2\n"
    "    :identifier ?mono2ID;\n"
    "    :BFMP ?mono2BFMP;\n"
    "    :isNucleotide false.\n\n"
    "}\n"
  )
  suffixString = "\'"
  
  queryString = prefixString + sourcesString + selectString + queryLogicString + suffixString
  
  log.debug("queryString: \n" + queryString)
  
  return queryString
  

def generatePlotlyHTML(linkageJson, linkage, writeToFile=False):
  # linkageJson should be a single linkage and its information 
  # in json format, returned by submitting the queryString from
  # createPlotlyQuery to virtuoso
  try:
      GemsPath = os.environ.get('GEMSHOME')
  except Exception as error:
      log.error("Unable to find GEMSHOME " + str(error))
      log.error(traceback.format_exc())
      raise error
  log.info("generatePlotlyHTML() was called")
  try:
    log.debug("linkageJson")
    log.debug(linkageJson["results"]["bindings"][0])
  except Exception as error:
    log.error("Error: " + str(error))
    raise error
  
  plotDataFilePath = GemsPath + "/gemsModules/deprecated/query/chiEnergyData/"
  
  #This is just one but it's easier to leave for now
  for link in linkageJson["results"]["bindings"]:
    phiFunction = link["PhiCHIFunction"]["value"]
    psiFunction = link["PsiCHIFunction"]["value"]
    
    referenceFigure = "Phi" + str(phiFunction) + "xPsi" + str(psiFunction) + ".csv"
    
    filePath = plotDataFilePath + referenceFigure
    with open(filePath) as path:
      contourData = numpy.loadtxt(path, delimiter=",")

    xTitle = (
      '<span style="font-size: 36px;">'
        'Φ'
        '<span style="font-size: 24px;">'
          '<sub>CHI function ' + str(phiFunction) + '</sub>'
        '</span>'
      '</span>'
    )
    yTitle = (
      '<span style="font-size: 36px;">'
        'Ψ'
        '<span style="font-size: 24px;">'
          '<sub>CHI function ' + str(psiFunction) + '</sub>'
        '</span>'
      '</span>'
    )
    
    fig = go.Figure(data =
      go.Contour(
        z=contourData,
        x=list(range(0,360)),
        dx=30,
        y=list(range(0,360)),
        dy=30,
        colorscale='RdBu_r',
        contours=dict(
          showlabels = True,
          start = 0,
          end = numpy.max(contourData),
          size = 1
        ),
        colorbar=dict(
          title='CHI Energy [kcal/mol]',
          titleside='right',
          titlefont=dict(
            size=26,
            family='Arial, sans-serif'),
        ),
        hoverinfo="skip"
      )
    )
    fig.update_xaxes(
      title_text=xTitle,
      # domain=(0.1, 0.9),
      constrain="domain",
      range=[0,360],
      tick0=0,
      dtick=30,
      ticks="outside",
      titlefont=dict(
        size=36,
        family='Arial, sans-serif'
      )
      )
    fig.update_yaxes(
      title_text=yTitle,
      # domain=(0.1, 0.9),
      constrain="domain",
      range=[0,360],
      scaleanchor = "x",
      scaleratio = 1,
      tick0=0,
      dtick=30,
      ticks="outside",
      titlefont=dict(
        size=36,
        family='Arial, sans-serif'
      )
    )
    # Create title to show residue name, number, and chain
    # Ex linkageResidueNames: GCD_B_2_?_?_1 (1-3) NG6_B_1_?_?_1
    titleStr = (
        linkage.split('_oligo')[0].upper() + "<br><sup>" 
        + str(link["LinkageResidueNames"]["value"]).split('_')[0] + "_"
        + str(link["LinkageResidueNames"]["value"]).split('_')[1] + "_"
        + str(link["LinkageResidueNames"]["value"]).split('_')[2] + " "
        + str(link["LinkageResidueNames"]["value"]).split(' ')[1] + " "
        + str(link["LinkageResidueNames"]["value"]).split(' ')[2].split('_')[0] + "_"
        + str(link["LinkageResidueNames"]["value"]).split(' ')[2].split('_')[1] + "_"
        + str(link["LinkageResidueNames"]["value"]).split(' ')[2].split('_')[2] 
        + "</sup>"
    )
    
    
    fig.update_layout(
      #template="plotly_dark",
      title=titleStr,
      title_font=dict(
        size=36,
        family='Arial, sans-serif'
      ),
      title_xanchor="center",
      title_xref="paper",
      title_x=0.5,
      font=dict(
        size=16,
        family='Arial, sans-serif'
      ),
    )
    # log.debug("Phi: " + str(link["phi"]["value"]))
    # log.debug("Psi: " + str(link["psi"]["value"]))
    
    phiNP = numpy.array(float(link["phi"]["value"]))
    psiNP = numpy.array(float(link["psi"]["value"]))
    
    
    hoverText=(linkage + "<br>" \
      # + str(link["LinkageResidueNames"]["value"]).replace('_?_?_1', '') + "<br>" \
      + str(link["LinkageResidueNames"]["value"]) + "<br>" \
      + "CHI Energy: " + str(link["TotalCHIEnergy"]["value"]) + " kcal/mol" + "<br>" \
      + "Φ: " + str(link["phi"]["value"]) + "<br>" \
      + "Ψ: " + str(link["psi"]["value"]) + "<br>" 
    )
    bgColor = "white"
    markerColor = "darkgray"
    markerLineColor = "black"
    
    
    if not re.search(r'4C1',str(link["mono1BFMP"]["value"])):
      hoverText = "<b>WARNING:<br>" + link["mono1ID"]["value"] + " is not in a 4C1 chair conformation" \
                + "<br>" + "CHI Energy functions were not<br>developed for this ring shape!" + "</b>" \
                + "<br>" + hoverText
      bgColor = "gold"
      markerColor = "orange"
      markerLineColor = "red"
      
    if not re.search(r'4C1',str(link["mono2BFMP"]["value"])):
      hoverText = "<b>WARNING:<br>" + link["mono2ID"]["value"] + " is not in a 4C1 chair conformation" \
                + "<br>" + "CHI Energy functions were not<br>developed for this ring shape! " + "</b>" \
                + "<br>" + hoverText
      bgColor = "gold"
      markerColor = "orange"
      markerLineColor = "red"
      
      
    fig.add_trace(go.Scatter(
      # name=link["Linkage"]["value"],
      x=phiNP,
      y=psiNP,
      mode='markers',
      marker=dict(
        size=15, 
        color=markerColor,
        opacity=1,
        line=dict(
          width=2,
          color=markerLineColor,
        ),
        symbol='star-diamond',
      ),
      hovertext=hoverText,
      hoverinfo='text',
    ))
    fig.update_layout(
      hoverlabel=dict(
        bgcolor=bgColor,
        # font_size=16,
      )
    )
    if(writeToFile):
      outputPath = "/website/userdata/tools/gf/"
      outputFileName = outputPath + linkage + "_CHI_Energy_Plot.html"
      divIdName = linkage + "-plotly"
      fig.write_html(outputFileName, full_html=False, include_plotlyjs=False, div_id=divIdName)
    else:
      link['figDiv'] = fig.to_html(full_html=False, include_plotlyjs=False, div_id=divIdName)

  return linkageJson

