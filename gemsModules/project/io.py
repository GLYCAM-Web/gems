#!/usr/bin/env python3
import  os, sys
import json
import uuid
from datetime import datetime
from gemsModules.common import services as commonservices
from gemsModules.project import settings as project_settings
from pydantic import BaseModel, Field, ValidationError
from pydantic.schema import schema
from typing import Any
from gemsModules.common.loggingConfig import *
import traceback

# ## TODO - a lot of this info really belongs elsewhere.  It's not really
#    project information.  For example, 'seqID' only applies to the sequence
#    entity.  In the GP builder, there might be many sequences, but still 
#    only one overall project.  So, one day, clean this up.


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


##  @brief The primary way of tracking data related to a project
#   @detail This is the generic project object. See subtypes for more specific fields
class Project(BaseModel):
    ## The name of the output dir is the pUUID
    pUUID : str = ""
    title : str = ""
    comment : str = ""
    timestamp : datetime = None
    gems_timestamp : datetime = None
    project_type : str = ""

    ## The parent_path can be used to override settings.output_data_dir
    parent_path : str = ""  
    compute_cluster_parent_path : str = ""  
    ## The project path. Used to be output dir, but now that is reserved for subdirs.
    project_dir : str = ""
    requesting_agent : str = ""
    has_input_files : bool = None
    
    gems_version : str = ""
    gems_branch : str = ""
    gmml_version : str = ""
    gmml_branch : str = ""
    site_mode : str = ""
    site_host_name : str = ""
    force_field : str = "default"
    parameter_version : str = "default"
    amber_version : str = "default"
    json_api_version : str = ""
    _django_version : str = ""
    django_project_id : str = ""
    

    def __init__(self, **data : Any):
        super().__init__(**data)

        ## Random uuid for the project uuid if none has been specified
        if self.pUUID is "" : 
            self.pUUID = str(uuid.uuid4()) 
        if self.timestamp is None : 
            self.gems_timestamp = datetime.now()


####### These might need to stay somehow:
####
#            log.debug("Checking for the django_project_id.")
#            if 'id' in project.keys():
#                self.django_project_id = project['id']
#                log.debug("self.django_project_id: " + self.django_project_id)
#            else:
#                log.error("Failed to find the django_project_id!")
#                log.error("project.keys(): "  + str(project.keys()))
#
#
#        else:
#            ##  For doing our best if the request doesn't include a project obj.
#            #   This is where we give defaults for whatever is needed.
#            self.requesting_agent = "command line"
#            log.debug("request entity type: " + request_dict['entity']['type'])
#            if request_dict['entity']['type'] == "Sequence":
#                self.project_type = "cb"
#            elif request_dict['entity']['type'] == "MmService":
#                self.project_type = "md"
#                self.has_input_files = True
#            elif request_dict['entity']['type'] == "Conjugate":
#                self.project_type = "gp"
#            elif request_dict['entity']['type'] == "StructureFile":
#                self.project_type = "pdb"
                

    def __str__(self):
        result = "\nproject:"
        result = result + "\ncomment: " + self.comment
        result = result + "\ntimestamp: " + str(self.timestamp)
        result = result + "\ngems_timestamp: " + str(self.gems_timestamp)
        result = result + "\nproject_type: " + self.project_type
        result = result + "\npUUID: " + self.pUUID
        result = result + "\nrequesting_agent: " + self.requesting_agent
        result = result + "\nhas_input_files: " + str(self.has_input_files)
        result = result + "\ngems_version: "  + self.gems_version
        result = result + "\ngems_branch: "  + self.gems_branch
        result = result + "\ngmml_version: "  + self.gmml_version
        result = result + "\ngmml_branch: "  + self.gmml_branch
        result = result + "\nsite_mode: "  + self.site_mode
        result = result + "\nsite_host_name: "  + self.site_host_name
        result = result + "\nforce_field: "  + self.force_field
        result = result + "\nparameter_version: "  + self.parameter_version
        result = result + "\namber_version: "  + self.amber_version
        result = result + "\njson_api_version: "  + self.json_api_version
        result = result + "\ndjango_project_id: "  + self.django_project_id
        result = result + "\nproject_dir: "  + self.project_dir
        return result

def buildProjectDir(parentPath, projectSubdirectory, pUUID):
    log.info("buildProjecDir() was called.")
    log.debug("parentPath: " + parentPath)
    log.debug("projectSubdirectory: " + projectSubdirectory)
    log.debug("pUUID: " + pUUID)
    # fun fact - os.path.join isn't very useful if your strings contain forward slashes.
    #            one day, we should make this more OS-independent.  But... not now.
    return os.path.join(parentPath,  projectSubdirectory, "git-ignore-me_userdata/Builds", pUUID )

## @brief cbProject is a typed project that inherits all the fields from project and adds 
#   its own.
class CbProject(Project):

    def __init__(self, **data : Any):
        super().__init__(**data)
        log.info("CbProject.__init__() was called.")
        self.project_type = "cb"


    def startMeUp(self, thisTransaction) :
        from gemsModules.project.projectUtil import getSequenceFromTransaction, getSeqIDForSequence
        self.has_input_files = False

        transIn = thisTransaction.transaction_in

#        self.sequence = thisTransaction.getInputSequencePayload()
#        if self.sequence is None :
#            raise AttributeError("Sequence")

#        self.seqID = getSeqIDForSequence(self.sequence) # poorly named, not indexOrdered version!
#        log.debug("self.seqID in CbProject.startMeUp is : >>>" + self.seqID + "<<<")
        log.debug("self.project_type in CbProject.startMeUp is : >>>" + self.project_type + "<<<")
#        log.debug("self.sequence in CbProject.startMeUp is : >>>" + self.sequence + "<<<")

        self.setParentPath(thisTransaction)
        if transIn.project is not None :
            if transIn.project.project_dir is not None  :
                if transIn.project.project_dir is not "" :
                    self.project_dir = transIn.project.project_dir
        if self.project_dir is None :
            self.project_dir =  buildProjectDir(self.parentPath, project_settings.project_subdirectory[self.project_type] , self.pUUID)
        if self.project_dir is  "" :
            self.project_dir =  buildProjectDir(self.parentPath, project_settings.project_subdirectory[self.project_type] , self.pUUID)
        log.debug("self.project_dir in CbProject.startMeUp is : >>>" + self.project_dir + "<<<")

    def setParentPath(self, thisTransaction, specifiedPath=None):
        # allow for direct setting of project dir
        if specifiedPath is not None :
            log.debug("Setting parent_path to specified path : " + specifiedPath)
            self.parent_path = specifiedPath
            return
        # if it wasn't directly specified, see if it can be found in the incoming transaction
        projectIn = thisTransaction.getProjectIn()
        if all(v is not None for v in [ 
            projectIn,
            projectIN.parent_path
            ]):
            if projectIn.parent_path != "" :
                message="Using the project directory specified in the incoming transaction." 
                log.debug(message) 
                projectOut.parent_path = projectIn.parent_path 
                return
    
        message="There is no incoming or specified project information.  Setting project parent_path internally."
        log.debug(message)
    
        GEMS_PARENT_PATH = os.environ.get('GEMS_PARENT_PATH')
        if GEMS_PARENT_PATH is None :
            theParentPath = project_settings.output_data_dir
        elif GEMS_PARENT_PATH == "" :
            theParentPath = project_settings.output_data_dir
        else :
            theParentPath = GEMS_PARENT_PATH
    
        if theParentPath is None :
            message="Unknown error trying to set project ParentPath."
            log.error(message)
            thisTransaction.generateCommonParserNotice(
                    noticeBrief='GemsError',
                    messagingEntity=settings.WhoIAm,
                    additionalInfo={'hint':message})
            return
    
        log.debug("Setting outgoing project ParentPath to : " + theParentPath)
        projectOut.parent_path = theParentPath
        return


    def __str__(self):
        result = super().__str__()
        result = result + "\nproject_type: " + self.project_type
#        result = result + "\nsequence: " + self.sequence
#        result = result + "\nseqID: " + self.seqID
#        result = result + "\nstructure_count: " + str(self.structure_count)
        #result = result + "\nstructure_mappings: " + str(self.structure_mappings)
        return result

class PdbProject(Project):
    uploaded_file_name : str = ""
    status : str = ""
    u_uuid : str = ""
    upload_path : str = ""
    pdb_id : str = ""
    input_source : str = ""

    def __init__(self, **data : Any):
        super().__init__(**data)

#    def __init__(self, request_dict: dict):
#        super().__init__(request_dict)
#        from gemsModules.structureFile.amber.logic import getPdbRequestInput
#        log.info("PdbProject.__init__() was called.")
#        self.project_type = "pdb"
#        self.has_input_files = True
#        self.uploaded_file_name = getPdbRequestInput(request_dict)
#        log.debug("uploaded_file_name: " + self.uploaded_file_name)
#        self.status = "submitted"
#
#        ##User may provide a project_dir.
#        if'project' in request_dict.keys():
#            log.debug("Found a project in the request.")
#            project = request_dict['project']
#            if "u_uuid" in project.keys():
#                self.u_uuid = project['u_uuid']
#            if "upload_path" in project.keys():
#                self.upload_path = project['upload_path']
#            if "pdb_id" in project.keys():
#                self.pdb_id = project['pdb_id']
#            if "input_source" in project.keys():
#                self.input_source = project['input_source']
#
#            if 'project_dir' in project.keys():
#                log.info("Found a project_dir in the request.")
#                if request_dict['project']['project_dir'] != " ":
#                    
#                    self.project_dir = project['project_dir']
#                else:
#                    log.debug("No project_dir found in the project. Using default.")
#                    ## Default, if none offered by the user.
#                    self.project_dir =  buildProjectDir(self.project_type , self.pUUID)
#            else:
#                log.debug("No project_dir found in the project. Using default.")
#                ## Default, if none offered by the user.
#                self.project_dir =  buildProjectDir(self.project_type , self.pUUID)
#        else:
#            ## Default, if no project offered by the user.
#            log.debug("No project found. Using default project dir.")
#            self.project_dir =  buildProjectDir(self.project_type , self.pUUID)
#
#        log.debug("project_dir: " + self.project_dir)

    def __str__(self): 
        result = super().__str__()
        result = result + "\nproject_type: " + self.project_type
        result = result + "\nuploaded_file_name: " + self.uploaded_file_name
        result = result + "\nstatus: " + self.status
        result = result + "\nu_uuid: " + self.u_uuid
        result = result + "\nupload_path: " + self.upload_path
        result = result + "\npdb_id: " + self.pdb_id
        result = result + "\ninput_source: " + self.input_source

        return result


class GpProject(Project):
    pdbProjectID : str = ""
    uploadFileName : str = ""
    status : str = ""

    def __init__(self, **data : Any):
        super().__init__(**data)

#    def __init__(self, request_dict : dict):
#        super().__init__(request_dict)
#        log.info("GpProject.__init__() was called.")
#        pdbProject = PdbProject(request_dict)
#        log.debug("pdbProject: \n" + str(pdbProject.__dict__))
#        self.pdbProjectID = pdbProject.pUUID
#        self.status = "submitted"
#        self.project_type = "gp"
#        self.has_input_files = True
#        self.uploadFileName = pdbProject.uploadFileName
#        ##User may provide a project_dir.
#        if'project' in request_dict.keys():
#            
#            if 'project_dir' in request_dict['project'].keys():
#                project = request_dict['project']
#                self.project_dir = project['project_dir']
#            else:
#                ## Default, if none offered by the user.
#                self.project_dir =  buildProjectDir(self.project_type , self.pUUID)
#        else:
#            ## Default, if none offered by the user.
#                self.project_dir =  buildProjectDir(self.project_type , self.pUUID)
#
#
#    def __str__(self):
#        result = super().__str__()
#        result = result + "\npdbProjectId: " + self.pdbProjectID
#        result = result + "\nstatus: " + self.status
#        return result


## Details and location of the build of a single pose of a structure.
class StructureMapping():
    ##  Path to the dir that holds this build. 
    #   May or may not be in this project dir.
    structure_path : str = ""
    ion : str = "No"
    solvation : str = "No"
    solvation_size : str = ""
    solvation_distance : str = ""
    splvation_shape : str = "REC"
    timestamp : str = None

##  Figures out the type of structure file being preprocessed.
def getStructureFileProjectType(request_dict):
    projectType = "not set"
    services = request_dict['entity']['services']
    for service in services:
        if 'Preprocess' in service.keys():
            if 'type' in service['Preprocess'].keys():
                if 'PreprocessPdbForAmber' == service['Preprocess']['type']:
                    projectType = "pdb"

    return projectType

##TODO: pydantic homework when model has settled down.

# def generateProjectSchema():
#     print(project.schema_json(indent=2))

if __name__ == "__main__":
    generateProjectSchema()
