from functools import lru_cache
from pydantic import BaseModel, ValidationError, Field
from typing import List, Dict, Literal, Optional, Any
from enum import Enum

from gemsModules.common.code_utils import GemsStrEnum
from gemsModules.configuration.resource_management_api import Resource_Specific_Information_Registry

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

#### 
## The next few classes are used to declare the execution contexts for a host.
##
## The host can be the local host or a remote host to which a job is delegated.
#### 
class SupportedEntities(GemsStrEnum):
    """
    Each key must match a service_id as defined in the relevant gemsModule.
    The 'service_id' designation is historically named and misleading. It corresponds to an Entity.
    The upper-case value is the form that should appear in the instance_config.json file.
    """
    ad = "AD"                  # Execution relevant to antibody docking (AAD2)
    bc = "BC"                  # Submit a computationally intensive job to the scheduler of an HPC cluster
    cb = "CB"                  # Sequence builder (CB) - used to be "Sequence-Build3DStructure"
    gm = "GM"                  # Execution relevant to Glycomimetics
    gp = "GP"                  # Execution relevant to the GlycoProtein Entity
    gr = "GR"                  # Execution relevant to Grafting, now known as GlySpec
    md = "MD"                  # Execution relevant to Molecular Dynamics
    pdb = "PDB"                # Execution relevant to a PDB file
    @property
    def description(self) -> str:
        descriptions = {
            Status.ad: "Execution relevant to antibody docking (AAD2)"
            Status.bc: "Submit a computationally intensive job to the scheduler of an HPC cluster"
            Status.cb: "Sequence builder (CB) - used to be 'Sequence-Build3DStructure'"
            Status.gm: "Execution relevant to Glycomimetics"
            Status.gp: "Execution relevant to the GlycoProtein Entity"
            Status.gr: "Execution relevant to Grafting, now known as GlySpec"
            Status.md: "Execution relevant to Molecular Dynamics"
            Status.pdb: "Execution relevant to a PDB file"
        }
        return descriptions[self]

class ExecutionEnvironments(GemsStrEnum):
    """
    Allowed ways to run jobs on a specific host.
    """
    swarm = "Swarm"            # Execution in a Docker Swarm-mode cloud
    batch = "Batch"            # Execution via a Batch computing scheduler
    docker = "Docker"          # Execution via Docker
    nodedocker = "NodeDocker"  # Execution via Docker on the compute nodes
    relay = "Relay"            # Ability to relay jobs to other environments
    standalone = "Standalone"  # Local execution on the command line or as a library
    website = "Website"        # Execution on behalf of a website, directly or not
    @property
    def description(self) -> str:
        descriptions = {
            Status.swarm: "Execution in a Docker Swarm-mode cloud"
            Status.batch: "Execution via a Batch computing scheduler"
            Status.docker: "Execution via Docker"
            Status.nodedocker: "Execution via Docker on the compute nodes"
            Status.relay: "Ability to relay jobs to other environments"
            Status.standalone: "Local execution on the command line or as a library"
            Status.website: "Execution on behalf of a website, directly or not"
        }
        return descriptions[self]
    
class WebsiteEnvironments(GemsStrEnum):
    """
    If this GEMS is directly serving a website, what is the role of the website?
    Note that this does not apply to remote hosts that provide services to the website.
    """
    actual = "Actual"          # Execution in the context of the main website
    dev = "Dev"                # Execution in the context of the move-in-swarm-testing website
    test = "Test"              # Execution in the context of the test website
    swarmtest = "SwarmTest"    # Execution in the context of the swarmtest website
    devenv = "DevEnv"          # Execution in the GLYCAM-Web development platform
    @property
    def description(self) -> str:
        descriptions = {
            Status.actual: "Execution in the context of the main website"
            Status.dev: "Execution in the context of the move-in-swarm-testing website"
            Status.test: "Execution in the context of the test website"
            Status.swarmtest: "Execution in the context of the swarmtest website"
            Status.devenv: "Execution in the GLYCAM-Web development platform"
        }
        return descriptions[self]
    

class BatchComputingResources(BaseModel):
    partition: str = Field( 
            None, 
            alias='partition',
            description="The partition or queue that provides the resources in this set."
            ) 
    supported_entities: List[SupportedEntities] = Field(
            None,
            description="The list of Entities, in upper-case service_id format, that this partition supports."
            )
    max_nodes_per_job: str = Field(
            None,
            description="The maximum number of nodes that can be reserved per job in this partition",
            )
    max_cores_per_node: str = Field(
            None,
            description="The maximum number of cores that can be reserved per node in this partition",
            )
    max_threads_per_node: str = Field(
            None,
            description="",
            description="The maximum number of threads that can be reserved per node in this partition",
            )
    max_gpus_per_node: str = Field(
            None,
            description="",
            description="The maximum number of gpus that can be reserved per node in this partition",
            )
    max_cpus_per_gpu: str = Field(
            "1",
            description="The maximum number of cpus (cores or threads) that can be reserved per gpu in this partition",
            )
    max_time_limit: str = Field(
            None,
            description = "Computing time limit in ISO 8601 format. Example: 2 days, 16 hours and 30 minutes = P2DT16H30M"
            )


class Host(BaseModel):
    ######################################################################
    ######################################################################
    ###!!!!! these fields have changed. Update the code.
    #
    # Was 'hostName'
    name: str = Field(
            "Glycon",
            description="Whatever the humans call this machine.",
            )
    # Was 'host', but was always really the address of a host. This is a better name.
    address: str = Field(
            "localhost",
            description="Networking contact information for the host, e.g.: 127.0.0.1, 172.16.0.200, example.com"
            )
    # Was 'slurmport', but we want to stop using 'slurmreceive' and use only gRPC/JSON for comunication,
    #      so the generic 'port' is better. Any code using gRPC/JSON or gRPC/SLURM should be updated.
    port: Optional[str] = Field(
            None,
            description="The gRPC port that should be used to connect to this GEMS instance.",
            )
    # Was: 'sbatch_arguments'
    scheduler: Optional[str] = Field(
            None,  
            description="The type of scheduler used on this host, e.g., 'slurm'.",
            )
    batch_computing_resources: Optional[List[BatchComputingResources]] = Field(
            None,
            description="For each partition/queue, what resources are available and which Entities are supported?",
            )
    ## For safety, the following should employ a custom validator based on the value of 'scheduler'
    ## The pseudo-code below is for clarification only. See also comments in resource_management_api.py
    ## The schema should be imported from resource_management_api.py
    resource_specific_information: Optional[Resource_Specific_Information_Registry(scheduler)]  = Field(
            None,
            description="Information needed by Batch Compute that is set during scheduler configuration and cannot be guessed otherwise.",
            )
    ######################################################################
    ######################################################################
    is_localhost : str = Field(
            "True",
            description="Be sure to set this to 'true' for (only!) one host or many things will never happen.",
            )
    entities_available: List[SupportedEntities] = Field(
            None,
            description="The Entities whose services can run on this host.",
            )
    execution_environments: List[ExecutionEnvironments] = Field(
            [ "Standalone" ],
            description="The ways that Services can be executed on this host.",
            )
    website_environments: List[WebsiteEnvironments] = Field(
            None,
            description="If this GEMS serves a website, which variant of the website is being served?",
            )


class InstanceConfig(BaseModel):
    date: str = Field(
            None,
            description="This date-time field will be set when this IC is written. Pre-existing values will be overwritten.",
            )
    hosts: Optional[List[Host]] = Field(
            None,
            description="List of Hosts that are contained in this IC.",
            )
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
    filesystem_paths:Optional[Dict[SupportedEntities, str]]  = Field(
            default=None,
            Description="Local filesystem paths for each Entity supported by any Host in this IC. If submitting to a cluster, where to drop files locally for transfer/sharing/reading."
            )
    secure_inputs_paths: Optional[Dict[SupportedEntities, str]]  = Field(
            default=None,
            Description="Local secured and sanitized space for storing uploads, sideloads, generic input. Must be included for each Entity supported by any Host in this IC that requires input from a user or external source."
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
        serviceID must be a member of the SupportedEntities enum.
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
        ## Syntactic sugar to correspond to SupportedEntities structure
        sID_Key   = serviceID
        try:
            SupportedEntities[sID] 
            log.debug("the serviceID is found in SupportedEntities.")
        except KeyError:
            message = f"The serviceID {serviceID} is NOT found in SupportedEntities."
            log.debug(message)
            raise KeyError (message)
        directory='Not Found'
        the_index = SupportedEntities[key].value
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
            SupportedEntities[sID] or SupportedEntities[sIDAlso] 
            log.debug("the serviceID is found in SupportedEntities.")
        except KeyError:
            message = f"The serviceID {serviceID} is NOT found in SupportedEntities."
            log.debug(message)
            raise KeyError (message)

        keys_to_check = [ sID, sIDAlso ]
        directory = next((self.secure_inputs_paths[SupportedEntities[key]] \
            for key in keys_to_check if key in self.secure_inputs_paths[SupportedEntities]), \
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


