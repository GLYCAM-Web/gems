#!/usr/bin/env python3
import  os, sys
import json
import uuid
from datetime import datetime
from gemsModules.common import services as commonservices
from gemsModules.common import settings as commonsettings
from gemsModules.common.io import Notice
from gemsModules.project import settings as project_settings
from pydantic import BaseModel, Field, ValidationError
from pydantic.schema import schema
from typing import Any, List
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
    parent_entity : str = ""
    requested_service : str = ""

    ## The filesystem_path can be used to override settings.default_filesystem_output_path
    filesystem_path : str = ""  
    compute_cluster_filesystem_path : str = ""  
    entity_id : str = ""
    service_id : str = ""
    service_dir : str = ""
    ## The project path. Used to be output dir, but now that is reserved for subdirs.
    # The project_dir should generally be set after the service dir is set
    project_dir : str = ""
    logs_dir : str = ""
    requesting_agent : str = ""
    has_input_files : bool = None
   
    ## These can be read in using getVersionsFileInfo
    site_version : str = ""
    site_branch : str = ""
    gems_version : str = ""
    gems_branch : str = ""
    md_utils_version : str = ""
    md_utils_branch : str = ""
    gmml_version : str = ""
    gmml_branch : str = ""
    gp_version : str = ""
    gp_branch : str = ""
    site_mode : str = ""
    site_host_name : str = ""
    versions_file_path : str = ""
    download_url_path :str = ""

    force_field : str = "default"
    parameter_version : str = "default"
    amber_version : str = "default"
    json_api_version : str = ""
    _django_version : str = ""
    django_project_id : str = ""
  
    notices : List[Notice] = []


    def __init__(self, **data : Any):
        super().__init__(**data)

        ## Random uuid for the project uuid if none has been specified
        if self.pUUID is "" : 
            self.pUUID = str(uuid.uuid4()) 
        if self.timestamp is None : 
            self.gems_timestamp = datetime.now()

    # In file _defaultInitializeProject.py:
    #    def defaultInitializeProject(self, referenceProject : Project = None, noClobber : bool = True):
#    from gemsModules.project._defaultInitializeProject import defaultInitializeProject

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
            (source, path) = commonlogic.getFilesystemOutputPath()
        except :
            message = "There was an error while asking common for the  GEMS Filesystem Output Path. \nForgins ahead with Project default anyway."
            log.error(message)
            self.filesystem_path = project.settings.default_filesystem_output_path
        # Assign the path based on the return values from common
        if source == 'Environment' :
            message = "GEMS Filesystem Output Path was set using an environment variable to: \n" + str(path)
            log.debug(message)
            self.filesystem_path = path
        elif source == 'Default':
            message = "Overriding GEMS Filesystem Output Path with the default from Project."
            log.debug(message)
            self.filesystem_path = project.settings.default_filesystem_output_path
        elif source == 'Error' :
            message = "Common reported an error trying to determine the GEMS Filesystem Output Path. \nForgins ahead with Project default anyway."
            log.error(message)
            self.filesystem_path = project.settings.default_filesystem_output_path
        else :
            message = "Unknown source for GEMS Filesystem Output Path.  Using default from Project."
            log.debug(message)
            self.filesystem_path = project.settings.default_filesystem_output_path


    def setServiceDir(self, specifiedDirectory : str = None, noClobber : bool = False) :
        # First, check if the service directory field is already populated
        if self.service_dir is not None and self.service_dir is not "" :
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
        #  Still here ?
        #    grab and store locally the entity_id and service_id for future use
        self.entity_id = gemsModules.project.settings.output_entity_id[self.parent_entity]
        self.service_id = gemsModules.project.settings.output_entity_service_id[self.parent_entity][self.requested_service]
        #    set the service_dir
        self.service_dir = os.path.join(
                self.filesystem_path,
                self.entity_id,
                self.service_id)
        message = "Setting the service dir to : " + self.service_dir
        log.debug(message)


    def setProjectDir(self, specifiedDirectory : str = None, noClobber : bool = False) :
        # First, check if the project directory field is already populated
        if self.project_dir is not None and self.project_dir is not "" :
            # If noClobber is set to true, return without changing the directory
            if noClobber : 
                return
        # If a directory was specified, set it and return
        if specifiedDirectory is not None :
            self.project_dir = specifiedDirectory
            return
        # If we are still here, attempt to build the project directory
        # First, try to determine the service_dir path
        if self.service_dir is None or self.service_dir is "" :
            message = "Cannot set project_dir because cannot determine service_dir"
            log.error(message)
            log.debug(self.json(indent=2))
            self.generateCommonParserNotice(
                    noticeBrief = 'GemsError',
                    additionalInfo = { 'hint' : message }
                    )
            return
        # Next, bail if somehow the pUUID didn't get set
        if self.pUUID is None or self.pUUID is "" :
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
        if self.versions_file_path is not None and self.versions_file_path is not "" :
            # If noClobber is set to true, return without changing the field
            if noClobber : 
                return
        # If a directory was specified, set it and return
        if specifiedPath is not None :
            self.versions_file_path = specifiedPath
            return
        # If we are still here, attempt to build the project directory
        # First, try to determine the filesystem path
        if self.filesystem_path is None or self.filesystem_path is "" :
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
        from gemsModules.project.projectUtilPydantic import getVersionsFileInfo
        log.debug("About to load the version info.")
        try : 
            theDict = getVersionsFileInfo(self.versions_file_path)
            log.debug("The dictionary is : " + str(theDict))
            for k in theDict.keys() :
                log.debug("k is : " + k)
                setattr(self, k, theDict[k])
            log.debug("My contents are now: ")
            log.debug(self.json(indent=2))
        except Exception as error :
            log.error("There was aproblem loading the versions file info")
            raise error

    def getFilesystemPath(self) :
        log.debug("getting filesystem_path: " + str(self.filesystem_path))
        return self.filesystem_path 

    def getEntityId(self) :
        log.debug("getting entity_id: " + str(self.entity_id))
        return self.entity_id 

    def getServiceId(self) :
        log.debug("getting service_id: " + str(self.service_id))
        return self.service_id 

    ## Set the download URL path for this project  
    #   @param  self.pUUID
    #   @param  self.project_type
    def setDownloadUrlPath(self):
        log.info("setDownloadUrlPath was called.\n")
        try :
            log.debug("pUUID: " + str(self.pUUID))
            log.debug("project_type: " + str(self.project_type))
            log.debug("site_host_name: " + str(self.site_host_name))
            self.download_url_path = "http://" + self.site_host_name + "/" + "json"+ "/" + "download" + "/" + self.project_type + "/" + self.pUUID
            log.debug("downloadUrl : " + self.download_url_path )
        except AttributeError as error:
            log.error("Something went wrong building the downloadUrlPath.")
            raise error

    def getDownloadUrlPath(self) :
        if self.download_url_path is None or self.download_url_path is "" :
            self.setDownloadUrlPath()
        if self.download_url_path is None or self.download_url_path is "" :
            log.error("There was a problem setting the download_url_path")
            return
        return self.download_url_path
        
    def generateCommonParserNotice(self, *args, **kwargs) :
        self.notices.append(commonsettings.generateCommonParserNotice(*args, **kwargs))

    def createDirectories(self) :
        # If not already set, set the service-level logs_dir
        if self.logs_dir is None or self.logs_dir is  "" :
            self.logs_dir = os.path.join( 
                    self.project_dir, 
                    "logs")
            message = "the project_dir was already set, and clobbering is not allowed  The path is: " + self.service_dir
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
    project_type : str = "cb"
    parent_entity : str = "Sequence"
    sequence_id : str = ""
    sequence_path : str = ""
    has_input_files : bool = False

#    def __init__(self, **data : Any):
#        super().__init__(**data)


class PdbProject(Project):
    has_input_files : bool = True
    uploaded_file_name : str = ""
    status : str = ""
    u_uuid : str = ""
    upload_path : str = ""
    pdb_id : str = ""
    input_source : str = ""
    project_type = 'pdb'
    parent_entity : str = "StrucureFile"

#    def __init__(self, **data : Any):
#        super().__init__(**data)


class GpProject(Project):
    pdb_project_uuid : str = ""
    has_input_files : bool = False
#  Presunably, the following can be obtained from the PdbProject
#    has_input_files : bool = True
#    uploaded_file_name : str = ""
#    upload_path : str = ""
    status : str = ""
    project_type = 'gp'
    parent_entity : str = "Conjugate"

#    def __init__(self, **data : Any):
#        super().__init__(**data)



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
