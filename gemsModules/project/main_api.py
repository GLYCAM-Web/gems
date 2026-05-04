#!/usr/bin/env python3
import os
import uuid
import traceback
from typing import Any, List, Dict
from datetime import datetime

from pydantic import BaseModel, constr

from gemsModules.common.main_api_notices import Notice
from gemsModules.configuration.main_api import session_instance_config 
from gemsModules.systemoperations.filesystem_ops import directory_is_writable
from gemsModules.systemoperations.environment_ops import getGemsExecutionContext
from gemsModules.project import settings as project_settings

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


# ## TODO - a lot of this info really belongs elsewhere.  It's not really
#    project information.  For example, 'seqID' only applies to the sequence
#    entity.  In the GP builder, there might be many sequences, but still 
#    only one overall project.  So, one day, clean this up.

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
    # For reporting statuses
    status : constr(max_length=10)="submitted"

    ## The filesystem_path can be used to override settings.default_website_filesystem_output_path
    filesystem_path : constr(max_length=255)="" 
    ## The uploads_path can be used to override settings.default_website_filesystem_uploads_path
    uploads_path : constr(max_length=255)="" 
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
    ## even if one is provided.  If you want to force
    ## GEMS to use this project, set this to True.
    force_use_this_project : bool = False


    ## If you need GEMS to use project info from the API JSON rather than from 
    ## the instance config, set this to true. Depending on the circumstances, 
    ## this setting might be ignored anyway.
    use_api_strict : bool = True


    notices : List[Notice] = []


    ## The host that first received the request - copied from instance config info
    initial_receiver : str = ""
    ## The host that fulfilled the request - copied from instance config info
    execution_host : str = ""
    #
    ## Populated for localhost ONLY 
    ## App-specific definitions from the instance config will be copied here.
    ## Mostly, it is up to the app to decide what to do with them.
    ## Generally, these options will be favored unless use_api_strict=True is set.
    #
    initial_reciever_options : Dict[str, str] = {}
    execution_host_options : Dict[str, str] = {}
    ## Populated for localhost ONLY 
    ## This is the list of contexts that are supported in the localhost instance.
    ## It lets GEMS know whether a certain capability is available locally or how it works.
    ## For example, it might tell GEMS that this host supports submission to a cluster by 
    ## noting which scheduler the cluster uses (e.g., Slurm).
    #
    initial_receiver_supported_contexts : List[str] = []
    execution_host_supported_contexts : List[str] = []
    ## Populated for localhost ONLY 
    ## Copied in from the instance config


    def __init__(self, **data : Any):
        super().__init__(**data)
        log.debug("Instantiation of a project is called.")

        ## Random uuid for the project uuid if none has been specified
        if self.pUUID == "" : 
            self.pUUID = str(uuid.uuid4()) 
        if self.gems_timestamp is None : 
            self.gems_timestamp = datetime.now()
        if self.timestamp is None : 
            self.timestamp = self.gems_timestamp

    def getLocalhostInstanceConfigContextOptions(self) :
        log.info("getLocalhostInstanceConfigContextOptions was called")
        IC = session_instance_config
        instanceConfigOptions = IC.get_locahost_context_options_by_service_ID(serviceID=self.service_id)
        if instanceConfigOptions is not None:
            self.instance_config_options.append(instanceConfigOptions)


    def setFilesystemPath(self, specifiedPath : str = None, noClobber : bool = True) :
        log.info("setFilesystemPath was called.")
        # If a path exists, and it should not be clobbered, return
        # This **SHOULD** be the case if the incoming JSON object specified a path.
        # For this to be true, ensure that your outgoing project is deep-copied from 
        # your incoming project before calling this.
        if self.filesystem_path is None:
            self.filesystem_path = ""  # shorten later if-thens
        IC = session_instance_config
        message="The service_id is: " + self.service_id
        log.debug(message)
        instanceConfigPath = IC.get_filesystem_path_by_service_ID(serviceID=self.service_id)
        context = getGemsExecutionContext()
        if noClobber is True :
            if self.filesystem_path != ""  :
                message = "Filesystem Output Path already exists in Project and cannot be clobbered.  It is:\n" + str(self.filesystem_path)
                log.debug(message)
                if specifiedPath != None :
                    message = "Not clobbering filesystem path specified in setFilesystemPath.  It is:\n" + str(specifiedPath)
                    log.debug(message)
                if instanceConfigPath != None :
                    message = "Not clobbering filesystem path specified in the instance config.  It is:\n" + str(instanceConfigPath)
                    log.debug(message)
                if context == 'website' :
                    message = "In website context, noClobber is set to True. Not overriding pre-set filesystem path."
                    log.info(message)
                return
        # If a path was specified, set it, if allowed, and return
        if context == 'website' :
            # TODO: collapse the next two into a single block
            if specifiedPath is not None :
                log.debug("An output path is specified in website context.  Checking to see if it is allowed." )
                log.debug("The specifiedPath is: " + str(specifiedPath))
                if specifiedPath in project_settings.allowed_website_filesystem_paths :
                    message = "The output path is allowed.  Using it."
                    log.debug(message)
                    self.filesystem_path = specifiedPath
                    return
                else: 
                    message = "The output path is not allowed."
                    log.error(message)
            if instanceConfigPath is not None :
                log.debug("An output path is specified in website context.  Checking to see if it is allowed." )
                log.debug("The instanceConfigPath is: " + str(instanceConfigPath))
                if instanceConfigPath in project_settings.allowed_website_filesystem_paths :
                    message = "The output path is allowed.  Using it."
                    log.debug(message)
                    self.filesystem_path = instanceConfigPath
                    return
                else: 
                    message = "The output path is not allowed."
                    log.error(message)
            self.filesystem_path = project_settings.default_website_filesystem_output_path
            message = "Using the default GEMS Website Filesystem Output Path: " + str(self.filesystem_path)
            log.debug(message) 
            return
        # Still here? We are not a website. See what else we can do.
        if specifiedPath is not None :
            if directory_is_writable(specifiedPath) :
                message = "The specifiedPath is allowed.  Using it."
                log.debug(message)
                self.filesystem_path = specifiedPath
            else :
                message = "Cannot write to the specifiedPath: " + str(specifiedPath)
                log.error(message)
            return
        if instanceConfigPath is not None :
            if directory_is_writable(instanceConfigPath) :
                message = "The instanceConfigPath is allowed.  Using it."
                log.debug(message)
                self.filesystem_path = instanceConfigPath
            else :
                message = "Cannot write to the instanceConfigPath: " + str(instanceConfigPath)
                log.error(message)
            return
        #
        # Try: 
        #     standalone filesystem path
        #                 Notes: 
        #                     - Standalone implies dockerized. If not writable, just bail. Don't try to make the directory.
        #     $HOME/GEMS_UserSpace
        #     $GEMSHOME/UserSpace
        #     website filesystem output path
        #
        if directory_is_writable(project_settings.default_standalone_filesystem_output_path) :
            message = "Setting filesystem output path to: " + project_settings.default_standalone_filesystem_output_path
            log.info(message)
            self.filesystem_path = project_settings.default_standalone_filesystem_output_path
            return
        userhome = os.environ.get("HOME")
        testdir = userhome + "/GEMS_UserSpace"
        if directory_is_writable(testdir, make_if_needed=True) :
            message = "Setting filesystem output path to: " + testdir
            log.info(message)
            self.filesystem_path = testdir
            return
        gemshome = os.environ.get("GEMSHOME")
        testdir = gemshome + "/UserSpace"
        if directory_is_writable(testdir, make_if_needed=True) :
            message = "Setting filesystem output path to: " + testdir
            log.info(message)
            self.filesystem_path = testdir
            return
        if directory_is_writable(project_settings.default_website_filesystem_output_path) :
            message = "Setting filesystem output path to: " + project_settings.default_website_filesystem_output_path
            log.info(message)
            self.filesystem_path = project_settings.default_website_filesystem_output_path
            return
        #
        # Still here? Something went wrong. Complain.
        message = "Unable to set the GEMS Filesystem Output Path. \nForging ahead, but not optimistic about it."
        log.error(message)


### TODO - Make this not be a copy-pasta of the previous function. They can be merged. For code readability,
###        these separate names should still exist, but they should point to a single generic function.
###        I can't do this at the moment, and I'm not sure yet the extent to which these two functions truly
###        are analogous. (BLF 2026-01-17)
    def setUploadsPath(self, specifiedPath : str = None, noClobber : bool = True) :
        log.info("setUploadsPath was called.")
        # If a path exists, and it should not be clobbered, return
        # This **SHOULD** be the case if the incoming JSON object specified a path.
        # For this to be true, ensure that your outgoing project is deep-copied from 
        # your incoming project before calling this.
        context = getGemsExecutionContext()
        if self.uploads_path is None:
            self.uploads_path = ""  # shorten later if-thens
        IC = session_instance_config
        instanceConfigPath = IC.get_secure_inputs_path_by_service_ID(serviceID=self.service_id)
        message = "The instanceConfigPath returned was: "  + str(instanceConfigPath)
        log.debug(message)
        if noClobber is True :
            if self.uploads_path != ""  :
                message = "Uploads Path already exists in Project and cannot be clobbered.  It is:\n" + str(self.uploads_path)
                log.debug(message)
                if specifiedPath != None :
                    message = "Not clobbering uploads path specified in setUploadsPath.  It is:\n" + str(specifiedPath)
                    log.debug(message)
                if instanceConfigPath != None :
                    message = "Not clobbering uploads path specified in the instance config.  It is:\n" + str(instanceConfigPath)
                    log.debug(message)
                if context == 'website' :
                    message = "In website context, noClobber is set to True. Not overriding pre-set uploads_path."
                    log.info(message)
                return
        # If a path was specified, set it, if allowed, and return
        if context == 'website' :
            # TODO: collapse the next two into a single block
            if specifiedPath is not None :
                log.debug("An uploads path is specified in website context.  Checking to see if it is allowed." )
                log.debug("The specifiedPath is: " + str(specifiedPath))
                if specifiedPath == project_settings.default_website_filesystem_uploads_path :
                    message = "The output path is allowed.  Using it."
                    log.debug(message)
                    self.filesystem_path = specifiedPath
                    return
                else: 
                    message = "The output path is not allowed."
                    log.error(message)
            if instanceConfigPath is not None :
                log.debug("An output path is specified in website context.  Checking to see if it is allowed." )
                log.debug("The instanceConfigPath is: " + str(instanceConfigPath))
                if instanceConfigPath == project_settings.default_website_filesystem_uploads_path :
                    message = "The output path is allowed.  Using it."
                    log.debug(message)
                    self.filesystem_path = instanceConfigPath
                    return
                else: 
                    message = "The output path is not allowed."
                    log.error(message)
            self.uploads_path = project_settings.default_website_filesystem_uploads_path
            message = "Using the default GEMS Website Uploads Path: " + str(self.uploads_path)
            log.debug(message) 
            return
        # Still here? We are not a website. See what else we can do.
        if specifiedPath is not None :
            if directory_is_writable(specifiedPath) :
                self.uploads_path = specifiedPath
                message = "The specifiedPath is allowed.  Using it."
                log.debug(message) 
            else :
                message = "Cannot write to the specifiedPath: " + str(specifiedPath)
                log.error(message)
            return
        if instanceConfigPath is not None :
            if directory_is_writable(instanceConfigPath) :
                message = "The instanceConfigPath is allowed.  Using it."
                log.debug(message)
                self.uploads_path = instanceConfigPath
            else :
                message = "Cannot write to the instanceConfigPath: " + str(instanceConfigPath)
                log.error(message)
            return
        #
        # Try: 
        #     standalone uploads_path
        #     $HOME/GEMS_UserSpace
        #     $GEMSHOME/UserSpace
        #     website uploads_path
        #
        if directory_is_writable(project_settings.default_standalone_filesystem_uploads_path) :
            message = "Setting uploads path to: " + project_settings.default_standalone_filesystem_uploads_path
            log.info(message)
            self.uploads_path = project_settings.default_standalone_filesystem_uploads_path
            return
        userhome = os.environ.get("HOME")
        testdir = userhome + "/GEMS_UserSpace"
        if directory_is_writable(testdir, make_if_needed=True) :
            message = "Setting uploads path to: " + testdir
            log.info(message)
            self.uploads_path = testdir
            return
        gemshome = os.environ.get("GEMSHOME")
        testdir = gemshome + "/UserSpace"
        if directory_is_writable(testdir, make_if_needed=True) :
            message = "Setting uploads path to: " + testdir
            log.info(message)
            self.uploads_path = testdir
            return
        if directory_is_writable(project_settings.default_website_filesystem_uploads_path) :
            message = "Setting uploads path to: " + project_settings.default_website_filesystem_uploads_path
            log.info(message)
            self.uploads_path = project_settings.default_website_filesystem_uploads_path
            return
        #
        # Still here? Something went wrong. Complain.
        message = "Unable to set the GEMS Uploads Path. \nForging ahead, but not optimistic about it."
        log.error(message)



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
                self.parent_entity.lower(),
                self.service_id)
        ### the path used to be defined this way, but that was always a bug
        ### note that the checks above use the parent entity not the entity id
        #self.service_dir = os.path.join(
        #        self.filesystem_path,
        #        self.entity_id,
        #        self.service_id)
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
        if not directory_is_writable(self.project_dir) :
            message = "Unable to write to the project directory. \nForging ahead, but not optimistic about it."
            log.error(message)
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
        from gemsModules.project.utils import getVersionsFileInfo
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
        if getGemsExecutionContext() == 'website' :
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
            from gemsModules.project import projectUtilPydantic as utils
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
        from gemsModules.deprecated.common import settings as commonsettings
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
                from gemsModules.systemoperations.filesystem_ops import build_filesystem_path, copy_file_from_A_to_B
                source = build_filesystem_path(self.upload_path,self.uploaded_file_name)
                destination = build_filesystem_path(self.project_dir,self.uploaded_file_name)
                copy_file_from_A_to_B(source, destination)
                # was: commonlogic.copyPathFileToPath(self.upload_path, self.uploaded_file_name, self.project_dir)
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



def generateProjectSchema():
    print(Project.schema_json(indent=2))


