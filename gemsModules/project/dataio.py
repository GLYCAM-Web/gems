#!/usr/bin/env python3
import  os, sys
import json
import uuid
from datetime import datetime
from gemsModules.common.transaction import *
from gemsModules.project import settings as projectSettings
from pydantic import BaseModel, Field
from pydantic.schema import schema
from gemsModules.common.loggingConfig import *
import traceback

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


##  @brief The primary way of tracking data related to a project
#   @detail This is the generic project object. See subtypes for more specific fields
##TODO: Add this class signature back in when ready for pydantic validation.
#class GemsProject(BaseModel):
class GemsProject():
    ## The name of the output dir is the pUUID
    pUUID : str = None
    timestamp : datetime = None

    title : str = None
    comment : str = None
    
    

    ## The project path. Used to be output dir, but now that is reserved for subdirs.
    project_dir : str = None
    requesting_agent : str = None
    has_input_files : bool = False
    gems_version : str = None
    gems_branch : str = None
    gmml_version : str = None
    gmml_branch : str = None
    site_mode : str = None
    site_host_name : str = None
    force_field : str = None
    parameter_version : str = None
    amber_version : str = None
    json_api_version : str = None
    
    project_type : str = None

    def __init__(self, thisTransaction : Transaction):
        log.info("GemsProject.__init__() was called.")
        request = thisTransaction.request_dict
        log.debug("request: " + str(request))
        if 'project' in request.keys():
            log.debug("found a project in the request.")
            fe_project = request['project']

            ## Random uuid for the project uuid.
            self.pUUID = str(uuid.uuid4())
            self.timestamp = datetime.now()
            
            if 'title' in fe_project.keys():
                self.title = fe_project['title']
            if 'comment' in fe_project.keys():
                self.comment = fe_project['comment']
            if 'type' in fe_project.keys():
                self.project_type = fe_project['project_type']
            if 'requesting_agent' in fe_project.keys():
                self.requesting_agent = fe_project['requesting_agent']
            if 'gems_version' in fe_project.keys():
                self.gems_version = fe_project['gems_version']
            if 'gems_branch' in fe_project.keys():
                self.gems_branch = fe_project['gems_branch']
            if 'gmml_version' in fe_project.keys():
                self.gmml_version = fe_project['gmml_version']
            if 'gmml_branch' in fe_project.keys():
                self.gmml_branch = fe_project['gmml_branch']
            if 'site_mode' in fe_project.keys():
                self.site_mode = fe_project['site_mode']
            if 'site_host_name' in fe_project.keys():
                self.site_host_name = fe_project['site_host_name']
            if 'force_field' in fe_project.keys():
                self.force_field = fe_project['force_field']
            if 'parameter_version' in fe_project.keys():
                self.parameter_version =  fe_project['parameter_version']
            if 'amber_version' in fe_project.keys():
                self.amber_version = fe_project['amber_version']
            if 'json_api_version' in fe_project.keys():
                self.json_api_version = fe_project['json_api_version']
                
            



## @brief cbProject is a typed project that inherits all the fields from GemsProject and adds its own.
#   
class CbProject(GemsProject):
    sequence : str = None
    seqUUID : str = None
    structure_count : int = 1
    structure_mappings : []
    

## Details and location of the build of a single pose of a structure.
class StructureMapping():
    ##  Path to the dir that holds this build. 
    #   May or may not be in this project dir.
    structure_path : str = None
    ion : str = "No"
    solvation : str = "No"
    solvation_size : str = None
    solvation_distance : str = None
    splvation_shape : str = "REC"
    timestamp : str = None

##  Figures out the type of structure file being preprocessed.
def getStructureFileProjectType(request):
    projectType = "not set"
    services = request['entity']['services']
    for service in services:
        if 'Preprocess' in service.keys():
            if 'type' in service['Preprocess'].keys():
                if 'PreprocessPdbForAmber' == service['Preprocess']['type']:
                    projectType = "pdb"

    return projectType

##TODO: pydantic homework when model has settled down.

# def generateGemsProjectSchema():
#     print(GemsProject.schema_json(indent=2))

if __name__ == "__main__":
    generateGemsProjectSchema()
