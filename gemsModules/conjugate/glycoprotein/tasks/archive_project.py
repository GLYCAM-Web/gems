import os
import sys
import subprocess
from pathlib import Path
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)
ARCHIVE_SH_SCRIPT_PATH = Path(__file__).parent / "create_project_archive.sh"

def execute(job_dir, pUUID) -> bool:
    """Executes the archiving of the project directory.
    Returns: True if successful, False otherwise.
    Args:
        job_dir (Path): The directory where the project files are located.
        pUUID (str): The unique identifier for the project.
    """
    log.debug(f"Archiving project {pUUID} at {job_dir}")
    
    if not ARCHIVE_SH_SCRIPT_PATH.exists():
        log.error(f"Archive script not found at {ARCHIVE_SH_SCRIPT_PATH}")
        return False
    
    # Run the archive script using subprocess instead of os.system
    try:
        log.debug(f"Running archive script: {ARCHIVE_SH_SCRIPT_PATH} {job_dir} {pUUID}")
        result = subprocess.run(
            ["bash", str(ARCHIVE_SH_SCRIPT_PATH), str(job_dir), pUUID],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            log.error(f"Archive script failed with exit code {result.returncode}")
            if result.stderr:
                log.error(f"Script stderr: {result.stderr}")
            if result.stdout:
                log.debug(f"Script stdout: {result.stdout}")
            return False
            
        log.debug(f"Archive script completed successfully.")
        if result.stdout:
            log.debug(f"Script output: {result.stdout}")
            
    except Exception as e:
        log.error(f"Error running archive script: {e}")
        return False
        
    return True