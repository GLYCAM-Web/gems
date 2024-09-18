import subprocess

from pathlib import Path

from gemsModules.logging.logger import Set_Up_Logging

from .amber_submit import execute as execute_amber_submit

log = Set_Up_Logging(__name__)


def execute(pUUID, project_dir: Path, GlycoWebtool_path: Path, use_serial: bool = False, use_project_dir: bool = False):
    """"""
    """
    ./programs/glycomimeticsWebtool/scripts/00.RUN_ALL.bash 3PHZ.pdb  input.txt  systemInfo.txt

    """
    # We're not copying scripts to the project for now, but this may be possible one day:
    if use_project_dir:
        log.debug("Running Glycomimetics scripts from the project directory.")
        run_all_script = project_dir / "scripts/00.RUN_ALL.bash"
    else:
        run_all_script = GlycoWebtool_path / "scripts/00.RUN_ALL.bash"
    
    # execute in project directory
    log.debug(f"About to execute {run_all_script} in {project_dir}") 
    
    # TODO: gRPC/swarm->remote execution
    #subprocess.Popen([run_all_script, "Complex.pdb", "input.txt", "systemInfo.txt"], cwd=project_dir)
    # if result.returncode != 0:
    #     log.error(f"Error running {run_all_script} in {project_dir}: {result}")
    #     raise RuntimeError(f"Error running {run_all_script} in {project_dir}: {result}")
    
   # first we need to call 
    if use_serial:
        execute_amber_submit(pUUID=pUUID, projectDir=project_dir, control_script=run_all_script, control_args=["Complex.pdb", "input.txt", "systemInfo.txt"])
    else:
        import multiprocessing
        from gemsModules.deprecated.common import logic as commonlogic

        def withArgs():
            execute_amber_submit(pUUID=pUUID, projectDir=str(project_dir), control_script=str(run_all_script), control_args=["Complex.pdb", "input.txt", "systemInfo.txt"])
       
        detached_build = multiprocessing.Process(target=commonlogic.spawnDaemon, args=(withArgs))
        detached_build.daemon = True
        detached_build.start()
        
        