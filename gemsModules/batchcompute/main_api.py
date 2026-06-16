#!/usr/bin/env python3
from pydantic import  Field
from typing import Literal, Dict
from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services

from gemsModules.batchcompute.main_settings import WhoIAm
from gemsModules.batchcompute.main_api_project import Batchcompute_Project
from gemsModules.batchcompute.services.settings.known_available import Available_Services
from gemsModules.batchcompute.services.SubmitJob.api import SubmitJobService_Request, SubmitJobService_Response
from gemsModules.batchcompute.main_api_common import Batchcompute_Service_Request, Batchcompute_Service_Response

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class Batchcompute_Service_Requests(main_api_services.Service_Requests):
    __root__ : dict[str, SubmitJobService_Request, Batchcompute_Service_Request] = None


class Batchcompute_Service_Responses(main_api_services.Service_Responses):
    __root__ : dict[str, SubmitJobService_Response, Batchcompute_Service_Response] = None

class Batchcompute_Scheduler_Inputs(BaseModel):
    partition: str = Field(None, alias='partition')
    working_directory: str = None
    job_name: str = None
    use_user_environment: bool = "True"
    ## For all the 'num_X_per_Y', a value of -1 will assign the maximum available
    num_nodes_per_job: str = None
    num_processes_per_node: str = None
    num_processes_per_job: str = None
    num_cores_per_job: str = None
    num_threads_per_job: str = None
    num_gpus_per_job: str = None
    time_limit: str = Field(
            None,
            description = "Computing time limit in ISO 8601 format. Example: 2 days, 16 hours and 30 minutes = P2DT16H30M "
            )
    execution_error_file_prefix: str = None
    execution_output_file_prefix: str = None

    @root_validator(pre=True)
    def handle_aliases(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Allow folks to use 'queue' instead of 'partition'
        If both are present, partition will be used and queue will be ignored.
        """
        # If 'queue' is present but 'partition' is not, map 'queue' to 'partition'
        if 'queue' in values and 'partition' not in values:
            values['partition'] = values.pop('queue')
        return values

class Batchcompute_Entity(main_api_entity.Entity) :

    entityType : Literal['Batchcompute'] = Field(  # This is the only required field in all of the API
            ...,
            title='Type',
            alias='type'
            )
    services : Batchcompute_Service_Requests = Batchcompute_Service_Requests()  
    responses : Batchcompute_Service_Responses = Batchcompute_Service_Responses()


class Batchcompute_API(main_api.Common_API):
    entity : Batchcompute_Entity
    project : Batchcompute_Project = Batchcompute_Project()


class Batchcompute_Transaction(main_api.Transaction):
    
    def get_API_type(self):  # This allows dependency injection in the children
        return Batchcompute_API


