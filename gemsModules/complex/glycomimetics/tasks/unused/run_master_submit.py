import os
import sys, subprocess

from gemsModules.complex.glycomimetics.tasks.make_master_submission_script import (
    execute as make_master_submission_script,
)
from gemsModules.complex.glycomimetics.tasks.makedir import execute as make_analog_dirs
from gemsModules.complex.glycomimetics.tasks.make_all_simulation_scripts_for_analogs import (
    execute as make_all_simulation_scripts,
)
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


# TODO: Must be run on a slurm head. need to use batchcompute.
def execute(job_workdir):
    # cd to job_workdir # This replicates original bash behavior. TODO: update tasks to use job_workdir directly.
    os.chdir(job_workdir)
    script_path = make_master_submission_script(job_workdir)
    # Might not do above due to slurm boundaries? TODO: unify below with make_master_submission_script.py's usage.
    # script_path = os.path.join(job_workdir, "slurm_submit_glycomimetics.sh")

    # If we assume that this is run after being sent to the right GEMS instance with Slurm. we could run makedirs task here.
    # Reminder: which would mean it is removed from from the master submit script sbatched below.
    # This here should be unified with other variables, such as the ones used to make the submission script.
    glycomimetics_output_dir_with_slash = os.path.join(
        job_workdir, "glycomimetics", "output"
    )
    simulation_dir = os.path.join(job_workdir, "simulation")
    make_analog_dirs(glycomimetics_output_dir_with_slash, simulation_dir)

    # Create the sim scripts, reference does this inside the master submit script.
    os.chdir(simulation_dir)
    make_all_simulation_scripts()

    # Submitting the Slurm job - TODO: batchcompute request/call instead
    # Note: job_workdir should be equivalent to job_workdir_absolute in the original bash script
    subprocess.run(["sbatch", "--partition=CPU", "-D", job_workdir, script_path])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <job_workdir>")
    else:
        # convenience for testing
        os.makedirs(sys.argv[1], exist_ok=True)
        execute(sys.argv[1])
