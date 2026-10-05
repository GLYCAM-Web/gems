#!/usr/bin/env python3
from gemsModules.batchcompute.services.SubmitJob.api import SubmitJobService_Request, SubmitJobService_Response
from gemsModules.networkconnections.grpc import is_GEMS_instance_for_SLURM_submission
from gemsModules.networkconnections.seek_correct_host import execute as seek_correct_host
from gemsModules.batchcompute.tasks.slurm.submit_job import execute as submit_slurm_job

from gemsModules.batchcompute.tasks import say_something_nice

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)


def Serve(service: SubmitJobService_Request) -> SubmitJobService_Response:
    log.debug("SERVE: Batchcompute SubmitJob")
    response = SubmitJobService_Response()

    context = None
    if hasattr(service.inputs, "context") and service.inputs.context:
        context = service.inputs.context
    elif hasattr(service.inputs, "__dict__"):
        context = service.inputs.__dict__.get("context")
    if not context:
        context = "MDaaS-RunMD"

    request_json = service.json(by_alias=True)

    if not is_GEMS_instance_for_SLURM_submission(context):
        log.debug("Host is not configured for Slurm execution of context '%s'. Rerouting via gRPC/JSON...", context)
        grpc_response = seek_correct_host(request_json, context, submission_fn_type="slurm")
        response.outputs.message = str(grpc_response)
        return response

    log.debug("Host is configured for Slurm execution of context '%s'. Submitting job locally...", context)
    job_result = submit_slurm_job(request_json)
    response.outputs.message = str(job_result)
    return response

    
