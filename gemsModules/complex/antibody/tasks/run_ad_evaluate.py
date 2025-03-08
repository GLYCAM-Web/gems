import subprocess

from pathlib import Path

from gemsModules.logging.logger import Set_Up_Logging

from .amber_submit import execute as execute_amber_submit

log = Set_Up_Logging(__name__)


def execute(pUUID, project_dir: Path, AAD2_BIN: Path = "/programs/website_aad2/test/bin", use_serial: bool = True):
    ad_evaluate_cmd = [f'cd {project_dir}', f'export PATH=\"{AAD2_BIN}:$PATH\"', "AD_Evaluate"]
    
   # first we need to call 
    if use_serial:
        execute_amber_submit(pUUID=pUUID, projectDir=project_dir, sbatch=False, control_lines=ad_evaluate_cmd, control_args=[])
    else:
        import multiprocessing
        from gemsModules.deprecated.common import logic as commonlogic

        def withArgs():
            execute_amber_submit(pUUID=pUUID, projectDir=project_dir, sbatch=False, control_lines=ad_evaluate_cmd, control_args=[])
       
        detached_build = multiprocessing.Process(target=commonlogic.spawnDaemon, args=(withArgs,))
        detached_build.daemon = True
        detached_build.start()
        
        