import subprocess

from pathlib import Path

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)

def execute(project_dir: Path, GlycoWebtool_path: Path):
    """"""
    """
    ./programs/glycomimeticsWebtool/scripts/00.RUN_ALL.bash 3PHZ.pdb  input.txt  systemInfo.txt

    """
    
    # From Oliver's code:
    run_all_script = GlycoWebtool_path / "scripts/00.RUN_ALL.bash"
    
    # execute in project directory
    log.debug(f"Running {run_all_script} in {project_dir}") 
    
    # Using Complex.pdb because we symlinked it, is this compatible with Oliver's code?
    result = subprocess.run([run_all_script, "Complex.pdb", "input.txt", "systemInfo.txt"], cwd=project_dir, capture_output=True)
    if result.returncode != 0:
        log.error(f"Error running {run_all_script} in {project_dir}: {result}")
        raise RuntimeError(f"Error running {run_all_script} in {project_dir}: {result}")
    