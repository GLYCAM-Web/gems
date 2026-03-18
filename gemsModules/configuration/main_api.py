from pydantic import BaseModel, ValidationError, Field
from typing import List, Dict, Literal, Optional, Any
from pathlib import Path
from enum import Enum

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class SupportedExecutionContexts(str, Enum) :
        ad = "AD"                  # Execution relevant to antibody docking (AAD2)
        devenv = "DevEnv"          # Execution in the GLYCAM-Web development platform
        freetier = "FreeTier"      # Batch computing job that is free
        gm = "GM"                  # Execution relevant to Glycomimetics
        gp = "GP"                  # Execution relevant to the GlycoProtein builder
        gr = "GR"                  # Execution relevant to Grafting / GlySpec
        md = "MD"                  # Execution relevant to Molecular Dynamics
        pdb = "PDB"                # Execution relevant to a PDB file
        cb = "CB"                  # Sequence builder (CB) - used to be "Sequence-Build3DStructure"
        shortjob = "ShortJob"      # Batch computing job that is short
        swarm = "Swarm"            # Execution in a cloud
        standalone = "Standalone"  # Local execution on command line
        website = "Website"        # Execution in the context of a website
        ## The following allow for backwards compatibility and some user-friendly verbosity
        cbAlso = "Sequence-Build3DStructure"
        gmAlso = "Glycomimetics"
        gpAlso = "GlycoProtein"
        mdAlso = "MDaaS-RunMD"
        adAlso = "AntibodyDocking"



class SbatchArguments(BaseModel):
    partition: str = None
    time: Optional[str]
    nodes: str = None
    tasks_per_node: str = None


class LocalParameters(BaseModel):
    numProcs: str


class Host(BaseModel):
    host: str = "localhost"  # Contact information for the host
    hostName: str = "Glycon" # Whatever the humans call this machine
    is_localhost : bool = True  # Be sure to set this for (only!) one host or many things will never happen
    slurmport: Optional[str] = None
    contexts: List[SupportedExecutionContexts] = [ "Standalone" ]
    routes: Optional[List[str]] = None
    ####
    context_options: Dict[SupportedExecutionContexts, Dict[str,str]] = None # These will vary with each app.
    # To be useful, these should correspond to options defined in the API for each entity/app.
    # They will be copied into the appropriate Project and presented to the entity.
    #
    # In general, the values used here will override whatever is found in a JSON object sent to the delegator.
    #     Caveats:
    #             - If this GEMS serves a website, 
    #                 - The values here will clobber values in the JSON if not dictated in the code.
    #                 - Values enforced in the code override everything.
    #             - If it is not serving a website, the incoming JSON values can be enforced if "use_api_strict=true".
    ####
    local_parameters: Optional[Dict[str, LocalParameters]]  = None # for example, number of procs
    sbatch_arguments: Optional[Dict[str, SbatchArguments]]  = None                    # only needed for batch execution
    cluster_filesystem_paths: Optional[Dict[SupportedExecutionContexts, str]]  = None # only needed for batch execution


class InstanceConfig(BaseModel):
    date: str = None
    hosts: Optional[Dict[str, Host]] = None
    default_sbatch_arguments: Optional[Dict[str, SbatchArguments]] = None
    default_local_parameters: Optional[Dict[str, LocalParameters]] = None
    filesystem_paths: Optional[Dict[SupportedExecutionContexts, str]]  = Field(
            default=None,
            Description="Local filesystem paths. If submitting to a cluster, where to drop files locally for transfer/sharing."
            )
    secure_inputs_paths: Optional[Dict[SupportedExecutionContexts, str]]  = Field(
            default=None,
            Description="Local secured space for storing uploads, sideloads, generic input. Assumed not visible to the cluster."
            )

    def get_localhost() -> Host :
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

    def get_localhost_hostName() -> str :
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
        serviceID must be a member of the SupportedExecutionContexts enum.
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
        log.info("get_filesystem_path_by_service_ID is called.")
        if self.filesystem_paths is None:
            log.debug("self.filesystem_paths is None")
            return None
        sID=serviceID.lower()
        sIDAlso = f"{sID}Also"
        try:
            SupportedExecutionContexts[sID] or SupportedExecutionContexts[sIDAlso] 
            log.debug("the serviceID is found in SupportedExecutionContexts.")
        except KeyError:
            message = f"The serviceID {serviceID} is NOT found in SupportedExecutionContexts."
            log.debug(message)
            raise KeyError (message)

        keys_to_check = [ sID, SIDAlso ]
        directory = next((self.filesystem_paths[SupportedExecutionContexts[key]] \
            for key in keys_to_check if key in self.filesystem_paths[SupportedExecutionContexts]), \
            'Not Found')
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
            SupportedExecutionContexts[sID] or SupportedExecutionContexts[sIDAlso] 
            log.debug("the serviceID is found in SupportedExecutionContexts.")
        except KeyError:
            message = f"The serviceID {serviceID} is NOT found in SupportedExecutionContexts."
            log.debug(message)
            raise KeyError (message)

        keys_to_check = [ sID, SIDAlso ]
        directory = next((self.secure_inputs_paths[SupportedExecutionContexts[key]] \
            for key in keys_to_check if key in self.secure_inputs_paths[SupportedExecutionContexts]), \
            'Not Found')
        if directory == 'Not Found' :
            log.debug("the serviceID is NOT found in secure_inputs_paths.")
            return None
        return directory


def load_instance_config(icFilePath: str = None):
    import os
    import json
    import pathlib
    from gemsModules.systemoperations.environment_ops import find_instance_config
    if icFilePath is None :
        #icPath =  pathlib.Path(os.getenv("GEMSHOME", "")) / "instance_config.json"
        icPath = pathlib.Path(find_instance_config())
    else :
        icPath = pathlib.Path(icFilePath)
    message = "The path of the file is: " + str(icPath) 
    log.debug(message)
    json_string = pathlib.Path(icPath).read_text()
    log.debug("The json string is:")
    log.debug(json_string)
    thisConfig = InstanceConfig.parse_file(icPath)
    log.debug("This is a dump of the newly read config")
    log.debug(str(thisConfig.json(indent=2)))
    return thisConfig


def generateSchema():
    import json
    print(Config.schema_json(indent=2))

def read_IC_from_file():
    import pathlib
    #json_string = pathlib.Path('tests/cluster_ic.json').read_text()
    json_string = pathlib.Path('temp.json').read_text()
    return InstanceConfig.parse_raw(json_string, encoding='json')
    

if __name__ == "__main__":
  #generateSchema()
  #thisConfig = read_IC_from_file()
  #print(thisConfig.model_dump_json(indent=2))
  thisConfig = load_instance_config()
  print(thisConfig.json(indent=2))


