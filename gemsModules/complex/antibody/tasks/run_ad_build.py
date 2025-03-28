import subprocess

from pathlib import Path

from gemsModules.logging.logger import Set_Up_Logging

from .amber_submit import execute as execute_amber_submit

log = Set_Up_Logging(__name__)

WRAPPER = Path(__file__).parent / "run_ad_build.sh"


def execute(project_dir: Path, use_serial: bool = True):
    """Execute the AD_Evaluate task."""
    
    results = subprocess.run(WRAPPER, cwd=project_dir, env={"GW_STACK_PATH_PREFIX": "/programs/website_aad2/test", "WD": project_dir, "USE_SERIAL": str(use_serial)}, capture_output=True)
    log.debug(f"results: {results}")
    return results
