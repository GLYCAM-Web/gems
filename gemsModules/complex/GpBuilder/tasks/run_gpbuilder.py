import subprocess
import logging
from pathlib import Path

from gemsModules.systemoperations.instance_config import InstanceConfig

logger = logging.getLogger(__name__)
ic = InstanceConfig()

def execute(input_file: Path, project_dir: Path):
    try:
        project_dir = Path(ic.get_filesystem_path("Glycomimetics")) / job_id
        if not project_dir.exists():
            project_dir.mkdir()
            
        log_file = project_dir / "gpbuilder.log"
        err_file = project_dir / "gpbuilder.err"

        # Run gpBuilder with timeout
        with open(log_file, "w") as log_out, open(err_file, "w") as err_out:
            subprocess.run(
                [str(GP_BUILDER), str(input_file), str(project_dir / "output")],
                text=True,
                check=True,
                stdout=log_out,
                stderr=err_out,
                cwd=str(project_dir),
                timeout=300  # 5 minute timeout
            )

        # Update job status in database
        # job.status = "completed"
        # job.completed_at = datetime.now()
        # job.output_path = str(project_dir / "output")
        # db.commit()

    except subprocess.CalledProcessError as e:
        # Handle process errors
        error_message = "Process error"
        if err_file.exists():
            error_message += f": {err_file.read_text()}"
        if log_file.exists():
            error_message += f"\nLog output: {log_file.read_text()}"

        # job.status = "failed"
        # job.error = error_message
        # db.commit()

    except Exception as e:
        logger.error(f"Error processing job {job_id}: {str(e)}")
        # job.status = "failed"
        # job.error = str(e)
        # db.commit()
