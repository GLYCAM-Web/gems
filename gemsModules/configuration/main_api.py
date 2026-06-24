from functools import lru_cache
from pydantic import BaseModel, ValidationError, Field
from typing import List, Dict, Literal, Optional, Any
from enum import Enum

from gemsModules.common.code_utils import GemsStrEnum
from gemsModules.configuration.resource_management_api import Resource_Specific_Information_Registry

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

#### 
## The next few classes are used to declare the supported execution contexts for a host.
##
## The host can be the local host or a remote host to which a job is delegated.
#### 
class SupportedServices(GemsStrEnum):
    """
    Each key must match a service_id as defined in the relevant gemsModule.
    The value is the form that should appear in the instance_config.json file.
    """
    ad = "AD"                  # Execution relevant to antibody docking (AAD2)
    bc = "BC"                  # Submit a computationally intensive job to the scheduler of an HPC cluster
    cb = "CB"                  # Sequence builder (CB) - used to be "Sequence-Build3DStructure"
    gm = "GM"                  # Execution relevant to Glycomimetics
    gp = "GP"                  # Execution relevant to the GlycoProtein builder
    gr = "GR"                  # Execution relevant to Grafting, now known as GlySpec
    md = "MD"                  # Execution relevant to Molecular Dynamics
    pdb = "PDB"                # Execution relevant to a PDB file
class ExecutionEnvironments(GemsStrEnum):
    swarm = "Swarm"            # Execution in a Docker Swarm-mode cloud
    batch = "Batch"            # Execution via a Batch computing scheduler
    docker = "Docker"          # Execution via Docker
    nodedocker = "NodeDocker"  # Execution via Docker on the compute nodes
    relay = "Relay"            # Ability to relay jobs to other environments
    standalone = "Standalone"  # Local execution on the command line or as a library
    website = "Website"        # Execution on behalf of a website, directly or not
class WebsiteEnvironments(GemsStrEnum):
    actual = "Actual"          # Execution in the context of the main website
    dev = "Dev"                # Execution in the context of the move-in-swarm-testing website
    test = "Test"              # Execution in the context of the test website
    swarmtest = "SwarmTest"    # Execution in the context of the swarmtest website
    devenv = "DevEnv"          # Execution in the GLYCAM-Web development platform



class BatchComputingResources(BaseModel):
    partition: str = Field("All", alias='partition') ## by default applies to all partitions
    supported_services: List[SupportedServices]: None
    cpu_hardware_equivalent: str = "core"   ## is a CPU considered to be a core or a thread?
    max_cores: str = None      
    max_threads: str = None    
    max_gpus: str = None       
    max_cpus_per_gpu: str = "1" 
    max_time_limit: str = Field(
            None,
            description = "Computing time limit in ISO 8601 format. Example: 2 days, 16 hours and 30 minutes = P2DT16H30M "
            )


class Host(BaseModel):
    ######################################################################
    ######################################################################
    ###!!!!! these fields have changed. Update the code.
    #
    # Was 'host', but was always really the address of a host. This is a better name.
    address: str = "localhost"  # Networking contact information for the host, e.g.: 127.0.0.1, localhost, example.com
    # Was 'slurmport', but we want to stop using 'slurmreceive' and use only gRPC/JSON for comunication,
    #      so the generic 'port' is better. Any code using gRPC/JSON or gRPC/SLURM should be updated.
    port: Optional[str] = None
    # Was 'hostName'
    name: str = "Glycon" # Whatever the humans call this machine
    # Was: 'sbatch_arguments'
    #     Because we want to support schedulers other than slurm, we need more information
    #     The following code is probably incorrect, but perhaps the desired behavior is clear enough
    #     We still want a nested dictionary, but it needs to be much more flexible
    #     The presence of "scheduler" helps the code know which dictionary to return and can be used
    #     in Batch Compute to know which set of tasks should be assigned to a service.
    scheduler: Optional[str] = None  # e.g., 'slurm' or 'torque'
    resource_specific_information: Optional[Resource_Specific_Information_Registry(scheduler)]  = None  
    ######################################################################
    ######################################################################
    is_localhost : str = "True"  # Be sure to set this for (only!) one host or many things will never happen
    services_available: List[SupportedServices] = None
    execution_environments: List[ExecutionEnvironments] = [ "Standalone" ]
    website_environments: List[WebsiteEnvironments] = None


class InstanceConfig(BaseModel):
    date: str = None
    hosts: Optional[Dict[str, Host]] = None
    ####
    ##   Design notes for future development
    ##
    ##   The next two dictionaries are sufficient for the current needs of the website. The directories are mounted 
    ##   into a predictable location inside a Docker container. 
    ##
    ##   In the future, it might make more sense to add Resources to the services for each host. These existing paths
    ##   can be used as fallback defaults, etc.
    ##
    ##   Resources are useful because the higher-level code does not need to care about the nature of the source or
    ##   the destination for files or directories. The Resource contains the needed information. Because of this, a
    ##   file on a website can be copied into a local directory without the higher-level code knowing that the file
    ##   originated from a website or was copied into a local directory. 
    ##
    ##   The methods available to a Resource can also be extended as needed, for example to access an object store
    ##   or to provide credentials.
    ##
    ##   See: gemsModules/common/main_api_resources.py and any code that references it.
    ##
    ####
    filesystem_paths:Optional[Dict[SupportedServices, str]]  = Field(
            default=None,
            Description="Local filesystem paths. If submitting to a cluster, where to drop files locally for transfer/sharing."
            )
    secure_inputs_paths: Optional[Dict[SupportedServices, str]]  = Field(
            default=None,
            Description="Local secured space for storing uploads, sideloads, generic input. Assumed sanitized for input as needed."
            )

    def get_localhost(self) -> Host :
        """ 
        Return the localhost's Host object
        """
        log.info("get_localhost was called")
        if self.hosts is None :
            return None
        for host_object in self.hosts.values() :
            if host_object.is_localhost :
                return host_object
        log.error("Cannot find localhost.")
        return None

    def get_localhost_hostName(self) -> str :
        """
        Return the hostName in the Host object
        """
        log.info("get_localhost_hostName was called")
        the_local_host = self.get_localhost()
        if the_local_host is None :
            return None
        return the_local_host.hostName


    def localhost_supports_context(self, context_names : List) -> bool :
        """ 
        Return True if the local host supports the requested context.
        context_names is a list of possible names, including short names, e.g., ["AD", "AntibodyDocking"]
        """
        log.info("localhost_supports_context was called")
        the_local_host = self.get_localhost()
        if the_local_host is None :
            return False
        if any(item in context_names for item in the_local_host.contexts) :
            return True
        return False

    def get_localhost_supported_contexts(self) -> bool :
        """ 
        Return the contexts supported by the localhost
        """
        log.info("get_localhost_supported_contexts was called")
        the_local_host = self.get_localhost()
        if the_local_host is None :
            return None
        return host_object.contexts

    def get_localhost_context_options_by_service_ID(self, serviceID: str):
        """ 
        Return the localhost's context_options for the requested service
        serviceID is the same as in service_id the Project class.
        serviceID must be a member of the SupportedServices enum.
        """
        log.info("get_localhost_context_options_by_service_ID was called")
        the_local_host = self.get_localhost()
        if the_local_host is None :
            return None
        if the_local_host.context_options is None:
            log.debug("local host has no context options defined.")
            return None
        if serviceID not in the_local_host.context_options.keys() :
            log.debug(f"local host has no context options defined for serviceID {serviceID}.")
            return None
        these_options=the_local_host.context_options[serviceID]
        log.debug(f"context_options for {serviceID} on {local_host.hostName} are:")
        log.debug(f"{these_options}")
        return these_options

    def get_filesystem_path_by_service_ID(self, serviceID: str):

######
######  This logic is not quite on target because too many targets
######
######  Reducing target count...
######
        log.info("get_filesystem_path_by_service_ID is called.")
        if self.filesystem_paths is None:
            log.debug("self.filesystem_paths is None")
            return None
        ## Syntactic sugar to correspond to SupportedServices structure
        sID_Key   = serviceID
        try:
            SupportedServices[sID] 
            log.debug("the serviceID is found in SupportedServices.")
        except KeyError:
            message = f"The serviceID {serviceID} is NOT found in SupportedServices."
            log.debug(message)
            raise KeyError (message)
        directory='Not Found'
        the_index = SupportedServices[key].value
        #print("the index is: " + the_index)
        if self.filesystem_paths[the_index] not in (None,""):
            directory = self.filesystem_paths[the_index]

        if directory == 'Not Found' :
            log.debug("the serviceID is NOT found in filesystem_paths.")
            return None
        return directory

    def get_secure_inputs_path_by_service_ID(self, serviceID: str):
        log.info("get_secure_inputs_path_by_service_ID is called.")
        if self.secure_inputs_paths is None:
            log.debug("self.secure_inputs_paths is None")
            return None
        sID=serviceID.lower()
        sIDAlso = f"{sID}Also"
        #message = "the sID is " + sID
        #log.debug(message)
        try:
            SupportedServices[sID] or SupportedServices[sIDAlso] 
            log.debug("the serviceID is found in SupportedServices.")
        except KeyError:
            message = f"The serviceID {serviceID} is NOT found in SupportedServices."
            log.debug(message)
            raise KeyError (message)

        keys_to_check = [ sID, sIDAlso ]
        directory = next((self.secure_inputs_paths[SupportedServices[key]] \
            for key in keys_to_check if key in self.secure_inputs_paths[SupportedServices]), \
            'Not Found')
        if directory == 'Not Found' :
            log.debug("the serviceID is NOT found in secure_inputs_paths.")
            return None
        return directory


@lru_cache(maxsize=1) ## Ensure that this is only loaded once in a given session
def _load_instance_config(icFilePath: str = None) -> InstanceConfig :
    import os
    import json
    import pathlib
    from gemsModules.systemoperations.environment_ops import find_instance_config
    if icFilePath is None :
        icPath = pathlib.Path(find_instance_config())
    else :
        icPath = pathlib.Path(icFilePath)
    message = "The path (icPath) of the instance config file is: " + str(icPath) 
    log.debug(message)
    if not icPath.exists():
        raise ValueError("The instance config file does not exist.")
    try:
        json_string = pathlib.Path(icPath).read_text()
        log.debug("The json string is:")
        log.debug(json_string)
        thisConfig = InstanceConfig.parse_file(icPath)
    except Exception:
        raise
    log.debug("This is a dump of the newly read config")
    log.debug(str(thisConfig.json(indent=2)))
    return thisConfig

## Instantiate the main instance config (GEMSHOME/instance_config.json)
## Import this from anywhere else.
session_instance_config = _load_instance_config()

def generateSchema():
    import json
    print(Config.schema_json(indent=2))


if __name__ == "__main__":
    #generateSchema()
    thisConfig = _load_instance_config()
    print(thisConfig.json(indent=2))


