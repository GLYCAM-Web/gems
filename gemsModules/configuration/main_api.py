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
    host: str = "localhost"  # Must contain contact information
    hostName: str = "LocalHost"
    slurmport: Optional[str] = None
    contexts: List[SupportedExecutionContexts] = [ "Standalone" ]
    routes: Optional[List[str]] = None
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

    def get_filesystem_path_by_service_ID(self, serviceID: str):
        if self.filesystem_paths is None:
            return None
        sID=serviceID.lower()
        try:
            SupportedExecutionContexts[sID]
            log.debug("the serviceID is found in SupportedExecutionContexts.")
        except KeyError:
            log.debug("the serviceID is NOT found in SupportedExecutionContexts.")
            return None
        try:
            directory = self.filesystem_paths[SupportedExecutionContexts[sID]]
            log.debug("the serviceID is found in filesystem_paths.")
            return directory
        except KeyError:
            log.debug("the serviceID is NOT found in filesystem_paths.")
            return None

    def get_secure_inputs_path_by_service_ID(self, serviceID: str):
        if self.secure_inputs_paths is None:
            log.debug("self.secure_inputs_paths is None")
            return None
        sID=serviceID.lower()
        message = "the sID is " + sID
        log.debug(message)
        try:
            SupportedExecutionContexts[sID]
            log.debug("the serviceID is found in SupportedExecutionContexts.")
        except KeyError:
            log.debug("the serviceID is NOT found in SupportedExecutionContexts.")
            return None
        try:
            directory = self.secure_inputs_paths[SupportedExecutionContexts[sID]]
            log.debug("the serviceID is found in filesystem_paths.")
            return directory
        except KeyError:
            log.debug("the serviceID is NOT found in filesystem_paths.")
            return None

    def localhost_supports_context(self, context_names : List) -> bool :
        if self.hosts is None :
            return False
        for host_object in self.hosts.values() :
            if host_object.host == "localhost" :
                if any(item in context_names for item in host_object.contexts) :
                    return True
        return False



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


