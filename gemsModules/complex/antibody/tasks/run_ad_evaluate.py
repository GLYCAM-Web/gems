import subprocess

from pathlib import Path

from gemsModules.logging.logger import Set_Up_Logging

from .amber_submit import execute as execute_amber_submit

log = Set_Up_Logging(__name__)

WRAPPER = Path(__file__).parent / "run_ad_evaluate.sh"


def execute(pUUID, project_dir: Path, AAD2_BIN: Path = "/programs/website_aad2/test/bin", use_serial: bool = True):
    """Execute the AD_Evaluate task."""
    
    results = subprocess.run(WRAPPER, cwd=project_dir, env={"AAD2_BIN": str(AAD2_BIN), "WD": project_dir, "USE_SERIAL": str(use_serial)}, capture_output=True)
    log.debug(f"results: {results}")
    
    # TODO: Instead of gRPC here, we are forwarding any AntibodyDocking calls directly to thoreau before servicing.
    # if use_serial:
    #     execute_amber_submit(pUUID=pUUID, projectDir=project_dir, sbatch=False, control_lines=ad_evaluate_cmd, control_args=[])
    # else:
    #     import multiprocessing
    #     from gemsModules.deprecated.common import logic as commonlogic

    #     def withArgs():
    #         execute_amber_submit(pUUID=pUUID, projectDir=project_dir, sbatch=False, control_lines=ad_evaluate_cmd, control_args=[])
       
    #     detached_build = multiprocessing.Process(target=commonlogic.spawnDaemon, args=(withArgs,))
    #     detached_build.daemon = True
    #     detached_build.start()
        
        