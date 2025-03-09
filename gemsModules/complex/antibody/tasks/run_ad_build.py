import subprocess

from pathlib import Path

from gemsModules.logging.logger import Set_Up_Logging

from .amber_submit import execute as execute_amber_submit

log = Set_Up_Logging(__name__)

WRAPPER = Path(__file__).parent / "run_ad_build.sh"


def execute(pUUID, project_dir: Path, AAD2_BIN: Path = None, use_serial: bool = True):
    """Execute the AD_Evaluate task."""
    
    results = subprocess.run(WRAPPER, cwd=project_dir, env={"AAD2_BIN": str("/programs/website_aad2/test/bin"), "WD": project_dir, "USE_SERIAL": str(use_serial)}, capture_output=True)
    log.debug(f"results: {results}")
