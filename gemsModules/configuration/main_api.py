from pydantic import BaseModel, ValidationError, Field
from typing import List, Dict, Literal, Optional
from enum import Enum

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class SupportedExecutionContexts(str, Enum) :
        ad = "AD"                         # Execution relevant to antibody docking (AAD2)
        devenv = "DevEnv"                     # Execution in the GLYCAM-Web development platform
        freetier = "FreeTier"                   # Batch computing job that is free
        gm = "GM"                         # Execution relevant to Glycomimetics
        gp = "GP"                         # Execution relevant to the GlycoProtein builder
        gr = "GR"                         # Execution relevant to Grafting / GlySpec
        md = "MD"                         # Execution relevant to Molecular Dynamics
        pdb = "PDB"                         # Execution relevant to a PDB file
        cb = "Sequence-Build3DStructure"  # Sequence builder (CB)
        shortjob = "ShortJob"                   # Batch computing job that is short
        swarm = "Swarm"                      # Execution in a cloud
        standalone = "Standalone"                 # Local execution on command line
        uploads = "Uploads"                     # Non-project-dir location of input files from somewhere
        

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


class Config(BaseModel):
    date: str
    hosts: Optional[Dict[str, Host]] = None
    default_sbatch_arguments: Optional[Dict[str, SbatchArguments]] = None
    default_local_parameters: Optional[Dict[str, LocalParameters]] = None
    filesystem_paths: Optional[Dict[SupportedExecutionContexts, str]]  = Field(
            default=None,
            Description="Local filesystem paths. If submitting to a cluster, where to drop files locally for transfer/sharing."
            )

def generateSchema():
    import json
    print(Config.schema_json(indent=2))

def read_IC_from_file():
    import pathlib
    json_string = pathlib.Path('tests/cluster_ic.json').read_text()
    return Config.model_validate_json(json_string)
    

if __name__ == "__main__":
  #generateSchema()
  thisConfig = read_IC_from_file()
  print(thisConfig.model_dump_json(indent=2))


