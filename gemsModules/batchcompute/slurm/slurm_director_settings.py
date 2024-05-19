from gemsModules.common.code_utils import GemsStrEnum

from gemsModules.mmservice.mdaas.tasks.create_slurm_submission import (
    execute as create_mdaas,
)


class Known_Slurm_Entities(GemsStrEnum):
    """
    The entities that Delegator knows about.
    """

    MDaaS_RunMD = "MDaaS-RunMD"


Known_Slurm_Submission_Builders = {
    "MDaaS-RunMD": create_mdaas,
}
