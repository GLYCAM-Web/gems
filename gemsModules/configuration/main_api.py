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
            SupportedEntities.ad: "Execution relevant to antibody docking (AAD2)",
            SupportedEntities.bc: "Submit a computationally intensive job to the scheduler of an HPC cluster",
            SupportedEntities.cb: "Sequence builder (CB) - used to be 'Sequence-Build3DStructure'",
            SupportedEntities.gm: "Execution relevant to Glycomimetics",
            SupportedEntities.gp: "Execution relevant to the GlycoProtein Entity",
            SupportedEntities.gr: "Execution relevant to Grafting, now known as GlySpec",
            SupportedEntities.md: "Execution relevant to Molecular Dynamics",
            SupportedEntities.pdb: "Execution relevant to a PDB file",
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
            ExecutionEnvironments.swarm: "Execution in a Docker Swarm-mode cloud",
            ExecutionEnvironments.batch: "Execution via a Batch computing scheduler",
            ExecutionEnvironments.docker: "Execution via Docker",
            ExecutionEnvironments.nodedocker: "Execution via Docker on the compute nodes",
            ExecutionEnvironments.relay: "Ability to relay jobs to other environments",
            ExecutionEnvironments.standalone: "Local execution on the command line or as a library",
            ExecutionEnvironments.website: "Execution on behalf of a website, directly or not",
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
            WebsiteEnvironments.actual: "Execution in the context of the main website",
            WebsiteEnvironments.dev: "Execution in the context of the move-in-swarm-testing website",
            WebsiteEnvironments.test: "Execution in the context of the test website",
            WebsiteEnvironments.swarmtest: "Execution in the context of the swarmtest website",
            WebsiteEnvironments.devenv: "Execution in the GLYCAM-Web development platform",
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
         description="The maximum number of threads that can be reserved per node in this partition",
         )
    max_gpus_per_node: str = Field(
         None,
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
    ## The schema should be imported from resource_management_api.py
    resource_specific_information: Optional[Any]  = Field(
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

    from pydantic import validator

    @validator('resource_specific_information', pre=True)
    def validate_resource_specific_information(cls, v, values):
        scheduler = values.get('scheduler')
        if not scheduler or v is None:
            return v
        sch_key = scheduler.lower()
        if sch_key in Resource_Specific_Information_Registry:
            model_cls = Resource_Specific_Information_Registry[sch_key]
            if isinstance(v, dict):
                return model_cls(**v)
        return v


class InstanceConfig(BaseModel):
    date: str = Field(
            None,
            description="This date-time field will be set when this IC is written. Pre-existing values will be overwritten.",
            )
    hosts: Optional[List[Host]] = Field(
            None,
            description="List of Hosts that are contained in this IC.",
            )

    from pydantic import validator

    @validator('hosts', pre=True)
    def validate_hosts(cls, v):
        if isinstance(v, dict):
            hosts_list = []
            for name, host_dict in v.items():
                if not isinstance(host_dict, dict):
                    continue
                h = host_dict.copy()
                if "name" not in h:
                    h["name"] = name
                if "host" in h:
                    h["address"] = h.pop("host")
                if "slurmport" in h:
                    h["port"] = h.pop("slurmport")
                if "contexts" in h:
                    h["entities_available"] = h.pop("contexts")
                
                # Coerce contexts to SupportedEntities enums where possible
                if h.get("entities_available"):
                    clean_entities = []
                    legacy_map = {
                        "MDaaS-RunMD": "MD",
                        "Sequence-Build3DStructure": "CB",
                        "AntibodyDocking": "AD",
                        "Glycomimetics": "GM",
                        "GlycoProtein": "GP",
                    }
                    for ent in h["entities_available"]:
                        norm = legacy_map.get(ent, ent)
                        # Check enum
                        for enum_member in SupportedEntities:
                            if enum_member.value == norm or enum_member.name == norm.lower():
                                clean_entities.append(enum_member)
                                break
                    h["entities_available"] = clean_entities

                scheduler = h.get("scheduler")
                if not scheduler and ("sbatch_arguments" in h or h.get("port") in ("50052", "42029")):
                    h["scheduler"] = "slurm"
                    scheduler = "slurm"
                
                if scheduler == "slurm" and "resource_specific_information" not in h:
                    slurm_info = {}
                    # Look up from old sbatch_arguments or local_parameters if any info is there
                    sbatch = h.get("sbatch_arguments", {})
                    # For MD context or defaults
                    md_args = sbatch.get("MD", {}) or sbatch.get("Default", {})
                    if md_args:
                        slurm_info["use_gres_for_gpus"] = "True" if "gres" in md_args else "False"
                    h["resource_specific_information"] = slurm_info
                
                hosts_list.append(h)
            return hosts_list
        return v

    @validator('filesystem_paths', 'secure_inputs_paths', pre=True)
    def validate_paths_dict(cls, v):
        if isinstance(v, dict):
            new_dict = {}
            for k, val in v.items():
                legacy_map = {
                    "MDaaS-RunMD": "MD",
                    "Sequence-Build3DStructure": "CB",
                    "AntibodyDocking": "AD",
                    "Glycomimetics": "GM",
                    "GlycoProtein": "GP",
                }
                norm_key = legacy_map.get(k, k)
                entity = None
                for e in SupportedEntities:
                    if e.value == norm_key or e.name == norm_key.lower():
                        entity = e
                        break
                if entity:
                    new_dict[entity] = val
                else:
                    new_dict[k] = val
            return new_dict
        return v
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
        for host_object in self.hosts :
            if str(host_object.is_localhost).lower() == "true":
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
        return the_local_host.name


    def localhost_supports_context(self, context_names : List) -> bool :
        """ 
        Return True if the local host supports the requested context.
        context_names is a list of possible names, including short names, e.g., ["AD", "AntibodyDocking"]
        """
        log.info("localhost_supports_context was called")
        the_local_host = self.get_localhost()
        if the_local_host is None or the_local_host.entities_available is None :
            return False
        for entity in the_local_host.entities_available:
            if entity.value in context_names or entity.name in context_names:
                return True
        return False

    def get_localhost_supported_contexts(self) -> List[str] :
        """ 
        Return the contexts supported by the localhost
        """
        log.info("get_localhost_supported_contexts was called")
        the_local_host = self.get_localhost()
        if the_local_host is None or the_local_host.entities_available is None :
            return None
        return [entity.value for entity in the_local_host.entities_available]

    def get_localhost_context_options_by_service_ID(self, serviceID: str):
        """ 
        Return the localhost's context_options for the requested service (Placeholder)
        """
        log.info("get_localhost_context_options_by_service_ID was called")
        return None

    def get_filesystem_path_by_service_ID(self, serviceID: str):
        log.info("get_filesystem_path_by_service_ID is called.")
        if self.filesystem_paths is None:
            log.debug("self.filesystem_paths is None")
            return None
        entity = None
        for e in SupportedEntities:
            if e.value == serviceID or e.name == serviceID.lower():
                entity = e
                break
        if entity is None:
            message = f"The serviceID {serviceID} is NOT found in SupportedEntities."
            log.debug(message)
            raise KeyError(message)
        
        if entity not in self.filesystem_paths:
            log.debug("the serviceID is NOT found in filesystem_paths.")
            return None
        return self.filesystem_paths[entity]

    def get_secure_inputs_path_by_service_ID(self, serviceID: str):
        log.info("get_secure_inputs_path_by_service_ID is called.")
        if self.secure_inputs_paths is None:
            log.debug("self.secure_inputs_paths is None")
            return None
        entity = None
        for e in SupportedEntities:
            if e.value == serviceID or e.name == serviceID.lower():
                entity = e
                break
        if entity is None:
            message = f"The serviceID {serviceID} is NOT found in SupportedEntities."
            log.debug(message)
            raise KeyError(message)
            
        if entity not in self.secure_inputs_paths:
            log.debug("the serviceID is NOT found in secure_inputs_paths.")
            return None
        return self.secure_inputs_paths[entity]

    def check_remote_host_connectivity(self, host_name: str) -> Dict[str, Any]:
        """
        Check connectivity using gRPC/JSON with Delegator's Marco Service
        """
        log.info(f"Checking connectivity for remote host: {host_name}")
        target_host = None
        if self.hosts:
            for host in self.hosts:
                if host.name == host_name:
                    target_host = host
                    break
        if not target_host:
            return {"Error": f"Host {host_name} not found in configuration."}
        
        if not target_host.port:
            return {"Error": f"Host {host_name} has no port configured."}
            
        from gemsModules.networkconnections.grpc import json_grpc_submit
        import json
        
        # Build a standard Marco explicit request
        marco_req = {
            "entity": {
                "type": "Delegator",
                "requests": {
                    "Marco": {
                        "type": "Marco",
                        "inputs": {
                            "message": "Polo"
                        }
                    }
                }
            }
        }
        
        try:
            res_str = json_grpc_submit(json.dumps(marco_req), host=target_host.address, port=target_host.port)
            res = json.loads(res_str)
            return {"status": "success", "response": res}
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def confirm_remote_host_capabilities(self, host_name: str) -> Dict[str, Any]:
        """
        Confirm remote host capabilities using Delegator's Check Configuration Service (placeholder)
        """
        log.info(f"Confirming capabilities for remote host: {host_name}")
        return {"status": "success", "message": f"Placeholder: capabilities confirmed for {host_name}"}

    def get_possible_hosts_for_context(
        self, context: str, with_slurmport=False, with_jsonport=False, return_names=False
    ) -> list:
        # Map legacy/alternate context names to SupportedEntities
        mapping = {
            "MDaaS-RunMD": "MD",
            "Sequence-Build3DStructure": "CB",
            "AntibodyDocking": "AD",
            "Glycomimetics": "GM",
            "GlycoProtein": "GP",
        }
        normalized_context = mapping.get(context, context)
        
        possible_hosts = []
        if self.hosts is None:
            return possible_hosts
            
        for host in self.hosts:
            if host.entities_available:
                for entity in host.entities_available:
                    if entity.value == normalized_context or entity.name == normalized_context.lower():
                        if return_names:
                            possible_hosts.append(host.name)
                        else:
                            if host.port:
                                possible_hosts.append(f"{host.address}:{host.port}")
                            else:
                                possible_hosts.append(host.address)
                        break
        return possible_hosts

    def get_available_contexts(self, instance_hostname=None) -> list:
        import socket
        if instance_hostname is None:
            instance_hostname = socket.gethostname()
            
        available_contexts = []
        if self.hosts:
            for host in self.hosts:
                # Matches either host name or address
                if instance_hostname == host.name or instance_hostname == host.address or (instance_hostname == "localhost" and str(host.is_localhost).lower() == "true"):
                    if host.entities_available:
                        for e in host.entities_available:
                            available_contexts.append(e.value)
                            available_contexts.append(e.name)
                            # map legacy names
                            legacy = {
                                "MD": "MDaaS-RunMD",
                                "CB": "Sequence-Build3DStructure",
                                "AD": "AntibodyDocking",
                                "GM": "Glycomimetics",
                                "GP": "GlycoProtein",
                            }
                            if e.value in legacy:
                                available_contexts.append(legacy[e.value])
        return list(set(available_contexts))


@lru_cache(maxsize=1) ## Ensure that this is only loaded once in a given session
def _load_instance_config(icFilePath: str = None) -> InstanceConfig :
    import os
    import json
    import pathlib
    from gemsModules.systemoperations.environment_ops import find_instance_config
    try:
        if icFilePath is None :
            icPath = pathlib.Path(find_instance_config())
        else :
            icPath = pathlib.Path(icFilePath)
    except Exception:
        log.warning("No instance configuration file found. Returning empty InstanceConfig.")
        return InstanceConfig()
        
    message = "The path (icPath) of the instance config file is: " + str(icPath) 
    log.debug(message)
    if not icPath.exists():
        log.warning("The instance config file does not exist. Returning empty InstanceConfig.")
        return InstanceConfig()
    try:
        json_string = pathlib.Path(icPath).read_text()
        log.debug("The json string is:")
        log.debug(json_string)
        thisConfig = InstanceConfig.parse_file(icPath)
    except Exception as e:
        log.warning(f"Error parsing instance config file: {e}. Returning empty InstanceConfig.")
        return InstanceConfig()
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


