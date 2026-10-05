
#!/usr/bin/env python3
import json
import os
from gemsModules.deprecated.batchcompute.slurm.dataio import SlurmJobInfo
from gemsModules.original_batchcompute.slurm.tasks.generate_submission_script import execute as generate_submission_script
from gemsModules.original_batchcompute.slurm.tasks.run_submission import execute as run_submission

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


def execute(job_data):
    """
    Generates submission script and submits Slurm job on localhost.
    job_data can be a JSON string, dict, or object.
    """
    if isinstance(job_data, str):
        json_str = job_data
    elif isinstance(job_data, dict):
        json_str = json.dumps(job_data)
    elif hasattr(job_data, "json"):
        json_str = job_data.json(by_alias=True)
    else:
        json_str = json.dumps(job_data)

    log.debug("batchcompute submit_job executing on localhost with: %s", json_str)
    thisSlurmJobInfo = SlurmJobInfo(json_str)
    thisSlurmJobInfo.parseIncomingString()

    generate_submission_script(thisSlurmJobInfo)
    response = run_submission(thisSlurmJobInfo)
    return response
