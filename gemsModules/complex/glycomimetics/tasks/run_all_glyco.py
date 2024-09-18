import subprocess

from pathlib import Path

from gemsModules.logging.logger import Set_Up_Logging

from .amber_submit import execute as execute_amber_submit

log = Set_Up_Logging(__name__)


def execute(pUUID, project_dir: Path, GlycoWebtool_path: Path, use_serial: bool = False):
    """"""
    """
    ./programs/glycomimeticsWebtool/scripts/00.RUN_ALL.bash 3PHZ.pdb  input.txt  systemInfo.txt

    """
    # TODO: Change this when copying script into project directory
    run_all_script = project_dir / "scripts/00.RUN_ALL.bash"
    
    # execute in project directory
    log.debug(f"Running {run_all_script} in {project_dir}") 
    
    # TODO: gRPC/swarm->remote execution
    #subprocess.Popen([run_all_script, "Complex.pdb", "input.txt", "systemInfo.txt"], cwd=project_dir)
    # if result.returncode != 0:
    #     log.error(f"Error running {run_all_script} in {project_dir}: {result}")
    #     raise RuntimeError(f"Error running {run_all_script} in {project_dir}: {result}")
    
   # first we need to call 
    if use_serial:
        execute_amber_submit(pUUID=pUUID, projectDir=project_dir, control_script=run_all_script)
    else:
        import multiprocessing
       
        def withArgs():
            execute_amber_submit(pUUID=pUUID, projectDir=project_dir, control_script=run_all_script, control_args=["Complex.pdb", "input.txt", "systemInfo.txt"])
       
        multiprocessing.Process(target=withArgs, daemon=False).start()