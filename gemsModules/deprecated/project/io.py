#!/usr/bin/env python3
import  os, sys
import json
import uuid
from datetime import datetime
from gemsModules.deprecated.common import services as commonservices
from gemsModules.deprecated.common import settings as commonsettings
from gemsModules.deprecated.common import logic as commonlogic
from gemsModules.deprecated.common.io import Notice
from gemsModules.deprecated.project import settings as project_settings
from pydantic import BaseModel, Field, ValidationError, constr
from pydantic.schema import schema
from typing import Any, List
from gemsModules.deprecated.common.loggingConfig import *
import traceback

# ## TODO - a lot of this info really belongs elsewhere.  It's not really
#    project information.  For example, 'seqID' only applies to the sequence
#    entity.  In the GP builder, there might be many sequences, but still 
#    only one overall project.  So, one day, clean this up.


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

##TODO It makes sense that the length of things like a git hash won't change often. System-wide vars could 
##  provide constants or single-points-of-edit for types of max-length values. 
##  TTITLE_MAX_LENGTH could then be edited in a single place, but applied to all gemsModule classes.


##  @brief The primary way of tracking data related to a project
#   @detail This is the generic project object. See subtypes for more specific fields
class Project(BaseModel):
    ## The name of the output dir is the pUUID
    pUUID : constr(max_length=36)=""
    title : constr(max_length=25)=""
    comment : constr(max_length=50)=""
    timestamp : datetime = None
    gems_timestamp : datetime = None
    # The following should be overridden as needed in child classes.  See CbProject, for example.
    # Each type of project known to the modules should have a child class.
    project_type : constr(max_length=25)="project"
    parent_entity : constr(max_length=25)="project"
    requested_service : constr(max_length=25)="project"
    entity_id : constr(max_length=25)="project"
    service_id : constr(max_length=25)="project"

    ## The filesystem_path can be used to override settings.default_filesystem_output_path
    filesystem_path : constr(max_length=255)="" 
    compute_cluster_filesystem_path : constr(max_length=255)=""
    service_dir : constr(max_length=255)=""
    ## The project path. Used to be output dir, but now that is reserved for subdirs.
    # The project_dir should generally be set after the service dir is set
    project_dir : constr(max_length=255)=""
    logs_dir : constr(max_length=255)=""
    requesting_agent : constr(max_length=25)=""
    has_input_files : bool = None
   
    ## These can be read in using getVersionsFileInfo
    site_version : constr(max_length=40)=""
    site_branch : constr(max_length=50)=""
    site_code_name : constr(max_length=50)=""

    gems_version : constr(max_length=40)=""
    gems_branch : constr(max_length=50)=""
    md_utils_version : constr(max_length=40)=""
    md_utils_branch : constr(max_length=50)=""
    gmml_version : constr(max_length=40)=""
    gmml_branch : constr(max_length=50)=""
    gp_version : constr(max_length=40)=""
    gp_branch : constr(max_length=50)=""
    site_mode : constr(max_length=25)=""
    site_host_name : constr(max_length=25)=""
    versions_file_path : constr(max_length=255)=""
    host_url_base_path : constr(max_length=255)=""
    download_url_path : constr(max_length=255)=""

    force_field : constr(max_length=25)="default"
    parameter_version : constr(max_length=25)="default"
    amber_version : constr(max_length=25)="default"
    json_api_version : constr(max_length=10)="0.0.1"
    _django_version : constr(max_length=10)=""
    django_project_id : constr(max_length=36)=""
    app : constr(max_length=25)="project"
  
    
    ## In some cases, GEMS will choose to start a new project 
    ## even if one is provided.  If you don't want to force
    ## GEMS to use this project, set this to True.
    force_use_this_project : bool = False


    notices : List[Notice] = []


    def __init__(self, **data : Any):
        super().__init__(**data)

        ## Random uuid for the project uuid if none has been specified
        if self.pUUID == "" : 
            self.pUUID = str(uuid.uuid4()) 
        if self.gems_timestamp is None : 
            self.gems_timestamp = datetime.now()
        if self.timestamp is None : 
            self.timestamp = self.gems_timestamp

    # In file _defaultInitializeProject.py:
    #    def defaultInitializeProject(self, referenceProject : Project = None, noClobber : bool = True):
#    from gemsModules.deprecated.project._defaultInitializeProject import defaultInitializeProject

    def setFilesystemPath(self, specifiedPath : str = None, noClobber : bool = True) :
        # If a path exists, and it shouldbot be clobbered, return
        # This **SHOULD** be the case if the incoming JSON object specified a path.
        # For this to be true, ensure that your outgoing project is deep-copied from 
        # your incoming project before calling this.
        if noClobber is True :
            if self.filesystem_path is not None and self.filesystem_path != ""  :
                message = "Filesystem Output Path already exists in Project and cannot be clobbered.  It is:\n" + str(self.filesystem_path)
                log.debug(message)
                return
        # If a path was specified, set it and return
        if specifiedPath is not None :
            self.filesystem_path = specifiedPath
            return
        # Still here?  Try to determine the path using internal logic
        try :
            ## this is the userdata dir.
            (source, path) = commonlogic.getFilesystemOutputPath()
        except :
            message = "There was an error while asking common for the  GEMS Filesystem Output Path. \nForgins ahead with Project default anyway."
            log.error(message)
            self.filesystem_path = gemsModules.deprecated.project.settings.default_filesystem_output_path
            return
        # Assign the path based on the return values from common
        if source == 'Environment' :
            message = "GEMS Filesystem Output Path was set using an environment variable to: \n" + str(path)
            log.debug(message)
            self.filesystem_path = path
        elif source == 'Default':
            context = commonlogic.getGemsExecutionContext()
            if context == 'website' :    
                message = "Overriding GEMS Filesystem Output Path with the default from Project." 
                log.debug(message) 
                self.filesystem_path = gemsModules.deprecated.project.settings.default_filesystem_output_path
            else :
                message = "Using the default GEMS Filesystem Output Path." 
                log.debug(message) 
                self.filesystem_path = path
        elif source == 'Error' :
            message = "Common reported an error trying to determine the GEMS Filesystem Output Path. \nForgins ahead with Project default anyway."
            log.error(message)
            self.filesystem_path = gemsModules.deprecated.project.settings.default_filesystem_output_path
        else :
            message = "Unknown source for GEMS Filesystem Output Path.  Using default from Project."
            log.debug(message)
            self.filesystem_path = gemsModules.deprecated.project.settings.default_filesystem_output_path


    def setServiceDir(self, specifiedDirectory : str = None, noClobber : bool = False) :
        # First, check if the service directory field is already populated
        if self.service_dir is not None and self.service_dir != "" :
            # If noClobber is set to true, return without changing the directory
            if noClobber : 
                return
        # If a directory was specified, set it and return
        if specifiedDirectory is not None :
            self.service_dir = specifiedDirectory
            return
        # check that parent_entity and requested_service exist
        # if either is not defined, whine and exit
        if self.parent_entity == '' or self.parent_entity is None :
            message = "Cannot initialize a project without a parent_entity specified."
            log.error(message)
            self.generateCommonParserNotice(
                    noticeBrief = 'GemsError',
                    additionalInfo = {'hint' : message } )
            return
        if self.requested_service == '' or self.requested_service is None :
            message = "Cannot initialize a project without a requested_service specified."
            log.error(message)
            self.generateCommonParserNotice(
                    noticeBrief = 'GemsError',
                    additionalInfo = {'hint' : message } )
            return
        #
        self.service_dir = os.path.join(
                self.filesystem_path,
                self.entity_id,
                self.service_id)
        message = "Setting the service dir to : " + self.service_dir
        log.debug(message)


    def setProjectDir(self, specifiedDirectory : str = None, noClobber : bool = False) :
        # First, check if the project directory field is already populated
        if self.project_dir is not None and self.project_dir != "" :
            # If noClobber is set to true, return without changing the directory
            if noClobber : 
                return
        # If a directory was specified, set it and return
        if specifiedDirectory is not None :
            self.project_dir = specifiedDirectory
            return
        # If we are still here, attempt to build the project directory
        # First, try to determine the service_dir path
        if self.service_dir is None or self.service_dir == "" :
            message = "Cannot set project_dir because cannot determine service_dir"
            log.error(message)
            log.debug(self.json(indent=2))
            self.generateCommonParserNotice(
                    noticeBrief = 'GemsError',
                    additionalInfo = { 'hint' : message }
                    )
            return
        # Next, bail if somehow the pUUID didn't get set
        if self.pUUID is None or self.pUUID == "" :
            message = "Cannot set project_dir because cannot determine pUUID"
            log.error(message)
            log.debug(self.json(indent=2))
            self.generateCommonParserNotice(
                    noticeBrief = 'GemsError',
                    additionalInfo = { 'hint' : message }
                    )
            return
        # If we are still here, set the directory 
        self.project_dir =  os.path.join(self.service_dir, self.pUUID )
        log.debug("self.project_dir is : >>>" + self.project_dir + "<<<")

    def setVersionsFilePath(self, specifiedPath : str = None, noClobber : bool = False) :
        log.debug("setVersionsFilePath was called.")
        # First, check if the versions file path field is already populated
        if self.versions_file_path is not None and self.versions_file_path != "" :
            # If noClobber is set to true, return without changing the field
            if noClobber : 
                return
        # If a directory was specified, set it and return
        if specifiedPath is not None :
            self.versions_file_path = specifiedPath
            return
        # If we are still here, attempt to build the project directory
        # First, try to determine the filesystem path
        if self.filesystem_path is None or self.filesystem_path == "" :
            message = "Cannot set versions file path because cannot determine filesystem path"
            log.error(message)
            self.generateCommonParserNotice(
                    noticeBrief = 'GemsError',
                    additionalInfo = { 'hint' : message }
                    )
            return
        # If we are still here, set the directory 
        self.versions_file_path =  os.path.join(self.filesystem_path, project_settings.default_versions_file_name  )
        log.debug("self.versions_file_path is : >>>" + self.versions_file_path + "<<<")

    def loadVersionsFileInfo(self) :
        log.debug("loadVersionsFileInfo was called.")
        if self.versions_file_path is None or self.versions_file_path == "" :
            self.setVersionsFilePath()
        if self.versions_file_path is None or self.versions_file_path == "" :
            log.error("There was a problem setting the versions file path.  Cannot load versions file info")
            return
        from gemsModules.deprecated.project.projectUtilPydantic import getVersionsFileInfo
        log.debug("About to load the version info.")
        try : 
            theDict = getVersionsFileInfo(self.versions_file_path)
            log.debug("The dictionary is : " + str(theDict))
            for k in theDict.keys() :
                #log.debug("k is : " + k)
                setattr(self, k, theDict[k])
            log.debug("My contents are now: ")
            log.debug(self.json(indent=2))
        except Exception as error :
            log.error("There was aproblem loading the versions file info")
            raise error

    def getFilesystemPath(self) :
        log.debug("getting filesystem_path: " + str(self.filesystem_path))
        return self.filesystem_path 

    def getPuuid(self) :
        log.debug("getting pUUID: " + str(self.pUUID))
        return self.pUUID

    def getEntityId(self) :
        log.debug("getting entity_id: " + str(self.entity_id))
        return self.entity_id 

    def getServiceId(self) :
        log.debug("getting service_id: " + str(self.service_id))
        return self.service_id 

    def getHostUrlBasePath(self) :
        return self.host_url_base_path

    def setHostUrlBasePath(self) :
        import os
        GEMS_HOST_URL_BASE_PATH =  os.environ.get('GEMS_HOST_URL_BASE_PATH')
        if GEMS_HOST_URL_BASE_PATH is not None and GEMS_HOST_URL_BASE_PATH != "" :
            self.host_url_base_path = GEMS_HOST_URL_BASE_PATH
            return
        if self.site_host_name == "" :
            log.error("Sete host name not set.  Cannot set Host Url Base Path.")
            return
        if commonlogic.getGemsExecutionContext() == 'website' :
            prefix = 'https://'
        else :
            prefix = 'http://'
        self.host_url_base_path = prefix + self.site_host_name

    ## Set the download URL path for this project  
    #   @param  self.pUUID
    #   @param  self.project_type
    def setDownloadUrlPath(self):
        log.info("setDownloadUrlPath was called.\n")
        try :
            if self.host_url_base_path == "" :
                log.error("the host url base path is not set so cannot set download url path.")
                return
            from gemsModules.deprecated.project import projectUtilPydantic as utils
            self.download_url_path = utils.buildDownloadUrlPath( 
                    self.host_url_base_path ,
                    self.entity_id ,
                    self.service_id ,
                    self.pUUID )
            log.debug("downloadUrl : " + self.download_url_path )
        except AttributeError as error:
            log.error("Something went wrong building the downloadUrlPath.")
            raise error

    def getDownloadUrlPath(self) :
        if self.download_url_path is None or self.download_url_path == "" :
            self.setDownloadUrlPath()
        if self.download_url_path is None or self.download_url_path == "" :
            log.error("The downloadUrlPath was unset, and could not be set, so could not be got.")
            return
        return self.download_url_path
        
    def generateCommonParserNotice(self, *args, **kwargs) :
        self.notices.append(commonsettings.generateCommonParserNotice(*args, **kwargs))

    def createDirectories(self) :
        # If not already set, set the service-level logs_dir
        if self.logs_dir is None or self.logs_dir ==  "" :
            self.logs_dir = os.path.join( 
                    self.project_dir, 
                    "logs")
            message = "The path to the logs directory is: " + self.logs_dir
            log.debug(message)
    
        ## Create the directories if needed
        import pathlib
        # This should generate them all
        # TODO - write code to check this and be more specific
        pathlib.Path(self.logs_dir).mkdir(parents=True, exist_ok=True)
   

    def copyUploadedFiles(self) :
        ### Copy any uploaded files.
        log.debug("project.has uploaded_input_files: " + str(self.has_input_files))
        if self.has_input_files != "True":
            log.error("This project says it does NOT have input files, but copyUploadedFiles was called.")
            try:
                common.logic.copyPathFileToPath(self.upload_path, self.uploaded_file_name, self.project_dir)
            except Exception as error:
                log.error("There was a problem uploading the input: " + str(error))
                raise error


    def writeInitialLogs(self) :
        try:
            log.info("About to write initial logs entry from Project.\n")
            with open(os.path.join( self.logs_dir, 'ProjectLog.json'), 'w', encoding='utf-8') as file:
                jsonString = self.json(indent=4, sort_keys=False)
                log.debug("jsonString: \n" + jsonString )
                file.write(jsonString)
        except Exception as error:
            log.error("There was a problem writing the project logs: " + str(error))
            raise error


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


## @brief cbProject is a typed project that inherits all the fields from project and adds 
#   its own.
class CbProject(Project):
    sequence_id : constr(max_length=255)=""
    sequence_path : constr(max_length=255)=""
    indexOrderedSequence : constr(max_length=65535)=""
    seqID : constr(max_length=36)=""
    selected_rotamers : constr(max_length=65535)=""

    def setIndexOrderedSequence(self, theSequence : str ) :
        self.indexOrderedSequence = theSequence

    def getIndexOrderedSequence(self) :
        log.debug("getting IndexOrderedSequence: " + str(self.indexOrderedSequence))
        return self.indexOrderedSequence
    
    def setSeqId(self, theSeqId : str ) :
        self.seqID = theSeqId

    def getSeqId(self) :
        log.debug("getting SeqId: " + str(self.seqID))
        return self.seqID

    def __init__(self, **data : Any):
        super().__init__(**data)
        self.project_type = "cb"
        self.parent_entity = "Sequence"
        self.entity_id = "sequence"
        self.service_id = "cb"
        self.has_input_files = False



class PdbProject(Project):
    #Contains path 
    uploaded_file_name : constr(max_length=255)=""
    status : constr(max_length=10)="submitted"
    u_uuid : constr(max_length=36)=""
    pdb_id : constr(max_length=4)=""
    input_source : constr(max_length=25)=""
    has_input_files : bool = True
    project_type : constr(max_length=25)='pdb'
    parent_entity : constr(max_length=25)="StructureFile"
    entity_id : constr(max_length=25)="structurefile"
    service_id : constr(max_length=25)="pdb"

    ## Not needed. Marked for deprecation
    upload_path : constr(max_length=255)=""


    def setUploadFile(self, uploadFile:str):
        log.info("PdbProject setUploadFile was called.")
        log.debug("uploadFile: " + uploadFile)
        self.uploaded_file_name = uploadFile

    def __init__(self, **data : Any):
        super().__init__(**data)
        #Service dir looks like 'structurefile/pdb'
        self.setFilesystemPath()
        self.setServiceDir()
        self.loadVersionsFileInfo()
        


class GpProject(Project):
    pdb_project_pUUID : constr(max_length=36)=""
    status : constr(max_length=10)="submitted"

    
    def __init__(self, **data : Any):
       super().__init__(**data)
       self.has_input_files = False
       self.project_type = 'gp'
       self.parent_entity = "Conjugate"
       self.entity_id = "conjugate"
       self.service_id = "gp"


class GrProject(Project):
    uploaded_file_name : constr(max_length=255)=""
    u_uuid : constr(max_length=36)=""
    upload_path :  constr(max_length=255)=""

    def __init__(self, **data : Any):
       super().__init__(**data)
       self.project_type = "gr"

class MdProject(Project):
    system_phase : constr(max_length=25) = "In solvent."
    input_type : constr(max_length=25) = "Amber-prmtop & inpcrd"
    prmtop_file_name : constr(max_length=255) = " "
    inpcrd_file_name : constr(max_length=255) = " "
    pdb_file_name  : constr(max_length=255) = " "
    mmcif_file_name : constr(max_length=255) = " "
    off_file_name : constr(max_length=255)  = " "
    u_uuid : constr(max_length=36) = " "
    water_model : constr(max_length=10) = "TIP-3P"
    sim_length : constr(max_length=5) = '100'
    notify : bool =True
    upload_path : constr(max_length=255)  = " "
    
    def __init__(self, **data : Any):
       super().__init__(**data)
       self.project_type = "md"

##  Are these used at all?????
### Details and location of the build of a single pose of a structure.
#class StructureMapping():
#    ##  Path to the dir that holds this build. 
#    #   May or may not be in this project dir.
#    structure_path : str = ""
#    ion : str = "No"
#    solvation : str = "No"
#    solvation_size : str = ""
#    solvation_distance : str = ""
#    splvation_shape : str = "REC"
#    timestamp : str = None
#
###  Figures out the type of structure file being preprocessed.
#def getStructureFileProjectType(request_dict):
#    projectType = "not set"
#    services = request_dict['entity']['services']
#    for service in services:
#        if 'Preprocess' in service.keys():
#            if 'type' in service['Preprocess'].keys():
#                if 'PreprocessPdbForAmber' == service['Preprocess']['type']:
#                    projectType = "pdb"
#
#    return projectType

def generateProjectSchemaForWeb():
    spaceCount=2
    log.info("generateProjectSchemaForWeb() was called.")
    
    log.debug("SCHEMA_DIR: " + commonsettings.SCHEMA_DIR)
    moduleSchemaDir = os.path.join(commonsettings.SCHEMA_DIR, "gemsProject")

    try:
        if not os.path.isdir(moduleSchemaDir):
            os.makedirs(moduleSchemaDir)
        
        # filePath = os.path.join(moduleSchemaDir, 'GemsProjectSchema.json')
        # with open(filePath, 'w') as file:
        #     file.write(Project.schema_json(indent=spaceCount))

        ## Need a file for cb, pdb, gp

        childFilePath = os.path.join(moduleSchemaDir, 'CbProject.json')
        with open(childFilePath, 'w') as childFile:
            childFile.write(CbProject.schema_json(indent=spaceCount))

        childFilePath = os.path.join(moduleSchemaDir, 'PdbProject.json')
        with open(childFilePath, 'w') as childFile:
            childFile.write(PdbProject.schema_json(indent=spaceCount))

        childFilePath = os.path.join(moduleSchemaDir, 'GpProject.json')
        with open(childFilePath, 'w') as childFile:
            childFile.write(GpProject.schema_json(indent=spaceCount))

        childFilePath = os.path.join(moduleSchemaDir, 'MdProject.json')
        with open(childFilePath, 'w') as childFile:
            childFile.write(MdProject.schema_json(indent=spaceCount))

        childFilePath = os.path.join(moduleSchemaDir, 'GrProject.json')
        with open(childFilePath, 'w') as childFile:
            childFile.write(GrProject.schema_json(indent=spaceCount))


    except Exception as error:
        log.error("There was a problem writing the Project schema to file: " + str(error))
        log.error(traceback.format_exc())
        raise error


def generateProjectSchema():
    print(Project.schema_json(indent=2))


if __name__ == "__main__":
    generateProjectSchema()
