""" DOCUMENTATION ONLY """

from pydantic import BaseModel
from typing import List, Dict, Optional

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class SbatchArguments(BaseModel):
    partition: str
    time: str
    nodes: str
    tasks_per_node: str


class LocalParameters(BaseModel):
    numProcs: str


class Host(BaseModel):
    host: str
    slurmport: Optional[str]
    contexts: List[str]
    routes: Optional[List[str]]
    sbatch_arguments: Optional[Dict[str, SbatchArguments]]
    local_parameters: Optional[Dict[str, LocalParameters]]


class Config(BaseModel):
    date: str
    hosts: Dict[str, Host]
    default_sbatch_arguments: Dict[str, SbatchArguments]
    default_local_parameters: Dict[str, LocalParameters]
    md_cluster_filesystem_path: str
