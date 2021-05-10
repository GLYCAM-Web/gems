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

    ## The filesystem_path can be used to override settings.default_filesystem_output_path
    filesystem_path : str = ""  
    compute_cluster_filesystem_path : str = ""  
    ## The project path. Used to be output dir, but now that is reserved for subdirs.
    project_dir : str = ""
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
    download_url :str = ""

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
        # First, try to determine the filesystem path
        if self.filesystem_path is None or self.filesystem_path is "" :
            self.setFilesystemPath()
        if self.filesystem_path is None or self.filesystem_path is "" :
            message = "Cannot set project_dir because cannot determine filesystem path"
            log.error(message)
            self.generateCommonParserNotice(
                    noticeBrief = 'GemsError',
                    additionalInfo = { 'hint' : message }
                    )
            return
        # If we are still here, set the directory 
        self.project_dir =  buildProjectDir(self.filesystem_path, project_settings.project_subdirectory[self.project_type] , self.pUUID)
        log.debug("self.project_dir is : >>>" + self.project_dir + "<<<")

    def setVersionsFilePath(self, specifiedPath : str = None, noClobber : bool = False) :
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
            self.setFilesystemPath()
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
        if self.versions_file_path is None :
            self.setVersionsFilePath()
        if self.versions_file_path is None :
            log.error("There was a problem setting the versions file path.  Cannot load versions file info")
        from gemsModules.project.projectUtilPydantic import getVersionsFileInfo
        try : 
            self(**getVersionsFileInfo(self.versions_file_path))
        except Exception as error :
            log.error("There was aproblem loading the versions file info")
            raise error

    def getFilesystemPath(self) :
        log.debug("getting filesystem_path: " + str(self.filesystem_path))
        return self.filesystem_path 
    def setFilesystemPath(self, specifiedPath:str) :
        # allow for direct setting of project dir
        log.debug("Setting filesystem_path to specified path : " + str(specifiedPath))
        self.filesystem_path = specifiedPath
        return

    def setDownloadUrl(self, optionalSubDir : str = None):
        log.info("getDownloadUrl was called.\n")
        try :
            log.debug("pUUID: " + str(self.pUUID))
            log.debug("project_type: " + str(self.project_type))
            log.debug("optionalSubDir: " + str(optionalSubDir))
            self.download_url = "http://" + self.site_host_name + "/json/download/" + self.project_type +"/" + self.pUUID + "/" + optionalSubDir
            log.debug("downloadUrl : " + self.download_url )
        except AttributeError as error:
            log.error("Something went wrong building the downloadUrl.")
            raise error

    def getDownloadUrl(self) :
        return self.download_url
                

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

def buildProjectDir(filesystemPath, projectSubdirectory, pUUID):
    log.info("buildProjecDir() was called.")
    log.debug("filesystemPath: " + filesystemPath)
    log.debug("projectSubdirectory: " + projectSubdirectory)
    log.debug("pUUID: " + pUUID)
    # fun fact - os.path.join isn't very useful if your strings contain forward slashes.
    #            one day, we should make this more OS-independent.  But... not now.
    return os.path.join(filesystemPath,  projectSubdirectory, "git-ignore-me_userdata/Builds", pUUID )

## @brief cbProject is a typed project that inherits all the fields from project and adds 
#   its own.
class CbProject(Project):
    has_input_files : bool = False

    def __init__(self, **data : Any):
        super().__init__(**data)
        log.info("CbProject.__init__() was called.")
        self.project_type = "cb"

#Is this still needed?
#    def __str__(self):
#        result = super().__str__()
##        result = result + "\nproject_type: " + self.project_type
##        result = result + "\nsequence: " + self.sequence
##        result = result + "\nseqID: " + self.seqID
##        result = result + "\nstructure_count: " + str(self.structure_count)
#        #result = result + "\nstructure_mappings: " + str(self.structure_mappings)
#        return result

class PdbProject(Project):
    uploaded_file_name : str = ""
    status : str = ""
    u_uuid : str = ""
    upload_path : str = ""
    pdb_id : str = ""
    input_source : str = ""

    def __init__(self, **data : Any):
        super().__init__(**data)

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
